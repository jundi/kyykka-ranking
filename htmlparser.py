"""Result database module"""
from html import parser
import codecs

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
        for player in sorted_players:
            print(player)

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
            self.serie = data
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




