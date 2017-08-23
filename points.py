import competition
import player
import result

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

MAX_MO_COMPETITIONS = 2
NUM_MO_COMPETITIONS = 3

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

def remove_none_elements_from_list(list):
    return [e for e in list if e != None]

class Points():
    def __init__(self, competition, player, result):
        self.competition = competition
        self.result = result
        self.player = player
        if result is None:
            self.position = None
            self.serie = None
        else:
            self.position = result.position
            self.serie = result.serie

    def get_points(self, point_list, position):
        if position <= len(point_list):
            return point_list[position-1]
        return 0

    def cup_points(self):
        if self.position is None:
            return None

        if not self.serie in self.competition.cup:
            return None
        if self.serie in ['MM', 'NM']:
            points = CUP_POINTS
            if 'henk_sm' in self.competition.tags\
                    or 'cup_finaali' in self.competition.tags:
                points = CUP_POINTS_SM

        elif self.serie in ['MJ', 'MP', 'NP']:
            points = CUP_POINTS_TEAM
            if 'joukkue_sm' in self.competition.tags\
                    or 'cup_finaali' in self.competition.tags:
                points = CUP_POINTS_TEAM_SM
        else:
            raise ValueError
        return self.get_points(points, self.position)

    def mm_points(self):
        if self.position is None:
            return None

        if self.serie in ['MM', 'NM']:
            if 'mm_kars' in self.competition.tags:
                points = MO_POINTS
                if 'henk_SM' in self.competition.tags:
                    points = MO_POINTS_SM
                return self.get_points(points, self.position)
        return None

    def mo_points(self):
        if self.position is None:
            return None

        if self.serie in ['MM', 'NM']:
            if 'mo_kars' in self.competition.tags:
                points = MO_POINTS
                if 'henk_sm' in self.competition.tags:
                    points = MO_POINTS_SM
                return self.get_points(points, self.position)
        return None

    def poy_points(self):
        if self.position is None:
            return None

        if self.serie in ['MM', 'MA', 'MB', 'MV', 'NM', 'NA', 'NV', 'MT', 'NP']:
            points = POY_POINTS
            if self.competition.is_cup:
                points = POY_POINTS_CUP

            if self.competition.is_sm:
                points = POY_POINTS_SM
            return self.get_points(points, self.position)+1 # One point for attending
        return None


class PointsDB():

    def __init__(self, competitiondb, playerdb, resultdb):
        self.competitiondb = competitiondb
        self.playerdb = playerdb
        self.resultdb = resultdb


    def cup_points(self, player_id):
        cup_points = []
        cup_pentathlon_points = 0
        player = self.playerdb.get_player_with_id(player_id)

        for competition in self.competitiondb.competition_list:
            result = self.resultdb.get_player_result(
                player_id,
                competition.competition_id
            )
            if result is None:
                # Did not attend
                continue

            points = Points(competition, player, result).cup_points()
            if points is None:
                # No points for this cup
                continue

            if 'vo' in competition.tags:
                cup_pentathlon_points = max(
                    cup_pentathlon_points,
                    Points(competition, player, result).cup_points()
                )
            else:
                cup_points.append(
                    Points(competition, player, result).cup_points()
                )

        cup_point_sum = cup_pentathlon_points + sum(sorted(cup_points)[-MAX_SINGLES_CUP_COMPETITIONS:])

        return cup_point_sum


    def poy_points(self, player_id):
        poy_points = []
        player = self.playerdb.get_player_with_id(player_id)

        for competition in self.competitiondb.competition_list:
            result = self.resultdb.get_player_result(
                player_id,
                competition.id
            )
            if result is None:
                # Did not attend
                continue

            poy_points.append(Points(competition, player, result).poy_points())

        poy_point_sum = sum(poy_points)
        return poy_point_sum


    def mm_points(self, player_id):
        # World cup qualification points
        mm_points = []

        for competition in self.competitiondb.get_competitions_with_tag('mm_kars'):
            result = self.resultdb.get_player_result(
                player_id,
                competition.competition_id
            )
            if result is None:
                # Did not attend
                continue

            mm_points.append(Points(competition, player, result).mm_points())

        mm_point_sum = sum(sorted(remove_none_elements_from_list(mm_points))[-MAX_MM_COMPETITIONS:])
        return mm_point_sum

    def mo_points(self, player_id):
        # Northern countries championship qualification points
        mo_points = []
        sm_points = 0

        for competition in self.competitiondb.competition_list:
            result = self.resultdb.get_player_result(
                player_id,
                competition.competition_id
            )
            if result is None:
                # Did not attend
                continue

            if 'henk_sm' in competition.tags:
                sm_points = Points(competition, player, result).mo_points()
                if sm_points is None:
                    sm_points = 0
                continue

            mo_points.append(Points(competition, player, result).mo_points())

        mo_point_sum = sm_points + sum(sorted(remove_none_elements_from_list(mo_points))[-MAX_MO_COMPETITIONS:])
        return mo_point_sum

    def sort_players(self, attribute_name):

        attribute_dict = {}
        for player in self.playerdb.player_list:
            if self.resultdb.player_has_results(player.id):
                attribute = getattr(self, attribute_name)(player.id)
                attribute_dict[player.id] = attribute

        sorted_player_ids = (sorted(attribute_dict, key=attribute_dict.get)[::-1])
        return sorted_player_ids
