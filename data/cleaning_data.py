import pandas as pd

reg_season_df = pd.read_csv("data/NBA_Regular_Season_Games_2014_2025.csv")
play_off_df = pd.read_csv("data/NBA_Playoff_Games_2014_2025.csv")


print(reg_season_df.dtypes)
print(play_off_df.dtypes)
#can confirm that the data type of each column is appropriate for the data