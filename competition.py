"""Competition database module
"""
from utils import str2list


class Competition():
    """Competition object class
    """

    def __init__(self,
                 competition_id,
                 name,
                 series=[],
                 cup=[],
                 tags=[],
                ):
        self.competition_id = competition_id
        self.name = name
        self.series = series
        self.cup = cup
        self.tags = tags
        self.tags += ([c + '_cup' for c in self.cup])



class CompetitionDB():
    """Competition database class.
    """

    def __init__(self, series, allowed_tags, competition_file_name=None):
        self.competition_list = []
        self.series = series
        self.allowed_tags = allowed_tags
        if competition_file_name is not None:
            self.read_file(competition_file_name)

    def read_file(self, competition_file_name):
        """Create competition list from file.

        :param competition_file_name: Path to competition list file
        :returns: None
        """
        with open(competition_file_name, 'r') as competition_file:
            competition_id = 0
            for line in competition_file:
                cup = []
                tags = []

                if line.startswith('#'):
                    continue

                fields = str2list(line)

                name = fields[0]
                for field in fields[1:]:
                    if field == '':
                        continue
                    if field in self.series:
                        cup.append(field)
                    elif field in self.allowed_tags:
                        tags.append(field)
                    else:
                        raise ValueError('Invalid field: ', field)

                self.competition_list.append(
                    Competition(
                        competition_id=competition_id,
                        name=name,
                        tags=tags,
                        cup=cup
                    )
                )
                competition_id = competition_id+1

    def get_competition_with_id(self, competition_id):
        """Find competition by id.
        :param competition_id: ID of competition
        :returns: Competition object
        """
        for competition in self.competition_list:
            if competition.competition_id is competition_id:
                return competition
        raise Exception('Competition with id "{}" not known'.format(competition_id))

    def get_competitions_with_tag(self, tag):
        """Find competitions by tag.

        :param tag: Tag to be found
        :returns: list of Competition objects
        """
        competition_list = []
        for competition in self.competition_list:
            if tag in competition.tags:
                competition_list.append(competition)
        return competition_list
