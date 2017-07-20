from utils import str2list

class Player():

    def __init__(self, id, name, serie='MM'):
        self.id = id
        self.name = name
        self.serie = serie

class PlayerDB():

    def __init__(self, player_file_name=None):
        if player_file_name is not None:
            self.read_file(player_file_name)

    def read_file(self, player_file_name):

        # Create player list from file
        n = 0
        self.player_list = []
        with open(player_file_name, 'r') as player_file:
            for line in player_file:

                if line.startswith('#'):
                    continue

                fields = str2list(line)

                self.player_list.append(
                    Player(
                        id = n,
                        name = fields[1],
                        serie = fields[0],
                        )
                )
                n = n+1

    def get_player_with_name(self, name):
        for player in self.player_list:
            if player.name == name:
                return player
        raise Exception('Player "{}" not known'.format(name))

