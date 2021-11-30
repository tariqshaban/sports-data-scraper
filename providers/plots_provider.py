import numpy as np

from providers.sports_scraper import SportsScraper
import matplotlib.pyplot as plt


class PlotsProvider:
    __teams_id = None

    @staticmethod
    def plot_players_nationality_uefa_super_cup_league_known_clubs_2020():
        """
        Plots players information

        :return: An array of two dataframe containing match results (0: Elapsed, 1: Fixtures)
        """

        # current_year = datetime.date.today().year
        # season_years = [current_year]
        # leagues = SportsScraper.scrap_leagues().index.tolist()
        # clubs = [e for e in ClubsEnum]

        season_years = [2020]
        leagues = ['UEFA Super Cup']
        clubs = SportsScraper.get_teams_id(leagues=SportsScraper.scrap_leagues()['URL'].tolist())

        df = SportsScraper.scrap_players(season_years=season_years,
                                         leagues=leagues,
                                         clubs=clubs
                                         )

        fig, ax = plt.subplots(figsize=(10, 9))

        df = df['CLUB'].groupby(df['NAT']).count()

        if df.size != 0:
            df.plot(kind='bar', ax=ax)
        else:
            print('Cannot view the plot; the dataframe is empty')

        plt.tight_layout()
        ax.set_xticks(np.arange(len(df.index)))
        ax.set_xticklabels(df.index, rotation=45)
        fig.suptitle('Players Nationality in UEFA Super Cup for Known Clubs 2020', fontsize=20)

        plt.show()
