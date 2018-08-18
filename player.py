"""Simple player database"""
from utils import str2list

class Player():
    """Player class"""

    def __init__(self, identity, name, serie='MM', aliases=None):
        if not aliases:
            aliases = []
        self.id = identity
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
        """Read player list file.

        :param player_file_name: Path to player list file
        :returns: None
        """

        # Create player list from file
        player_id = 0
        self.player_list = []
        with open(player_file_name, 'r') as player_file:
            for line in player_file:

                if line.startswith('#'):
                    continue

                fields = str2list(line)

                if fields[0] not in self.series:
                    raise Exception("Unknown serie: ", fields[0])

                self.player_list.append(
                    Player(identity=player_id,
                           serie=fields[0],
                           name=fields[1],
                           aliases=fields[2:])
                )
                player_id = player_id+1

    def get_player_with_name(self, name):
        """Find player by name

        :param name: Player name
        :returns: Player object
        """
        for player in self.player_list:
            if player.name == name or name in player.aliases:
                return player
        raise ValueError('Player "{}" not known'.format(name))

    def get_player_with_id(self, player_id):
        """Find player by ID

        :param player_id: Player ID
        :returns: Player object
        """
        for player in self.player_list:
            if player.id == player_id:
                return player
        raise Exception('Player "{}" not known'.format(player_id))

    def get_players_of_serie(self, serie):
        """Find all players in serie

        :param serie: serie
        :returns: list of players in serie.
        """
        player_list = []
        for player in self.player_list:
            if player.serie == serie:
                player_list.append(player)
        return player_list
