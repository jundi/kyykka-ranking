#!/usr/bin/python3

import competition
import player
import result
import utils

competitiondb = competition.CompetitionDB('data/kisat')

for competition in competitiondb.competition_list:
    print("{} {}".format(competition.name,competition.is_mm))

playerdb = player.PlayerDB('data/pellaajat')
for player in playerdb.player_list:
    print("{} {} {}".format(player.id, player.serie, player.name))

resultdb = result.ResultDB('data/tulokset', playerdb)

