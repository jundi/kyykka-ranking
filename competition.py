from utils import str2bool
from utils import str2list

SERIES = ['MM', 'MA', 'MB', 'MV', 'NM', 'NA', 'NV', 'MJ', 'MP', 'NP']
TAGS = ['MM_kars', 'cup_finaali', 'MO_kars', 'joukkue_SM', 'henk_SM', 'VO']

class Competition():

    def __init__(self,
                 competition_id,
                 name,
                 series=['MM', 'MA', 'MB', 'MV', 'NM', 'NA', 'NV', 'MJ', 'NP'],
                 cup=['NM', 'NM', 'MJ', 'MP', 'NP'],
                 tags=['MO', 'MM', 'SM', 'VO'],
                ):
        self.competition_id = competition_id
        self.name = name
        self.series = series
        self.cup = cup
        self.tags = tags
        self.tags += ([c + '_cup' for c in self.cup])

        def is_sm():
            return bool('SM' in self.tags)
        def is_mm():
            return bool('MM_kars' in self.tags)
        def is_mo():
            return bool('MO_kars' in self.tags)
        def is_pentathlon():
            return bool('VO' in self.tags)


class CompetitionDB():

    def __init__(self, competition_file_name=None):
        if competition_file_name is not None:
            self.read_file(competition_file_name)

    def read_file(self, competition_file_name):
        # Create competition list from file
        n = 0
        self.competition_list = []
        with open(competition_file_name, 'r') as competition_file:
            for line in competition_file:
                cup = []
                tags = []

                if line.startswith('#'):
                    continue

                fields = str2list(line)

                name = fields[0]
                for field in fields[1:]:
                    if field == '':
                        continue
                    if field in SERIES:
                        cup.append(field)
                    elif field in TAGS:
                        tags.append(field)
                    else:
                        raise ValueError('Invalid field: ', field)

                self.competition_list.append(
                    Competition(
                        competition_id=n,
                        name=name,
                        tags=tags,
                        cup=cup
                    )
                )
                n = n+1

    def get_competition_with_id(self, competition_id):
        for competition in self.competition_list:
            if competition.competition_id is competition_id:
                return competition
        raise Exception('Competition with id "{}" not known'.format(competition_id))

    def get_competitions_with_tag(self, tag):
        competition_list = []
        for competition in self.competition_list:
            if tag in competition.tags:
                competition_list.append(competition)
        return competition_list

