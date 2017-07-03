#!/usr/bin/python3

MAX_PAIRS_CUP_COMPETITIONS = 5
NUM_PAIRS_CUP_COMPETITIONS = 6

MAX_TEAM_CUP_COMPETITIONS = 5
NUM_TEAM_CUP_COMPETITIONS = 6

MAX_WOMENS_PAIRS_CUP_COMPETITIONS = 6
NUM_WOMENS_PAIRS_CUP_COMPETITIONS = 8

MAX_SINGLES_CUP_COMPETITIONS = 5
NUM_SINGLES_CUP_COMPETITIONS = 6

MAX_MM_COMPETITIONS = 3
MAX_MO_COMPETITIONS = 2 # SM not included

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


class Player():

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.cup_points = 0
        self.poy_points = 0
        self.mo_points = 0
        self.mm_points = 0


class Competition():

    def __init__(self,
                 id,
                 name,
                 gender = 'male',
                 type = 'singles',
                 is_cup = False,
                 is_mo = False,
                 is_mm = False,
                 is_sm = False,
                 is_pentathlon = False,
        ):
        self.id = id
        self.name = name
        self.type = type
        self.is_cup = is_cup,
        self.is_sm = is_sm,
        self.is_mm = is_mm,
        self.is_mo = is_mo,
        self.is_pentathlon = is_pentathlon,

    def get_points(self, point_list, position):
        if position <= len(point_list):
            return point_list[position]
        else:
            return 0

    def cup_points(self, position):
        if not self.is_cup:
            return 0
        if self.type is 'singles':
            points = CUP_POINTS
            if self.is_sm:
                points = CUP_POINTS_SM

        elif (self.type is 'pairs') or (self.type is 'team'):
            points = CUP_POINTS_TEAM
            if self.is_sm:
                points = CUP_POINTS_TEAM_SM
        else:
            raise ValueError
        return self.get_points(points, position)

    def mm_points(self, position):
        if self.type is 'singles':
            if self.is_mm:
                points = MO_POINTS
                if self.is_sm:
                    points = MO_POINTS_SM
                return self.get_points(points, position)
        return 0

    def mo_points(self, position):
        if self.type is 'singles':
            if self.is_mm:
                points = MO_POINTS
                if self.is_sm:
                    points = MO_POINTS_SM
                return self.get_points(points, position)
        return 0

    def poy_points(self, position):
        if self.type is 'singles':
            points = POY_POINTS
            if self.is_cup:
                points = POY_POINTS_CUP

            if self.is_sm:
                points = POY_POINTS_SM
            return self.get_points(points, position)+1 # One point for attending
        return 0



players = [
    Player(
        id = 1,
        name = 'Mikkolainen',
    ),
    Player(
        id = 2,
        name = 'Sorvali',
    ),
    Player(
        id = 3,
        name = 'Hokkinen',
    ),
]

competitions = [
    Competition(
        id = 1,
        name = 'Nääskyykkä',
        is_cup = True,
        is_mm = True,
    ),
    Competition(
        id = 2,
        name = 'S-kyykkä',
        is_mm = True,
    ),
]

results = {
    1:[1,2,3],
    2:[3,2,1],
}

for player in players:
    cup_points = []
    poy_points = []
    mo_points = []
    mm_points = []
    mo_sm_points = 0
    cup_pentathlon_points = 0

    for competition in competitions:
        try:
            position = results[competition.id].index(player.id)+1
        except ValueError:
            # Didn't attend
            continue

        # Cup-points
        if competition.is_pentathlon:
            cup_pentathlon_points = max(cup_pentathlon_points,
                                        competition.cup_points(position))

        else:
            cup_points.append(competition.cup_points(position))

        # POY-POINTS
        poy_points.append(competition.poy_points(position))

        # World cup qualification points
        mm_points.append(competition.mm_points(position))

        # Northern countries championship qualification points
        if competition.is_sm:
            mo_sm_points = competition.mo_points(position)
        mo_points.append(competition.mo_points(position))


    player.cup_points = cup_pentathlon_points + \
                        sum(sorted(cup_points)[-MAX_SINGLES_CUP_COMPETITIONS:])
    player.poy_points = sum(poy_points)
    player.mo_points = mo_sm_points + \
                       sum(sorted(mo_points)[-MAX_MO_COMPETITIONS:])
    player.mm_points = sum(sorted(mm_points)[-MAX_MM_COMPETITIONS:])

    line = "{} {} {} {} {}".format(
        player.name,
        player.cup_points,
        player.poy_points,
        player.mo_points,
        player.mm_points,
    )
    print(line)
