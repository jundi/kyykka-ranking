import competition
from points import SERIES, TAGS


db = competition.CompetitionDB(SERIES, TAGS, 'data/kisat')

for competition in db.competition_list:
    print(competition.name,competition.cup,competition.tags)
