"""Result database module"""
from html import parser
import codecs

SERIES = {
    'Miesten Mestaruussarja':    'MM',
    'Miesten A-sarja':           'MA',
    'Miesten B-sarja':           'MB',
    'Miesten Veteraanisarja':    'MV',
    'Naisten Mestaruussarja':    'NM',
    'Naisten  Mestaruussarja':    'NM',
    'Naisten A-sarja':           'NA',
    'Naisten Veteraanisarja':    'NV',
    'Miesten joukkuekilpailu':   'MJ',
    'Miesten parikilpailu':      'MP',
    'Naisten parikilpailu':      'NP',
    'Juniorit - 15v sekasarja':  'J15',
    'Juniorit - 10v sekasarja':  'J10',
    'Juniorit - 15v pojat':      'JP15',
    'Juniorit - 15v tytöt':      'JT15',
    'Juniorit - 10v pojat':      'JP10',
    'Juniorit - 10v tytöt':      'JT10',
    'Juniorit - 10v tyt?t':      'JT10',
    'Juniorit - 10v tytÃ¶t':    'JT10',
}

NOTES = {'SE-siv.':'SE-siv',
         '*SE siv.*':'SE-siv',
         'SE*':'SE',
         '*SE*':'SE'}

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
    note = None
    scores = []
    attr = ""
    competition = -1

    def handle_starttag(self, tag, attrs):
        if attrs:
            if attrs[0][0] == "class":
                self.attr = attrs[0][1]
                self.add_result()

    def add_result(self):
        """Add new result to list"""
        if self.name is  None\
            or self.position is None:
            return
        if self.attr in ['Sija', 'Sarja', 'Kilpailu']:
            self.resultlist.append({'competition': self.competition,
                                    'serie': self.serie,
                                    'position': self.position,
                                    'name': self.name,
                                    'scores': self.scores,
                                    'note':self.note})
            self.name = None
            self.position = None
            self.scores = []
            self.note = None

    def handle_data(self, data):
        """Read one row of data"""
        if data in ['\n', '\n ', '\n  ', 'Sija', 'Nimi', 'Tulos', 'Seura', '',
                    'Alkuun', 'Huom!']:
            return
        data = data.strip()
        if data == '':
            return
        if self.attr == 'Sarja':
            if data in SERIES:
                self.serie = SERIES[data]
            else:
                raise ValueError("Unknown serie: ", data)
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
        elif self.attr == 'Huom':
            if data in NOTES:
                self.note = NOTES[data]
            else:
                raise ValueError("Unknown note: ", data)

    def get_result_list(self):
        """Return list of results"""
        return self.resultlist
