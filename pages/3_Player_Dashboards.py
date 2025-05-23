import streamlit as st
from metrics import *
import pandas as pd
import altair as alt

st.set_page_config(page_title="Player Dashboards", page_icon="👤")

# Gather players
team_stats_df = pd.read_csv("./data/Cleaned_NBA_Per_Game_Stats_2015_2024.csv")

st.write("# Player Dashboards")
st.divider()

# Get selected player by URL ID
url_player_name = st.query_params.get("player", None)

# Try to find player name with that ID
preselect_player = None
if url_player_name:
    try:
        matches = team_stats_df[team_stats_df["Player"] == url_player_name]
        if not matches.empty:
            preselect_player = matches["Player"].iloc[0]
    except ValueError:
        pass

unique_players = team_stats_df["Player"].dropna().sort_values().unique().tolist()
default_index = unique_players.index(preselect_player) if preselect_player in unique_players else 0

selected_player = st.selectbox(
    "Search for a player:",
    options=unique_players,
    index=default_index
)
st.query_params["player"] = team_stats_df.query("Player == @selected_player")["Player"].iloc[0]

if selected_player:
    with st.container(border=True):
        # Season selector
        seasons = team_stats_df[team_stats_df["Player"] == selected_player]["Season"].sort_values(ascending=False).unique().tolist()
        default_season = seasons[0] if len(seasons) > 0 else None
        selected_season = st.segmented_control("Season", options=seasons, default=default_season)

        try:
            # Get current season metrics
            selected_index = seasons.index(selected_season)
            current_season_metrics = get_player_metrics(team_stats_df, selected_player, selected_season)

            previous_season_metrics = {}
            player_metric_diffs = {}

            # Get previous season metrics
            if selected_index + 1 < len(seasons):
                previous_season_metrics = get_player_metrics(team_stats_df, selected_player, seasons[selected_index + 1])
                player_metric_diffs = calculate_metric_diffs(current_season_metrics, previous_season_metrics)


            # Basic Info
            st.markdown("<h3>Basic Info</h3>", unsafe_allow_html=True)
            a1, a2, a3 = st.columns([1, 2, 2])
            a1.metric("Age", current_season_metrics.get('Age'), border=True)
            a2.metric("Position", current_season_metrics.get('Position'), border=True)
            a3.metric("Team", current_season_metrics.get('Team'), border=True)
            st.divider()


            # Game Stats
            st.markdown("<h3>Game Stats</h3>", unsafe_allow_html=True)
            gp = player_metric_diffs.get("GamesPlayed", 0)
            mp = player_metric_diffs.get("MinutesPlayed", 0)
            b1, b2 = st.columns(2)
            b1.metric("Games Played", current_season_metrics.get('GamesPlayed', 0), border=True, delta=gp)
            b2.metric("Minutes Played", current_season_metrics.get('MinutesPlayed', 0), border=True, delta=mp)
            st.divider()


            # Field Goals
            st.markdown("<h3>Field Goals</h3>", unsafe_allow_html=True)
            fgm = round(player_metric_diffs.get("FieldGoalsMade"), 1) if player_metric_diffs.get("FieldGoalsMade", None) else 0
            fga = round(player_metric_diffs.get("FieldGoalsAttempted"), 1) if player_metric_diffs.get("FieldGoalsAttempted", None) else 0
            fgr = round(player_metric_diffs.get("FieldGoalPercentage"), 1) if player_metric_diffs.get("FieldGoalPercentage", None) else 0
            c1, c2, c3 = st.columns(3)
            c1.metric("Made", current_season_metrics.get("FieldGoalsMade", 0), border=True, delta=fgm)
            c2.metric("Attempted", current_season_metrics.get("FieldGoalsAttempted", 0), border=True, delta=fga)
            c3.metric("Rate (%)", current_season_metrics.get("FieldGoalPercentage", 1), border=True, delta=fgr)


            # Three Pointers
            st.markdown("<h3>Three Pointers</h3>", unsafe_allow_html=True)
            tpm = round(player_metric_diffs.get("ThreePointersMade"), 1) if player_metric_diffs.get("ThreePointersMade", None) else 0
            tpa = round(player_metric_diffs.get("ThreePointersAttempted"), 1) if player_metric_diffs.get("ThreePointersAttempted", None) else 0
            tpr = round(player_metric_diffs.get("ThreePointersPercentage"), 1) if player_metric_diffs.get("ThreePointersPercentage", None) else 0
            c1, c2, c3 = st.columns(3)
            c1.metric("Made", current_season_metrics.get("ThreePointersMade", 0), border=True, delta=tpm)
            c2.metric("Attempted", current_season_metrics.get("ThreePointersAttempted", 0), border=True, delta=tpa)
            c3.metric("Rate (%)", round(current_season_metrics.get("ThreePointersPercentage", 0), 1), border=True, delta=tpr)


            # Free Throws
            st.markdown("<h3>Free Throws</h3>", unsafe_allow_html=True)
            ftm = round(player_metric_diffs.get("FreeThrowsMade"), 1) if player_metric_diffs.get("FreeThrowsMade", None) else 0
            fta = round(player_metric_diffs.get("FreeThrowsAttempted"), 1) if player_metric_diffs.get("FreeThrowsAttempted", None) else 0
            ftr = round(player_metric_diffs.get("FreeThrowsPercentage"), 1) if player_metric_diffs.get("FreeThrowsPercentage", None) else 0
            c1, c2, c3 = st.columns(3)
            c1.metric("Made", current_season_metrics.get("FreeThrowsMade", 0), border=True, delta=ftm)
            c2.metric("Attempted", current_season_metrics.get("FreeThrowsAttempted", 0), border=True, delta=fta)
            c3.metric("Rate (%)", round(current_season_metrics.get("FreeThrowsPercentage", 0), 1), border=True,delta=ftr)
            st.divider()


            metrics_to_plot = ["FG%", "FT%", "3P%"]
            team_stats_df[metrics_to_plot] = team_stats_df[metrics_to_plot].apply(pd.to_numeric, errors='coerce')

            # Calculate metric means per season
            season_avg_df = (team_stats_df
                             .query("Player == @selected_player")
                             .groupby("Season")[metrics_to_plot]
                             .mean()
                             .reset_index())

            # Melt to long format
            melted_avg_df = season_avg_df.melt(
                id_vars="Season",
                var_name="Metric",
                value_name="Average"
            )
            melted_avg_df["Metric"] = melted_avg_df["Metric"].map({"FG%": "Field Goals", "FT%": "Free Throws", "3P%": "3-Pointers"})
            melted_avg_df["Average"] *= 100

            chart = alt.Chart(melted_avg_df).mark_line(point=True).encode(
                x=alt.X("Season:N", title="Season"),
                y=alt.Y("Average:Q", title="Percentage (%)", scale=alt.Scale(domain=[0, 100])),
                color=alt.Color("Metric:N", title="Metric")
            ).properties(
                title="Shooting Percentages Over Seasons",
                height=700
            )
            st.altair_chart(chart, use_container_width=True)
            st.divider()


            # Playmaking and Defense
            st.markdown("<h3>Playmaking and Defense</h3>", unsafe_allow_html=True)
            f1, f2, f3 = st.columns(3)
            f1.metric("Assists", current_season_metrics.get('Assists'),
                      border=True, delta=player_metric_diffs.get("Assists"))
            f2.metric("Steals", current_season_metrics.get('Steals'),
                      border=True, delta=player_metric_diffs.get("Steals"))
            f3.metric("Blocks", current_season_metrics.get('Blocks'),
                      border=True, delta=player_metric_diffs.get("Blocks"))
            st.divider()
        except ValueError:
            st.warning("Please select a valid season")
            st.stop()


        # Display raw data as table
        players_display_df = (team_stats_df
                     .query("Player == @selected_player")
                     .set_index("Season")
                     .sort_index(ascending=False))

        players_display_df["Team"] = players_display_df["Team"].apply(team_abbr_to_name)
        players_display_df = players_display_df.rename(columns={
            "G": "Games Played", "MP": "Minutes Played",
            "FG": "Field Goals Made", "FGA": "Field Goals Attempted", "FG%": "Field Goals Rate",
            "3P": "3-Pointers Made", "3PA": "3-Pointers Attempted", "3P%": "3-Pointers Rate",
            "FT": "Free Throws Made", "FTA": "Free Throws Attempted", "FT%": "Free Throws Rate",
            "AST": "Assists", "STL": "Steals", "BLK": "Blocks",
        })[[
            "Team", "Games Played", "Minutes Played",
            "Field Goals Made", "Field Goals Attempted", "Field Goals Rate",
            "3-Pointers Made", "3-Pointers Attempted", "3-Pointers Rate",
            "Free Throws Made", "Free Throws Attempted", "Free Throws Rate",
            "Assists", "Steals", "Blocks",
        ]]
        st.dataframe(players_display_df)