import datetime
import pandas as pd

from models.club import Club
from plots_provider import PlotsProvider
from sports_api import SportsApi
from sports_scraper import SportsScraper

print('Scraping....')
print('--------------------------------------------------')
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

# df = SportsScraper.scrap_players(season_years=[2021],
#                                  leagues=['English Premier League'],
#                                  clubs=[Club(359, 'Arsenal')]
#                                  )

# df = SportsScraper.scrap_leagues()
#
# df = SportsScraper.scrap_clubs(leagues=['UEFA Europa League', 'English Premier League'])
#
# df = SportsScraper.scrap_matches(start_date=datetime.date(2021, 11, 27),
#                                  end_date=datetime.date.today())
#
# df = SportsScraper.scrap_matches(start_date=datetime.date(2021, 11, 15),
#                                  end_date=datetime.date(2021, 12, 15))

# print(df)
# print(df[0].shape)
# print(df[1])

PlotsProvider.plot_players_nationality_uefa_super_cup_league_known_clubs_2021()

print('--------------------------------------------------')
print('Done.')
