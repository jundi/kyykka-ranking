#!/usr/bin/python3

import HTML
from competition import Competition, CompetitionDB
from player import Player, PlayerDB
from result import Result, ResultDB
from points import Points, SumPoints

def mm_qualification_table(competitiondb, playerdb, resultdb, pointdb):
    point_sum_dict = {}
    for player in playerdb.get_players_of_serie('MM'):
        if resultdb.player_has_results(player.id):
            mm_points = SumPoints(
                competitiondb,
                playerdb,
                resultdb).mm_points(player.id)
            point_sum_dict[player.id] = mm_points

    sorted_player_ids = (sorted(point_sum_dict, key=point_sum_dict.get)[::-1])

    rows = []
    for player_id in sorted_player_ids:
        player = playerdb.get_player_with_id(player_id)
        cells = []
        cells.append(player.name)
        for competition in competitiondb.get_mm_competitions():
            result = resultdb.get_player_result(player.id, competition.id)
            if result is None:
                cells.append("")
            else:
                cells.append(Points(competition, player, result).mm_points())
        cells.append(pointdb.mm_points(player_id))
        rows.append(cells)
    return rows

def main():
    competitiondb = CompetitionDB('data/kisat')
    playerdb = PlayerDB('data/pellaajat')
    resultdb = ResultDB('data/tulokset', playerdb)
    pointdb = SumPoints(competitiondb, playerdb, resultdb)

    tbl = mm_qualification_table(competitiondb, playerdb, resultdb, pointdb)
    print (HTML.Table(tbl))







if __name__ == "__main__":
    main()
