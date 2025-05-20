import streamlit as st
from metrics import *
import pandas as pd
import altair as alt

st.set_page_config(page_title="Player Dashboard", page_icon="👤")

# Gather players
players_df = pd.read_csv("./data/NBA_Player_Info_And_Stats_2014_2025.csv", index_col=0).reset_index(drop=True)


st.write("# Player Dashboards")
st.divider()

# Get selected player by URL ID
url_player_id = st.query_params.get("id", None)

# Try to find player name with that ID
preselect_player = None
if url_player_id:
    try:
        match = players_df[players_df["PLAYER_ID"] == int(url_player_id)]
        if not match.empty:
            preselect_player = match["Player_Name"].iloc[0]
    except ValueError:
        pass

player_names = players_df["Player_Name"].dropna().sort_values().unique().tolist()
default_index = player_names.index(preselect_player) if preselect_player in player_names else 0

selected_player = st.selectbox(
    "Search for a player:",
    options=player_names,
    index=default_index
)

player_id = players_df.query("Player_Name == @selected_player")["PLAYER_ID"].iloc[0]
st.query_params["id"] = player_id

if selected_player:
    with st.container(border=True):
        # Season selector
        seasons = players_df[players_df["Player_Name"] == selected_player]["SEASON_ID"].sort_values(ascending=False).unique().tolist()
        default_season = seasons[0] if len(seasons) > 0 else None
        selected_season = st.segmented_control("Season", options=seasons, default=default_season)

        try:
            selected_index = seasons.index(selected_season)
            current_season_metrics = get_player_metrics(players_df, selected_player, selected_season)
            previous_season_metrics = None

            if len(seasons) > 1:
                try:
                    previous_season_metrics = get_player_metrics(players_df, selected_player, seasons[selected_index + 1])
                except IndexError:
                    pass


            # Header
            st.markdown(
                f"<center><img style='height:10rem;' src='https://cdn.nba.com/headshots/nba/latest/1040x760/{current_season_metrics.get('PlayerID')}.png'></center>",
                unsafe_allow_html=True)
            st.markdown(f"<h2 style='margin:0;padding-bottom:0;height:2em;'><center>{selected_player}</center></h2>",
                        unsafe_allow_html=True)
            st.markdown(f"<center style='color:grey;'>{current_season_metrics.get('Team')}</center>",
                        unsafe_allow_html=True)
            st.markdown(f"<center style='color:grey;'>{current_season_metrics.get('Position')}</center>",
                        unsafe_allow_html=True)
            st.divider()


            # Get selected seasons' metrics
            player_metric_diffs = {}
            for season in seasons:
                if selected_season == season:
                    current_season_metrics = get_player_metrics(players_df, selected_player, season)
                else:
                    if previous_season_metrics:
                        player_metric_diffs = calculate_metric_diffs(current_season_metrics, previous_season_metrics)


            # Basic Info
            st.markdown("<h3>Basic Info</h3>", unsafe_allow_html=True)
            a1, a2, a3, a4 = st.columns(4)
            a1.metric("Age", current_season_metrics.get('Age'), border=True)
            a2.metric("Height (m)", round(current_season_metrics.get('Height') / 100, 2), border=True)
            a3.metric("Weight (kg)", current_season_metrics.get('Weight'), border=True)
            st.divider()


            # Game Stats
            st.markdown("<h3>Game Stats</h3>", unsafe_allow_html=True)
            b1, b2 = st.columns(2)
            b1.metric("Games Played", current_season_metrics.get('GamesPlayed'),
                      border=True, delta=player_metric_diffs.get("GamesPlayed"))
            b2.metric("Minutes Played", current_season_metrics.get('MinutesPlayed'),
                      border=True, delta=player_metric_diffs.get("MinutesPlayed"))
            st.divider()


            # Field Goals
            st.markdown("<h3>Field Goals</h3>", unsafe_allow_html=True)
            fg_delta = None if player_metric_diffs == {} else str(player_metric_diffs.get("FieldGoalPercentage")) + "%"
            c1, c2, c3 = st.columns(3)
            c1.metric("Made", current_season_metrics.get('FieldGoalsMade'),
                      border=True, delta=player_metric_diffs.get("FieldGoalsMade"))
            c2.metric("Attempted", current_season_metrics.get('FieldGoalsAttempted'),
                      border=True, delta=player_metric_diffs.get("FieldGoalsAttempted"))
            c3.metric("Rate (%)", current_season_metrics.get('FieldGoalPercentage'),
                      border=True, delta=fg_delta)


            # Three Pointers
            st.markdown("<h3>Three Pointers</h3>", unsafe_allow_html=True)
            tp_delta = None if player_metric_diffs == {} else str(player_metric_diffs.get("ThreePointersPercentage")) + "%"

            d1, d2, d3 = st.columns(3)
            d1.metric("Made", current_season_metrics.get('ThreePointersMade'),
                      border=True, delta=player_metric_diffs.get("ThreePointersMade"))
            d2.metric("Attempted", current_season_metrics.get('ThreePointersAttempted'),
                      border=True, delta=player_metric_diffs.get("ThreePointersAttempted"))
            d3.metric("Rate (%)", current_season_metrics.get('ThreePointersPercentage'),
                      border=True, delta=tp_delta)


            # Free Throws
            st.markdown("<h3>Free Throws</h3>", unsafe_allow_html=True)
            ft_delta = None if player_metric_diffs == {} else str(player_metric_diffs.get("FreeThrowsPercentage")) + "%"
            e1, e2, e3 = st.columns(3)
            e1.metric("Made", current_season_metrics.get('FreeThrowsMade'),
                      border=True, delta=player_metric_diffs.get("FreeThrowsMade"))
            e2.metric("Attempted", current_season_metrics.get('FreeThrowsAttempted'),
                      border=True, delta=player_metric_diffs.get("FreeThrowsAttempted"))
            e3.metric("Rate (%)", current_season_metrics.get('FreeThrowsPercentage'),
                      border=True, delta=ft_delta)
            st.divider()


            metrics_to_plot = ["FG_PCT", "FT_PCT", "FG3_PCT"]
            stat_renames = {"FG_PCT": "Field Goals", "FT_PCT": "Free Throws", "FG3_PCT": "Three-Pointers"}

            # Calculate metric means per season
            season_avg_df = players_df.query("Player_Name == @selected_player").groupby("SEASON_ID")[
                metrics_to_plot].mean().reset_index()

            # Melt to long format
            melted_avg_df = season_avg_df.melt(
                id_vars="SEASON_ID",
                var_name="Metric",
                value_name="Average"
            )
            melted_avg_df["Metric"] = melted_avg_df["Metric"].map(stat_renames)
            melted_avg_df["Average"] *= 100

            chart = alt.Chart(melted_avg_df).mark_line(point=True).encode(
                x=alt.X("SEASON_ID:N", title="Season"),
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
            st.write("Please select a valid season.")


        # Display raw data as table
        players_display_df = (players_df
                     .query("Player_Name == @selected_player")
                     .set_index("SEASON_ID")
                     .sort_index(ascending=False))

        players_display_df["TEAM_ID"] = players_display_df["TEAM_ID"].apply(team_id_to_name)
        players_display_df = players_display_df.rename(columns={
            "TEAM_ID": "Team", "GP": "Games Played", "MIN": "Minutes Played",
            "FGM": "Field Goals Made", "FGA": "Field Goals Attempted", "FG_PCT": "Field Goals Rate",
            "FG3M": "Three Pointers Made", "FG3A": "Three Pointers Attempted", "FG3_PCT": "Three Pointers Percentage",
            "FTM": "Free Throws Made", "FTA": "Free Throws Attempted", "FT_PCT": "Free Throws Percentage",
            "AST": "Assists", "STL": "Steals", "BLK": "Blocks",
        }, index={"SEASON_ID": "Season"})
        # Select relevant columns
        players_display_df = players_display_df.loc[:, players_display_df.columns.str.contains('[a-z]')].iloc[:, :-6]
        st.dataframe(players_display_df)