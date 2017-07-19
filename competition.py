from utils import str2bool
from utils import str2list

class Competition():

    def __init__(self,
                 id,
                 name,
                 series = ['MM','MA','MB','MV','NM','NA','NV','MT','MP','NP'],
                 is_singles_cup = False,
                 is_MT_cup = False,
                 is_MP_cup = False,
                 is_NP_cup = False,
                 is_cup_final = False,
                 is_mo = False,
                 is_mm = False,
                 is_sm = False,
                 is_pentathlon = False,
        ):
        self.id = id
        self.name = name
        self.series = series
        self.is_MT_cup = is_MT_cup
        self.is_MP_cup = is_MP_cup
        self.is_NP_cup = is_NP_cup
        self.is_cup_final = is_cup_final
        self.is_sm = is_sm
        self.is_mm = is_mm
        self.is_mo = is_mo
        self.is_pentathlon = is_pentathlon


class CompetitionDB():

    def __init__(self, competition_file_name=None):
        if competition_file_name is not None:
            read_file(competition_file_name)

    def read_file(self, competition_file_name):
        # Create competition list from file
        n = 0
        self.competition_list = []
        with open(competition_file_name, 'r') as competition_file:
            for line in competition_file:

                if line.startswith('#'):
                    continue

                fields = str2list(line)

                name = fields[0]
                is_cup = str2bool(fields[1])
                is_cup_final = str2bool(fields[2])
                is_mo = str2bool(fields[3])
                is_mm = str2bool(fields[4])
                is_sm = str2bool(fields[5])
                is_pentathlon = str2bool(fields[6])

                self.competitions.append(
                    Competition(
                        id = n,
                        name = name,
                        is_cup = is_cup,
                        is_cup_final = is_cup_final,
                        is_mo = is_mo,
                        is_mm = is_mm,
                        is_sm = is_sm,
                        is_pentathlon = is_pentathlon,
                        )
                )
                n = n+1

    def get_competition_with_id(self, id):
        for competition in self.competition_list:
            if competition.id is id:
                return competition
    raise Exception('Competition with id "{}" not known'.format(name))

