import socket
import select
import json
import sys

class TictactoeGame():
    """
    Implements a TicTacToe match
    """

    EMPTY = 0
    DRAW = 0

    DEFAULT_CONFIG = {
        'multiply_normalization_by': 10.0,
        'debug': False,
        'timeout': 60,
        'buffer': 5000,
        'port': 7800,
        'host': 'localhost',
        'requests_timeout': 120,
        'silent_errors': False,
    }
    
    TEST_CONFIG = {
        'multiply_normalization_by': 10.0,
        'debug': False,
        'timeout': 60,
        'buffer': 5000,
        'port': 7801,
        'host': 'localhost',
        'requests_timeout': 120,
        'silent_errors': True,
    }

    CONFIG = {}

    def __init__(self, test_mode):
        if test_mode:
            TictactoeGame.CONFIG = TictactoeGame.TEST_CONFIG
        else:
            TictactoeGame.CONFIG = TictactoeGame.DEFAULT_CONFIG

        self.inputs_ = [TictactoeGame.EMPTY, TictactoeGame.EMPTY, TictactoeGame.EMPTY,
                        TictactoeGame.EMPTY, TictactoeGame.EMPTY, TictactoeGame.EMPTY,
                        TictactoeGame.EMPTY, TictactoeGame.EMPTY, TictactoeGame.EMPTY]
        self.result_ = -1
        self.print_game_ = TictactoeGame.CONFIG['debug']
        self.player_label = {}
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(TictactoeGame.CONFIG['timeout'])
        try:
            self.client_socket.connect((TictactoeGame.CONFIG['host'], TictactoeGame.CONFIG['port']))
            ready = select.select([self.client_socket], [], [], TictactoeGame.CONFIG['timeout'])
            if ready[0]:
                data = self.client_socket.recv(TictactoeGame.CONFIG['buffer'])
                data = json.loads(data)
                if 'connection' in data and data['connection']:
                    if TictactoeGame.CONFIG['debug']:
                        print "Connected to SBB server."
                else:
                    raise socket.error("Server did not answer with a 'success connection' message")
            else:
                raise socket.timeout("Timeout to receive 'success connection' message")
        except Exception as e:
            print "\n<< It was not possible to connect to the SBB server. >>\n"
            raise e

    def wait_for_requests(self):
        while True:
            try:
                ready = select.select([self.client_socket], [], [self.client_socket], TictactoeGame.CONFIG['requests_timeout'])
                if not ready[0]:
                    raise socket.timeout("Timeout to receive requests messages")
                else:
                    data = self.client_socket.recv(TictactoeGame.CONFIG['buffer'])
                    if TictactoeGame.CONFIG['debug']:
                        print "data: "+str(data)

                    if not data:
                        raise socket.error("Server sent an empty request")
                    else:
                        data = json.loads(data)

                        if not self._is_valid_request(data):
                            raise socket.error("Server did not send a valid request")
                        else:
                            if TictactoeGame.CONFIG['debug']:
                                print "Starting new match."
                            # TODO
                            self.player_label[1] = 'p1'
                            self.player_label[2] = 'p2'

                            message = {
                                'request_result': True,
                            }
                            self.client_socket.send(json.dumps(message))
            except Exception as e:
                if TictactoeGame.CONFIG['silent_errors']:
                    raise SystemExit
                else:
                    print "\n<< It was not possible to connect to the SBB server. >>\n"
                    raise e

    def _is_valid_request(self, data):
        if 'request' in data and data['request'] == 'new_match':
            return True
        return False

    def perform_action(self, current_player, action):
        """
        Perform the action for the current_player in the board, modifying 
        the attribute inputs_.
        """
        self.inputs_[action] = current_player
        if self.print_game_:
            print "---"
            print str(self.inputs_[0:3])
            print str(self.inputs_[3:6])
            print str(self.inputs_[6:9])

    def valid_actions(self):
        """
        The valid actions are the empty spaces.
        """
        valids = []
        for index, space in enumerate(self.inputs_):
            if space == TictactoeGame.EMPTY:
                valids.append(index)
        return valids

    def inputs_from_the_point_of_view_of(self, position):
        """
        Get a copy of the inputs so that the player in 'position' always see the board with 
        spaces with '1' as their spaces, and '2' as the opponent's spaces.
        """
        if position == 1:
            return [x*TictactoeGame.CONFIG['multiply_normalization_by'] for x in list(self.inputs_)]
        else:
            mapping = [0, 2, 1]
            inputs = [mapping[x]*TictactoeGame.CONFIG['multiply_normalization_by'] for x in list(self.inputs_)]
            return inputs

    def is_over(self):
        """
        Check if all spaces were used. If yes, sets the attribute result_ with the 
        number of the winner or 0 if a draw occured.
        """
        winner = TictactoeGame.get_winner(self.inputs_)
        if winner:
            self.result_ = winner
            if self.print_game_:
                print "It is over! Player "+str(self.result_)+" ("+str(self.player_label[self.result_])+") wins!"
            return True
        for value in self.inputs_:
            if value == TictactoeGame.EMPTY:
                if self.print_game_:
                    print "Go!"
                return False
        self.result_ = TictactoeGame.DRAW
        if self.print_game_:
            print "It is over! Draw!"
        return True

    def result_for_player(self, current_player):
        if self.result_ == current_player:
            return 1 # win
        if self.result_ == TictactoeGame.DRAW:
            return 0.5 # draw
        else:
            return 0 # lose

    @staticmethod
    def get_winner(inputs):
        winning_configs = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
                       (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
        for config in winning_configs:
            if inputs[config[0]] == inputs[config[1]] and inputs[config[1]] == inputs[config[2]]:
                if inputs[config[0]] != 0:
                    return inputs[config[0]]
        return None # no winner

if __name__ == "__main__":
    test_mode = False
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_mode = True
    game = TictactoeGame(test_mode)
    game.wait_for_requests()