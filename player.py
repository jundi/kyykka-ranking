"""Simple player database"""
from utils import str2list

class Player():
    """Player class"""

    def __init__(self, id, name, serie='MM', aliases=[]):
        self.id = id
        self.name = name
        self.aliases = aliases
        self.serie = serie

class PlayerDB():
    """Player database"""

    def __init__(self, series, player_file_name=None):
        self.series = series
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

                if fields[0] not in self.series:
                    raise Exception("Unknown serie: ", fields[0])

                self.player_list.append(
                    Player(
                        id = n,
                        serie = fields[0],
                        name = fields[1],
                        aliases = fields[2:]
                        )
                )
                n = n+1

    def get_player_with_name(self, name):
        for player in self.player_list:
            if player.name == name or name in player.aliases:
                return player
        raise ValueError('Player "{}" not known'.format(name))

    def get_player_with_id(self, player_id):
        for player in self.player_list:
            if player.id == player_id:
                return player
        raise Exception('Player "{}" not known in serie {}'.format(player_id, serie))

    def get_players_of_serie(self, serie):
        player_list = []
        for player in self.player_list:
            if player.serie == serie:
                player_list.append(player)
        return player_list

