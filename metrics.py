# --- Metric calculation related functions ---
import pandas as pd
# pip install nba_api
from nba_api.stats.static import teams

def team_id_to_name(tid):
    nba_teams = teams.get_teams()
    team_lookup = {team['id']: team['full_name'] for team in nba_teams}
    return str(team_lookup.get(tid))

def team_abbr_to_name(abbr):
    nba_teams = teams.get_teams()
    team_lookup = {team['abbreviation']: team['full_name'] for team in nba_teams}
    return str(team_lookup.get(abbr))

def abbreviation_to_position(abbr: str) -> str:
    positions = {
        "PF": "Power Forward",
        "SG": "Shooting Guard",
        "SF": "Small Forward",
        "C": "Center",
        "PG": "Point Guard",
    }
    return positions.get(abbr, abbr)

def get_player_metrics(team_stats_df: pd.DataFrame, selected_player: str, season: str) -> dict:
    player_season_df = team_stats_df.query("Player == @selected_player & Season == @season")

    return {
        "Team": team_id_to_name(player_season_df["Team"].iloc[0]),
        "Position": abbreviation_to_position(player_season_df["Pos"].iloc[0]),
        "Age": int(player_season_df["Age"].iloc[0]),

        "GamesPlayed": int(player_season_df["G"].iloc[0]),
        "MinutesPlayed": int(player_season_df["MP"].iloc[0]),

        "FieldGoalsMade": player_season_df["FG"].iloc[0],
        "FieldGoalsAttempted": player_season_df["FGA"].iloc[0],
        "FieldGoalPercentage": player_season_df["FG%"].iloc[0] * 100,

        "ThreePointersMade": player_season_df["3P"].iloc[0],
        "ThreePointersAttempted": player_season_df["3PA"].iloc[0],
        "ThreePointersPercentage": player_season_df["3P%"].iloc[0] * 100,

        "FreeThrowsMade": player_season_df["FT"].iloc[0],
        "FreeThrowsAttempted": player_season_df["FTA"].iloc[0],
        "FreeThrowsPercentage": player_season_df["FT%"].iloc[0] * 100,

        "Assists": int(player_season_df["AST"].iloc[0]),
        "Steals": int(player_season_df["STL"].iloc[0]),
        "Blocks": int(player_season_df["BLK"].iloc[0])
    }

def feet_inches_to_cm(hgt: str) -> float:
    try:
        feet, inches = map(int, hgt.split("-"))
        return round((feet * 12 + inches) * 2.54, 2)
    except Exception:
        return float(hgt)

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
                diffs[key] = current[key] - previous[key]
            except TypeError:
                continue
    return diffs