from ..reinforcement_point import ReinforcementPoint

class PokerPoint(ReinforcementPoint):
    """
    Encapsulates a poker opponent, seeded hand, and position as a point.
    """

    def __init__(self, label, info):
        super(PokerPoint, self).__init__()

        self.label_ = label
        self.seed_ = info['id']
        self.board_cards_ = [str(x) for x in info['bc']]
        self.players = {}

        self.players['team'] = {}
        self.players['team']['position'] = info['pos']
        self.players['team']['hand_strength'] = info['p']['str']
        self.players['team']['effective_potential'] = info['p']['ep']
        self.players['team']['hole_cards'] = [str(x) for x in info['p']['hc']]

        self.players['opponent'] = {}
        if self.players['team']['position'] == 0:
            self.players['opponent']['position'] = 1
        else:
            self.players['opponent']['position'] = 0
        self.players['opponent']['hand_strength'] = info['o']['str']
        self.players['opponent']['effective_potential'] = info['o']['ep']
        self.players['opponent']['hole_cards'] = [str(x) for x in info['o']['hc']]
        
        if self.players['team']['hand_strength'][3] > self.players['opponent']['hand_strength'][3]:
            self.sbb_sd_label_ = 0
        elif self.players['team']['hand_strength'][3] < self.players['opponent']['hand_strength'][3]:
            self.sbb_sd_label_ = 2
        else:
            self.sbb_sd_label_ = 1

        self.point_id_ = str(self.seed_)+"-"+str(self.players['team']['position'])
        self.last_validation_opponent_id_ = None
        self.teams_results_ = []

    def __repr__(self):
        return "("+str(self.point_id_)+":"+str(self.label_)+")"

    def __str__(self):
        m = "\n---"
        m += "\npoint_id: "+str(self.point_id_)
        m += "\nlabel: "+str(self.label_)
        m += "\nboard_cards: "+str(self.board_cards_)
        m += "\nsbb_sd_label: "+str(self.sbb_sd_label_)
        m += "\n\nteam"
        m += "\n- position: "+str(self.players['team']['position'])
        m += "\n- hole_cards: "+str(self.players['team']['hole_cards'])
        m += "\n- hand_strength: "+str(self.players['team']['hand_strength'])
        m += "\n- effective_potential: "+str(self.players['team']['effective_potential'])
        m += "\n\nopponent"
        m += "\n- position: "+str(self.players['opponent']['position'])
        m += "\n- hole_cards: "+str(self.players['opponent']['hole_cards'])
        m += "\n- hand_strength: "+str(self.players['opponent']['hand_strength'])
        m += "\n- effective_potential: "+str(self.players['opponent']['effective_potential'])
        m += "\n---\n"
        return m