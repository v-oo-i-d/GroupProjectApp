import streamlit as st
import pandas as pd
from metrics import feet_inches_to_cm, pounds_to_kg
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import NearestNeighbors

st.set_page_config(page_title="Tools", page_icon="🔧")

# Gather relevant data
players_df = pd.read_csv("./data/NBA_Player_Info_And_Stats_2014_2025csv")
games_df = pd.read_csv("./data/NBA_Regular_And_Playoff_Games.csv")

st.write("# Tools")
similar_players_tab, player_vs_player_tab, game_prediction_tab = st.tabs(["Find Similar Players", "Player vs Player Predictor", "Game Prediction"])

def create_player_pairs() -> list:
    pairs = list()
    n = len(players_df)
    sample_size = 1000 # Pair count

    while len(pairs) < sample_size:
        i, j = random.sample(range(n), 2)
        if i > j:
            i, j = j, i  # avoid duplicates
        pairs.append((
            players_df.iloc[i],
            players_df.iloc[j]
        ))
    return pairs

def calculate_hypothetical_winner(p1: pd.Series, p2: pd.Series) -> pd.Series:
    def score_player(p: pd.Series) -> float:
        return (
            0.5 * p.get("Age", 0) +
            0.8 * feet_inches_to_cm(p.get("Height", 0)) +
            0.8 * p.get("Weight", 0) +
            0.9 * p.get("REB", 0) +
            0.9 * p.get("AST", 0) +
            0.9 * p.get("STL", 0) +
            0.9 * p.get("BLK", 0) -
            1.0 * p.get("FG_PCT", 0) +
            1.0 * p.get("FG3_PCT", 0) +
            1.0 * p.get("FT_PCT", 0)
        )

    score1 = score_player(p1)
    score2 = score_player(p2)

    if score1 > score2:
        return p1
    elif score2 > score1:
        return p2
    else:
        return random.choice([p1, p2])

def create_features(p1: pd.Series, p2: pd.Series) -> dict:
    return {
        "age_diff": p1["PLAYER_AGE"] - p2["PLAYER_AGE"],
        "height_diff": feet_inches_to_cm(p1["Height"]) - feet_inches_to_cm(p2["Height"]),
        "weight_diff": p1["Weight"] - p2["Weight"],
        "reb_diff": p1["REB"] - p2["REB"],
        "ast_diff": p1["AST"] - p2["AST"],
    }

#TODO: add to notebook
with similar_players_tab:
    # Select a player
    selected_player = st.selectbox(
        "Search for a player:",
        placeholder="Search",
        options=players_df["Player_Name"].dropna().sort_values().unique().tolist()
    )

    feature_cols = ["GP", "GS", "MIN", "FGM", "FGA",
                     "FG_PCT", "FG3M", "FG3A", "FG3_PCT", "FTM",
                     "FTA", "FT_PCT", "OREB", "DREB", "REB",
                     "AST", "STL", "BLK", "TOV", "PF", "PTS"]

    X = players_df[feature_cols]
    y = players_df["PLAYER_ID"]

    X_player = pd.DataFrame([players_df.query(f"Player_Name == '{selected_player}'")[feature_cols].mean()], columns=feature_cols)

    # Traint the model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    nn = NearestNeighbors(n_neighbors=12, metric='euclidean') .fit(X_train, y_train)

    # Find similar players
    distances, indices = nn.kneighbors(X_player)
    similar_players = players_df.iloc[indices[0]]
    similar_players = similar_players[similar_players["Player_Name"] != selected_player]

    st.subheader("Most Similar Players")

    c1, c2, c3 = st.columns(3)
    cols = [c1, c2, c3]

    player_ids = similar_players["PLAYER_ID"].tolist()

    for idx, player_id in enumerate(player_ids):
        col = cols[idx % 3]  # cycle through c1, c2, c3
        with col:
            with st.container(border=True):
                player_name = players_df.query('PLAYER_ID == @player_id').iloc[0]["Player_Name"]
                st.markdown(f"""
                <div style='display:flex;flex-direction:column;justify-content:center;align-items:center'>
                    <p>{player_name}<span style='color:grey'> {player_id} </span></p>
                    <a style='padding:0.2em 1em;text-decoration:none;border:1px solid white;border-radius:0.5em;color:white' href='/Player_Dashboards?id={player_id}'>View</a>
                    <img src='https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png'>
                </div>
                """, unsafe_allow_html=True)

