"""test resultdb"""
from result import ResultDB
from player import PlayerDB

playerdb = PlayerDB('data/pellaajat')
result = ResultDB('data/results.htm', playerdb)

for r in result.result_list:
    p=playerdb.get_player_with_id(r.player_id)
    print(r.competition_id,r.serie,p.name,r.position,r.scores)
