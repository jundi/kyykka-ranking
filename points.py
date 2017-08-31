"""Ranking point calculator module

Reads results from result database, competition information from competition
database, and player information form player database. Based on this
information and rules defined in this module the PointsDB calculates
Cup-points, qualification points, and player of the year -points.
"""

SERIES = ['MM', 'MA', 'MB', 'MV', 'NM', 'NA', 'NV', 'MJ', 'MP', 'NP',
          'JP15', 'JT15', 'J15', 'JP10', 'JT10', 'J10']

TAGS = ['mm_kars', 'mo_kars', 'henk_sm', 'vo', 'HK_cup_plus', 'NP_cup_plus', 'MP_cup_plus', 'MJ_cup_plus']

# Number of competitions
MAX_PAIRS_CUP_COMPETITIONS = 5
NUM_PAIRS_CUP_COMPETITIONS = 6

MAX_TEAM_CUP_COMPETITIONS = 5
NUM_TEAM_CUP_COMPETITIONS = 6

MAX_WOMENS_PAIRS_CUP_COMPETITIONS = 6
NUM_WOMENS_PAIRS_CUP_COMPETITIONS = 8

MAX_SINGLES_CUP_COMPETITIONS = 5
NUM_SINGLES_CUP_COMPETITIONS = 8

MAX_MM_COMPETITIONS = 3
NUM_MM_COMPETITIONS = 4

MAX_MO_COMPETITIONS = 2
NUM_MO_COMPETITIONS = 3

# pylint: disable=bad-whitespace
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

def remove_none_elements_from_list(lst):
    """Removes elements with value None from list"""
    return [e for e in lst if e != None]

def read_point_table(point_list, position):
    """Return points according to the list, and zero points if points is
    not defined for this position"""
    if position <= len(point_list):
        return point_list[position-1]
    return 0


class Points():
    """Calculate points earned from a competition"""
    def __init__(self, competition, result):
        self.competition = competition
        self.result = result
        if result is None:
            self.position = None
            self.serie = None
        else:
            self.position = result.position
            self.serie = result.serie

    def cup_points(self):
        """Cup points"""
        if self.position is None:
            return None

        if not self.serie in self.competition.cup:
            return None
        if self.serie in ['MM', 'NM', 'NV', 'MV']:
            points = CUP_POINTS
            if 'HK_cup_plus' in self.competition.tags:
                points = CUP_POINTS_SM

        elif self.serie in ['MJ', 'MP', 'NP']:
            points = CUP_POINTS_TEAM
            cup_plus_tag = self.serie + "_cup_plus"
            if cup_plus_tag in self.competition.tags:
                points = CUP_POINTS_TEAM_SM
        else:
            raise ValueError
        return read_point_table(points, self.position)

    def mm_points(self):
        """World Championships qualification points"""
        if self.position is None:
            return None

        if self.serie in ['MM', 'NM']:
            if 'mm_kars' in self.competition.tags:
                points = MO_POINTS
                if 'henk_SM' in self.competition.tags:
                    points = MO_POINTS_SM
                return read_point_table(points, self.position)
        return None

    def mo_points(self):
        """National team qualification points"""
        if self.position is None:
            return None

        if self.serie in ['MM', 'NM']:
            if 'mo_kars' in self.competition.tags:
                points = MO_POINTS
                if 'henk_sm' in self.competition.tags:
                    points = MO_POINTS_SM
                return read_point_table(points, self.position)
        return None

    def poy_points(self):
        """Player of the year points"""
        if self.position is None:
            return None

        points = POY_POINTS
        if self.serie in self.competition.cup:
            points = POY_POINTS_CUP
        if self.serie in ['MM', 'MA', 'MB', 'MV', 'NM', 'NA', 'NV']:
            if 'henk_sm' in self.competition.tags:
                points = POY_POINTS_SM

        # One additional point for attending
        return read_point_table(points, self.position)+1


class PointsDB():
    """Sum cup points, qualification points, and player of the year points"""

    def __init__(self, competitiondb, playerdb, resultdb):
        self.competitiondb = competitiondb
        self.playerdb = playerdb
        self.resultdb = resultdb


    def cup_points(self, player_id, serie):
        """Sum cup points for player"""
        cup_points = []
        cup_pentathlon_points = 0

        for competition in self.competitiondb.competition_list:
            result = self.resultdb.get_player_result(
                player_id,
                competition.competition_id,
                serie
            )

            points = Points(competition, result).cup_points()
            if points is None:
                # No points for this cup
                continue

            if 'vo' in competition.tags and serie not in ['MP','MJ','NP']:
                cup_pentathlon_points = max(
                    cup_pentathlon_points,
                    Points(competition, result).cup_points()
                )
            else:
                cup_points.append(
                    Points(competition, result).cup_points()
                )

        cup_points = remove_none_elements_from_list(cup_points)
        cup_point_sum = cup_pentathlon_points\
                      + sum(sorted(cup_points)[-MAX_SINGLES_CUP_COMPETITIONS:])

        return cup_point_sum


    def poy_points(self, player_id, serie):
        """Sum player of the year points"""
        poy_points = []

        for competition in self.competitiondb.competition_list:
            result = self.resultdb.get_player_result(
                player_id,
                competition.competition_id,
                serie
            )

            poy_points.append(Points(competition, result).poy_points())

        poy_points = remove_none_elements_from_list(poy_points)
        poy_point_sum = sum(poy_points)
        return poy_point_sum


    def mm_points(self, player_id, serie):
        """Sum World championships qualification points"""
        mm_points = []

        for competition in self.competitiondb.\
                get_competitions_with_tag('mm_kars'):
            result = self.resultdb.get_player_result(
                player_id,
                competition.competition_id,
                serie
            )

            mm_points.append(Points(competition, result).mm_points())

        mm_points = remove_none_elements_from_list(mm_points)
        mm_point_sum = sum(sorted(mm_points)[-MAX_MM_COMPETITIONS:])
        return mm_point_sum

    def mo_points(self, player_id, serie):
        """Sum National team qualification points"""
        # Northern countries championship qualification points
        mo_points = []
        sm_points = 0

        for competition in self.competitiondb.competition_list:
            if 'mo_kars' not in competition.tags:
                continue
            result = self.resultdb.get_player_result(
                player_id,
                competition.competition_id,
                serie
            )

            if 'henk_sm' in competition.tags:
                sm_points = Points(competition, result).mo_points()
                if sm_points is None:
                    sm_points = 0
                continue

            mo_points.append(Points(competition, result).mo_points())

        mo_points = remove_none_elements_from_list(mo_points)
        mo_point_sum = sm_points\
                     + sum(sorted(mo_points)[-MAX_MO_COMPETITIONS:])

        return mo_point_sum

    def sort_players(self, attribute_name, serie):
        """Sort players by attribute, which is 'cup_points', 'mm_points',
        'mo_points' or 'poy_points'"""

        attribute_dict = {}
        for player in self.playerdb.player_list:
            if self.resultdb.player_has_results(player.id, serie):
                attribute = getattr(self, attribute_name)(player.id, serie)
                attribute_dict[player.id] = attribute

        return sorted(attribute_dict, key=attribute_dict.get)[::-1]
