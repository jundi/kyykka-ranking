"""Result database module"""
from utils import str2list

class Result():
    """Result class"""
    # pylint: disable=too-many-arguments,too-few-public-methods
    def __init__(self,
                 competition_id,
                 player_id,
                 serie,
                 position,
                 result,
                ):
        self.competition_id = competition_id
        self.player_id = player_id
        self.serie = serie
        self.position = position
        self.result = result


class ResultDB():
    """Result database class"""
    def __init__(self, result_file_name, playerdb):
        self.read_result_file(result_file_name, playerdb)

    def get_player_position(self, player_id, competition_id):
        for result in self.result_list:
            if result.player_id == player_id \
                    and result.competition_id == competition_id:
                return result.position
        return None

    def get_player_result(self, player_id, competition_id):
        for result in self.result_list:
            if (result.player_id == player_id) \
                    and (result.competition_id == competition_id):
                return result
        return None

    def get_player_competitions(self, player_id):
        competition_id_list = []
        for result in self.result_list:
            if result.player_id == player_id:
                competition_id_list.append(result.competition_id)
        return competition_id_list

    def read_result_file(self, result_file_name, playerdb):
        self.result_list = []

        last_competition_id = None
        last_serie = None

        with open(result_file_name, 'r') as result_file:
            for line in result_file:

                if line.startswith('#'):
                    continue

                fields = str2list(line)
                competition_id = int(fields[0])
                serie = fields[1]
                name = fields[2]
                result = [int(x) for x in fields[3:]]

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
                        result,
                    )
                )
    def player_has_results(self, player_id):
        for result in self.result_list:
            if result.player_id == player_id:
                return True
        return False
