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
print(play_off_df.isna().sum())
#identified some emtpy rows <10 so just going to remove them :)

reg_season_df_clean = reg_season_df.dropna()
play_off_df_clean = play_off_df.dropna()

print(reg_season_df.duplicated().sum())
print(play_off_df.duplicated().sum())
#no duplicated rows

#ensure values are consitent
reg_season_df['TEAM_NAME'] = reg_season_df['TEAM_NAME'].str.strip().str.upper()
play_off_df['TEAM_NAME'] = play_off_df['TEAM_NAME'].str.strip().str.upper()

#followed suit with Michael's approach to remove "irrelevant columns"
if "SEASON" in reg_season_df.columns:
    reg_season_df = reg_season_df.drop("SEASON", axis=1)
if "SEASON" in play_off_df.columns:
    play_off_df = play_off_df.drop("SEASON", axis=1)

reg_season_df['IS_PLAYOFF'] = 0
play_off_df['IS_PLAYOFF'] = 1

combined_df = pd.concat([reg_season_df, play_off_df], ignore_index=True)
play_off_df.to_csv("data/NBA_Playoff_Games_2014_2025_Cleaned.csv")
reg_season_df.to_csv("data/NBA_Regular_Season_Games_2014_2025_Cleaned.csv")
combined_df.to_csv("data/NBA_Regular_And_Playoff_Games.csv")

#print(combined_df['IS_PLAYOFF'].value_counts())  
#print(combined_df.head())

#was just used to check that df's had been combined with flags established
###--- Cleaning the player dataset ---###

# Dropping irrelevant/duplicate columns:
if "Player_ID" in player_info.columns:
    player_info = player_info.drop("Player_ID", axis=1)
if "LEAGUE_ID" in player_info.columns:
    player_info = player_info.drop("LEAGUE_ID", axis=1)
if "Season" in player_info.columns:
    player_info = player_info.drop("Season", axis=1)
if "Team" in player_info.columns:
    player_info = player_info.drop("Team", axis=1)

# Dropping rows where team_id is 0
player_info = player_info[player_info["TEAM_ID"] != 0]

# Replacing country "DRC" with "Democratic Republic of the Congo"
player_info.loc[:, "Country"] = player_info["Country"].copy().replace({"DRC": "Democratic Republic of the Congo"})

# Renaming and removing invalid colleges
player_info = player_info[player_info["College"] != "New Zealand Breakers"]
player_info.loc[:, "College"] = player_info["College"].copy().replace({
    "St. John's, N.Y.": "St. John's (NY)",
    "California-Santa Barbara": "Cal-Santa Barbara",
    "Louisana-Lafayette": "Louisiana-Lafayette"
})

# No NA rows
player_info[player_info.isna().all(axis=1)]

# Drop any dupes
player_info = player_info.drop_duplicates()

# Export
player_info.to_csv("NBA_Player_Info_And_Stats_2014_2025_Cleaned.csv")
