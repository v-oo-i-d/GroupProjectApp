import streamlit as st
import pandas as pd

st.set_page_config(page_title="Predictor Tools", page_icon="🔧")

# Gather relevant data
players_df = pd.read_csv("./data/Players.csv")
games_df = pd.read_csv("./data/Games.csv")

st.write("# Predictor Tools")
similar_players_tab, player_vs_player_tab, game_prediction_tab = st.tabs(["Find Similar Players", "Player vs Player Predictor", "Game Prediction"])


def calculate_age(bd: str) -> int:
    pass


with similar_players_tab:
    pass


with player_vs_player_tab:
    st.write("Who would come out on top in a 1v1 match? Enter player stats and let us predict the likely winner!")

    plr1, _, plr2 = st.columns([3, 0.2, 3])

    # Predictors
    height_range = list(range(int(players_df["height"].min()), int(players_df["height"].max()) + 1))
    weight_range = list(range(int(players_df["bodyWeight"].min()), int(players_df["bodyWeight"].max()) + 1))
    countries = players_df["country"].sort_values().dropna().unique()
    #TODO: "Anla" is not a country
    universities = players_df["lastAttended"].sort_values().dropna().unique()
    #TODO: "--" is not a university

    with plr1:
        st.markdown("<h1 style='text-align:center'>Player 1</h1></div>", unsafe_allow_html=True)
        plr1_height = st.select_slider("Height", key="plr1_height", options=height_range)
        plr1_weight = st.select_slider("Weight", key="plr1_weight", options=weight_range)
        plr1_country = st.selectbox("Origin", key="plr1_country", options=countries)
        plr1_uni = st.selectbox("University", key="plr1_uni", options=universities)

    with plr2:
        st.markdown("<h1 style='text-align:center'>Player 2</h1></div>", unsafe_allow_html=True)
        plr2_height = st.select_slider("Height", key="plr2_height", options=height_range)
        plr2_weight = st.select_slider("Weight", key="plr2_weight", options=weight_range)
        plr2_country = st.selectbox("Origin", key="plr2_country", options=countries)
        plr2_uni = st.selectbox("University", key="plr2_uni", options=universities)


with game_prediction_tab:
    st.write("Based on these stats, which team is more likely to win?")

    team1, _, team2 = st.columns([3, 0.2, 3])
    teams = sorted(pd.concat([games_df["hometeamName"], games_df["awayteamName"]]).unique())

    with team1:
        st.markdown("<h1 style='text-align:center'>Team 1</h1></div>", unsafe_allow_html=True)
        team1 = st.selectbox("Team 1", key="team1", options=teams)

    with team2:
        st.markdown("<h1 style='text-align:center'>Team 2</h1></div>", unsafe_allow_html=True)
        team2 = st.selectbox("Team 2", key="team2", options=teams)
