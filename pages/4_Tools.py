import streamlit as st
import pandas as pd
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import NearestNeighbors

st.set_page_config(page_title="Tools", page_icon="🔧")

# Gather relevant data
team_stats_df = pd.read_csv("./data/Cleaned_NBA_Per_Game_Stats_2015_2024.csv")
regular_df = pd.read_csv("./data/Cleaned_NBA_Regular_Season_Games_2015_2024.csv")
playoff_df = pd.read_csv("./data/Cleaned_NBA_Playoff_Games_2015_2024.csv")
all_games_df = pd.read_csv("./data/Cleaned_NBA_All_Games_2015_2024.csv")

st.write("# Tools")
similar_players_tab, player_vs_player_tab, game_prediction_tab = st.tabs(["Find Similar Players", "Player vs Player Predictor", "Game Prediction"])

def create_player_pairs() -> list:
    pairs = list()
    n = len(team_stats_df)
    sample_size = 1000 # Pair count

    while len(pairs) < sample_size:
        i, j = random.sample(range(n), 2)
        if i > j:
            i, j = j, i  # avoid duplicates
        pairs.append((
            team_stats_df.iloc[i],
            team_stats_df.iloc[j]
        ))
    return pairs

def calculate_hypothetical_winner(p1: pd.Series, p2: pd.Series) -> pd.Series:
    def score_player(p: pd.Series) -> float:
        return (
            0.7 * p.get("Age", 0) +
            0.9 * p.get("TRB", 0) +
            0.9 * p.get("STL", 0) +
            0.9 * p.get("BLK", 0) -
            1.0 * p.get("FG%", 0) +
            1.0 * p.get("3P%", 0) +
            1.0 * p.get("FT%", 0)
        )

    score1 = score_player(p1)
    score2 = score_player(p2)

    if score1 > score2:
        return p1
    elif score2 > score1:
        return p2
    else:
        return p1 if p1["Age"] < p2["Age"] else p2

def create_features(p1: pd.Series, p2: pd.Series) -> dict:
    return {
        "age_diff": p1["Age"] - p2["Age"],
        "reb_diff": p1["TRB"] - p2["TRB"],
        "blk_diff": p1["BLK"] - p2["BLK"],
        "fg%_diff": p1["FG%"] - p2["FG%"],
        "3p%_diff": p1["3P%"] - p2["3P%"],
        "ft%_diff": p1["FT%"] - p2["FT%"],
    }

#TODO: add to notebook
with similar_players_tab:
    # Select a player
    selected_player = st.selectbox(
        "Search for a player:",
        placeholder="Search",
        options=team_stats_df["Player"].dropna().sort_values().unique().tolist()
    )

    feature_cols = ["G", "GS", "MP", "FG", "FGA",
                     "FG%", "3P", "3PA", "3P%", "FT",
                     "FTA", "FT%", "ORB", "DRB", "TRB",
                     "AST", "STL", "BLK", "TOV", "PF", "PTS"]

    team_stats_df[feature_cols] = team_stats_df[feature_cols].apply(pd.to_numeric, errors='coerce')
    valid_rows = team_stats_df[feature_cols].dropna().index
    X = team_stats_df.loc[valid_rows, feature_cols]
    y = team_stats_df.loc[valid_rows, "Player"]

    X_player = pd.DataFrame([team_stats_df.query(f"Player == '{selected_player}'")[feature_cols].mean()], columns=feature_cols)

    # Traint the model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    nn = NearestNeighbors(n_neighbors=10, metric='euclidean').fit(X_train, y_train)

    st.subheader("Most Similar Players")

    # Find similar players
    distances, indices = nn.kneighbors(X_player)
    similar_players = team_stats_df.iloc[indices[0]]
    similar_players = similar_players[similar_players["Player"] != selected_player]
    similar_player_names = similar_players["Player"].tolist()

    for idx, player_name in enumerate(similar_player_names):
        with st.container(border=True):
            plr, _, btn = st.columns([3, 5, 1])
            with plr:
                st.write(idx+1, player_name)
            with btn:
                st.link_button("View", url=f"/Player_Dashboards?player={player_name}")

