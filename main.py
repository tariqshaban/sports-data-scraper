import datetime

import pandas as pd

from sports_scrapper import SportsScraper

print('Scraping....')
print('-------------------------')
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

# df = SportsScraper.scrap_players(season_years=[2021],
#                                   leagues=['English Premier League'],
#                                   clubs=[ClubsEnum.Man_City]
#                                   )

# df = SportsScraper.scrap_clubs(leagues=['UEFA Europa League', 'English Premier League'])

# df = SportsScraper.scrap_matches(start_date=datetime.date(2021, 11, 27),
#                                  end_date=datetime.date.today())

df = SportsScraper.scrap_matches(start_date=datetime.date(2021, 11, 15),
                                 end_date=datetime.date(2021, 12, 15))
print('-------------------------')
print('Done.')
print(df[0].shape)
print(df[1])
