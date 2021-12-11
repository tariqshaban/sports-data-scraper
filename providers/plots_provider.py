import numpy as np
import pandas as pd
import seaborn as sns
from providers.sports_scraper import SportsScraper
import matplotlib.pyplot as plt
import datetime
from calplot import calplot


class PlotsProvider:
    """
    Static methods which perform the plotting functionality.

    Attributes
    ----------

    Methods
    -------
        plot_players_nationality_uefa_champions_league_2020(fast_fetch=True, fast_fetch_clubs=True):
            Shows players nationalities in the UEFA Champions League in 2020 as a plot.
    """

    @staticmethod
    def matches_result_between_barcelona_real_madrid():
        df = SportsScraper.scrap_matches(fast_fetch=True)

        df = df[(df.club1 == 'Barcelona') & (df.club2 == 'Real Madrid') | (
                (df['club1'] == 'Real Madrid') & (df['club2'] == 'Barcelona'))]

        df = df[~df['SCORE'].str.contains('v')]
        df['club1_score'] = pd.to_numeric(df['SCORE'].str.split('-').str[0].str.strip())
        df['club2_score'] = pd.to_numeric(df['SCORE'].str.split('-').str[1].str.strip())

        df['winner'] = df.apply(
            lambda x: x['club1'] if (x['club1_score'] > x['club2_score']) else x['club2'] if (
                    x['club1_score'] < x['club2_score']) else None, axis=1)

        labels = ['Barcelona', 'Real Madrid']

        plt.pie(df['winner'].value_counts(), labels=labels, autopct='%1.1f%%')
        plt.show()

    @staticmethod
    def plot_highest_15_countries_attendance_2017():
        df = SportsScraper.scrap_matches(fast_fetch=True,
                                         start_date=datetime.date(2017, 1, 1),
                                         end_date=datetime.date(2017, 12, 31)
                                         )

        df = df[df['ATTENDANCE'].notna() & df['LOCATION'].notna()]

        # remove the following line next push since it is already int
        df['ATTENDANCE'] = pd.to_numeric(df['ATTENDANCE'].str.replace(',', ''))

        df['LOCATION'] = df['LOCATION'].str.split(',').str[-1].str.strip()

        df = df.groupby('LOCATION')['ATTENDANCE'].sum().sort_values(ascending=False).head(15)

        fig, ax = plt.subplots()
        df.plot(kind='bar')
        ax.set_yticklabels([str(int(tick) / 1000000) + 'M' for tick in ax.get_yticks()])
        plt.show()

    @staticmethod
    def plot_comparison_between_attendance_number_over_years():
        df = SportsScraper.scrap_matches(fast_fetch=True)
        df = df[df['ATTENDANCE'].notna() & df['LOCATION'].notna()]
        # remove the following line next push since it is already int
        df['ATTENDANCE'] = pd.to_numeric(df['ATTENDANCE'].str.replace(',', ''))
        df['date'] = df['date'].astype(str).str.split('-').str[0].str.strip()
        df = df.groupby('date')['ATTENDANCE'].sum()
        fig, ax = plt.subplots()
        df.plot(kind='bar')
        ax.set_yticklabels([str(int(tick) / 1000000) + 'M' for tick in ax.get_yticks()])
        plt.show()

    @staticmethod
    def plot_matches_occurrences_from_2017_to_2020():
        df = SportsScraper.scrap_matches(fast_fetch=True,
                                         start_date=datetime.date(2017, 1, 1),
                                         end_date=datetime.date(2020, 12, 31)
                                         )

        #Make date column date datatime
        df['date'] = pd.to_datetime(df['date'], utc=True)

        df = df.groupby('date')['date'].count()

        calplot(df, colorbar=True, tight_layout=False, cmap='Reds',
                suptitle='Matches during 2017')

        plt.show()

    @staticmethod
    def top_scorer_in_leagues():
        season_years = [2020]
        leagues = ['UEFA Champions League', 'English Premier League',
                   'German Bundesliga', 'Spanish LaLiga', 'French Ligue 1']
        clubs = [x.name for x in SportsScraper.get_clubs(fast_fetch=True)]
        f = SportsScraper.scrap_players(season_years=season_years,
                                        leagues=leagues,
                                        clubs=clubs, fast_fetch_clubs=True, fast_fetch=True)
        df1 = pd.DataFrame()
        df2 = pd.DataFrame()
        df1['id'] = f.groupby(['LEAGUE', 'YEAR'])['G'].idxmax()
        df2 = f.merge(df1, how='inner', left_index=True, right_on='id')
        df2 = df2.loc[:, ['LEAGUE', 'YEAR', 'NAME']]
        df2['Goals'] = f.groupby(['LEAGUE', 'YEAR'])['G'].max()
        df2.reset_index(drop=True, inplace=True)
        g = sns.barplot(x='NAME', y='Goals', hue='LEAGUE', data=df2)
        g.set_title("Top scorer in 2020")
        plt.show()

    @staticmethod
    def barcelona_goals_over_last_10_years_spanish_laliga():
        years = np.arange(2010, 2020)
        clubs = [x.name for x in SportsScraper.get_clubs(fast_fetch=True)]
        leagues = ['Spanish LaLiga']
        df = SportsScraper.scrap_players(season_years=years, leagues=leagues, clubs=clubs
                                         , fast_fetch_clubs=True
                                         , fast_fetch=True)
        df1 = pd.DataFrame()
        barcelona_goals = df[df['CLUB'] == 'Barcelona'].groupby('YEAR')
        df1['Goals'] = barcelona_goals['G'].sum()
        sns.lineplot(data=df1, x='YEAR', y='Goals')
        plt.show()

    @staticmethod
    def plot_show_relation_between_players_age_and_goals():
        df = SportsScraper.scrap_players(fast_fetch_clubs=True, fast_fetch=True)
        df1 = pd.DataFrame()
        df1['Age_mean'] = df.groupby('CLUB')['AGE'].mean()
        df1['Goals'] = df.groupby('CLUB')['G'].sum()
        sns.regplot(x="Age_mean", y="Goals", data=df1)
        plt.show()

    @staticmethod
    def most_league_contain_red_and_yellow_cards():
        season_years = [2020]
        leagues = ['UEFA Champions League', 'English Premier League',
                   'German Bundesliga', 'Spanish LaLiga', 'French Ligue 1']
        clubs = [x.name for x in SportsScraper.get_clubs(fast_fetch=True)]
        df = SportsScraper.scrap_players(season_years=season_years,
                                         leagues=leagues,
                                         clubs=clubs, fast_fetch_clubs=True, fast_fetch=True)
        df1 = pd.DataFrame()
        df1['Yellow Card'] = df.groupby('LEAGUE')['YC'].sum()
        df1['Red Card'] = df.groupby('LEAGUE')['RC'].sum()
        df1.plot(kind='barh', color={'Yellow Card': "yellow", 'Red Card': 'red'})
        plt.title("Number of Yellow cards and Red cards for most 5 common League")
        plt.ylabel("League")
        plt.xlabel("Number of cards")
        plt.show()

    @staticmethod
    def plot_players_nationality_uefa_champions_league_2020(fast_fetch=True, fast_fetch_clubs=True):
        """
        Shows players nationalities in the UEFA Champions League in 2020 as a plot.

        :param bool fast_fetch: Retrieves clubs from a saved snapshot instantly
        :param bool fast_fetch_clubs: Retrieves clubs from a saved snapshot instantly
        """

        # season_years = [datetime.date.today().year]
        # leagues = SportsScraper.scrap_leagues().index.tolist()
        # clubs = SportsScraper.get_clubs()
        season_years = [2020]
        leagues = ['UEFA Champions League']
        clubs = [x.name for x in SportsScraper.get_clubs(fast_fetch=True)]

        df = SportsScraper.scrap_players(season_years=season_years,
                                         leagues=leagues,
                                         clubs=clubs,
                                         fast_fetch=True,
                                         fast_fetch_clubs=True
                                         )

        fig, ax = plt.subplots(figsize=(10, 9))

        df = df['CLUB'].groupby(df['NAT']).count()

        df = df[df > 1]  # Removes the clutter from the plot by removing nationalities with only one player

        if df.size != 0:
            df.plot(kind='bar', ax=ax)
        else:
            print('Cannot view the plot; the dataframe is empty')

        plt.tight_layout()
        ax.set_xticks(np.arange(len(df.index)))
        ax.set_xticklabels(df.index, rotation=45)
        fig.suptitle('Players Nationality in UEFA Champions League 2020', fontsize=20)
        plt.show()
