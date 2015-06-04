import random
import numpy
from collections import defaultdict
from tictactoe_match import TictactoeMatch
from tictactoe_opponents import TictactoeRandomOpponent, TictactoeSmartOpponent
from ..default_environment import DefaultEnvironment, DefaultPoint
from ...diversity_maintenance import DiversityMaintenance
from ...pareto_dominance import ParetoDominance
from ...utils.helpers import round_value, flatten, is_nearly_equal_to
from ...config import Config

class TictactoePoint(DefaultPoint):
    """
    Encapsulates a tictactoe board configuration as a point.
    """

    def __init__(self, point_id, opponent):
        super(TictactoePoint, self).__init__(point_id)
        self.opponent = opponent

class TictactoeEnvironment(DefaultEnvironment):
    """
    This environment encapsulates all methods to deal with a reinforcement learning task for TicTacToe.
    This is a dummy environment, where the only point in the population is a random player.

    Observations:
    - Uses the same point population for training and testing.
    - The point population is fixed.
    """

    def __init__(self):
        self.total_actions_ = 9 # spaces in the board
        self.total_inputs_ = 9 # spaces in the board (0, 1, 2 as the states, 0: no player, 1: player 1, 2: player 2)
        self.total_positions_ = 2
        self.opponents_ = [TictactoeRandomOpponent, TictactoeSmartOpponent]
        self.point_population_ = None
        self.test_population_ = self._initialize_random_balanced_population(Config.USER['reinforcement_parameters']['validation_population'])
        self.action_mapping_ = {
            '[0,0]': 0, '[0,1]': 1, '[0,2]': 2,
            '[1,0]': 3, '[1,1]': 4, '[1,2]': 5,
            '[2,0]': 6, '[2,1]': 7, '[2,2]': 8,
        }
        Config.RESTRICTIONS['total_actions'] = self.total_actions_
        Config.RESTRICTIONS['total_inputs'] = self.total_inputs_
        Config.RESTRICTIONS['action_mapping'] = self.action_mapping_
        Config.RESTRICTIONS['use_memmory'] = False # since the point population output is not predictable

        # ensures the population size is multiple of the total opponents
        total_samples_per_opponents = Config.USER['training_parameters']['populations']['points']/len(self.opponents_)
        Config.USER['training_parameters']['populations']['points'] = total_samples_per_opponents*len(self.opponents_)

    def _initialize_random_balanced_population(self, population_size):
        population = []
        for opponent_class in self.opponents_:
            for index in range(population_size/len(self.opponents_)):
                instance = opponent_class()
                population.append(TictactoePoint(str(instance), instance))
        random.shuffle(population)
        return population

    def reset_point_population(self):
        self.point_population_ = None

    def setup_point_population(self, teams_population):
        """
        Get a sample of the training dataset to create the point population. If it is the first generation 
        of the run, just gets random samples for each action of the dataset. For the next generations, it 
        replaces some of the points in the sample for new points.
        """
        if not self.point_population_: # first sampling of the run
            self.point_population_ = self._initialize_random_balanced_population(Config.USER['training_parameters']['populations']['points'])
        else: # uses attributes defined in evaluate_point_population()
            # remove the removed points from the teams, in order to save memory. If you want to speed up and
            # don't care about the memory, you may comment the next 5 lines
            to_remove = flatten(self.samples_per_opponent_to_remove)
            for team in teams_population:
                for point in to_remove:
                    if point.point_id in team.results_per_points_:
                        team.results_per_points_.pop(point.point_id)

            sample = flatten(self.samples_per_opponent_to_keep) # join samples per opponent
            random.shuffle(sample)
            self.point_population_ = sample
        self._check_for_bugs()

    def _check_for_bugs(self):
        if len(self.point_population_) != Config.USER['training_parameters']['populations']['points']:
            raise ValueError("The size of the points population changed during selection! You got a bug! (it is: "+str(len(self.point_population_))+", should be: "+str(Config.USER['training_parameters']['populations']['points'])+")")

    def evaluate_point_population(self, teams_population):
        total_samples_per_opponent = Config.USER['training_parameters']['populations']['points']/len(self.opponents_)
        current_subsets_per_opponent = self._get_data_per_opponent(self.point_population_)
        samples_per_opponent_to_keep = int(round(total_samples_per_opponent*(1.0-Config.USER['training_parameters']['replacement_rate']['points'])))

        kept_subsets_per_opponent = []
        removed_subsets_per_opponent = []
        if Config.USER['advanced_training_parameters']['use_pareto_for_point_population_selection']:
            # obtain the pareto front for each subset
            for subset in current_subsets_per_opponent:
                # create the results_map, so that the pareto front will contain points that are selecting distinct teams
                results_map = self._generate_results_map_for_pareto(subset, teams_population)
                front, dominateds = ParetoDominance.pareto_front(subset, results_map)

                keep_solutions = front
                remove_solutions = dominateds
                if len(keep_solutions) < samples_per_opponent_to_keep:  # must include some teams from dominateds
                    subset = DiversityMaintenance.fitness_sharing_for_points(subset, results_map)
                    keep_solutions, remove_solutions = ParetoDominance.balance_pareto_front_to_up(subset, keep_solutions, remove_solutions, samples_per_opponent_to_keep)
                if len(keep_solutions) > samples_per_opponent_to_keep: # must discard some teams from front
                    front = DiversityMaintenance.fitness_sharing_for_points(front, results_map)
                    keep_solutions, remove_solutions = ParetoDominance.balance_pareto_front_to_down(front, keep_solutions, remove_solutions, samples_per_opponent_to_keep)
                kept_subsets_per_opponent.append(keep_solutions)
                removed_subsets_per_opponent.append(remove_solutions)

            # add new points
            for subset, opponent_class in zip(kept_subsets_per_opponent, self.opponents_):
                instance = opponent_class()
                subset.append(TictactoePoint(str(instance), instance))
        else:
            # obtain the data points that will be kept and that will be removed for each subset using uniform probability
            total_samples_per_opponent_to_add = total_samples_per_opponent - samples_per_opponent_to_keep
            for index, subset in enumerate(current_subsets_per_opponent):
                kept_subsets = random.sample(subset, samples_per_opponent_to_keep) # get points that will be kept
                for x in range(total_samples_per_opponent_to_add):
                    instance = self.opponents_[index]()
                    kept_subsets.append(TictactoePoint(str(instance), instance)) # add new points
                kept_subsets_per_opponent.append(kept_subsets)
                removed_subsets_per_opponent.append(list(set(subset) - set(kept_subsets))) # find the remvoed points

        self.samples_per_opponent_to_keep = kept_subsets_per_opponent
        self.samples_per_opponent_to_remove = removed_subsets_per_opponent

    def _get_data_per_opponent(self, point_population):
        subsets_per_opponent = []
        for opponent_class in self.opponents_:
            values = [point for point in point_population if type(point.opponent) is opponent_class]
            subsets_per_opponent.append(values)
        return subsets_per_opponent

    def _generate_results_map_for_pareto(self, subset, teams_population):
        """
        Create a a matrix of (points) x (array version of a matrix that compares all teams outcomes against 
        each other for this point  (0: <=, 1: >)). This matrix is used by pareto to find a front of points 
        that characterize distinct teams.
        """
        results_map = []
        try:
            for point in subset:      
                distinction_vector = []
                for team1 in teams_population:
                    outcome1 = team1.results_per_points_[point.point_id]
                    for team2 in teams_population:
                        outcome2 = team2.results_per_points_[point.point_id]                 
                        if outcome1 > outcome2 and not is_nearly_equal_to(outcome1, outcome2):
                            distinction_vector.append(1)
                        else:
                            distinction_vector.append(0)
                results_map.append(distinction_vector)
        except KeyError as e:
            raise KeyError("A team hasn't processed the point "+str(e)+" before! You got a bug!")
        return results_map
                        
    def point_population(self):
        return self.point_population_

    def evaluate_team(self, team, is_training = False, total_matches = Config.USER['reinforcement_parameters']['training_matches']):
        """
        Each team plays 2 matches against each point in the point population.
        One match as the player 1, another as player 2. The final score is 
        the mean of the scores in the matches (1: win, 0.5: draw, 0: lose)
        """
        if is_training:
            population = self.point_population_
        else:
            population = self.test_population_

        results = []
        extra_metrics = {}
        extra_metrics['opponents'] = defaultdict(list)

        for point in population:
            outputs = []
            for match_id in range(total_matches):
                for position in range(1, self.total_positions_+1):
                    outputs.append(self._play_match(position, point, team, is_training))
            result = numpy.mean(outputs)
            results.append(result)
            if is_training:
                team.results_per_points_[point.point_id] = result
            else:
                extra_metrics['opponents'][point.opponent.opponent_id].append(result)

        score = numpy.mean(results)
        
        if is_training:
            team.fitness_ = score
            team.score_trainingset_ = score
        else:
            for key in extra_metrics['opponents']:
                extra_metrics['opponents'][key] = round_value(numpy.mean(extra_metrics['opponents'][key]))
            team.score_testset_ = score
            team.extra_metrics_ = extra_metrics

    def _play_match(self, position, point, team, is_training):
        if position == 1:
            first_player = point.opponent
            second_player = team
            sbb_player = 2
        else:
            first_player = team
            second_player = point.opponent
            sbb_player = 1

        match = TictactoeMatch()
        point.opponent.initialize()
        while True:
            player = 1
            inputs = match.inputs_from_the_point_of_view_of(player)
            action = first_player.execute(point.point_id, inputs, match.valid_actions(), is_training)
            match.perform_action(player, action)
            if match.is_over():
                return match.result_for_player(sbb_player)
            player = 2
            inputs = match.inputs_from_the_point_of_view_of(player)
            action = second_player.execute(point.point_id, inputs, match.valid_actions(), is_training)
            match.perform_action(player, action)
            if match.is_over():
                return match.result_for_player(sbb_player)

    def validate(self, current_generation, teams_population):
        for team in teams_population:
            if team.generation != current_generation: # dont evaluate tems that have just being created (to improve performance and to get training metrics)
                self.evaluate_team(team, is_training = False, total_matches = Config.USER['reinforcement_parameters']['test_matches'])
        score = [p.score_testset_ for p in teams_population]
        best_team = teams_population[score.index(max(score))]
        print("\nChampion team test score in the initial matches: "+str(best_team.score_testset_))
        self.evaluate_team(best_team, is_training = False, total_matches = Config.USER['reinforcement_parameters']['champion_matches'])
        return best_team

    def metrics(self):
        msg = ""
        msg += "\n### Environment Info:"
        msg += "\ntotal inputs: "+str(self.total_inputs_)
        msg += "\ntotal actions: "+str(self.total_actions_)
        msg += "\nactions mapping: "+str(self.action_mapping_)
        msg += "\nsamples per opponents: "+str(Config.USER['training_parameters']['populations']['points']/len(self.opponents_))
        return msg