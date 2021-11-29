import datetime

import pandas as pd
import numpy as np
import bs4
import re
import requests as requests
from enums.clubs_enum import ClubsEnum
from helpers.date_time_handler import DateTimeHandler
from helpers.progress_handler import ProgressHandler


class SportsScraper:
    @staticmethod
    def scrap_players(season_years=None, leagues=None, clubs=None, tolerate_bad_index=False):
        """
        Scraps data containing information about club's players

        :param list[int] season_years: Collect the data from the provided year(s)
        :param list[str] leagues: Specify the desired league(s)
        :param list[Clubs] clubs: Specify the desired club(s)
        :param bool tolerate_bad_index: Specify to whether throw an exception if a league does not exist or not
        :return: A dataframe containing team players
        """

        if (season_years is None) or (len(season_years) == 0):
            season_years = [2021]
        leagues_df = SportsScraper.scrap_leagues()
        if (leagues is not None) and (len(leagues) != 0):
            if tolerate_bad_index:
                valid_keys = leagues_df.index.intersection(leagues)
                leagues_df = leagues_df.loc[valid_keys]
            else:
                leagues_df = leagues_df.loc[leagues]
        if (clubs is None) or (len(clubs) == 0):
            clubs = [e for e in ClubsEnum]

        if not all(isinstance(x, np.int32) or isinstance(x, int) for x in season_years):
            raise ValueError('season_year must be a list of integer')
        if not all(isinstance(x, ClubsEnum) for x in clubs):
            raise ValueError('clubs must be a list of clubs_enum')

        players_df_goalkeeper = pd.DataFrame()

        players_df_player = pd.DataFrame()

        processed = 0
        for season_year in season_years:
            for index, league in leagues_df.iterrows():
                for club in clubs:
                    print(ProgressHandler.show_progress(processed,
                                                        len(season_years) * len(leagues_df['URL']) * len(clubs)))
                    processed += 1
                    res = requests.get(
                        f'https://www.espn.com/soccer/team/squad/_/'
                        f'id/{club.value}/'
                        f'league/{league[0]}/'
                        f'season/{season_year}')

                    soup = bs4.BeautifulSoup(res.text, 'html.parser')
                    tables = soup.find_all('table', attrs={'class': 'Table'})

                    if not tables:
                        continue

                    for x in np.arange(0, 2):
                        data = []
                        rows = tables[x].find_all('tr')
                        for row in rows:
                            cols = row.find_all('td')
                            cols = [ele.text.strip() for ele in cols]  # Strips elements
                            if cols:  # If column is not empty
                                buff = [ele for ele in cols if ele]  # If element is not empty
                                number_list = re.findall(r'\d+$', buff[0])
                                if number_list:  # Checks if there is a number for the player
                                    buff.insert(1, number_list[0])  # Extract player's number
                                    buff[0] = re.findall(r'^([^0-9]*)', buff[0])[0]  # Remove player's name number
                                else:
                                    buff.insert(1, np.nan)
                                data.append(buff)

                        if x == 0:
                            players_df_goalkeeper = players_df_goalkeeper.append(data)
                        else:
                            players_df_player = players_df_player.append(data)

        if players_df_goalkeeper.empty:
            players_df_goalkeeper = pd.DataFrame(np.empty((0, 16)))

        if players_df_player.empty:
            players_df_player = pd.DataFrame(np.empty((0, 17)))

        players_df_goalkeeper.columns = ['NAME', 'NUM', 'POS', 'AGE', 'HT', 'WT', 'NAT', 'APP', 'SUB',
                                         'SV', 'GA', 'A',
                                         'FC', 'FA', 'YC', 'RC']
        players_df_player.columns = ['NAME', 'NUM', 'POS', 'AGE', 'HT', 'WT', 'NAT', 'APP', 'SUB',
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
        return df

    @staticmethod
    def scrap_leagues():
        """
        Scraps data containing a list of leagues
        
        :return: A dataframe containing leagues
        """

        df = pd.DataFrame()

        res = requests.get('https://www.espn.com/soccer/teams')
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        ddl = soup.find('select', attrs={'class': 'dropdown__select'})

        if not ddl:
            return df

        data = []
        options = ddl.find_all('option')
        for option in options:
            data.append([option.text, option['value']])

        df = df.append(data)

        if df.empty:
            df = pd.DataFrame(np.empty((0, 2)))

        df.columns = ['LEAGUE', 'URL']
        df.set_index('LEAGUE', inplace=True)
        return df

    @staticmethod
    def scrap_clubs(leagues=None, tolerate_bad_index=False):
        """
        Scraps data containing a list of clubs

        :param list[str] leagues: Specify the desired league(s)
        :param bool tolerate_bad_index: Specify to whether throw an exception if a league does not exist or not
        :return: A dataframe containing clubs
        """

        leagues_df = SportsScraper.scrap_leagues()
        if (leagues is not None) and (len(leagues) != 0):
            if tolerate_bad_index:
                valid_keys = leagues_df.index.intersection(leagues)
                leagues_df = leagues_df.loc[valid_keys]
            else:
                leagues_df = leagues_df.loc[leagues]

        df = pd.DataFrame()

        data = []
        processed = 0
        for index, league in leagues_df.iterrows():
            print(ProgressHandler.show_progress(processed, len(leagues_df['URL'])))
            processed += 1
            res = requests.get(
                f'https://www.espn.com/soccer/teams/_/'
                f'league/{league[0]}')
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
            clubs = soup.find_all('h2', attrs={'class': 'di clr-gray-01 h5'})

            if not clubs:
                continue

            for club in clubs:
                data.append([club.text, index])

        df = df.append(data)

        if df.empty:
            df = pd.DataFrame(np.empty((0, 2)))

        df.columns = ['LEAGUE', 'CLUB']
        df.set_index('LEAGUE', inplace=True)
        return df

    @staticmethod
    def scrap_matches(start_date=datetime.date.today() - datetime.timedelta(days=7), end_date=datetime.date.today()):
        """
        Scraps data containing information about the results of the matches

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
                                team1 = cols[col].find('span').text
                                result = cols[col].find_all('a')[-1].text
                                arr.append(team1)
                                arr.append(result)
                            elif col == 1:
                                team2 = cols[col].find_all('span')[-1].text
                                arr.append(team2)
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

            # elapsed_matches_list = list(filter(lambda x: len(x) == 6, data))
            # fixtures_list = list(filter(lambda x: len(x) != 6, data))

            elapsed_matches_list = list(filter(lambda x: x[3] != 'LIVE' or ':' not in x[3], data))
            fixtures_list = list(filter(lambda x: x[3] == 'LIVE' or ':' in x[3], data))

            elapsed_matches_df = elapsed_matches_df.append(elapsed_matches_list)
            fixtures_list_df = fixtures_list_df.append(fixtures_list)

        if elapsed_matches_df.empty:
            elapsed_matches_df = pd.DataFrame(np.empty((0, 6)))
        if fixtures_list_df.empty:
            fixtures_list_df = pd.DataFrame(np.empty((0, 5)))

        elapsed_matches_df.columns = ['TEAM1', 'RESULT', 'TEAM2', 'RESULT', 'LOCATION', 'ATTENDANCE']
        fixtures_list_df.columns = ['TEAM1', 'RESULT', 'TEAM2', 'TIME', 'TV']

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

        return [elapsed_matches_df, fixtures_list_df]
