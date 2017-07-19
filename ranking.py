#!/usr/bin/python3

# Number of competitions
MAX_PAIRS_CUP_COMPETITIONS = 5
NUM_PAIRS_CUP_COMPETITIONS = 6

MAX_TEAM_CUP_COMPETITIONS = 5
NUM_TEAM_CUP_COMPETITIONS = 6

MAX_WOMENS_PAIRS_CUP_COMPETITIONS = 6
NUM_WOMENS_PAIRS_CUP_COMPETITIONS = 8

MAX_SINGLES_CUP_COMPETITIONS = 5
NUM_SINGLES_CUP_COMPETITIONS = 6

MAX_MM_COMPETITIONS = 3
NUM_MM_COMPETITIONS = 4

MAX_MO_COMPETITIONS = 3
NUM_MO_COMPETITIONS = 4

# Points for competition type
                      #1  #2  #3  #4  #5  #6  #7  #8  #9 #10
CUP_POINTS         = [15, 13, 11,  9,  7,  5,  3,  1,        ]
CUP_POINTS_SM      = [20, 18, 16, 14, 12, 10,  8,  6,  4,  2,]
CUP_POINTS_TEAM    = [10,  8,  6,  5,  4,  3,  2,  1,        ]
CUP_POINTS_TEAM_SM = [15, 13, 11,  9,  7,  5,  3,  1,        ]
POY_POINTS         = [ 5,  3,  1,                            ]
POY_POINTS_CUP     = [10,  6,  4,                            ]
POY_POINTS_SM      = [30, 20, 10,  5,  3,  1,                ]
MO_POINTS          = [10,  9,  8,  7,  6,  5,  4,  3,  2,  1,]
MO_POINTS_SM       = [15, 12,  9,  7,  6,  5,  4,  3,  2,  1,]

def str2list(line):
                fields = line.split(',')
                fields = [x.strip() for x in fields]


def str2bool(string):
    if string in ('False', '0'):
        return False
    elif string in ('True', '1'):
        return True
    else:
        raise Exception


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

    def read_file():
        # Create competition list from file
        n = 0
        competition_list = []
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

                competitions.append(
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


class Result():
    def __init__(competition_id,
                 player_id,
                 serie,
                 position,
                 result,
                 ):
        self.competition_id = competition_id,
        self.player_id = player_id,
        self.serie = serie,
        self.position = position,
        self.result = result,


class ResultDB():
    def __init__(self, result_file_name=None):
        if competition_file_name is not None:
            read_file(result_file_name)

    def get_player_position(self, player_id, competition_id):
        for result in self.result_list:
            if result.player_id = player_id \
                    and result.competition_id = competition_id:
                return result.position

    def read_result_file(self, result_file_name, playerdb):
        self.result_list = []

        last_competition_id = None
        last_serie = None

        with open(result_file_name, 'r') as result_file:
            for line in result_file:

                if line.startswith('#'):
                    continue

                fields = str2list(line)
                competition_id = fields[0]
                serie = fields[1]
                name = fields[2]
                result = [fields[3:]

                if (competition_id is last_competition_id) and (serie is last_serie):
                    position = position + 1
                else:
                    position = 1

                self.result_list.append(
                        competition_id,
                        playerdb.get_player_with_name(name).id,
                        serie,
                        position,
                        result,
                )


class PointCalculator():
    def __init__(self, competition, player, result):
        self.competition = competition
        self.result = result
        self.player = player
        self.position = result.position

    def get_points(self, point_list, position):
        if position <= len(point_list):
            return point_list[position-1]
        else:
            return 0

    def cup_points(self, competition_id, serie, player_id):

        if position is None:
            return None

        if not ( \
            (self.competition.is_MT_cup and self.serie == 'MT') or \
            (self.competition.is_MP_cup and self.serie == 'MP') or \
            (self.competition.is_NP_cup and self.serie == 'NP') or \
            ):
            return None
        if self.serie in ['MM','NM']:
            points = CUP_POINTS
            if self.competition.is_sm or self.competition.is_cup_final:
                self.points = CUP_POINTS_SM

        elif serie in ['MT','MP','NP']:
            self.points = CUP_POINTS_TEAM
            if self.competition.is_sm or self.competition.is_cup_final:
                points = CUP_POINTS_TEAM_SM
        else:
            raise ValueError
        return self.get_points(points, self.position)

    def mm_points(self, competition_id, serie, player_id):
        if self.serie in ['MM','NM']:
            if self.competition.is_mm:
                points = MO_POINTS
                if self.competition.is_sm:
                    points = MO_POINTS_SM
                return self.competition.get_points(points, position)
        return None

    def mo_points(self, competition_id, serie, player_id)
        if self.serie in ['MM','NM']:
            if self.competition.is_mo:
                points = MO_POINTS
                if self.competition.is_sm:
                    points = MO_POINTS_SM
                return self.competition.get_points(points, position)
        return None

    def poy_points(self, competition_id, serie, player_id)
        if serie in ['MM','MA','MB','MV','NM','NA','NV','MT','NP']:
            points = POY_POINTS
            if competition.is_cup:
                points = POY_POINTS_CUP

            if competition.is_sm:
                points = POY_POINTS_SM
            return competition.get_points(points, position)+1 # One point for attending
        return None



for player in players:
    # print(player.name)
    cup_points = []
    poy_points = []
    mo_points = []
    mm_points = []
    cup_pentathlon_points = 0

    for competition in competitions:
        # print(competition.name)

        try:
            position = results[competition.id].index(player.id)+1
        except ValueError:
            # Did not attend
            continue

        # print(position)

        # Cup-points
        if competition.is_pentathlon:
            cup_pentathlon_points = max(cup_pentathlon_points,
                                        competition.cup_points(position,
                                                               player.serie))
        else:
            cup_points.append(competition.cup_points(position,
                                                     player.serie))

        # POY-POINTS
        poy_points.append(competition.poy_points(position, player.serie))

        # World cup qualification points
        mm_points.append(competition.mm_points(position, player.serie))

        # Northern countries championship qualification points
        mo_points.append(competition.mo_points(position, player.serie))


    player.cup_points = cup_pentathlon_points + \
                        sum(sorted(cup_points)[-MAX_SINGLES_CUP_COMPETITIONS:])
    player.poy_points = sum(poy_points)
    player.mo_points = sum(sorted(mo_points)[-MAX_MO_COMPETITIONS:])
    player.mm_points = sum(sorted(mm_points)[-MAX_MM_COMPETITIONS:])

    line = "{} {} {} {} {}".format(
        player.name,
        player.cup_points,
        player.poy_points,
        player.mo_points,
        player.mm_points,
    )
    print(line)
