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
MAX_MO_COMPETITIONS = 2 # SM not included

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


class Player():

    def __init__(self, id, name, serie='MM'):
        self.id = id
        self.name = name
        self.serie = serie
        self.cup_points = 0
        self.poy_points = 0
        self.mo_points = 0
        self.mm_points = 0


class Competition():

    def __init__(self,
                 id,
                 name,
                 series = ['MM','MA','MB','MV','NM','NA','NV','MT','NP'],
                 is_cup = False,
                 is_cup_final = False,
                 is_mo = False,
                 is_mm = False,
                 is_sm = False,
                 is_pentathlon = False,
        ):
        self.id = id
        self.name = name
        self.series = series
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

    def cup_points(self, position, serie):
        if not self.is_cup:
            return 0
        if serie in ['MM','MA','MB','MV','NM','NA','NV','MT','NP']:
            points = CUP_POINTS
            if self.is_sm or self.is_cup_final:
                points = CUP_POINTS_SM

        elif serie in ['MT','MP','NP']:
            points = CUP_POINTS_TEAM
            if self.is_sm or self.is_cup_final:
                points = CUP_POINTS_TEAM_SM
        else:
            raise ValueError
        return self.get_points(points, position)

    def mm_points(self, position, serie):
        if serie in ['MM','MA','MB','MV','NM','NA','NV','MT','NP']:
            if self.is_mm:
                points = MO_POINTS
                if self.is_sm:
                    points = MO_POINTS_SM
                return self.get_points(points, position)
        return 0

    def mo_points(self, position, serie):
        if serie in ['MM','MA','MB','MV','NM','NA','NV','MT','NP']:
            if self.is_mm:
                points = MO_POINTS
                if self.is_sm:
                    points = MO_POINTS_SM
                return self.get_points(points, position)
        return 0

    def poy_points(self, position, serie):
        if serie in ['MM','MA','MB','MV','NM','NA','NV','MT','NP']:
            points = POY_POINTS
            if self.is_cup:
                points = POY_POINTS_CUP

            if self.is_sm:
                points = POY_POINTS_SM
            return self.get_points(points, position)+1 # One point for attending
        return 0



# Create player list from file
n = 0
players = []
with open('pellaajat', 'r') as pelaajatiedosto:
    for line in pelaajatiedosto:
        name = line.strip('\n')
        players.append(
            Player(
                id = n,
                name = name,
                )
        )
        n = n+1


# Create competition list from file
n = 0
competitions = []
with open('kisat', 'r') as kisatiedosto:
    for line in kisatiedosto:
        fields = line.split(',')
        name = fields[0]
        is_cup = fields[1],
        is_cup_final = fields[2],
        is_mo = fields[3],
        is_mm = fields[4],
        is_sm = fields[5],
        is_pentathlon = fields[6],
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

# Set results
results = {
    0:[1,2,3],
    1:[],
    2:[],
    3:[],
    4:[],
    5:[],
    6:[],
    7:[],
    8:[],
    9:[],
    10:[],
    11:[],
    12:[],
    13:[],
    14:[],
    15:[],
    16:[],
    17:[],
}


# Print header
print("{} {} {} {} {}".format(
        "name",
        "cup_points",
        "poy_points",
        "mo_points",
        "mm_points",
    )
)


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
        if competition.is_sm:
            mo_sm_points = competition.mo_points(position, player.serie)
        mo_points.append(competition.mo_points(position, player.serie))


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
