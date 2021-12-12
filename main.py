import datetime

from models.club import Club
from providers.plots_provider import PlotsProvider
from providers.sports_scraper import SportsScraper
from providers.hypothesis_container import HypothesisContainer
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
# PlotsProvider.plot_players_nationality_uefa_champions_league_2020()
# SportsScraper.cache_matches()
#
# print(SportsScraper.scrap_matches(fast_fetch=True))


# PlotsProvider.matches_result_between_barcelona_real_madrid()
# PlotsProvider.plot_highest_15_countries_attendance_2017()
# PlotsProvider.plot_comparison_between_attendance_number_over_years()
# PlotsProvider.plot_matches_occurrences_from_2017_to_2020()
# PlotsProvider.top_scorer_in_leagues_2020()
# PlotsProvider.barcelona_goals_over_last_10_years_spanish_laliga()
# PlotsProvider.plot_relation_between_players_age_and_goals()
# PlotsProvider.plot_red_and_yellow_cards_2020()
# PlotsProvider.plot_players_nationality_uefa_champions_league_2020()

# print(HypothesisContainer.significant_difference_between_attendance_2019_and_2020())
# print(HypothesisContainer.significant_difference_between_attendance_2015_and_2016())
# print(HypothesisContainer.significant_difference_between_attendance_barcelona_and_real_madrid())
print(HypothesisContainer.significant_difference_between_goalkeeper_and_player_height_2020())
print(HypothesisContainer.significant_difference_between_forward_and_midfielder_players_goals_2020())
print(HypothesisContainer.significant_difference_between_defender_and_midfielder_players_yellow_cards_2020())
print('--------------------------------------------------')
print('Done.')