#TODO: add to notebook
with player_vs_player_tab:
    st.write("Who would come out on top in a 1v1 match? Enter player stats and let us predict the likely winner!")

    plr1, _, plr2 = st.columns([3, 0.2, 3])

    # Predictors
    age_range = list(range(
        int(players_df["PLAYER_AGE"].min()),
        int(players_df["PLAYER_AGE"].max()) + 1)
    )
    height_range = list(range(
        int(feet_inches_to_cm(players_df["Height"].min())),
        int(feet_inches_to_cm(players_df["Height"].max())) + 1)
    )
    weight_range = list(range(
        int(pounds_to_kg(players_df["Weight"].min())),
        int(pounds_to_kg(players_df["Weight"].max()) + 1)
    ))
    rebound_range = list(range(
        int(players_df["REB"].min()),
        int(players_df["REB"].max() + 1)
    ))
    assist_range = list(range(
        int(players_df["AST"].min()),
        int(players_df["AST"].max() + 1)
    ))
    blocks_range = list(range(
        int(players_df["BLK"].min()),
        int(players_df["BLK"].max() + 1)
    ))

    # Inputs
    with plr1:
        st.markdown("<h1 style='text-align:center'>Player 1</h1></div>", unsafe_allow_html=True)
        plr1_age = st.select_slider("Age", key="plr1_age", options=age_range, value=(age_range[-1]+age_range[0])//2)
        plr1_height = st.select_slider("Height (cm)", key="plr1_height", options=height_range, value=(height_range[-1]+height_range[0])//2)
        plr1_weight = st.select_slider("Weight (kg)", key="plr1_weight", options=weight_range, value=(weight_range[-1]+weight_range[0])//2)
        plr1_rebounds = st.select_slider("Rebounds", key="plr1_rebounds", options=rebound_range, value=rebound_range[-1]//2)
        plr1_assists = st.select_slider("Assists", key="plr1_assists", options=assist_range, value=assist_range[-1]//2)
        plr1_blocks = st.select_slider("Blocks", key="plr1_blocks", options=blocks_range, value=blocks_range[-1]//2)
        plr1_fgpct = st.select_slider("Field Goal %", key="plr1_fgpct", options=range(0, 101), value=50)
        plr1_fg3pct = st.select_slider("Three Pointer %", key="plr1_fg3pct", options=range(0, 101), value=50)
        plr1_ftpct = st.select_slider("Free Throw %", key="plr1_ftpct", options=range(0, 101), value=50)

    with plr2:
        st.markdown("<h1 style='text-align:center'>Player 2</h1></div>", unsafe_allow_html=True)
        plr2_age = st.select_slider("Age", key="plr2_age", options=age_range, value=(age_range[-1]+age_range[0])//2)
        plr2_height = st.select_slider("Height (cm)", key="plr2_height", options=height_range, value=(height_range[-1]+height_range[0])//2)
        plr2_weight = st.select_slider("Weight (kg)", key="plr2_weight", options=weight_range, value=(weight_range[-1]+weight_range[0])//2)
        plr2_rebounds = st.select_slider("Rebounds", key="plr2_rebounds", options=rebound_range, value=rebound_range[-1]//2)
        plr2_assists = st.select_slider("Assists", key="plr2_assists", options=assist_range, value=assist_range[-1]//2)
        plr2_blocks = st.select_slider("Blocks", key="plr2_blocks", options=blocks_range, value=blocks_range[-1]//2)
        plr2_fgpct = st.select_slider("Field Goal %", key="plr2_fgpct", options=range(0, 101), value=50)
        plr2_fg3pct = st.select_slider("Three Pointer %", key="plr2_fg3pct", options=range(0, 101), value=50)
        plr2_ftpct = st.select_slider("Free Throw %", key="plr2_ftpct", options=range(0, 101), value=50)


    # Create fake players
    p1 = pd.DataFrame({
        "PLAYER_AGE": [plr1_age], "Height": [plr1_height], "Weight": [plr1_weight],
        "REB": [plr1_rebounds], "AST": [plr1_assists], "BLK": [plr1_blocks],
        "FG_PCT": [plr1_fgpct], "FG3_PCT": [plr1_fg3pct], "FT_PCT": [plr1_ftpct],
    }).iloc[0]

    p2 = pd.DataFrame({
        "PLAYER_AGE": [plr2_age], "Height": [plr2_height], "Weight": [plr2_weight],
        "REB": [plr2_rebounds], "AST": [plr2_assists], "BLK": [plr1_blocks],
        "FG_PCT": [plr2_fgpct], "FG3_PCT": [plr2_fg3pct], "FT_PCT": [plr2_ftpct],
    }).iloc[0]


    # Create the training dataset
    pairs = create_player_pairs()
    X, y = [], []
    for _p1, _p2 in pairs:
        features = create_features(_p1, _p2)
        winner = calculate_hypothetical_winner(_p1, _p2)
        label = 1 if winner.equals(_p1) else 0
        X.append(features)
        y.append(label)

    X = pd.DataFrame(X)
    y = pd.Series(y)

    # Train the model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    rfc = RandomForestClassifier().fit(X_train, y_train)
    y_pred = rfc.predict(X_test)

    # Use the user inputted data to predict the winner
    example_features = create_features(p1, p2)
    prediction = rfc.predict(pd.DataFrame([example_features]))[0]

    with st.container(border=True):
        if prediction == 1:
            st.markdown("""
                <p style='text-align:center;'>Predicted Winner:</p>
                <b style='display:block;font-size:3rem;text-align:center;margin:0 auto'>Player 1</b>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <p style='text-align:center;'>Predicted Winner:</p>
                <div style='font-size:3rem;text-align:center;margin:0 auto'>Player 2</b>
            """, unsafe_allow_html=True)


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