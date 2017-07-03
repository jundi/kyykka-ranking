import sqlite3

database = sqlite3.connect('ranking.db')

def create_player_table():
    command="""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY,
            name varchar(255),
            cup_points int DEFAULT 0
        )
        """

    print(command)

    database.execute(command)

def add_player(name):
    command="""
        INSERT INTO players (name) VALUES ('{}')
        """.format(name)

    print(command)

    database.execute(command)


create_player_table()

add_player('miika')

add_player('heikki')


command="""
SELECT * FROM players
"""
o=database.execute(command)

# database.close()
