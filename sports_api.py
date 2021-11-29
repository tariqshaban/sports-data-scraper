import requests

from helpers.progress_handler import ProgressHandler
from models.club import Club


class SportsApi:
    __teams_id = None

    @staticmethod
    def __get_teams_id(leagues, tolerate_too_many_requests=False, head=None):
        """
        Calls http://site.api.espn.com/apis/site/v2/sports/soccer/{league}/teams iteratively to retrieve all teams ids

        :param bool tolerate_too_many_requests: Specify to whether throw an exception if the status code is not 200
        :param int head: Specify to limit the number of league iterations, resulting in faster fetching
        :return: A list of team ids
        """

        teams = []

        if head is None:
            head = len(leagues)

        processed = 0
        for league in leagues:
            if processed > head:
                break
            print(ProgressHandler.show_progress(processed, head))
            processed += 1
            response = requests.get(f'http://site.api.espn.com/apis/site/v2/sports/soccer/{league}/teams')
            if response.status_code != 200 and tolerate_too_many_requests:
                continue
            for team in response.json()['sports'][0]['leagues'][0]['teams']:
                teams.append(Club(team['team']['id'], team['team']['name']))

        ProgressHandler.reset_progress()
        return teams

    @staticmethod
    def get_teams_id(leagues):
        if SportsApi.__teams_id is None:
            print('Getting team\'s ids, this is a one time process...')
            SportsApi.__teams_id = SportsApi.__get_teams_id(leagues=leagues, tolerate_too_many_requests=True, head=3)
            print('Received team\'s ids\n')

        return SportsApi.__teams_id
