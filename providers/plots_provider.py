import numpy as np

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
