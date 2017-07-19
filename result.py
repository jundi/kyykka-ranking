from utils import import str2list
class Result():
    def __init__(competition_id,
                 player_id,
                 serie,
                 position,
                 result,
                 ):
        self.competition_id = competition_id,
        self.player_id = player_id,
        self.serie = serie,
        self.position = position,
        self.result = result,


class ResultDB():
    def __init__(self, result_file_name=None):
        if competition_file_name is not None:
            read_file(result_file_name)

    def get_player_position(self, player_id, competition_id):
        for result in self.result_list:
            if result.player_id = player_id \
                    and result.competition_id = competition_id:
                return result.position
        return None

    def get_player_result(self, player_id, competition_id):
        for result in self.result_list:
            if result.player_id = player_id \
                    and result.competition_id = competition_id:
                return result
        return None

    def get_player_competitions(self, player_id)
        competition_id_list = []
        for result in self.result_list:
            if result.player_id == player_id
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
                competition_id = fields[0]
                serie = fields[1]
                name = fields[2]
                result = [fields[3:]

                if (competition_id is last_competition_id) and (serie is last_serie):
                    position = position + 1
                else:
                    position = 1

                self.result_list.append(
                        competition_id,
                        playerdb.get_player_with_name(name).id,
                        serie,
                        position,
                        result,
                )
