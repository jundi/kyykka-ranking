import competition
from points import SERIES


db = competition.CompetitionDB(SERIES, 'data/kisat')

for competition in db.competition_list:
    print(competition.name,competition.cup,competition.tags)
