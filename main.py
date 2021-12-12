from providers.plots_provider import PlotsProvider
from providers.hypothesis_container import HypothesisContainer
print('Scraping....')
print('--------------------------------------------------')

# Fetches from matches
PlotsProvider.matches_result_between_barcelona_real_madrid()
PlotsProvider.plot_highest_15_countries_attendance_2017()
PlotsProvider.plot_comparison_between_attendance_number_over_years()
PlotsProvider.plot_matches_occurrences_from_2017_to_2020()
PlotsProvider.plot_attendance_time_series()

# Fetches from players
PlotsProvider.top_scorer_in_leagues_2020()
PlotsProvider.barcelona_goals_over_last_10_years_spanish_laliga()
PlotsProvider.plot_relation_between_players_age_and_goals()
PlotsProvider.plot_red_and_yellow_cards_2020()
PlotsProvider.plot_players_nationality_uefa_champions_league_2020()
PlotsProvider.plot_players_goals_with_assists_scatter()
PlotsProvider.plot_players_columns_correlation()
PlotsProvider.plot_german_bundesliga_team_goals_2017()
PlotsProvider.plot_players_goals_with_assists_stacked_bar()
PlotsProvider.plot_players_goals_with_assists_box()

#########################################################
#########################################################

# Fetches from matches and applies hypothesis testing
print(HypothesisContainer.significant_difference_between_attendance_2019_and_2020())
print(HypothesisContainer.significant_difference_between_attendance_2015_and_2016())
print(HypothesisContainer.significant_difference_between_attendance_barcelona_and_real_madrid())

# Fetches from players and applies hypothesis testing
print(HypothesisContainer.significant_difference_between_goalkeeper_and_player_height_2020())
print(HypothesisContainer.significant_difference_between_forward_and_midfielder_players_goals_2020())
print(HypothesisContainer.significant_difference_between_defender_and_midfielder_players_yellow_cards_2020())

print('--------------------------------------------------')
print('Done.')
