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
        plot_players_nationality_uefa_champions_league_2020():
            Shows players nationalities in the UEFA Champions League in 2020 as a plot.
    """

    @staticmethod
    def plot_players_nationality_uefa_champions_league_2020():
        """
        Shows players nationalities in the UEFA Champions League in 2020 as a plot.
        """

        # season_years = [datetime.date.today().year]
        # leagues = SportsScraper.scrap_leagues().index.tolist()
        # clubs = SportsScraper.get_clubs()

        season_years = [2020]
        leagues = ['UEFA Champions League']
        clubs = [x.name for x in SportsScraper.get_clubs(fast_fetch=True)]

        df = SportsScraper.scrap_players(season_years=season_years,
                                         leagues=leagues,
                                         clubs=clubs
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
        years_2010, years_2011, years_2012, years_2013, years_2014, years_2015, years_2016, years_2017, years_2018, \
        years_2019, years_2020 = [2010], [2011], [2012], [2013], [2014], [2015], [2016], [2017], [2018], [2019], [2020]
        leagues = ['Spanish LaLiga']

        barcelona_players_in_2010 = SportsScraper.scrap_players(season_years=years_2010, leagues=leagues,
                                                                clubs=['Barcelona'])
        barcelona_players_in_2011 = SportsScraper.scrap_players(season_years=years_2011, leagues=leagues,
                                                                clubs=['Barcelona'])
        barcelona_players_in_2012 = SportsScraper.scrap_players(season_years=years_2012, leagues=leagues,
                                                                clubs=['Barcelona'])
        barcelona_players_in_2013 = SportsScraper.scrap_players(season_years=years_2013, leagues=leagues,
                                                                clubs=['Barcelona'])
        barcelona_players_in_2014 = SportsScraper.scrap_players(season_years=years_2014, leagues=leagues,
                                                                clubs=['Barcelona'])
        barcelona_players_in_2015 = SportsScraper.scrap_players(season_years=years_2015, leagues=leagues,
                                                                clubs=['Barcelona'])
        barcelona_players_in_2016 = SportsScraper.scrap_players(season_years=years_2016, leagues=leagues,
                                                                clubs=['Barcelona'])
        barcelona_players_in_2017 = SportsScraper.scrap_players(season_years=years_2017, leagues=leagues,
                                                                clubs=['Barcelona'])
        barcelona_players_in_2018 = SportsScraper.scrap_players(season_years=years_2018, leagues=leagues,
                                                                clubs=['Barcelona'])
        barcelona_players_in_2019 = SportsScraper.scrap_players(season_years=years_2019, leagues=leagues,
                                                                clubs=['Barcelona']
                                                                )
        barcelona_players_in_2020 = SportsScraper.scrap_players(season_years=years_2020, leagues=leagues,
                                                                clubs=['Barcelona']
                                                                )
        total_goals_in_2010 = barcelona_players_in_2010['G'].sum()
        total_goals_in_2011 = barcelona_players_in_2011['G'].sum()
        total_goals_in_2012 = barcelona_players_in_2012['G'].sum()
        total_goals_in_2013 = barcelona_players_in_2013['G'].sum()
        total_goals_in_2014 = barcelona_players_in_2014['G'].sum()
        total_goals_in_2015 = barcelona_players_in_2015['G'].sum()
        total_goals_in_2016 = barcelona_players_in_2016['G'].sum()
        total_goals_in_2017 = barcelona_players_in_2017['G'].sum()
        total_goals_in_2018 = barcelona_players_in_2018['G'].sum()
        total_goals_in_2019 = barcelona_players_in_2019['G'].sum()
        total_goals_in_2020 = barcelona_players_in_2020['G'].sum()
        df = pd.DataFrame({'Year': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020],
                           'Goals': [total_goals_in_2010, total_goals_in_2011, total_goals_in_2012,
                                     total_goals_in_2013, total_goals_in_2014, total_goals_in_2015,
                                     total_goals_in_2016, total_goals_in_2017, total_goals_in_2018,
                                     total_goals_in_2019, total_goals_in_2020]})
        sns.lineplot(data=df, x='Year', y='Goals')
        plt.show()

    @staticmethod
    def plot_show_relation_between_players_age_and_goals_2019_english_premier_league():
        season_years = [2019]
        leagues = ['English Premier League']
        clubs = [x.name for x in SportsScraper.get_clubs(fast_fetch=True)]
        df = SportsScraper.scrap_players(season_years=season_years, leagues=leagues,
                                         clubs=clubs
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
                                         clubs=clubs)
        df1 = pd.DataFrame()
        df1['Yellow Card'] = df.groupby('LEAGUE')['YC'].sum()
        df1['Red Card'] = df.groupby('LEAGUE')['RC'].sum()
        df1.plot(kind='barh', color={'Yellow Card': "yellow", 'Red Card': 'red'})
        plt.title("Number of Yellow cards and Red cards for most 5 common League")
        plt.ylabel("League")
        plt.xlabel("Number of cards")
        plt.show()
