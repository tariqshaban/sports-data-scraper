import datetime

from matplotlib import pyplot as plt
from scipy import stats
import pandas as pd
import statsmodels.stats.weightstats as ws

from providers.sports_scraper import SportsScraper


class HypothesisContainer:

    @staticmethod
    def __perform_test(df, col1, col2, alpha):
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
    def __visualize_test(df, col1, col2, alpha=0.05):
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

        return t_stat

    @staticmethod
    def significant_difference_between_goalkeeper_and_player_height_2020():
        df = SportsScraper.scrap_players(season_years=[2020], fast_fetch=True)

        df = df[df['HT'].notna() & (df['HT'] > 100) & df['POS'].notna()]

        df1 = pd.DataFrame({
            'KeeperHT': df[df['POS'] == 'G']['HT'].head(1000).tolist(),
            'PlayerHT': df[df['POS'] != 'G']['HT'].head(1000).tolist()
        })

        print(HypothesisContainer.__visualize_test(df1, 'KeeperHT', 'PlayerHT'))

        plt.show()

    @staticmethod
    def significant_difference_between_forward_and_midfielder_players_goals_2020():
        df = SportsScraper.scrap_players(season_years=[2020], fast_fetch=True)

        df = df[df['G'].notna() & df['POS'].notna()]

        df1 = pd.DataFrame({
            'ForwardG': df[df['POS'] == 'F']['G'].head(1000).tolist(),
            'MiddleG': df[df['POS'] == 'M']['G'].head(1000).tolist()
        })

        print(HypothesisContainer.__visualize_test(df1, 'ForwardG', 'MiddleG'))

        plt.show()

    @staticmethod
    def significant_difference_between_defender_and_midfielder_players_yellow_cards_2020():
        df = SportsScraper.scrap_players(season_years=[2020], fast_fetch=True)

        df = df[df['YC'].notna() & df['POS'].notna()]

        df1 = pd.DataFrame({
            'DefenderYC': df[df['POS'] == 'D']['YC'].head(1000).tolist(),
            'MiddleYC': df[df['POS'] == 'M']['YC'].head(1000).tolist()
        })

        print(HypothesisContainer.__visualize_test(df1, 'DefenderYC', 'MiddleYC'))

        plt.show()

    @staticmethod
    def significant_difference_between_attendance_2017_and_2020():
        df_2017 = SportsScraper.scrap_matches(fast_fetch=True,
                                              start_date=datetime.date(2017, 1, 1),
                                              end_date=datetime.date(2017, 12, 31)
                                              )

        df_2020 = SportsScraper.scrap_matches(fast_fetch=True,
                                              start_date=datetime.date(2020, 1, 1),
                                              end_date=datetime.date(2020, 12, 31)
                                              )

        df = df_2017.append(df_2020)

        df = df[df['ATTENDANCE'].notna()]

        # Make date column date datatime
        df['date'] = pd.to_datetime(df['date'], utc=True)

        # remove the following line next push since it is already int
        df['ATTENDANCE'] = pd.to_numeric(df['ATTENDANCE'].str.replace(',', ''))

        df1 = pd.DataFrame({
            'Attendance2017': df[df['date'].dt.year == 2017]['ATTENDANCE'].head(800).tolist(),
            'Attendance2020': df[df['date'].dt.year == 2020]['ATTENDANCE'].head(800).tolist()
        })

        print(HypothesisContainer.__visualize_test(df1, 'Attendance2017', 'Attendance2020'))

        plt.show()

    @staticmethod
    def significant_difference_between_attendance_2010_and_2016():
        df_2010 = SportsScraper.scrap_matches(fast_fetch=True,
                                              start_date=datetime.date(2010, 1, 1),
                                              end_date=datetime.date(2010, 12, 31)
                                              )

        df_2016 = SportsScraper.scrap_matches(fast_fetch=True,
                                              start_date=datetime.date(2016, 1, 1),
                                              end_date=datetime.date(2016, 12, 31)
                                              )

        df = df_2010.append(df_2016)

        df = df[df['ATTENDANCE'].notna()]

        # Make date column date datatime
        df['date'] = pd.to_datetime(df['date'], utc=True)

        # remove the following line next push since it is already int
        df['ATTENDANCE'] = pd.to_numeric(df['ATTENDANCE'].str.replace(',', ''))

        df1 = pd.DataFrame({
            'Attendance2010': df[df['date'].dt.year == 2010]['ATTENDANCE'].head(1000).tolist(),
            'Attendance2016': df[df['date'].dt.year == 2016]['ATTENDANCE'].head(1000).tolist()
        })

        print(HypothesisContainer.__visualize_test(df1, 'Attendance2010', 'Attendance2016'))

        plt.show()

    @staticmethod
    def significant_difference_between_attendance_barcelona_and_real_madrid():
        df = SportsScraper.scrap_matches(fast_fetch=True,
                                         start_date=datetime.date(2002, 10, 1),
                                         end_date=datetime.date(2022, 5, 22)
                                         )

        df = df[df['ATTENDANCE'].notna()]

        # remove the following line next push since it is already int
        df['ATTENDANCE'] = pd.to_numeric(df['ATTENDANCE'].str.replace(',', ''))

        df1 = pd.DataFrame({
            'Barcelona': df[(df['club1'] == 'Barcelona') | (df['club2'] == 'Barcelona')]['ATTENDANCE']
                .head(200).tolist(),
            'RealMadrid': df[(df['club1'] == 'Real Madrid') | (df['club2'] == 'Real Madrid')]['ATTENDANCE']
                .head(200).tolist()
        })

        print(HypothesisContainer.__visualize_test(df1, 'Barcelona', 'RealMadrid'))

        plt.show()
