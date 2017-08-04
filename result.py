"""Result database module"""
import codecs
from html import parser
from utils import str2list


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
        if len(attrs) > 0:
            if attrs[0][0] == "class":
                self.attr = attrs[0][1]

    def handle_data(self, data):
        if data in ['\n', '\n ','\n  ', 'Sija', 'Nimi']:
            return
        if self.attr == 'Sarja':
            if data in 'Miesten Mestaruussarja':
                self.serie = 'MM'
            elif data in ['Miesten A-sarja']:
                self.serie = 'MA'
            elif data in ['Miesten B-sarja']:
                self.serie = 'MB'
            elif data in ['Miesten Veteraanisarja']:
                self.serie = 'MV'
            elif data in ['Naisten Mestaruussarja']:
                self.serie = 'NM'
            elif data in ['Naisten A-sarja']:
                self.serie = 'NA'
            elif data in ['Naisten Veteraanisarja']:
                self.serie = 'NV'
            elif data in ['Miesten joukkuekilpailu']:
                self.serie = 'MJ'
            elif data in ['Miesten joukkuekilpailu']:
                self.serie = 'MP'
            elif data in ['Naisten parikilpailu']:
                self.serie = 'NP'
            elif data in ['Juniorit - 15v sekasarja']:
                self.serie = 'J15'
            elif data in ['Juniorit - 10v sekasarja']:
                self.serie = 'J10'
            else:
                assert Exception('Unknown serie: ' + data)

        if self.attr == 'Kilpailu':
            self.competition = self.competition + 1
        if self.attr == 'Sija':
            if self.name is not None and self.position is not None:
                self.resultlist.append({'competition': self.competition,
                                        'serie': self.serie,
                                        'position': self.position,
                                        'name': self.name,
                                        'scores': self.scores})
            self.name = None
            self.position = data
            self.name = None
            self.scores = []
        if self.attr == 'Nimi':
            self.name = data
        if self.attr == 'Seura':
            self.team = data
        if self.attr == 'Tulos':
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
        # self.read_result_file(result_file_name, playerdb)
        self.parse_html_file(result_file_name, playerdb)

    def generate_player_list(self, result_file_name, playerdb):
        """Read results from html"""
        # self.result_list = []
        with codecs.open(result_file_name, 'r', 'ISO-8859-1') as result_file:
            lines = ""
            for line in result_file:
                lines = lines + line
            resultparser = ResultsParser()
            resultparser.feed(lines)
            result_list = resultparser.get_result_list()
            players=[]
            for result in result_list:
                players.append(result['serie'] + "," + result['name'])
            unique_players=list(set(players))
            sorted_players=sorted(unique_players)
            for p in sorted_players:
                print(p)


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
                pla.append(result['serie'] + "," + result['name'])
                self.result_list.append(
                    Result(
                        result['competition'],
                        playerdb.get_player_with_name(result['name']).id,
                        result['serie'],
                        result['position'],
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
        self.result_list = []

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
