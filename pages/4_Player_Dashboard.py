import streamlit as st
import pandas as pd

st.set_page_config(page_title="Player Dashboard", page_icon="👤")

# Gather players
players_df = pd.read_csv("./data/Players.csv")
players_df["fullName"] = players_df["firstName"] + " " + players_df["lastName"]

st.write("# Player Dashboards")
st.write("Need to clean data (weights exceeding 70k lbs)")
st.markdown("<hr>", unsafe_allow_html=True)

# Select a player
selected_player = st.selectbox("Search for a player:",
                     placeholder="Search",
                     options=players_df["fullName"].dropna().sort_values().tolist())

if selected_player:
    # Get player data
    birthday = (pd.to_datetime(players_df.query("fullName == @selected_player")["birthdate"])).dt.date.iloc[0]
    birthday = birthday.strftime("%B %d, %Y") if pd.notna(birthday) else "nan"

    weight = round(pd.to_numeric(players_df.query("fullName == @selected_player")["bodyWeight"]).iloc[0], 1)
    weightUnit = "lbs"

    height = round(pd.to_numeric(players_df.query("fullName == @selected_player")["height"]).iloc[0], 1)
    heightUnit = "in"

    country = players_df.query("fullName == @selected_player")["country"].iloc[0]


    units = st.segmented_control("Units", options=["Metric", "Imperial"], default="Metric")

    with st.container(border=True):
        st.markdown(f"<h2 style='text-align: center;'>{selected_player}</h2>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:0'>", unsafe_allow_html=True)

        if units == "Metric":
            # Convert
            weight = round(weight / 2.205, 1)
            weightUnit = "kg"
            height = round(height * 2.54, 1)
            heightUnit = "cm"

        # Styles
        st.markdown("""
            <style>
                .section-header {
                    font-weight: bold;
                    text-align: center;
                    margin-bottom: 10px;
                }
                .section-container {
                    display: flex;
                    justify-content: space-evenly;
                    align-items: center;
                    width: 100%;
                }
                .stat-header {
                    color: grey;
                    margin-bottom: 5px;
                }
                .section-stat {
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    flex: 1;
                }
            </style>
        """, unsafe_allow_html=True)

        # Content
        st.markdown(f"""
            <p class='section-header'>Basic Info</p>
            <div class='section-container'>
                <div class='section-stat'>
                    <p class='stat-header'>Born</p>
                    <p>{birthday}</p>
                </div>
                <div class='section-stat'>
                    <p class='stat-header'>Height ({heightUnit})</p>
                    <p>{height}</p>
                </div>
                <div class='section-stat'>
                    <p class='stat-header'>Weight ({weightUnit})</p>
                    <p>{weight}</p>
                </div>
                <div class='section-stat'>
                    <p class='stat-header'>Country</p>
                    <p>{country}</p>
                </div>
            </div>
            <hr style="width: 30%; margin: 1em auto 2em auto">
            
            <p class='section-header'>More Stats</p>
            <div class='section-container'>
                <div class='section-stat'>
                    <p class='stat-header'>Stat 1</p>
                    <p>A</p>
                </div>
                <div class='section-stat'>
                    <p class='stat-header'>Stat 2</p>
                    <p>B</p>
                </div>
                <div class='section-stat'>
                    <p class='stat-header'>Stat 3</p>
                    <p>C</p>
                </div>
                <div class='section-stat'>
                    <p class='stat-header'>Stat 4</p>
                    <p>D</p>
                </div>
            </div>
            <hr style="width: 30%; margin: 1em auto 2em auto">
            
            
        """, unsafe_allow_html=True)