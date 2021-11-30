import datetime

import pandas as pd
import numpy as np
import bs4
import re
import requests
from helpers.date_time_handler import DateTimeHandler
from helpers.progress_handler import ProgressHandler
from models.club import Club
from models.league import League


class SportsScraper:
    """
    Set of static methods that aid some progress manipulations.

    Attributes
    ----------
        __clubs        Acts as a cache for storing club   ids/names
        __leagues      Acts as a cache for storing league url/name

    Methods
    -------
        scrap_players(season_years=None, leagues=None, clubs=None):
            Scraps data containing information about club's players.
        __scrap_leagues():
            Scraps data containing a list of leagues.
        scrap_leagues():
            Calls __get_leagues if __leagues is None, otherwise, it retrieves __leagues immediately.
        scrap_matches(start_date=datetime.date.today() - datetime.timedelta(days=7), end_date=datetime.date.today()):
            Scraps data containing information about the results of the matches.
        __get_clubs(leagues, tolerate_too_many_requests=False, top=None):
            Calls http://site.api.espn.com/apis/site/v2/sports/soccer/{league}/clubs iteratively to fetch all clubs ids.
        get_clubs(leagues, tolerate_too_many_requests=False, top=None):
            Calls __get_clubs if __clubs is None, otherwise, it retrieves __clubs immediately.
        __get_cached_clubs():
            Retrieves the clubs snapshot.
        __cache_clubs():
            Collects a snapshot of the clubs for faster fetch in the future.
    """

    __clubs = None
    __leagues = None

    @staticmethod
    def __scrap_leagues():
        """
        Scraps data containing a list of leagues.

        :return: A list of leagues object
        """

        leagues = []

        res = requests.get('https://www.espn.com/soccer/teams')
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        ddl = soup.find('select', attrs={'class': 'dropdown__select'})

        if not ddl:
            return leagues

        options = ddl.find_all('option')
        for option in options:
            leagues.append(League(option['value'], option.text))

        return leagues

    @staticmethod
    def scrap_leagues():
        """
        Calls __get_leagues if __leagues is None, otherwise, it retrieves __leagues immediately.

        :return: A list of leagues object
        """

        if SportsScraper.__leagues is None:
            print('Fetching leagues, this is a one time process...')
            SportsScraper.__leagues = SportsScraper.__scrap_leagues()
            print('Received leagues\n')

        return SportsScraper.__leagues

    @staticmethod
    def __get_cached_clubs():
        """
        Retrieves the clubs snapshot.
        """

        clubs = []
        df = pd.read_csv('cached_clubs.csv', index_col='club_id')

        for index, row in df.iterrows():
            clubs.append(Club(index, row['club_name'], League(row['league_url'], row['league_name'])))

        return clubs

    @staticmethod
    def cache_clubs():
        """
        Collects a snapshot of the clubs for faster fetch in the future.
        """
        clubs = SportsScraper.get_clubs()

        data = {
            'club_id': [x.club_id for x in clubs],
            'club_name': [x.name for x in clubs],
            'league_url': [x.league.url for x in clubs],
            'league_name': [x.league.name for x in clubs],
        }

        df = pd.DataFrame(data)

        df.set_index('club_id', inplace=True)

        # noinspection PyTypeChecker
        df.to_csv('cached_clubs.csv')

        print(df)

    @staticmethod
    def __get_clubs(tolerate_too_many_requests=False, fast_fetch=False):
        """
        Calls http://site.api.espn.com/apis/site/v2/sports/soccer/{league}/clubs iteratively to fetch all clubs ids.

        :param bool tolerate_too_many_requests: Specify to whether throw an exception if the status code is not 200
        :param bool fast_fetch: Retrieves clubs from an only snapshot instantly
        :return: A list of clubs object
        """

        if fast_fetch:
            return SportsScraper.__get_cached_clubs()

        scraped_leagues = SportsScraper.scrap_leagues()
        clubs = []

        processed = 0
        for league in scraped_leagues:
            print(ProgressHandler.show_progress(processed, len(scraped_leagues)))
            processed += 1
            response = requests.get(f'http://site.api.espn.com/apis/site/v2/sports/soccer/{league.url}/teams')
            if response.status_code != 200 and tolerate_too_many_requests:
                continue
            for club in response.json()['sports'][0]['leagues'][0]['teams']:
                clubs.append(Club(club['team']['id'], club['team']['name'], league))

        ProgressHandler.reset_progress()

        return clubs

    @staticmethod
    def get_clubs(fast_fetch=False):
        """
        Calls __get_clubs if __clubs is None, otherwise, it retrieves __clubs immediately.

        :param bool fast_fetch: Retrieves clubs from an only snapshot instantly
        :return: A list of clubs object
        """

        if SportsScraper.__clubs is None:
            print('Fetching clubs, this is a one time process (if top maintained the same value)...')
            SportsScraper.__clubs = SportsScraper.__get_clubs(tolerate_too_many_requests=True, fast_fetch=fast_fetch)
            print('Received clubs\n')

        return SportsScraper.__clubs

    @staticmethod
    def scrap_players(season_years=None, leagues=None, clubs=None, fast_fetch_clubs=False):
        """
        Scraps data containing information about club's players.

        :param list[int] season_years: Collect the data from the provided year(s)
        :param list[str] leagues: Specify the desired league(s)
        :param list[str] clubs: Specify the desired club(s)
        :param bool fast_fetch_clubs: Retrieves clubs from an only snapshot instantly
        :return: A dataframe containing club players
        """

        if (season_years is None) or (len(season_years) == 0):
            season_years = np.arange(2000, 2022)

        scraped_leagues = SportsScraper.scrap_leagues()
        if (leagues is not None) and (len(leagues) != 0):
            scraped_leagues = list(filter(lambda x: x.name in leagues, scraped_leagues))

        if fast_fetch_clubs:
            scraped_clubs = SportsScraper.__get_cached_clubs()
        else:
            scraped_clubs = SportsScraper.get_clubs()

        if (clubs is not None) and (len(clubs) != 0):
            scraped_clubs = list(
                filter(lambda x:
                       x.name in clubs and
                       x.league.name in [x.name for x in scraped_leagues]
                       , scraped_clubs))

        if not all(isinstance(x, np.int32) or isinstance(x, int) for x in season_years):
            raise ValueError('season_year must be a list of integer')
        if not all(isinstance(x, str) for x in clubs):
            raise ValueError('clubs must be a list of string')
        if not all(isinstance(x, str) for x in leagues):
            raise ValueError('leagues must be a list of string')

        players_df_goalkeeper = pd.DataFrame()

        players_df_player = pd.DataFrame()

        processed = 0
        for season_year in season_years:
            for club in scraped_clubs:
                print(ProgressHandler.show_progress(processed,
                                                    len(season_years) * len(scraped_clubs)))
                processed += 1
                res = requests.get(
                    f'https://www.espn.com/soccer/team/squad/_/'
                    f'id/{club.club_id}/'
                    f'league/{club.league.url}/'
                    f'season/{season_year}')

                soup = bs4.BeautifulSoup(res.text, 'html.parser')
                tables = soup.find_all('table', attrs={'class': 'Table'})

                if not tables or len(tables) != 2:
                    continue

                for x in np.arange(0, 2):
                    data = []
                    rows = tables[x].find_all('tr')
                    for row in rows:
                        cols = row.find_all('td')
                        cols = [ele.text.strip() for ele in cols]  # Strips elements
                        if cols:  # If column is not empty
                            buff = [club.league.name, club.name] + [ele for ele in cols if
                                                                    ele]  # If element is not empty
                            number_list = re.findall(r'\d+$', buff[2])
                            if number_list:  # Checks if there is a number for the player
                                buff.insert(3, number_list[0])  # Extract player's number
                                buff[2] = re.findall(r'^([^0-9]*)', buff[2])[0]  # Remove player's name number
                            else:
                                buff.insert(3, np.nan)
                            data.append(buff)

                    if x == 0:
                        players_df_goalkeeper = players_df_goalkeeper.append(data)
                    else:
                        players_df_player = players_df_player.append(data)

        if players_df_goalkeeper.empty:
            players_df_goalkeeper = pd.DataFrame(np.empty((0, 18)))

        if players_df_player.empty:
            players_df_player = pd.DataFrame(np.empty((0, 19)))

        players_df_goalkeeper.columns = ['LEAGUE', 'CLUB', 'NAME', 'NUM', 'POS', 'AGE', 'HT', 'WT', 'NAT', 'APP', 'SUB',
                                         'SV', 'GA', 'A',
                                         'FC', 'FA', 'YC', 'RC']
        players_df_player.columns = ['LEAGUE', 'CLUB', 'NAME', 'NUM', 'POS', 'AGE', 'HT', 'WT', 'NAT', 'APP', 'SUB',
                                     'G', 'A', 'SH', 'ST',
                                     'FC', 'FA', 'YC', 'RC']

        df = players_df_goalkeeper.append(players_df_player)
        df = df.replace(r'^\s*$', np.nan, regex=True) \
            .replace('--', np.nan) \
            .reset_index(drop=True)

        df['WT'] = df['WT'].apply(lambda x: x if (pd.isnull(x)) else int(x.split(" ")[0]) / 2.205)
        df['HT'] = df['HT'].apply(
            lambda x: x
            if (pd.isnull(x)) else
            int(x.split("'")[0]) * 30.48 +
            int(x.split("'")[1].split("\"")[0]) * 2.54
        )

        cols = df.columns.drop(['LEAGUE', 'CLUB', 'NAME', 'POS', 'NAT'])
        df[cols] = df[cols].apply(pd.to_numeric)

        ProgressHandler.reset_progress()
        return df

    @staticmethod
    def scrap_matches(start_date=datetime.date.today() - datetime.timedelta(days=7), end_date=datetime.date.today()):
        """
        Scraps data containing information about the results of the matches.

        :param datetime.date start_date: Specify the start date of the search
        :param datetime.date end_date: Specify the end date of the search
        :return: An array of two dataframe containing match results (0: Elapsed, 1: Fixtures)
        """

        if start_date > end_date:
            raise ValueError('start_date cannot be less than end_date')

        elapsed_matches_df = pd.DataFrame()
        fixtures_list_df = pd.DataFrame()

        data = []
        processed = 0

        days_between = DateTimeHandler.get_dates_between(start_date, end_date)

        for singleDay in DateTimeHandler.get_dates_between(start_date, end_date):
            print(ProgressHandler.show_progress(processed, len(days_between)))
            processed += 1
            res = requests.get(
                f'https://www.espn.in/football/fixtures/_/'
                f'date/{singleDay}')
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
            tables = soup.find_all('tbody')

            if not tables:
                continue

            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    if cols:  # If column is not empty
                        arr = []
                        for col in np.arange(0, len(cols)):
                            if cols[col].find('small'):
                                continue
                            if col == 0:
                                club1 = cols[col].find('span').text
                                result = cols[col].find_all('a')[-1].text
                                arr.append(club1)
                                arr.append(result)
                            elif col == 1:
                                club2 = cols[col].find_all('span')[-1].text
                                arr.append(club2)
                            elif col == 2:
                                if cols[col].get('data-date'):
                                    date = datetime.datetime.strptime(cols[col].get('data-date'), '%Y-%m-%dT%H:%MZ')
                                    local_date = DateTimeHandler.datetime_from_utc_to_local(date)
                                    arr.append(
                                        '{:d}:{:02d}'.format(local_date.hour, local_date.minute))
                                else:
                                    arr.append(cols[col].find('a').text)
                            else:
                                arr.append(cols[col].text)
                        data.append(arr)

            data = list(filter(lambda x: len(x) != 0, data))

            elapsed_matches_list = list(filter(lambda x: x[3] != 'LIVE' or ':' not in x[3], data))
            fixtures_list = list(filter(lambda x: x[3] == 'LIVE' or ':' in x[3], data))

            elapsed_matches_df = elapsed_matches_df.append(elapsed_matches_list)
            fixtures_list_df = fixtures_list_df.append(fixtures_list)

        if elapsed_matches_df.empty:
            elapsed_matches_df = pd.DataFrame(np.empty((0, 6)))
        if fixtures_list_df.empty:
            fixtures_list_df = pd.DataFrame(np.empty((0, 5)))

        elapsed_matches_df.columns = ['club1', 'RESULT', 'club2', 'RESULT', 'LOCATION', 'ATTENDANCE']
        fixtures_list_df.columns = ['club1', 'RESULT', 'club2', 'TIME', 'TV']

        elapsed_matches_df = elapsed_matches_df.replace(r'^\s*$', np.nan, regex=True) \
            .replace('--', np.nan) \
            .fillna(value=np.nan) \
            .dropna(thresh=3) \
            .reset_index(drop=True)

        fixtures_list_df = fixtures_list_df.replace(r'^\s*$', np.nan, regex=True) \
            .replace('--', np.nan) \
            .fillna(value=np.nan) \
            .dropna(thresh=3) \
            .reset_index(drop=True)

        ProgressHandler.reset_progress()
        return [elapsed_matches_df, fixtures_list_df]
