import datetime

from matplotlib import pyplot as plt
from scipy import stats
import pandas as pd
import statsmodels.stats.weightstats as ws

from providers.sports_scraper import SportsScraper


class HypothesisContainer:
    """
    Static methods which perform the hypothesis testing.

    Attributes
    ----------

    Methods
    -------
        __perform_test(df, col1, col2, alpha):
            Performs a t-test on two dataframe columns with numeric values.
        __visualize_test(df, col1, col2, alpha=0.05):
            Visualizes a t-test on two dataframe columns with numeric values, shows confidence interval.

        significant_difference_between_attendance_2019_and_2020(fast_fetch=True):
            Conducts a null hypothesis test on whether attendance in 2019 is higher than 2020 or not.
        significant_difference_between_attendance_2015_and_2016(fast_fetch=True):
            Conducts a null hypothesis test on whether attendance in 2015 is higher than 2016 or not.
        significant_difference_between_attendance_barcelona_and_real_madrid(fast_fetch=True):
            Conducts a null hypothesis test on whether attendance at Barcelona is higher than Real Madrid or not.

        significant_difference_between_goalkeeper_and_player_height_2020(fast_fetch=True, fast_fetch_clubs=True):
            Conducts a null hypothesis test on whether goalkeeper are taller than players or not.
        significant_difference_between_forward_and_midfielder_players_goals_2020(fast_fetch=True,
                                                                                 fast_fetch_clubs=True):
            Conducts a null hypothesis test on whether forward players attain more goals than midfielders or not.
        significant_difference_between_defender_and_midfielder_players_yellow_cards_2020(fast_fetch=True,
                                                                                         fast_fetch_clubs=True):
            Conducts a null hypothesis test on whether defenders have higher yellow cards than midfielder or not.
    """

    @staticmethod
    def __perform_test(df, col1, col2, alpha=0.05):
        """
        Performs a t-test on two dataframe columns with numeric values.

        :param pd.Dataframe df: Dataframe containing required columns
        :param str col1: First column name
        :param str col2: Second column name
        :param float alpha: Confidence interval level

        :return: A list of statistical information
        """

        n, _, diff, var, _, _ = stats.describe(df[col1] - df[col2])

        temp1 = df[col1].to_numpy()
        temp2 = df[col2].to_numpy()
        res = stats.ttest_rel(temp1, temp2)

        means = ws.CompareMeans(ws.DescrStatsW(temp1), ws.DescrStatsW(temp2))
        confint = means.tconfint_diff(alpha=alpha, alternative='two-sided', usevar='unequal')
        degfree = means.dof_satt()

        index = ['DegFreedom', 'Difference', 'Statistic', 'PValue', 'Low95CI', 'High95CI']
        return pd.Series([degfree, diff, res[0], res[1], confint[0], confint[1]], index=index)

    @staticmethod
    def __visualize_test(df, col1, col2, alpha=0.05, title=''):
        """
        Visualizes a t-test on two dataframe columns with numeric values, shows confidence interval.

        :param pd.Dataframe df: Dataframe containing required columns
        :param str col1: First column name
        :param str col2: Second column name
        :param float alpha: Confidence interval level

        :return: A list of statistical information
        """

        fig, ax = plt.subplots(2, 1, figsize=(12, 8))

        mins = min([df[col1].min(), df[col2].min()])
        maxs = max([df[col1].max(), df[col2].max()])

        mean1 = df[col1].mean()
        mean2 = df[col2].mean()

        t_stat = HypothesisContainer.__perform_test(df, col1, col2, alpha)
        pv1 = mean2 + t_stat[4]
        pv2 = mean2 + t_stat[5]

        temp = df[col1].to_numpy()
        ax[1].hist(temp, bins=30, alpha=0.7)
        ax[1].set_xlim([mins, maxs])
        ax[1].axvline(x=mean1, color='red', linewidth=4)
        ax[1].axvline(x=pv1, color='red', linestyle='--', linewidth=4)
        ax[1].axvline(x=pv2, color='red', linestyle='--', linewidth=4)
        ax[1].set_ylabel('Count')
        ax[1].set_xlabel(col1)

        temp = df[col2].to_numpy()
        ax[0].hist(temp, bins=30, alpha=0.7)
        ax[0].set_xlim([mins, maxs])
        ax[0].axvline(x=mean2, color='red', linewidth=4)
        ax[0].set_ylabel('Count')
        ax[0].set_xlabel(col2)

        plt.suptitle(title)

        return t_stat

    @staticmethod
    def significant_difference_between_attendance_2019_and_2020(fast_fetch=True):
        """
        Conducts a null hypothesis test on whether attendance in 2019 is higher than 2020 or not.

        :param bool fast_fetch: Retrieves clubs from a saved snapshot instantly

        :return: A list of statistical information
        """

        df_2019 = SportsScraper.scrap_matches(fast_fetch=fast_fetch,
                                              start_date=datetime.date(2019, 1, 1),
                                              end_date=datetime.date(2019, 12, 31)
                                              )

        df_2020 = SportsScraper.scrap_matches(fast_fetch=True,
                                              start_date=datetime.date(2020, 1, 1),
                                              end_date=datetime.date(2020, 12, 31)
                                              )

        df = df_2019.append(df_2020)

        df = df[df['ATTENDANCE'].notna()]

        df['date'] = pd.to_datetime(df['date'], utc=True)

        attendance_2019 = df[df['date'].dt.year == 2019]['ATTENDANCE'].tolist()
        attendance_2020 = df[df['date'].dt.year == 2020]['ATTENDANCE'].tolist()
        attendance_2019 = attendance_2019[:min(len(attendance_2019), len(attendance_2020))]
        attendance_2020 = attendance_2020[:min(len(attendance_2019), len(attendance_2020))]
        df1 = pd.DataFrame({
            'Attendance in 2019': attendance_2019,
            'Attendance in 2020': attendance_2020
        })

        results = HypothesisContainer.__visualize_test(df1,
                                                       'Attendance in 2019',
                                                       'Attendance in 2020',
                                                       title='Attendance in 2019 and 2020'
                                                       )
        plt.show()

        return results

    @staticmethod
    def significant_difference_between_attendance_2015_and_2016(fast_fetch=True):
        """
        Conducts a null hypothesis test on whether attendance in 2015 is higher than 2016 or not.

        :param bool fast_fetch: Retrieves clubs from a saved snapshot instantly

        :return: A list of statistical information
        """

        df_2015 = SportsScraper.scrap_matches(fast_fetch=fast_fetch,
                                              start_date=datetime.date(2015, 1, 1),
                                              end_date=datetime.date(2015, 12, 31)
                                              )

        df_2016 = SportsScraper.scrap_matches(fast_fetch=True,
                                              start_date=datetime.date(2016, 1, 1),
                                              end_date=datetime.date(2016, 12, 31)
                                              )

        df = df_2015.append(df_2016)

        df = df[df['ATTENDANCE'].notna()]

        df['date'] = pd.to_datetime(df['date'], utc=True)

        attendance_2015 = df[df['date'].dt.year == 2015]['ATTENDANCE'].tolist()
        attendance_2016 = df[df['date'].dt.year == 2016]['ATTENDANCE'].tolist()
        attendance_2015 = attendance_2015[:min(len(attendance_2015), len(attendance_2016))]
        attendance_2016 = attendance_2016[:min(len(attendance_2015), len(attendance_2016))]
        df1 = pd.DataFrame({
            'Attendance in 2015': attendance_2015,
            'Attendance in 2016': attendance_2016
        })

        results = HypothesisContainer.__visualize_test(df1,
                                                       'Attendance in 2015',
                                                       'Attendance in 2016',
                                                       title='Attendance in 2015 and 2016'
                                                       )
        plt.show()

        return results

    @staticmethod
    def significant_difference_between_attendance_barcelona_and_real_madrid(fast_fetch=True):
        """
        Conducts a null hypothesis test on whether attendance at Barcelona is higher than Real Madrid or not.

        :param bool fast_fetch: Retrieves clubs from a saved snapshot instantly

        :return: A list of statistical information
        """

        df = SportsScraper.scrap_matches(fast_fetch=fast_fetch,
                                         start_date=datetime.date(2002, 10, 1),
                                         end_date=datetime.date(2022, 5, 22)
                                         )

        df = df[df['ATTENDANCE'].notna()]

        barcelona = df[(df['club1'] == 'Barcelona') | (df['club2'] == 'Barcelona')]['ATTENDANCE'].tolist()
        real_madrid = df[(df['club1'] == 'Real Madrid') | (df['club2'] == 'Real Madrid')]['ATTENDANCE'].tolist()
        barcelona = barcelona[:min(len(barcelona), len(real_madrid))]
        real_madrid = real_madrid[:min(len(barcelona), len(real_madrid))]
        df1 = pd.DataFrame({
            'Barcelona': barcelona,
            'Real Madrid': real_madrid
        })

        results = HypothesisContainer.__visualize_test(df1,
                                                       'Barcelona',
                                                       'Real Madrid',
                                                       title='Attendance at Barcelona and Real Madrid Matches'
                                                       )
        plt.show()

        return results

    @staticmethod
    def significant_difference_between_goalkeeper_and_player_height_2020(fast_fetch=True, fast_fetch_clubs=True):
        """
        Conducts a null hypothesis test on whether goalkeeper are taller than players or not.

        :param bool fast_fetch: Retrieves clubs from a saved snapshot instantly
        :param bool fast_fetch_clubs: Retrieves clubs from a saved snapshot instantly

        :return: A list of statistical information
        """

        df = SportsScraper.scrap_players(season_years=[2020],
                                         fast_fetch=fast_fetch,
                                         fast_fetch_clubs=fast_fetch_clubs
                                         )

        df = df[df['HT'].notna() & (df['HT'] > 100) & df['POS'].notna()]

        keeper_ht = df[df['POS'] == 'G']['HT'].tolist()
        player_ht = df[df['POS'] != 'G']['HT'].tolist()
        keeper_ht = keeper_ht[:min(len(keeper_ht), len(player_ht))]
        player_ht = player_ht[:min(len(keeper_ht), len(player_ht))]
        df1 = pd.DataFrame({
            'Goalkeeper Height': keeper_ht,
            'Player Height': player_ht
        })

        results = HypothesisContainer.__visualize_test(df1,
                                                       'Goalkeeper Height',
                                                       'Player Height',
                                                       title='Goalkeeper\'s and Players\'s Heights'
                                                       )
        plt.show()

        return results

    @staticmethod
    def significant_difference_between_forward_and_midfielder_players_goals_2020(fast_fetch=True,
                                                                                 fast_fetch_clubs=True):
        """
        Conducts a null hypothesis test on whether forward players attain more goals than midfielders or not.

        :param bool fast_fetch: Retrieves clubs from a saved snapshot instantly
        :param bool fast_fetch_clubs: Retrieves clubs from a saved snapshot instantly

        :return: A list of statistical information
        """

        df = SportsScraper.scrap_players(season_years=[2020],
                                         fast_fetch=fast_fetch,
                                         fast_fetch_clubs=fast_fetch_clubs
                                         )

        df = df[df['G'].notna() & df['POS'].notna()]

        forward_g = df[df['POS'] == 'F']['G'].tolist()
        middle_g = df[df['POS'] == 'M']['G'].tolist()
        forward_g = forward_g[:min(len(forward_g), len(middle_g))]
        middle_g = middle_g[:min(len(forward_g), len(middle_g))]
        df1 = pd.DataFrame({
            'Forward Goals': forward_g,
            'Middle-Fielder Goals': middle_g
        })

        results = HypothesisContainer.__visualize_test(df1,
                                                       'Forward Goals',
                                                       'Middle-Fielder Goals',
                                                       title='Forward and Middle-Fielder Goals')
        plt.show()

        return results

    @staticmethod
    def significant_difference_between_defender_and_midfielder_players_yellow_cards_2020(fast_fetch=True,
                                                                                         fast_fetch_clubs=True):
        """
        Conducts a null hypothesis test on whether defenders have higher yellow cards than midfielder or not.

        :param bool fast_fetch: Retrieves clubs from a saved snapshot instantly
        :param bool fast_fetch_clubs: Retrieves clubs from a saved snapshot instantly

        :return: A list of statistical information
        """

        df = SportsScraper.scrap_players(season_years=[2020],
                                         fast_fetch=fast_fetch,
                                         fast_fetch_clubs=fast_fetch_clubs)

        df = df[df['YC'].notna() & df['POS'].notna()]

        defender_yc = df[df['POS'] == 'D']['YC'].tolist()
        middle_yc = df[df['POS'] == 'M']['YC'].tolist()
        defender_yc = defender_yc[:min(len(defender_yc), len(middle_yc))]
        middle_yc = middle_yc[:min(len(defender_yc), len(middle_yc))]
        df1 = pd.DataFrame({
            'Defender Yellow Cards': defender_yc,
            'Middle-Fielder Yellow Cards': middle_yc
        })

        results = HypothesisContainer.__visualize_test(df1,
                                                       'Defender Yellow Cards',
                                                       'Middle-Fielder Yellow Cards',
                                                       title='Defender and Middle-Fielder Yellow Cards'
                                                       )
        plt.show()

        return results
