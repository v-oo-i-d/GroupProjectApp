# --- Metric calculation related functions ---
import pandas as pd

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
        "PlayerID": player_season_df["Player_ID"].iloc[0],
        "Position": abbreviation_to_position(player_season_df["Position"].iloc[0]),
        "Age": round(player_season_df["PLAYER_AGE"].iloc[0]),
        "Weight": pounds_to_kg(pd.to_numeric(player_season_df["Weight"]).iloc[0]),
        "Height": feet_inches_to_m(player_season_df["Height"].iloc[0]),
        "Country": player_season_df["Country"].iloc[0],
        "GamesPlayed": player_season_df["GP"].iloc[0],
        "HoursPlayed": round(player_season_df["MIN"].iloc[0] / 60, 1),
    }

def feet_inches_to_m(hgt: str) -> float:
    feet, inches = map(int, hgt.split("-"))
    return round((feet * 12 + inches) * 0.0254, 2)

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
            except TypeError as e:
                continue
    return diffs