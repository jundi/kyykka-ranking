class Player():

    def __init__(self, id, name, serie='MM'):
        self.id = id
        self.name = name
        self.serie = serie
        self.cup_points = 0
        self.poy_points = 0
        self.mo_points = 0
        self.mm_points = 0

class PlayerDB():

    def __init__(self, player_file_name=None):
        if player_file_name is not None:
            read_file(player_file_name)

    def read_file(self, player_file_name):

        # Create player list from file
        n = 0
        self.player_list = []
        with open(player_file_name, 'r') as player_file:
            for line in player_file:
                name = line.strip('\n')
                player_list.append(
                    Player(
                        id = n,
                        name = name,
                        )
                )
                n = n+1

    def get_player_with_name(self, name):
        for player in self.player_list:
            if player.name is name:
                return player
        raise Exception('Player "{}" not known'.format(name))

