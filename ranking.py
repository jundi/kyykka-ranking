#!/usr/bin/python3

from competition import Competition, CompetitionDB
from player import Player, PlayerDB
from result import Result, ResultDB
from points import Points, SumPoints

def mm_qualification(competitiondb, playerdb, resultdb):
    for player in playerdb.get_players_of_serie('MM'):
        print(player.name)
        for competition in competitiondb.get_mm_competitions():
            result = resultdb.get_player_result(player.id, competition.id)
            if result is None:
                print("")
            else:
                print("{} {}".format(result.position, Points(competition, player,
                    result).mm_points()))

def main():
    competitiondb = CompetitionDB('data/kisat')
    playerdb = PlayerDB('data/pellaajat')
    resultdb = ResultDB('data/tulokset', playerdb)




if __name__ == "__main__":
    main()
