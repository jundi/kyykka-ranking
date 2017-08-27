"""Result database module"""
from html import parser
import codecs
import player
from utils import str2list

def generate_player_list(result_file_name):
    """Read results from html"""
    with codecs.open(result_file_name, 'r', 'ISO-8859-15') as result_file:
        lines = ""
        for line in result_file:
            lines = lines + line
        resultparser = ResultsParser()
        resultparser.feed(lines)
        result_list = resultparser.get_result_list()
        players = []
        for result in result_list:
            players.append(result['serie'] + "," + result['name'])
        unique_players = list(set(players))
        sorted_players = sorted(unique_players)
        for player_ in sorted_players:
            print(player_)

# pylint: disable=abstract-method
class ResultsParser(parser.HTMLParser):
    """Parse html code"""
    resultlist = []
    name = None
    position = None
    name = None
    team = None
    serie = None
    scores = []
    attr = ""
    competition = -1

    def handle_starttag(self, tag, attrs):
        if attrs:
            if attrs[0][0] == "class":
                self.attr = attrs[0][1]
                if self.name is  None\
                    or self.position is None:
                    return
                if self.attr in ['Sija', 'Sarja', 'Kilpailu']:
                    self.resultlist.append({'competition': self.competition,
                                            'serie': self.serie,
                                            'position': self.position,
                                            'name': self.name,
                                            'scores': self.scores})
                    self.name = None
                    self.position = None
                    self.scores = []

    def handle_data(self, data):
        if data in ['\n', '\n ', '\n  ', 'Sija', 'Nimi', 'Tulos', 'Seura', '',
                    'Alkuun']:
            return
        else:
            data = data.strip()
        if data == '':
            return
        if self.attr == 'Sarja':
            self.serie = player.SERIES[data]
        elif self.attr == 'Kilpailu':
            self.competition = self.competition + 1
        elif self.attr == 'Sija':
            self.position = data
        elif self.attr == 'Nimi':
            self.name = data.strip()
        elif self.attr == 'JP-seura':
            self.name = data.strip()
        elif self.attr == 'Seura':
            self.team = data
        elif self.attr == 'Tulos':
            self.scores.append(data)

    def get_result_list(self):
        """Return list of results"""
        return self.resultlist





class Result():
    """Result class"""
    # pylint: disable=too-many-arguments,too-few-public-methods
    def __init__(self,
                 competition_id,
                 player_id,
                 serie,
                 position,
                 scores,
                ):
        self.competition_id = competition_id
        self.player_id = player_id
        self.serie = serie
        self.position = position
        self.scores = scores


class ResultDB():
    """Result database class"""
    def __init__(self, result_file_name, playerdb):
        self.result_list = []
        self.parse_html_file(result_file_name, playerdb)


    def parse_html_file(self, result_file_name, playerdb):
        """Read results from html"""
        self.result_list = []
        with codecs.open(result_file_name, 'r', 'ISO-8859-1') as result_file:
            lines = ""
            for line in result_file:
                lines = lines + line
            resultparser = ResultsParser()
            resultparser.feed(lines)
            result_list = resultparser.get_result_list()
            for result in result_list:
                self.result_list.append(
                    Result(
                        result['competition'],
                        playerdb.get_player_with_name(result['name']).id,
                        result['serie'],
                        int(result['position'].strip('.')),
                        result['scores'],
                    )
                )


    def get_player_position(self, player_id, competition_id):
        """Get position of player in given competition"""
        for result in self.result_list:
            if result.player_id == player_id \
                    and result.competition_id == competition_id:
                return result.position
        return None


    def get_player_result(self, player_id, competition_id):
        """Get result of player in competition"""
        for result in self.result_list:
            if (result.player_id == player_id) \
                    and (result.competition_id == competition_id):
                return result
        return None


    def get_player_competitions(self, player_id):
        """Get list of competitions the player has attended"""
        competition_id_list = []
        for result in self.result_list:
            if result.player_id == player_id:
                competition_id_list.append(result.competition_id)
        return competition_id_list


    def read_result_file(self, result_file_name, playerdb):
        """Initialize the result database from file"""
        last_competition_id = None
        last_serie = None

        with open(result_file_name, 'r') as result_file:
            for line in result_file:

                if line.startswith('#'):
                    continue

                fields = str2list(line)
                competition_id = int(fields[0])
                serie = fields[1]
                name = fields[2]
                scores = [int(x) for x in fields[3:]]

                if not (competition_id == last_competition_id \
                        and serie == last_serie):
                    position = 1
                else:
                    position = position + 1

                last_competition_id = competition_id
                last_serie = serie

                self.result_list.append(
                    Result(
                        competition_id,
                        playerdb.get_player_with_name(name).id,
                        serie,
                        position,
                        scores,
                    )
                )


    def player_has_results(self, player_id):
        """Check if player has attended any competitions"""
        for result in self.result_list:
            if result.player_id == player_id:
                return True
        return False
