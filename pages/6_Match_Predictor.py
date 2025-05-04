import streamlit as st
import pandas as pd

st.set_page_config(page_title="Player Dashboard", page_icon="👤")

players_df = pd.read_csv("./data/Players.csv")
players_df["fullName"] = players_df["firstName"] + " " + players_df["lastName"]

st.write("# Predict an NBA game")
st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("""
    <style>
        .player2 [data-testid="stTextInput"] label {
            text-align: right !important;
            display: block;
            width: 100%;
            background-color: red;
        }
        .player2 [data-testid="stTextInput"] input {
            text-align: right !important;
        }
    </style>
""", unsafe_allow_html=True)

plr1, divider, plr2 = st.columns([3, 0.2, 3])

with plr1:
    st.markdown("<h1 style='text-align:center'>Player 1</h1></div>", unsafe_allow_html=True)
    plr1_height = st.select_slider("Height",
                                   key="plr1_height",
                                   options=list(range(int(players_df["height"].min()), int(players_df["height"].max()) + 1)))
    plr1_weight = st.select_slider("Weight",
                                   key="plr1_weight",
                                   options=list(range(int(players_df["bodyWeight"].min()), int(players_df["bodyWeight"].max()) + 1)))

with divider:
    st.markdown("<div class='vl'>&nbsp;</div>", unsafe_allow_html=True)

with plr2:
    st.markdown("<h1 style='text-align:center'>Player 2</h1></div>", unsafe_allow_html=True)
    plr2_height = st.select_slider("Height",
                                   key="plr2_height",
                                   options=list(range(int(players_df["height"].min()), int(players_df["height"].max()) + 1)))
    plr2_weight = st.select_slider("Weight",
                                   key="plr2_weight",
                                   options=list(range(int(players_df["bodyWeight"].min()), int(players_df["bodyWeight"].max()) + 1)))
