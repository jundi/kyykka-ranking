#!/usr/bin/python3
""""Print kyykkä rankings"""

import HTML
from competition import CompetitionDB
from player import PlayerDB
from result import ResultDB
from points import Points, PointsDB


def get_point_table(competitiondb, playerdb, resultdb, pointdb, serie):
    """Get list of world cup qualification points"""

    sorted_player_ids = pointdb.sort_players('mm_points')

    rows = []
    for player_id in sorted_player_ids:
        player = playerdb.get_player_with_id(player_id)
        if player.serie != serie:
            continue
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
    """Main function"""

    competitiondb = CompetitionDB('data/kisat')
    playerdb = PlayerDB('data/pellaajat')
    resultdb = ResultDB('data/tulokset', playerdb)
    pointdb = PointsDB(competitiondb, playerdb, resultdb)

    header_row = ['']
    for competition in competitiondb.get_mm_competitions():
        header_row.append(competition.name)
    header_row.append('yht.')

    print("""<head>
        <meta charset="UTF-8">
            <link href="mm.css" rel=stylesheet type="text/css" />
    </head>""")
    tbl = get_point_table(competitiondb, playerdb, resultdb, pointdb, 'MM')
    print(HTML.Table(tbl, header_row=header_row))


if __name__ == "__main__":
    main()
