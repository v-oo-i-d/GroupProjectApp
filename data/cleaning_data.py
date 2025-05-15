import pandas as pd

reg_season_df = pd.read_csv("data/NBA_Regular_Season_Games_2014_2025.csv")
play_off_df = pd.read_csv("data/NBA_Playoff_Games_2014_2025.csv")
player_info = pd.read_csv("data/NBA_Player_Info_And_Stats_2014_2025.csv")


reg_season_df['GAME_DATE'] = pd.to_datetime(reg_season_df['GAME_DATE'], errors='coerce')

print(reg_season_df['GAME_DATE'].dtypes)
print(reg_season_df['GAME_DATE'].head())

play_off_df['GAME_DATE'] = pd.to_datetime(play_off_df['GAME_DATE'], errors='coerce')

print(play_off_df['GAME_DATE'].dtypes)
print(play_off_df['GAME_DATE'].head())
#can confirm that the data type of each column is appropriate for the data (now)

print(reg_season_df.isna().sum())
print(player_info.isna().sum())
print(play_off_df.isna().sum())
#identified some emtpy rows <10 so just going to remove them :)

reg_season_df_clean = reg_season_df.dropna()
play_off_df_clean = play_off_df.dropna()
player_info = player_info.dropna()

print(reg_season_df.duplicated().sum())
print(play_off_df.duplicated().sum())
print(player_info.duplicated().sum())
#no duplicated rows.

