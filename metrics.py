# --- Metric calculation related functions ---
import pandas as pd
# pip install nba_api
from nba_api.stats.static import teams

def team_id_to_name(tid):
    nba_teams = teams.get_teams()
    team_lookup = {team['id']: team['full_name'] for team in nba_teams}
    return str(team_lookup.get(tid))

def abbreviation_to_position(abbr: str) -> str:
    positions = {
        "G": "Point Guard / Shooting Guard",
        "G-F": "Guard / Forward",
        "F-G": "Forward / Guard",
        "F": "Small Forward / Power Forward",
        "F-C": "Forward / Center",
        "C-F": "Center / Forward",
        "C": "Center"
    }
    return positions.get(abbr, abbr)

def get_player_metrics(players_df: pd.DataFrame, selected_player: str, season: str) -> dict:
    player_season_df = players_df.query("Player_Name == @selected_player & SEASON_ID == @season")

    return {
        "PlayerID": player_season_df["PLAYER_ID"].iloc[0],
        "Team": team_id_to_name(player_season_df["TEAM_ID"].iloc[0]),
        "Position": abbreviation_to_position(player_season_df["Position"].iloc[0]),
        "Age": round(player_season_df["PLAYER_AGE"].iloc[0]),
        "Weight": pounds_to_kg(pd.to_numeric(player_season_df["Weight"]).iloc[0]),
        "Height": feet_inches_to_cm(player_season_df["Height"].iloc[0]),
        "Country": player_season_df["Country"].iloc[0],

        "GamesPlayed": player_season_df["GP"].iloc[0],
        "MinutesPlayed": round(player_season_df["MIN"].iloc[0]),

        "FieldGoalsMade": player_season_df["FGM"].iloc[0],
        "FieldGoalsAttempted": player_season_df["FGA"].iloc[0],
        "FieldGoalPercentage": round(player_season_df["FG_PCT"].iloc[0] * 100),

        "ThreePointersMade": player_season_df["FG3M"].iloc[0],
        "ThreePointersAttempted": player_season_df["FG3A"].iloc[0],
        "ThreePointersPercentage": round(player_season_df["FG3_PCT"].iloc[0] * 100),

        "FreeThrowsMade": player_season_df["FTM"].iloc[0],
        "FreeThrowsAttempted": player_season_df["FTA"].iloc[0],
        "FreeThrowsPercentage": round(player_season_df["FT_PCT"].iloc[0] * 100),

        "Assists": player_season_df["AST"].iloc[0],
        "Steals": player_season_df["STL"].iloc[0],
        "Blocks": player_season_df["BLK"].iloc[0]
    }

def feet_inches_to_cm(hgt: str) -> float:
    feet, inches = map(int, hgt.split("-"))
    return round((feet * 12 + inches) * 2.54, 2)

def pounds_to_kg(lbs: float) -> float:
    return round(lbs / 2.205, 1)

def calculate_percentage_change(old: float, new: float) -> str:
    try:
        return f"{round(((new - old) / old) * 100)}%"
    except ZeroDivisionError:
        return "0%"

def calculate_metric_diffs(current: dict, previous: dict) -> dict:
    diffs = {}
    for key in current:
        if key in previous:
            try:
                diffs[key] = int(current[key] - previous[key])
            except TypeError:
                continue
    return diffs