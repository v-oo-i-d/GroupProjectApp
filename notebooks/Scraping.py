# -----------------------------
# FULL NBA DATA 2014–2025: Games + Players + Stats (Multi-threaded)
# -----------------------------

import pandas as pd
from IPython.display import clear_output
from nba_api.stats.endpoints import leaguegamefinder, commonteamroster, playercareerstats
from nba_api.stats.static import teams
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep
import random

!pip install pandas nba_api tqdm
!pip install ipywidgets

# --- Settings ---
seasons = [f"{y}-{str(y+1)[-2:]}" for y in range(2014, 2026)]
team_list = teams.get_teams()
all_player_data = []

# -----------------------------
# PART 1: Regular Season Games
# -----------------------------
print("📊 Fetching regular season games from 2014–2025...")
regular_games = []

for season in tqdm(seasons, desc="📅 Regular Seasons"):
    try:
        gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable=season, season_type_nullable="Regular Season")
        sleep(1)
        games = gamefinder.get_data_frames()[0]
        games['SEASON'] = season
        regular_games.append(games)
    except:
        continue

regular_df = pd.concat([df for df in regular_games if df is not None and not df.empty], ignore_index=True)
regular_df.to_csv("NBA_Regular_Season_Games_2014_2025.csv", index=False)
print("✅ Saved regular season games.")

# -----------------------------
# PART 2: Playoff Games
# -----------------------------
print("🏆 Fetching playoff games from 2014–2025...")
playoff_games = []

for season in tqdm(seasons, desc="📅 Playoff Seasons"):
    try:
        gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable=season, season_type_nullable="Playoffs")
        sleep(1)
        games = gamefinder.get_data_frames()[0]
        games['SEASON'] = season
        playoff_games.append(games)
    except:
        continue
        
playoff_df = pd.concat([df for df in playoff_games if df is not None and not df.empty], ignore_index=True)
playoff_df.to_csv("NBA_Playoff_Games_2014_2025.csv", index=False)
print("✅ Saved playoff games.")

# -----------------------------
# PART 3: Player Info + Stats (Multithreaded by Roster)
# -----------------------------
print("🧍‍♂️ Fetching rosters, bios, and stats for 2014–2025...")

def fetch_player_info(player_row, team_name, season):
    try:
        player_id = player_row['PLAYER_ID']
        player_name = player_row['PLAYER']
        position = player_row['POSITION']
        height = player_row['HEIGHT']
        weight = player_row['WEIGHT']
        college = player_row['SCHOOL']
        
        response = requests.get(f"https://www.nba.com/player/{player_id}/{player_row.get('PLAYER_SLUG')}")
        soup = BeautifulSoup(response.text, "lxml")
        country = soup.find_all("p", "PlayerSummary_playerInfoValue__JS8_v")[2].text.strip()
        
        stats_df = playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]
        season_stats = stats_df[stats_df['SEASON_ID'] == season].copy()
        if not season_stats.empty:
            season_stats['Player_Name'] = player_name
            season_stats['Player_ID'] = player_id
            season_stats['Team'] = team_name
            season_stats['Season'] = season
            season_stats['Position'] = position
            season_stats['Height'] = height
            season_stats['Weight'] = weight
            season_stats['Country'] = country
            season_stats['College'] = college
            return season_stats
    except Exception:
        return None


for season in tqdm(seasons, desc="📅 Stats by Season"):
    for team in tqdm(team_list, desc=f"🏀 Teams in {season}", leave=False):
        team_id = team['id']
        team_name = team['full_name']

        try:
            roster = commonteamroster.CommonTeamRoster(team_id=team_id, season=season)
            roster_df = roster.get_data_frames()[0]
        except:
            continue

        with ThreadPoolExecutor(max_workers=25) as executor:
            futures = [executor.submit(fetch_player_info, row, team_name, season) for _, row in roster_df.iterrows()]
            for future in as_completed(futures):
                result = future.result()
                if result is not None:
                    all_player_data.append(result)
                else:
                    sleep(random.uniform(0.01, 0.05))

# --- Combine and export
final_player_df = pd.concat(all_player_data, ignore_index=True)
final_player_df.to_csv("NBA_Player_Info_And_Stats_2014_2025.csv", index=False)
clear_output()
print("✅ Done. All player info + stats saved.")
