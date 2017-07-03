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
                 cup_points = [],
                 poy_points = [],
                 mo_points = [],
                 mm_points = []
        ):
        self.id = id
        self.name = name
        self.cup_points = cup_points
        self.poy_points = poy_points
        self.mo_points = mo_points
        self.mm_points = mm_points


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
        cup_points = [8, 6, 4, 3, 2, 1],
        poy_points = [30, 25, 20, 15],
        mo_points = [21, 18, 16, 14,12],
        mm_points = [21, 18, 16, 14,12],
    ),
    Competition(
        id = 2,
        name = 'S-kyykkä',
        cup_points = [8, 6, 4, 3, 2, 1],
        poy_points = [30, 25, 20, 15],
        mo_points = [21, 18, 16, 14,12],
        mm_points = [21, 18, 16, 14,12],
    ),
]

results = {
        1:[1,2,3],
        2:[3,2,1],
        }

for player in players:
    for competition in competitions:
        place = results[competition.id].index(player.id)+1
        player.cup_points += competition.cup_points[place]
    print(player.name + ' ' + str(player.cup_points))
