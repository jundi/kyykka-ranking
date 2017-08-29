"""Result database module"""
from html import parser
import codecs
import player
import htmlparser
from utils import str2list


class Result():
    """Result class"""
    # pylint: disable=too-many-arguments,too-few-public-methods
    def __init__(self,
                 competition_id,
                 player_id,
                 serie,
                 position,
                 scores,
                ):
        self.competition_id = competition_id
        self.player_id = player_id
        self.serie = serie
        self.position = position
        self.scores = scores


class ResultDB():
    """Result database class"""
    def __init__(self, result_file_name, playerdb):
        self.result_list = []
        self.parse_html_file(result_file_name, playerdb)


    def parse_html_file(self, result_file_name, playerdb):
        """Read results from html"""
        self.result_list = []
        with codecs.open(result_file_name, 'r', 'ISO-8859-1') as result_file:
            lines = ""
            for line in result_file:
                lines = lines + line
            resultparser = htmlparser.ResultsParser()
            resultparser.feed(lines)
            result_list = resultparser.get_result_list()
            for result in result_list:
                self.result_list.append(
                    Result(
                        result['competition'],
                        playerdb.get_player_with_name(result['name']).id,
                        result['serie'],
                        int(result['position'].strip('.')),
                        result['scores'],
                    )
                )


    def get_player_position(self, player_id, competition_id):
        """Get position of player in given competition"""
        for result in self.result_list:
            if result.player_id == player_id \
                    and result.competition_id == competition_id:
                return result.position
        return None


    def get_player_result(self, player_id, competition_id, serie):
        """Get result of player in competition"""
        for result in self.result_list:
            if (result.player_id == player_id) \
                    and (result.serie == serie)\
                    and (result.competition_id == competition_id):
                return result
        return None


    def get_player_competitions(self, player_id):
        """Get list of competitions the player has attended"""
        competition_id_list = []
        for result in self.result_list:
            if result.player_id == player_id:
                competition_id_list.append(result.competition_id)
        return competition_id_list


    def read_result_file(self, result_file_name, playerdb):
        """Initialize the result database from file"""
        last_competition_id = None
        last_serie = None

        with open(result_file_name, 'r') as result_file:
            for line in result_file:

                if line.startswith('#'):
                    continue

                if line.strip() == '':
                    continue

                fields = str2list(line)
                competition_id = int(fields[0])
                serie = fields[1]
                name = fields[2]
                scores = [int(x) for x in fields[3:]]

                if not (competition_id == last_competition_id \
                        and serie == last_serie):
                    position = 1
                else:
                    position = position + 1

                last_competition_id = competition_id
                last_serie = serie

                self.result_list.append(
                    Result(
                        competition_id,
                        playerdb.get_player_with_name(name).id,
                        serie,
                        position,
                        scores,
                    )
                )


    def player_has_results(self, player_id, serie):
        """Check if player has attended any competitions"""
        for result in self.result_list:
            if result.player_id == player_id\
                    and result.serie == serie:
                return True
        return False
