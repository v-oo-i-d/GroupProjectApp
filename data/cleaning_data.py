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

###--- Cleaning the player dataset ---###

# Dropping irrelevant/duplicate columns:
if "Player_ID" in players_df.columns:
    players_df = players_df.drop("Player_ID", axis=1)
if "LEAGUE_ID" in players_df.columns:
    players_df = players_df.drop("LEAGUE_ID", axis=1)
if "Season" in players_df.columns:
    players_df = players_df.drop("Season", axis=1)
if "Team" in players_df.columns:
    players_df = players_df.drop("Team", axis=1)

# Dropping rows where team_id is 0
players_df = players_df[players_df["TEAM_ID"] != 0]

# Replacing country "DRC" with "Democratic Republic of the Congo"
players_df.loc[:, "Country"] = players_df["Country"].copy().replace({"DRC": "Democratic Republic of the Congo"})

# Replacing and removing invalid colleges
players_df = players_df[players_df["College"] != "New Zealand Breakers"]
players_df.College.sort_values().unique()
players_df.loc[:, "College"] = players_df["College"].copy().replace({
    "St. John's, N.Y.": "St. John's (NY)",
    "California-Santa Barbara": "Cal-Santa Barbara",
    "Louisana-Lafayette": "Louisiana-Lafayette"
})

# No NA rows
players_df[players_df.isna().all(axis=1)]

# Drop any dupes
players_df = players_df.drop_duplicates()

