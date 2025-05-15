import streamlit as st
from metrics import *
import pandas as pd

st.set_page_config(page_title="Predictor Tools", page_icon="🔧")

# Gather relevant data
players_df = pd.read_csv("./data/NBA_Player_Info_And_Stats_2014_2025.csv")
games_df = pd.read_csv("./data/NBA_Regular_Season_Games_2014_2025.csv")

st.write("# Predictor Tools")
similar_players_tab, player_vs_player_tab, game_prediction_tab = st.tabs(["Find Similar Players", "Player vs Player Predictor", "Game Prediction"])



with similar_players_tab:
    pass


with player_vs_player_tab:
    st.write("Who would come out on top in a 1v1 match? Enter player stats and let us predict the likely winner!")
    st.write("(Classification problem)")

    plr1, _, plr2 = st.columns([3, 0.2, 3])

    # Predictors
    age_range = list(range(int(players_df["PLAYER_AGE"].min()), int(players_df["PLAYER_AGE"].max()) + 1))
    height_range = list(range(int(feet_inches_to_cm(players_df["Height"].min())), int(feet_inches_to_cm(players_df["Height"].max())) + 1))
    weight_range = list(range(int(players_df["Weight"].min()), int(players_df["Weight"].max()) + 1))
    countries = players_df["Country"].sort_values().dropna().unique()
    #TODO: "DRC" -> "Democratic Republic of the Congo"
    universities = players_df["College"].sort_values().dropna().unique()
    #TODO: "St. John's, N.Y." -> "St. John's (NY)"
    #TODO: "New Zealand Breakers" is not a college

    with plr1:
        st.markdown("<h1 style='text-align:center'>Player 1</h1></div>", unsafe_allow_html=True)
        plr1_age = st.select_slider("Age", key="plr1_age", options=age_range)
        plr1_height = st.select_slider("Height", key="plr1_height", options=height_range)
        plr1_weight = st.select_slider("Weight", key="plr1_weight", options=weight_range)
        plr1_country = st.selectbox("Origin", key="plr1_country", options=countries)
        plr1_uni = st.selectbox("University", key="plr1_uni", options=universities)

    with plr2:
        st.markdown("<h1 style='text-align:center'>Player 2</h1></div>", unsafe_allow_html=True)
        plr2_age = st.select_slider("Age", key="plr2_age", options=age_range)
        plr2_height = st.select_slider("Height", key="plr2_height", options=height_range)
        plr2_weight = st.select_slider("Weight", key="plr2_weight", options=weight_range)
        plr2_country = st.selectbox("Origin", key="plr2_country", options=countries)
        plr2_uni = st.selectbox("University", key="plr2_uni", options=universities)


with game_prediction_tab:
    st.write("Based on these stats, which team is more likely to win?")
    st.write("(Classification problem)")

    team1, _, team2 = st.columns([3, 0.2, 3])
    teams = games_df["TEAM_NAME"].sort_values().unique()

    with team1:
        st.markdown("<h1 style='text-align:center'>Team 1</h1></div>", unsafe_allow_html=True)
        team1 = st.selectbox("Team 1", key="team1", options=teams)

    with team2:
        st.markdown("<h1 style='text-align:center'>Team 2</h1></div>", unsafe_allow_html=True)
        team2 = st.selectbox("Team 2", key="team2", options=teams)