#TODO: add to notebook
with player_vs_player_tab:
    st.write("Who would come out on top in a 1v1 match? Enter player stats and let us predict the likely winner!")

    plr1, _, plr2 = st.columns([3, 0.2, 3])

    # Predictors
    age_range = list(range(
        int(team_stats_df["Age"].min()),
        int(team_stats_df["Age"].max()) + 1)
    )
    rebound_range = list(range(
        int(team_stats_df["TRB"].min()),
        int(team_stats_df["TRB"].max() + 1)
    ))
    blocks_range = list(range(
        int(team_stats_df["BLK"].min()),
        int(team_stats_df["BLK"].max() + 1)
    ))

    # Inputs
    with plr1:
        st.markdown("<h1 style='text-align:center'>Player 1</h1></div>", unsafe_allow_html=True)
        plr1_age = st.select_slider("Age", key="plr1_age", options=age_range, value=(age_range[-1]+age_range[0])//2)
        plr1_rebounds = st.select_slider("Rebounds", key="plr1_rebounds", options=rebound_range, value=rebound_range[-1]//2)
        plr1_blocks = st.select_slider("Blocks", key="plr1_blocks", options=blocks_range, value=blocks_range[-1]//2)
        plr1_fgpct = st.select_slider("Field Goal %", key="plr1_fgpct", options=range(0, 101), value=50)
        plr1_fg3pct = st.select_slider("Three Pointer %", key="plr1_fg3pct", options=range(0, 101), value=50)
        plr1_ftpct = st.select_slider("Free Throw %", key="plr1_ftpct", options=range(0, 101), value=50)

    with plr2:
        st.markdown("<h1 style='text-align:center'>Player 2</h1></div>", unsafe_allow_html=True)
        plr2_age = st.select_slider("Age", key="plr2_age", options=age_range, value=(age_range[-1]+age_range[0])//2)
        plr2_rebounds = st.select_slider("Rebounds", key="plr2_rebounds", options=rebound_range, value=rebound_range[-1]//2)
        plr2_blocks = st.select_slider("Blocks", key="plr2_blocks", options=blocks_range, value=blocks_range[-1]//2)
        plr2_fgpct = st.select_slider("Field Goal %", key="plr2_fgpct", options=range(0, 101), value=50)
        plr2_fg3pct = st.select_slider("Three Pointer %", key="plr2_fg3pct", options=range(0, 101), value=50)
        plr2_ftpct = st.select_slider("Free Throw %", key="plr2_ftpct", options=range(0, 101), value=50)


    # Create fake players
    p1 = pd.DataFrame({
        "Age": [plr1_age], "TRB": [plr1_rebounds], "BLK": [plr1_blocks],
        "FG%": [plr1_fgpct], "3P%": [plr1_fg3pct], "FT%": [plr1_ftpct],
    }).iloc[0]

    p2 = pd.DataFrame({
        "Age": [plr2_age], "TRB": [plr2_rebounds], "BLK": [plr1_blocks],
        "FG%": [plr2_fgpct], "3P%": [plr2_fg3pct], "FT%": [plr2_ftpct],
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
    _, c, _ = st.columns([1,2,1])
    with c:
        with st.container(border=True):
            if prediction == 1:
                st.markdown("""
                    <p style='text-align:center;margin:0'>Predicted Winner:</p>
                    <div style='font-size:3rem;text-align:center;margin:0 auto 0.2em auto'>Player 1</b>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <p style='text-align:center;margin:0'>Predicted Winner:</p>
                    <div style='font-size:3rem;text-align:center;margin:0 auto 0.2em auto'>Player 2</b>
                """, unsafe_allow_html=True)