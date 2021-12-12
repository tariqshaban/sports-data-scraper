import numpy as np
import pandas as pd
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose

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
        matches_result_between_barcelona_real_madrid(fast_fetch=True):
            Shows the winning percentage of Barcelona and Real Madrid against each other.
        plot_highest_15_countries_attendance_2017(fast_fetch=True):
            Shows highest 15 countries which had the highest attendance count for 2017.
        plot_comparison_between_attendance_number_over_years(fast_fetch=True):
            Shows worldwide attendance fluctuation across the years.
        plot_matches_occurrences_from_2017_to_2020(fast_fetch=True):
            Shows worldwide matches counts on a daily basis between 2017 and 2020.
        plot_attendance_time_series(fast_fetch=True):
            Shows worldwide matches counts on a daily basis between 2017 and 2020.

        top_scorer_in_leagues_2020(fast_fetch=True, fast_fetch_clubs=True):
            Shows the highest players who scored for selected leagues in 2020.
        barcelona_goals_over_last_10_years_spanish_laliga(fast_fetch=True, fast_fetch_clubs=True):
            Shows barcelona score fluctuations over the last 10 years.
        plot_relation_between_players_age_and_goals(fast_fetch=True, fast_fetch_clubs=True):
            Determines for a correlation between age and number of goals.
        plot_red_and_yellow_cards_2020(fast_fetch=True, fast_fetch_clubs=True):
            Shows the number of attained red and yellow cards for selected leagues in 2020.
        plot_players_nationality_uefa_champions_league_2020(fast_fetch=True, fast_fetch_clubs=True):
            Shows players nationalities in the UEFA Champions League in 2020 as a plot.
        plot_players_goals_with_assists_scatter(fast_fetch=True, fast_fetch_clubs=True):
            Shows scattered goals with assists for each club.
        plot_players_columns_correlation(fast_fetch=True, fast_fetch_clubs=True):
            Shows correlation for all columns in the players dataframe.
        plot_german_bundesliga_team_goals_2017(fast_fetch=True, fast_fetch_clubs=True):
            Compares German Bundesliga teams in total goals during 2017.
        plot_players_goals_with_assists_stacked_bar(fast_fetch=True, fast_fetch_clubs=True):
            Compares German Bundesliga teams in total goals and assists during 2017.
        plot_players_goals_with_assists_box(fast_fetch=True, fast_fetch_clubs=True):
            Compares German Bundesliga average team player goals during 2017.

    """

    @staticmethod
    def matches_result_between_barcelona_real_madrid(fast_fetch=True):
        """
        Shows the winning percentage of Barcelona and Real Madrid against each other.

        :param bool fast_fetch: Retrieves clubs from a saved snapshot instantly
        """

        df = SportsScraper.scrap_matches(fast_fetch=fast_fetch)

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
        plt.suptitle('Winning Percentage of Barcelona and Real Madrid Against Each Other')
        plt.show()

    @staticmethod
    def plot_highest_15_countries_attendance_2017(fast_fetch=True):
        """
        Shows highest 15 countries which had the highest attendance count for 2017.

        :param bool fast_fetch: Retrieves clubs from a saved snapshot instantly
        """

        df = SportsScraper.scrap_matches(fast_fetch=fast_fetch,
                                         start_date=datetime.date(2017, 1, 1),
                                         end_date=datetime.date(2017, 12, 31)
                                         )

        df = df[df['ATTENDANCE'].notna() & df['LOCATION'].notna()]

        df['LOCATION'] = df['LOCATION'].str.split(',').str[-1].str.strip()

        df = df.groupby('LOCATION')['ATTENDANCE'].sum().sort_values(ascending=False).head(15)

        fig, ax = plt.subplots()
        df.plot(kind='bar')
        plt.tight_layout()
        ax.set_yticklabels([str(int(tick) / 1000000) + 'M' for tick in ax.get_yticks()], fontsize=8)
        ax.set_xticklabels(df.index, rotation=45)
        fig.suptitle('Highest 15 Countries Attendance Count for 2017')
        plt.show()

    @staticmethod
    def plot_comparison_between_attendance_number_over_years(fast_fetch=True):
        """
        Shows worldwide attendance fluctuation across the years.

        :param bool fast_fetch: Retrieves clubs from a saved snapshot instantly
        """

        df = SportsScraper.scrap_matches(fast_fetch=fast_fetch)
        df = df[df['ATTENDANCE'].notna() & df['LOCATION'].notna()]
        df['date'] = df['date'].astype(str).str.split('-').str[0].str.strip()
        df = df.groupby('date')['ATTENDANCE'].sum()
        fig, ax = plt.subplots()
        df.plot(kind='bar')
        plt.tight_layout()
        ax.set_yticklabels([str(int(tick) / 1000000) + 'M' for tick in ax.get_yticks()], fontsize=7)
        ax.set_xticklabels(df.index, rotation=45)
        fig.suptitle('Worldwide Attendance Fluctuation Across The Years')
        plt.show()

    @staticmethod
    def plot_matches_occurrences_from_2017_to_2020(fast_fetch=True):
        """
        Shows worldwide matches counts on a daily basis between 2017 and 2020.

        :param bool fast_fetch: Retrieves clubs from a saved snapshot instantly
        """

        df = SportsScraper.scrap_matches(fast_fetch=fast_fetch,
                                         start_date=datetime.date(2017, 1, 1),
                                         end_date=datetime.date(2020, 12, 31)
                                         )

        df['date'] = pd.to_datetime(df['date'], utc=True)

        df = df.groupby('date')['date'].count()

        calplot(df, colorbar=True, tight_layout=False, cmap='Reds',
                suptitle='Worldwide Matches Counts on A Daily Basis Between 2017 and 2020')

        plt.show()

    @staticmethod
    def plot_attendance_time_series(fast_fetch=True):
        """
        Shows worldwide daily attendance fluctuation across the years as a time series.

        :param bool fast_fetch: Retrieves clubs from a saved snapshot instantly
        """

        df = SportsScraper.scrap_matches(fast_fetch=fast_fetch,
                                         start_date=datetime.date(2005, 1, 1),
                                         end_date=datetime.date(2021, 12, 31)
                                         )

        df = df[df['ATTENDANCE'].notna() & df['LOCATION'].notna()]
        fig, ax = plt.subplots()
        df = df[['date', 'ATTENDANCE']]

        df['date'] = pd.to_datetime(df['date'])
        df = df.groupby(pd.Grouper(key='date', freq='D')).sum()
        df = df.dropna()
        df.sort_index(inplace=True)

        decomposition = seasonal_decompose(df['ATTENDANCE'])
        plt.plot(decomposition.trend)

        ax.set_yticklabels([str(int(tick) / 1000000) + 'M' for tick in ax.get_yticks()])
        fig.suptitle('Worldwide Attendance Fluctuation Across The Years')
        plt.show()

    @staticmethod
    def top_scorer_in_leagues_2020(fast_fetch=True, fast_fetch_clubs=True):
        """
        Shows the highest players who scored for selected leagues in 2020.

        :param bool fast_fetch: Retrieves clubs from a saved snapshot instantly
        :param bool fast_fetch_clubs: Retrieves clubs from a saved snapshot instantly
        """

        season_years = [2020]
        leagues = ['UEFA Champions League', 'English Premier League',
                   'German Bundesliga', 'Spanish LaLiga', 'French Ligue 1']
        f = SportsScraper.scrap_players(season_years=season_years,
                                        leagues=leagues,
                                        fast_fetch=fast_fetch,
                                        fast_fetch_clubs=fast_fetch_clubs)
        df1 = pd.DataFrame()
        df1['id'] = f.groupby(['LEAGUE', 'YEAR'])['G'].idxmax()
        df2 = f.merge(df1, how='inner', left_index=True, right_on='id')
        df2 = df2.loc[:, ['LEAGUE', 'YEAR', 'NAME']]
        df2['Goals'] = f.groupby(['LEAGUE', 'YEAR'])['G'].max()
        df2.reset_index(drop=True, inplace=True)
        g = sns.barplot(x='NAME', y='Goals', hue='LEAGUE', data=df2)

        g.set_xticklabels(df2['NAME'], rotation=10)
        g.set_title("Highest Players Who Scored For Selected Leagues in 2020")
        plt.show()

    @staticmethod
    def barcelona_goals_over_last_10_years_spanish_laliga(fast_fetch=True, fast_fetch_clubs=True):
        """
        Shows barcelona score fluctuations over the last 10 years.

        :param bool fast_fetch: Retrieves clubs from a saved snapshot instantly
        :param bool fast_fetch_clubs: Retrieves clubs from a saved snapshot instantly
        """

        years = np.arange(2012, 2022).ravel()
        leagues = ['Spanish LaLiga']
        df = SportsScraper.scrap_players(season_years=years,
                                         leagues=leagues,
                                         fast_fetch=fast_fetch,
                                         fast_fetch_clubs=fast_fetch_clubs)
        df1 = pd.DataFrame()
        barcelona_goals = df[df['CLUB'] == 'Barcelona'].groupby('YEAR')
        df1['Goals'] = barcelona_goals['G'].sum()
        sns.lineplot(data=df1, x='YEAR', y='Goals')
        plt.suptitle("Barcelona Score Fluctuations Over the Last 10 Years")
        plt.show()

    @staticmethod
    def plot_relation_between_players_age_and_goals(fast_fetch=True, fast_fetch_clubs=True):
        """
        Determines for a correlation between age and number of goals.

        :param bool fast_fetch: Retrieves clubs from a saved snapshot instantly
        :param bool fast_fetch_clubs: Retrieves clubs from a saved snapshot instantly
        """

        df = SportsScraper.scrap_players(fast_fetch=fast_fetch, fast_fetch_clubs=fast_fetch_clubs)
        df1 = pd.DataFrame()
        df1['Age_mean'] = df.groupby('CLUB')['AGE'].mean()
        df1['Goals'] = df.groupby('CLUB')['G'].sum()
        sns.regplot(x="Age_mean", y="Goals", data=df1)
        plt.xlabel("Age Mean")
        plt.suptitle("Correlation Between Age and Number of Goals")
        plt.show()

    @staticmethod
    def plot_red_and_yellow_cards_2020(fast_fetch=True, fast_fetch_clubs=True):
        """
        Shows the number of attained red and yellow cards for selected leagues in 2020.

        :param bool fast_fetch: Retrieves clubs from a saved snapshot instantly
        :param bool fast_fetch_clubs: Retrieves clubs from a saved snapshot instantly
        """

        season_years = [2020]
        leagues = ['UEFA Champions League', 'English Premier League',
                   'German Bundesliga', 'Spanish LaLiga', 'French Ligue 1']
        df = SportsScraper.scrap_players(season_years=season_years,
                                         leagues=leagues,
                                         fast_fetch=fast_fetch,
                                         fast_fetch_clubs=fast_fetch_clubs,
                                         )
        df1 = pd.DataFrame()
        df1['Yellow Card'] = df.groupby('LEAGUE')['YC'].sum()
        df1['Red Card'] = df.groupby('LEAGUE')['RC'].sum()
        df1.plot(kind='barh', color={'Yellow Card': "yellow", 'Red Card': 'red'})
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.title("Yellow cards and Red cards for Known Leagues")
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

        season_years = [2020]
        leagues = ['UEFA Champions League']

        df = SportsScraper.scrap_players(season_years=season_years,
                                         leagues=leagues,
                                         fast_fetch=fast_fetch,
                                         fast_fetch_clubs=fast_fetch_clubs
                                         )

        fig, ax = plt.subplots(figsize=(10, 9))

        df = df['CLUB'].groupby(df['NAT']).count()

        df = df[df > 1]  # Removes the clutter from the plot by removing nationalities with only one player

        df.plot(kind='bar', ax=ax)

        plt.tight_layout()
        ax.set_xticks(np.arange(len(df.index)))
        ax.set_xticklabels(df.index, rotation=45)
        fig.suptitle('Players Nationality in UEFA Champions League 2020', fontsize=20)
        plt.xlabel('Nationality')
        plt.show()

    @staticmethod
    def plot_players_goals_with_assists_scatter(fast_fetch=True, fast_fetch_clubs=True):
        """
        Shows scattered goals with assists for each club.

        :param bool fast_fetch: Retrieves clubs from a saved snapshot instantly
        :param bool fast_fetch_clubs: Retrieves clubs from a saved snapshot instantly
        """

        df = SportsScraper.scrap_players(fast_fetch=fast_fetch,
                                         fast_fetch_clubs=fast_fetch_clubs
                                         )

        df = df.groupby(df['CLUB']).mean()
        sns.regplot(data=df, x='G', y='A', line_kws={'color': 'b'})
        sns.scatterplot(data=df, x='G', y='A', hue='AGE')

        plt.suptitle('Scattered Goals With Assists for Each Club')
        plt.xlabel('Goals')
        plt.ylabel('Assists')
        plt.show()

    @staticmethod
    def plot_players_columns_correlation(fast_fetch=True, fast_fetch_clubs=True):
        """
        Shows correlation for all columns in the players dataframe.

        :param bool fast_fetch: Retrieves clubs from a saved snapshot instantly
        :param bool fast_fetch_clubs: Retrieves clubs from a saved snapshot instantly
        """

        df = SportsScraper.scrap_players(fast_fetch=fast_fetch,
                                         fast_fetch_clubs=fast_fetch_clubs
                                         )

        sns.heatmap(df.corr(), cmap='Reds')

        plt.suptitle('Correlation for Player\'s Properties')
        plt.show()

    @staticmethod
    def plot_german_bundesliga_team_goals_2017(fast_fetch=True, fast_fetch_clubs=True):
        """
        Compares German Bundesliga teams in total goals during 2017.

        :param bool fast_fetch: Retrieves clubs from a saved snapshot instantly
        :param bool fast_fetch_clubs: Retrieves clubs from a saved snapshot instantly
        """

        season_years = [2017]
        leagues = ['German Bundesliga']

        df = SportsScraper.scrap_players(season_years=season_years,
                                         leagues=leagues,
                                         fast_fetch=fast_fetch,
                                         fast_fetch_clubs=fast_fetch_clubs
                                         )
        df = df.groupby('CLUB').sum().sort_values('G')

        plt.hlines(y=df.index, xmin=0, xmax=df.G, alpha=0.4, linewidth=5)

        plt.tight_layout(rect=[0.05, 0.03, 1, 0.95])
        plt.suptitle('German Bundesliga Team\'s Total Goals During 2017')
        plt.xlabel('Goals')
        plt.ylabel('Team')
        plt.show()

    @staticmethod
    def plot_players_goals_with_assists_stacked_bar(fast_fetch=True, fast_fetch_clubs=True):
        """
        Compares German Bundesliga teams in total goals and assists during 2017.

        :param bool fast_fetch: Retrieves clubs from a saved snapshot instantly
        :param bool fast_fetch_clubs: Retrieves clubs from a saved snapshot instantly
        """

        season_years = [2017]
        leagues = ['German Bundesliga']

        df = SportsScraper.scrap_players(season_years=season_years,
                                         leagues=leagues,
                                         fast_fetch=fast_fetch,
                                         fast_fetch_clubs=fast_fetch_clubs
                                         )
        df = df.groupby('CLUB').sum()

        df[['G', 'A']].plot(kind='bar', use_index=True,
                            stacked=True,
                            title='Stacked Bar Graph by dataframe')

        plt.tight_layout(rect=[0.05, 0.03, 1, 0.95])
        plt.suptitle('German Bundesliga Team\'s Total Goals and Assists During 2017')
        plt.xlabel('Team')
        plt.legend(['Goals', 'Assists'])
        plt.show()

    @staticmethod
    def plot_players_goals_with_assists_box(fast_fetch=True, fast_fetch_clubs=True):
        """
        Compares German Bundesliga average team player goals during 2017.

        :param bool fast_fetch: Retrieves clubs from a saved snapshot instantly
        :param bool fast_fetch_clubs: Retrieves clubs from a saved snapshot instantly
        """

        season_years = [2017]
        leagues = ['German Bundesliga']

        df = SportsScraper.scrap_players(season_years=season_years,
                                         leagues=leagues,
                                         fast_fetch=fast_fetch,
                                         fast_fetch_clubs=fast_fetch_clubs
                                         )

        df['CLUB'] = df['CLUB'] \
            .apply(lambda x: (x[:10] + '..') if len(x) > 10 else x)

        df.boxplot(column='G', by='CLUB')

        plt.tight_layout(rect=[0.05, 0.03, 1, 0.95])
        plt.suptitle('German Bundesliga Average Team Player Goals During 2017')
        plt.xticks(rotation=35)
        plt.ylabel('Goals')
        plt.show()
