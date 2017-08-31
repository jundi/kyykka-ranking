#!/usr/bin/python3
""""Print kyykkä rankings"""

import HTML
from competition import CompetitionDB
from player import PlayerDB
from result import ResultDB
# pylint: disable=import-error
from points import Points, PointsDB, SERIES, TAGS


# pylint: disable=too-many-arguments,too-many-locals
def get_point_table(competitiondb, playerdb, resultdb, pointdb, serie,
                    point_type, tag):
    """Get list of  qualification points"""

    sorted_player_ids = pointdb.sort_players(point_type, serie)

    rows = []
    for player_id in sorted_player_ids:
        player = playerdb.get_player_with_id(player_id)
        cells = []
        cells.append(player.name)
        if tag is None:
            competitions = competitiondb.competition_list
        else:
            competitions = competitiondb.get_competitions_with_tag(tag)
        for competition in  competitions:
            result = resultdb.get_player_result(player.id,
                                                competition.competition_id,
                                                serie)
            if result is None:
                cells.append("")
            else:
                points = getattr(Points(competition, result),
                                 point_type)()
                # number 0 is not printed, string "0" is printed
                if points == 0:
                    cells.append("0")
                else:
                    cells.append(points)
        cells.append(getattr(pointdb, point_type)(player_id, serie))
        rows.append(cells)
    return rows

def print_html_table(table, competitiondb, tag):
    """Print list of lists as html table"""
    header_row = ['']
    if tag is None:
        competitions = competitiondb.competition_list
    else:
        competitions = competitiondb.get_competitions_with_tag(tag)
    for competition in competitions:
        header_row.append(competition.name)
    header_row.append('yht.')

    print(HTML.Table(table, header_row=header_row))

HEAD = """<!DOCTYPE html>
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

TAIL = """</body>
</html>"""

def main():
    """Main function"""

    competitiondb = CompetitionDB(SERIES, TAGS, 'data/kisat')
    playerdb = PlayerDB(SERIES, 'data/pellaajat')
    resultdb = ResultDB('data/results.htm', playerdb)
    resultdb.read_result_file('data/loppukauden_tulokset', playerdb)
    pointdb = PointsDB(competitiondb, playerdb, resultdb)

    print(HEAD)

    print("<h2>MM-kisa karsinta</h2>")
    tbl = get_point_table(competitiondb, playerdb, resultdb, pointdb,
                          'MM', 'mm_points', 'mm_kars')
    print_html_table(tbl, competitiondb, 'mm_kars')

    print("<h2>Maaottelu karsinta</h2>")
    tbl = get_point_table(competitiondb, playerdb, resultdb, pointdb,
                          'MM', 'mo_points', 'mo_kars')
    print_html_table(tbl, competitiondb, 'mo_kars')

    print("<h2>MM Cup</h2>")
    tbl = get_point_table(competitiondb, playerdb, resultdb, pointdb,
                          'MM', 'cup_points', 'MM_cup')
    print_html_table(tbl, competitiondb, 'MM_cup')

    print("<h2>Miesten joukkue Cup</h2>")
    tbl = get_point_table(competitiondb, playerdb, resultdb, pointdb,
                          'MJ', 'cup_points', 'MJ_cup')
    print_html_table(tbl, competitiondb, 'MJ_cup')

    print("<h2>Miesten pari Cup</h2>")
    tbl = get_point_table(competitiondb, playerdb, resultdb, pointdb,
                          'MP', 'cup_points', 'MP_cup')
    print_html_table(tbl, competitiondb, 'MP_cup')

    print("<h2>NM Cup</h2>")
    tbl = get_point_table(competitiondb, playerdb, resultdb, pointdb,
                          'NM', 'cup_points', 'NM_cup')
    print_html_table(tbl, competitiondb, 'NM_cup')

    print("<h2>Naisten pari Cup</h2>")
    tbl = get_point_table(competitiondb, playerdb, resultdb, pointdb,
                          'NP', 'cup_points', 'NP_cup')
    print_html_table(tbl, competitiondb, 'NP_cup')

    print("<h2>MV Cup</h2>")
    tbl = get_point_table(competitiondb, playerdb, resultdb, pointdb,
                          'MV', 'cup_points', 'MV_cup')
    print_html_table(tbl, competitiondb, 'MV_cup')

    print("<h2>NV Cup</h2>")
    tbl = get_point_table(competitiondb, playerdb, resultdb, pointdb,
                          'NV', 'cup_points', 'NV_cup')
    print_html_table(tbl, competitiondb, 'NV_cup')

    print("<h2>Vuoden pelaaja MM</h2>")
    tbl = get_point_table(competitiondb, playerdb, resultdb, pointdb,
                          'MM', 'poy_points', None)
    print_html_table(tbl, competitiondb, None)


    print(TAIL)


if __name__ == "__main__":
    main()
