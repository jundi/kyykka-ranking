#!/usr/bin/python3
""""Print kyykkä rankings"""

import HTML
from competition import CompetitionDB
from player import PlayerDB
from result import ResultDB
from points import Points, PointsDB


def get_point_table(competitiondb, playerdb, resultdb, pointdb, serie,
                    point_type, tag):
    """Get list of  qualification points"""

    sorted_player_ids = pointdb.sort_players(point_type)

    rows = []
    for player_id in sorted_player_ids:
        player = playerdb.get_player_with_id(player_id)
        if player.serie != serie:
            continue
        cells = []
        cells.append(player.name)
        for competition in competitiondb.get_competitions_with_tag(tag):
            result = resultdb.get_player_result(player.id, competition.competition_id)
            if result is None:
                cells.append("")
            else:
                points = getattr(Points(competition, player, result), point_type)()
                cells.append(points)
        cells.append(getattr(pointdb, point_type)(player_id))
        rows.append(cells)
    return rows

def print_html_table(table, competitiondb, tag):
    header_row = ['']
    for competition in competitiondb.get_competitions_with_tag(tag):
        header_row.append(competition.name)
    header_row.append('yht.')

    print(HTML.Table(table, header_row=header_row))

HEAD="""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        table {
            width:100%;
        }
        th {
            font-size:10px;
            height: 150px;
            width: 40px;
            margin-left: 0;
            margin-right: 0;
            padding-right: 5px;
            padding-bottom: 5px;
            position: relative;
            writing-mode: sideways-lr;
        }
        tr {
            align: right;
            height: 16px;
        }
        td {
            align: right;
            height: 16px;
        }
    </style>
</head>
<body>
"""

TAIL="""</body>
</html>"""

def main():
    """Main function"""

    competitiondb = CompetitionDB('data/kisat')
    playerdb = PlayerDB('data/pellaajat')
    resultdb = ResultDB('data/results.htm', playerdb)
    pointdb = PointsDB(competitiondb, playerdb, resultdb)

    print(HEAD)
    tbl = get_point_table(competitiondb, playerdb, resultdb, pointdb, 'MM', 'mm_points', 'mm_kars')
    print_html_table(tbl, competitiondb, 'mm_kars')
    tbl = get_point_table(competitiondb, playerdb, resultdb, pointdb, 'MM', 'mo_points', 'mo_kars')
    print_html_table(tbl, competitiondb, 'mo_kars')
    tbl = get_point_table(competitiondb, playerdb, resultdb, pointdb, 'MM', 'cup_points', 'MM_cup')
    print_html_table(tbl, competitiondb, 'MM_cup')
    print(TAIL)


if __name__ == "__main__":
    main()
