import streamlit as st
import pandas as pd
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import NearestNeighbors
from statsmodels.tsa.seasonal import seasonal_decompose

st.set_page_config(page_title="Tools", page_icon="🔧")

# Gather relevant data
team_stats_df = pd.read_csv("./data/Cleaned_NBA_Per_Game_Stats_2015_2024.csv")
regular_df = pd.read_csv("./data/Cleaned_NBA_Regular_Season_Games_2015_2024.csv")
playoff_df = pd.read_csv("./data/Cleaned_NBA_Playoff_Games_2015_2024.csv")
all_games_df = pd.read_csv("./data/Cleaned_NBA_All_Games_2015_2024.csv")

st.write("# Tools")
similar_players_tab, player_vs_player_tab, matchup_prediction_tab = st.tabs([
    "Find Similar Players", "Player vs Player Predictor", "Match-up Predictor"
])

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

    # Check for valid data
    player_data = team_stats_df.query(f"Player == '{selected_player}'")[feature_cols].dropna()
    if not player_data.empty:
        X_player = pd.DataFrame([player_data.mean()], columns=feature_cols)
    else:
        st.warning(f"Not enough data available for {selected_player}")
        st.stop()

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
                st.markdown(f"""
                    <div style='height:2.5em;margin:0;display:flex;flex-direction:column;justify-content:center'>
                        <span style='margin-right:1em;color:grey'>{idx+1}</span>
                        {player_name}
                    </div>
                """, unsafe_allow_html=True)
            with btn:
                st.link_button("View", url=f"/Player_Dashboards?player={player_name}")

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

    st.success(f"Predicted winner: {'Player 1' if prediction == 1 else 'Player 2'}")

with matchup_prediction_tab:
    # Mapping of NBA team names to CDN logo IDs
    NBA_TEAM_IDS = {
        'Atlanta Hawks': 1610612737, 'Boston Celtics': 1610612738, 'Brooklyn Nets': 1610612751,
        'Charlotte Hornets': 1610612766, 'Chicago Bulls': 1610612741, 'Cleveland Cavaliers': 1610612739,
        'Dallas Mavericks': 1610612742, 'Denver Nuggets': 1610612743, 'Detroit Pistons': 1610612765,
        'Golden State Warriors': 1610612744, 'Houston Rockets': 1610612745, 'Indiana Pacers': 1610612754,
        'LA Clippers': 1610612746, 'Los Angeles Lakers': 1610612747, 'Memphis Grizzlies': 1610612763,
        'Miami Heat': 1610612748, 'Milwaukee Bucks': 1610612749, 'Minnesota Timberwolves': 1610612750,
        'New Orleans Pelicans': 1610612740, 'New York Knicks': 1610612752, 'Oklahoma City Thunder': 1610612760,
        'Orlando Magic': 1610612753, 'Philadelphia 76ers': 1610612755, 'Phoenix Suns': 1610612756,
        'Portland Trail Blazers': 1610612757, 'Sacramento Kings': 1610612758, 'San Antonio Spurs': 1610612759,
        'Toronto Raptors': 1610612761, 'Utah Jazz': 1610612762, 'Washington Wizards': 1610612764
    }

    def get_nba_logo_url(team_name: str) -> str:
        """Return the CDN URL for the given NBA team logo."""
        team_id = NBA_TEAM_IDS.get(team_name)
        if team_id:
            return f"https://cdn.nba.com/logos/nba/{team_id}/global/L/logo.svg"
        return "https://cdn.nba.com/logos/nba/nba-logoman-75x75.png"

    # Ensure GAME_DATE column is in datetime format for grouping
    all_games_df['GAME_DATE'] = pd.to_datetime(all_games_df['GAME_DATE'])

    # Aggregate average points per game by season and team
    team_season = (
        all_games_df
            .groupby([pd.Grouper(key='GAME_DATE', freq='Y'), 'TEAM_NAME'])['PTS']
            .mean()
            .reset_index()
            .rename(columns={'GAME_DATE':'SEASON','PTS':'AVG_PTS'})
    )

    # Dropdown selections for two teams to compare
    teams_list = sorted(team_season['TEAM_NAME'].unique())
    t1 = st.selectbox('Team A', teams_list, key='game_t1')
    t2 = st.selectbox('Team B', teams_list, index=1, key='game_t2')

    if t1 and t2:
        # --- Forecast calculation helper ---
        def forecast_pts(team):
            # Filter for the team's historical avg PTS
            df = team_season[team_season['TEAM_NAME'] == team].copy()
            df.set_index('SEASON', inplace=True)
            df.index = pd.to_datetime(df.index)

            # Compute 3-year rolling average as trend
            roll = df['AVG_PTS'].rolling(3, min_periods=1).mean()

            # Build a proper time series object for decomposition
            ts = df['AVG_PTS'].copy()
            ts.index = pd.date_range(start=df.index.min(), periods=len(ts), freq='Y')

            # Decompose into trend, seasonal, and residual components
            dec = seasonal_decompose(ts, model='additive', period=3)

            # Combine latest trend, seasonal factor, and average residual for forecast
            return round(roll.iloc[-1] + dec.seasonal.iloc[-3] + dec.resid.mean(skipna=True))

        # Compute forecasts for selected teams
        sA, sB = forecast_pts(t1), forecast_pts(t2)

        # --- Display logos, names, and points ---
        colA, colVS, colB = st.columns([3, 1, 3])
        with colA:
            # Centered block for Team A
            st.markdown(f"""
                <div style='text-align:center;'>
                  <img src='{get_nba_logo_url(t1)}' width='150'><br>
                  <strong>{t1}</strong><br>
                  <span style='font-size:18px;'>{sA} pts</span>
                </div>
            """, unsafe_allow_html=True)
        with colVS:
            # Visual separator
            st.markdown("<h2 style='text-align:center; margin-top:50px;'>VS</h2>", unsafe_allow_html=True)
        with colB:
            # Centered block for Team B
            st.markdown(f"""
                <div style='text-align:center;'>
                  <img src='{get_nba_logo_url(t2)}' width='150'><br>
                  <strong>{t2}</strong><br>
                  <span style='font-size:18px;'>{sB} pts</span>
                </div><br><br>
            """, unsafe_allow_html=True)

        # --- Determine and display winner ---
        winner = t1 if sA > sB else t2 if sB > sA else 'Tie'
        st.success(f"Projected Winner: {winner}")