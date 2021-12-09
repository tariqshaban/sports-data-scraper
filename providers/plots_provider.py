import numpy as np
import pandas as pd
import seaborn as sns
from providers.sports_scraper import SportsScraper
import matplotlib.pyplot as plt


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

    # ---********--------*********---------****
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
    def plot_show_relation_between_players_age_and_goals_2019_english_premier_league():
        season_years = [2019]
        leagues = ['English Premier League']
        clubs = [x.name for x in SportsScraper.get_clubs(fast_fetch=True)]
        df = SportsScraper.scrap_players(season_years=season_years, leagues=leagues,
                                         clubs=clubs, fast_fetch_clubs=True, fast_fetch=True
                                         )
        df1 = pd.DataFrame()
        df1['Age_mean'] = df.groupby('CLUB')['AGE'].mean()
        df1['Goals'] = df.groupby('CLUB')['G'].sum()
        print(df1.head(10))
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
        df1['id'] = f.groupby(['LEAGUE','YEAR'])['G'].idxmax()
        df2 = f.merge(df1,how='inner',left_index=True,right_on='id')
        df2 = df2.loc[:, ['LEAGUE','YEAR','NAME']]
        df2['Goals'] = f.groupby(['LEAGUE','YEAR'])['G'].max()
        df2.reset_index(drop=True,inplace=True)
        g=sns.barplot(x='NAME', y='Goals',hue='LEAGUE', data=df2)
        g.set_title("Top scorer in 2020")
        plt.show()
