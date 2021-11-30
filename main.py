import datetime

from models.club import Club
from providers.plots_provider import PlotsProvider
from providers.sports_scraper import SportsScraper

print('Scraping....')
print('--------------------------------------------------')
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

# df = SportsScraper.scrap_players(season_years=[2021],
#                                  leagues=['English Premier League'],
#                                  clubs=['Arsenal'],
#                                  fast_fetch_clubs=True
#                                  )
#
# df = SportsScraper.scrap_leagues()
#
# df = SportsScraper.scrap_matches(start_date=datetime.date(2021, 11, 27),
#                                  end_date=datetime.date.today())
#
# df = SportsScraper.scrap_matches(start_date=datetime.date(2021, 11, 15),
#                                  end_date=datetime.date(2021, 12, 15))

# print(SportsScraper.get_clubs())
# print(df)
# print(df[0].shape)
# print(df[1])


PlotsProvider.plot_players_nationality_uefa_champions_league_2020()

print('--------------------------------------------------')
print('Done.')
