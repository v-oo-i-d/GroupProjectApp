import streamlit as st
from metrics import *
import pandas as pd

st.set_page_config(page_title="Player Dashboard", page_icon="👤")

# Gather players
players_df = pd.read_csv("./data/NBA_Player_Info_And_Stats_2014_2025.csv")


st.write("# Player Dashboards")
st.markdown("<hr>", unsafe_allow_html=True)

# Select a player
selected_player = st.selectbox("Search for a player:",
                     placeholder="Search",
                     options=players_df["Player_Name"].dropna().sort_values().unique().tolist())


if selected_player:
    with st.container(border=True):
        # Season selector
        seasons = players_df[players_df["Player_Name"] == selected_player]["SEASON_ID"].sort_values(ascending=False).unique().tolist()
        default_season = seasons[0] if len(seasons) > 0 else None
        selected_season = st.segmented_control("Season", options=seasons, default=default_season)
        selected_index = seasons.index(selected_season)
        current_season_metrics = get_player_metrics(players_df, selected_player, selected_season)
        previous_season_metrics = None

        if len(seasons) > 1:
            try:
                previous_season_metrics = get_player_metrics(players_df, selected_player, seasons[selected_index+1])
            except IndexError:
                pass


        # Header
        st.markdown(f"<center><img style='height:10rem;' src='https://cdn.nba.com/headshots/nba/latest/1040x760/{current_season_metrics.get('PlayerID')}.png'></center>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='margin:0;padding-bottom:0;height:2em;'><center>{selected_player}</center></h2>", unsafe_allow_html=True)
        st.markdown(f"<center style='color:grey;'>{current_season_metrics.get('Position')}</center>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:1em 0;'>", unsafe_allow_html=True)


        # Get selected seasons' metrics
        player_metric_diffs = {}
        for season in seasons:
            if selected_season == season:
                current_season_metrics = get_player_metrics(players_df, selected_player, season)
            else:
                if previous_season_metrics:
                    player_metric_diffs = calculate_metric_diffs(current_season_metrics, previous_season_metrics)


        # Basic Info
        st.markdown("<center style='margin-bottom:1rem;'><b>Basic Info</b></center>", unsafe_allow_html=True)
        a1, a2, a3, a4 = st.columns(4)
        a1.metric("Age", current_season_metrics.get('Age'), border=True)
        a2.metric("Height (m)", current_season_metrics.get('Height'),
            border=True,
            delta=round(player_metric_diffs.get("Height"), 1) if player_metric_diffs.get("Height") is not None else None,
            delta_color="off"
        )
        a3.metric("Weight (kg)", current_season_metrics.get('Weight'),
            border=True,
            delta=round(player_metric_diffs.get("Weight"), 1) if player_metric_diffs.get("Weight") is not None else None,
            delta_color="off"
        )
        a4.metric("Country", current_season_metrics.get('Country'), border=True)