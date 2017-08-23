import competition


db = competition.CompetitionDB('data/kisat')

for competition in db.competition_list:
    print(competition.name,competition.cup,competition.tags)
