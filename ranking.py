#!/usr/bin/python3

from competition import Competition, CompetitionDB
from player import Player, PlayerDB
from result import Result, ResultDB
from points import Points, SumPoints

def main():
    competitiondb = CompetitionDB('data/kisat')

    for competition in competitiondb.competition_list:
        print("{} {}".format(competition.name, competition.is_mm))

    playerdb = PlayerDB('data/pellaajat')
    for player in playerdb.player_list:
        print("{} {} {}".format(player.id, player.serie, player.name))

    resultdb = ResultDB('data/tulokset', playerdb)

    for player in playerdb.get_players_of_serie('MM'):
        print(player.name)
        for competition in competitiondb.get_mm_competitions():
            print(
                Points(
                    competition,
                    player,
                    resultdb.get_player_result(player.id, competition.id)
                )
            ).mm_points()

if __name__ == "__main__":
    main()
