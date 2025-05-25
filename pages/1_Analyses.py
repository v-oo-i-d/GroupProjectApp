import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import seaborn as sns
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

st.set_page_config(page_title="Analyses", page_icon="🔎", layout="wide")

team_stats_df = pd.read_csv("./data/Cleaned_NBA_Per_Game_Stats_2015_2024.csv")
all_games_df = pd.read_csv("./data/Cleaned_NBA_All_Games_2015_2024.csv")


st.header("Analyses")
st.write("""
    This page's goal is to go into greater depth regarding the steps that are taken to transform our cleaned NBA performance datasets into a form that is analytically ready. 
    These processes typically include, but are not limited to, dealing with missing values, inconsistencies in formats, duplicate records, and correcting data types. 
    In addition to demonstrating our wrangling skills, this part describes the approach we utilised to formulate and examine many research problems. 
    These questions prompted our investigation into player performance patterns, team statistics, and other relevant insights, all backed by well-presented data visualisations and summaries.
""")
st.divider()

st.header("Classification")
st.write("""
    This section focuses on classifying player performance using statistical similarity metrics. It includes classification questions, responses, and thorough investigation into how individual players compare to their teammates. 
    Using distance calculations and z-score-based performance labels, we determine which players are underperforming, average, or outperforming their teams, providing insights into player fit and contribution. 
    I also investigated several classification models, detailing how they function and their pros and cons in order to find the optimal method for the specific study issue.
""")
st.subheader("Identifying Players Who Underperform Their Teams and Potential Better Team Fits")
st.write("""
    The objective of this analysis is to identify the players who are not performing as well as their team. Using a K-Nearest Neighbors classification model, we can compare each underperforming player's average statistics with other teams' average statistics.
    This comparison allows us to make suggestions regarding where the player's performance metrics might be more suited.
""")
st.markdown("""
    **Steps Included:**
    1. Form the teams
    2. Calculate average metrics for every team
    3. Calculate average metrics for every player in chosen team
    4. Calculate every players distance from the average
    5. Identify underperforming players using Z-score and label appropriately
    6. Suggest better suited teams with KNN Classifier
""")

st.markdown("##### Forming teams rosters")
st.code("""
    unique_teams = team_stats["Team"].unique()

    def form_teams() -> dict:
        team_rosters = {}
    
        for team in unique_teams:
            team_players = team_stats.query("Team == @team")["Player"].unique().tolist()
            team_rosters[team] = players
            
        return team_rosters
    
    team_rosters = form_teams()
""")
st.write("""
    This function looks through the entire dataset, extracts the unique teams, and filters the dataset to find every player on that team.
    The result, ```team_rosters```, is a dictionary in the format: 
""")
st.json({"Team Abbreviation": ["Player1","Player2","Player3",]})

st.markdown("##### Calculate average metrics for every team")
st.code("""
    def generate_team_averages():
        team_averages = []
    
        for team in unique_teams:
            team_df = team_stats.replace("nan", None).query("Team == @team")
            avg_stats = team_df.agg({
                "FG%": "mean", "3P%": "mean", "FT%": "mean", 
                "AST": "mean", "STL": "mean", "BLK": "mean", 
                "TOV": "mean", "PF": "mean", "PTS": "mean"
            })
            avg_stats["Team"] = team
            team_averages.append(avg_stats)
    
        # Combine all averages into a single DataFrame
        return pd.DataFrame(team_averages).set_index("Team")
""")
st.write("This function calculates the averages of the given metrics for every team and stores them in a dataframe.")
st.dataframe(pd.DataFrame(data={
    'FG%': [0.438814, 0.454188, 0.439247, 0.440115, 0.447876],
    '3P%': [0.304016, 0.329192, 0.297453, 0.318241, 0.309920],
    'FT%': [0.755054, 0.740247, 0.742995, 0.754721, 0.735717],
    'AST': [1.786935, 1.830570, 2.001370, 1.996196, 1.838830],
    'STL': [0.601005, 0.590155, 0.565753, 0.599457, 0.626596],
    'BLK': [0.356784, 0.388083, 0.398630, 0.384239, 0.375532],
    'TOV': [1.019095, 0.947150, 1.149772, 1.039130, 1.062234],
    'PF': [1.602010, 1.516062, 1.687215, 1.585326, 1.636170],
    'PTS': [8.071859, 8.081347, 8.598174, 8.616848, 8.583511]
}, index=['ATL', 'BOS', 'BRK', 'CHO', 'CHI']))

st.markdown("##### Calculate average metrics for every player in chosen team")
st.write("We are going to look at the Houston Rockets (HOU) as our team of choice.")
st.code("""
    def compute_team_averages(team) -> pd.DataFrame:
        example_team = team_rosters[team]
        player_stats = {}
        
        for player in example_team:
            player_games = team_stats.query("Player == @player")
            player_games_stats = player_games.agg(
                {"FG%":"mean", "3P%":"mean", "FT%":"mean", 
                 "AST":"mean", "STL":"mean", "BLK":"mean", 
                 "TOV":"mean", "PF":"mean", "PTS":"mean"})
            player_games_stats["GAME_COUNT"] = len(player_games)
            player_stats[player] = player_games_stats
    
        result = pd.DataFrame.from_dict(player_stats, orient="index").sort_index().copy()
        # Filter out players with fewer than 3 games
        result = result[result["GAME_COUNT"] >= 3].copy()
        # Compute and append the average row safely
        average_row = result.mean(numeric_only=True)
        result.loc["Average"] = average_row
        
        return result
    
    houston_rockets_stats = compute_team_averages("HOU")
    houston_rockets_stats
""")
st.write("""
    This function selects the chosen teams roster from the dataset, accumulates every players average metrics in that team, and stores it in ```houston_rockets_stats```.
""")
st.dataframe(pd.DataFrame(data={
    'FG%': [0.421000, 0.378667, 0.521333, 0.287000, 0.342000, 0.415000, 0.660143, 0.361667, 0.426000, 0.435476],
    '3P%': [0.383429, 0.334000, 0.292667, 0.230333, 0.326000, 0.325000, 0.000000, 0.219000, 0.340273, 0.295287],
    'FT%': [0.856286, 0.813333, 0.706333, 0.812000, 0.731250, 0.770833, 0.615714, 0.610333, 0.764455, 0.727156],
    'AST': [2.214286, 2.200000, 3.833333, 1.166667, 1.050000, 1.950000, 0.800000, 0.600000, 3.881818, 1.866285],
    'STL': [0.628571, 0.600000, 0.966667, 0.266667, 0.425000, 0.483333, 0.428571, 0.400000, 1.472727, 0.657229],
    'BLK': [0.171429, 0.133333, 0.833333, 0.166667, 0.200000, 0.116667, 0.557143, 0.466667, 0.390909, 0.363125],
    'TOV': [0.957143, 1.100000, 2.400000, 0.566667, 0.575000, 0.983333, 1.071429, 0.400000, 2.418182, 1.092803],
    'PF': [1.500000, 1.000000, 3.233333, 1.200000, 1.150000, 1.116667, 2.228571, 1.100000, 2.336364, 1.680199],
    'PTS': [6.571429, 9.300000, 15.166667, 4.066667, 6.050000, 4.166667, 5.785714, 1.833333, 16.590909, 8.020594],
    'GAME_COUNT': [7.0, 3.0, 3.0, 3.0, 4.0, 6.0, 7.0, 3.0, 11.0, 7.010204]
}, index=[
    "Aaron Holiday", "Alexey Shved", "Alperen Şengün", "Anthony Lamb", "Armoni Brooks",
    "Tyler Ennis", "Tyson Chandler", "Usman Garuba", "Victor Oladipo", "Average"
]))

st.markdown("##### Calculate everyone's distance from the average")
st.write("""
    To assess whether a player is underperforming, we will calculate the average statistics of the team and use that as the threshold.
    This can be achieved by representing the "Average" row as a 9-dimensional vector, then using linear algebra to find the euclidean distance.
""")
st.code("""
    def calculate_distance_from_avg(team: pd.DataFrame) -> pd.Series:
        stat_cols = team.columns[:9]
        
        # Extract the average as a vector
        average_vector = team.loc["Average", stat_cols]
        
        def distance_from_average(row):
            diff = row[stat_cols] - average_vector
            return np.linalg.norm(diff)
        
        # Compute distances for non-average rows
        distances = team.loc[team.index != "Average"].apply(distance_from_average, axis=1)
        
        return distances.dropna()
    
    houston_rockets_stats["DISTANCE_FROM_AVG"] = calculate_distance_from_avg(houston_rockets_stats)
    houston_rockets_stats = houston_rockets_stats.sort_values("DISTANCE_FROM_AVG", ascending=False)
    houston_rockets_stats = houston_rockets_stats.loc[
        (houston_rockets_stats.index == "Average") | 
        (~houston_rockets_stats.isna().any(axis=1))
    ]
    houston_rockets_stats.iloc[:-1, [-3]]
""")

st.markdown("##### Identify underperforming players using Z-score and label appropriately")
st.write("""
    To identify underperforming players we can calculate each players Z-score and see how many standard deviations it is from the mean. 
    I'm using ±1 standard deviations as the threshold.
""")
st.code("""
    def calculate_z_score(team: pd.DataFrame) -> pd.Series:
        distances = team['DISTANCE_FROM_AVG']
        z_scores = (distances - distances.mean()) / distances.std()
        return z_scores
        
    def calculate_performance(team: pd.DataFrame) -> pd.Series:
        z_scores = calculate_z_score(team)
        
        # Assign performance labels based on z-score
        performance = pd.cut(
            z_scores,
            bins=[-np.inf, -1, 1, np.inf],
            labels=['Underperforming', 'Average', 'Overperforming']
        )
        
        return pd.DataFrame({
            "Z_SCORE": z_scores,
            "PERFORMANCE": performance
        })
        
    houston_rockets_stats[["Z_SCORE", "PERFORMANCE"]] = calculate_performance(houston_rockets_stats)
    houston_rockets_stats.iloc[:, -3:]
""")
st.dataframe(pd.DataFrame(data={
    "DISTANCE_FROM_AVG": [20.078258, 15.926157, 13.211909, 11.794021, 10.883128, 1.041478, 0.878695, 0.772126, 0.711175],
    "Z_SCORE": [4.890265, 3.612323, 2.776926, 2.340526, 2.060169, -0.968913, -1.019015, -1.051814, -1.070574],
    "PERFORMANCE": ["Overperforming", "Overperforming", "Overperforming", "Overperforming", "Overperforming", "Average", "Underperforming", "Underperforming", "Underperforming"]
}, index=[
    "James Harden", "Russell Westbrook", "John Wall", "Jalen Green", "Chris Paul",
    "Josh Smith", "KJ Martin", "Frank Kaminsky", "Austin Rivers"
]))
st.write("Now we have successfully identified underperforming (and overperforming) player to some degree.")

st.markdown("##### Suggest better suited teams with KNN Classifier")
st.write("Next comes the fun part, using the KNeighborsClassifier to get the 10 most similar teams.")
st.code("""
    underperforming_players = houston_rockets_stats.query("PERFORMANCE == 'Underperforming'")

    X = average_team_stats # Predictors (stats)
    y = average_team_stats.index # Classes (teams)
    
    # Getting closest suggestions
    knn = KNeighborsClassifier(n_neighbors=10, metric='euclidean').fit(X, y)
    
    try:
        player_stats = underperforming_players.iloc[-1, :9].to_frame().T
        distances, indices = knn.kneighbors(player_stats)
    except IndexError:
        print("No underperforming players!")
""")

st.markdown("##### Visualising")
values = [
    0.11137566043893536,
    0.10556061087271537,
    0.10170136556722124,
    0.10035136986417396,
    0.10034025192877818,
    0.09978468757119704,
    0.09934822539312019,
    0.09547419255625489,
    0.0938480622885409,
    0.0922155735190628
]
colors = [
    "#b40426", "#da5948", "#f18e70", "#f7b89c", "#ead4c8",
    "#ced9ec", "#aac7fd", "#83a6fb", "#5d7ce6", "#3b4cc0"
]
teams = ["MIA","NOP","DET","IND","BRK","MIN","LAC","HOU","PHO","CHO"]
fig = go.Figure()
cumulative = 0

for i, (val, color, team) in enumerate(zip(values, colors, teams)):
    fig.add_trace(go.Bar(
        y=["Team"],
        x=[val],
        orientation='h',
        base=[cumulative],
        text=team,
        textposition="inside",
        marker=dict(color=color),
        hoverinfo=None
    ))
    cumulative += val

fig.update_layout(
    barmode='stack',
    height=250,
    width=700,
    showlegend=False,
    xaxis=dict(showticklabels=False, showgrid=False, zeroline=False, title=''),
    yaxis=dict(showticklabels=False, showgrid=False, zeroline=False, title='')
)
st.plotly_chart(fig)

st.write("""
    Austin Rivers has been labelled as an underperforming player this season, owing to his below-average shooting efficiency, with a field goal percentage of only 42.0%. 
    However, statistical compatibility suggests that Miami Heat (MIA) is a good possible fit. Miami Heat has a very modest team FG% of 44.4% and 3P% of 31.8%, 
    implying that Rivers' present shooting stats would not significantly trail behind his teammates and may grow within a system that does not rely heavily on exceptional shooting from his position. 
    In addition, Rivers' strong defensive contributions (0.73 steals and 0.16 blocks per game) are somewhat consistent with Miami's defensive identity and needs.

    Let's assume, Austin Rivers plays on the Miami Heat, would he now be considered underperforming, average, or overperforming? Let's fetch his data and find out.
""")

st.code("austin_rivers_data = houston_rockets_stats.iloc[[-2]].copy()")
st.dataframe(data={
    'Player': ['Austin Rivers'],
    'DISTANCE_FROM_AVG': [0.711175],
    'Z_SCORE': [-1.070574],
    'PERFORMANCE': ['Underperforming']
})
st.write("Repeating the process with Austin Rivers on the Miami Heat yielded a promising result:")
st.dataframe(data = {
    'Player': ['Austin Rivers'],
    'DISTANCE_FROM_AVG': [1.020882],
    'Z_SCORE': [-0.958928],
    'PERFORMANCE': ['Average']
})

st.header("Predicting Game Outcomes: Home vs. Away Using Different Classification Models")
st.write("The purpose of this analysis is to explore several classifiers and determine which would be more suitable for this certain application.")
st.write("Training the models:")
st.code("""
    def train_model(classifier):
        X = training_df[["HOME", "PTS", "FG_PCT", "FG3_PCT", "FT_PCT", "REB", "AST", "STL", "BLK", "TOV"]]
        y = training_df["WL"]
        
        # Train the model
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        cls = classifier.fit(X_train, y_train)
        
        # Predict and evaluate
        y_pred = cls.predict(X_test)
""")
st.code("""
    classifiers = [
        ("KNN", KNeighborsClassifier()),
        ("Random Forest", RandomForestClassifier()),
        ("SVC", SVC()),
        ("Gradient Boosting", GradientBoostingClassifier())
    ]
    
    for name, clf in classifiers:
        train_model(clf)
""")
st.badge("KNN Accuracy: 71.0%", color="red")
st.write("""
    K-Nearest Neighbors (KNN) is a basic classification algorithm which makes predictions based on the similarity between data points. 
    KNN represents each game as a vector in multidimensional space; looking for the K most similar games using euclidean distance by default. 
    The algorithm then looks at what happened in the K most similar games and predicts the most frequent outcome as the outcome for the new game. 
    KNN is an all round safe bet when it comes to classifying numerical data, but may not be the best suited in every case. 
    For this example, we achieved an accuracy of 71% which is decent and means its classifying correctly most of the time.
""")
st.badge("Random Forest Accuracy: 80.3%", color="green")
st.write("""
    Random Forest is a powerful classifier that constructs several decision trees on several random subsets of the data and the features. 
    To predict, it takes all of the sub-trees and forms a prediction on the grounds of majority voting to provide a more precise and stable prediction than a single decision tree. 
    Random Forest is designed to reduce overfitting and improve generalization by combining the predictions of multiple decision trees trained on different subsets of the data. 
    This has proved successful, as we have a much better accuracy of 80.3%, meaning it's classifying correctly four fifths of the time.
""")
st.badge("SVC: 75.2%", color="orange")
st.write("""
    Support Vector Classification (SVC) is an algorithm for machine learning which tries to separate the data into classes by learning the best boundary between them. 
    SVC tries to find not just the line that separates the classes, but the line as far as it can from the closest points in each set. 
    These are called support vectors, and are the defining points which make the line of separation. If the data cannot be divided neatly using a line, SVC can apply what's called a kernel function to transform the data so it can be divided. 
    Once it's trained, the model uses the boundary to determine into what grouping a new item of data fits. With an accuracy of 75.2% it's proving to be a decent choice.
""")
st.badge("Gradient Boosting Accuracy: 80.2%", color="orange")
st.write("""
    Gradient Boosting Classification is another ensemble ML process where it builds an efficient prediction model by aggregating multiple weak decision trees in an iterative process. 
    Each iteration entails trying to minimize the previous iterations' residual errors as much as possible. This process is performed by training the new learner on the errors of previous decision trees. 
    Gradient boosting works well for many classification problems and can be adjusted to perform even better by choosing different ways to measure errors (loss functions) and by using techniques that help prevent the model from becoming too complicated. 
    This resulted in an accuracy of 80.2%.
    
    To summarise, each of the classifiers performed as anticipated and in line with the type and quality of the dataset. From the observed performance, each of the models was suited for the task and was capable of dealing with the information in a satisfactory manner. 
    Differences in performance did occur, but were primarily a result of the nature of each of the classifiers and how it operates on the patterns in the information.
""")

st.divider()
st.divider()

st.header("Time Series")
st.write("""
For this section of the project, I focused on time series analysis. I wanted to understand how teams' average points per game (PPG) changed over time, and to forecast where a team might be headed based on its historical performance.

I chose this approach because it allowed me to look beyond isolated game stats and focus on long-term patterns. Whilst I wanted to research more into advanced forecasting models like ARIMA, I opted for a simpler and more explainable method given our time constraints and other aspects of this project.
""")
st.subheader("Step 1: Preparing the Time Series Data")
st.write("""
I began by grouping regular season game data by `TEAM_NAME` and the season end date. I opted to only use regular season games as I knew all teams would play the same amount of games through a regular season and I did not want playoff fixtures to skew the results, so with that being said this analysis is only applicable for regular season games. For each team, I calculated the average points per game per season. This gave a clean summary of team performance over time.

Here’s the code I used to generate the time series:
""")
st.code("""
team_season_stats = (
    regular_games.groupby([pd.Grouper(key="GAME_DATE", freq="Y"), "TEAM_NAME"])["PTS"]
    .mean()
    .reset_index()
    .rename(columns={"GAME_DATE": "SEASON", "PTS": "AVG_PTS"})
)
""")
st.subheader("Step 2: Visualisations")
st.write("""
I created four visualisations for each team, ordered in a way that makes logical sense. We started with raw performance, then showing change, breaking down patterns, and finally estimating a forecast for next season.
""")
st.markdown("**1. Average Points Per Game (APPG)**")
st.write("""
This line graph shows how a team's average points per game has changed across seasons. It gives a good sense of whether a team has improved, declined, or stayed relatively consistent over time. 
""")
st.markdown("**2. Change in APPG (Year-over-Year)**")
st.write("""
This bar chart displays how much the team’s scoring changed from one season to the next. It helps identify sudden jumps or drops, which often relate to roster changes, coaching adjustments, or other external factors.
""")
st.markdown("**3. Time Series Decomposition**")
st.write("""
I used the `seasonal_decompose` function from the `statsmodels` library to break down the scoring time series into:
- **Trend** – the overall direction of scoring over time
- **Seasonal** – repeating patterns, in this case roughly every three years
- **Residual** – random or unexplained variation

This breakdown made it easier to identify whether a team's performance was steadily improving, cycling seasonally, or fluctuating without clear structure.

Here’s how I implemented it:
""")
st.code("""
ts = data["AVG_PTS"].copy()
ts.index = pd.date_range(start=data.index.min(), periods=len(ts), freq='Y')
decomp = seasonal_decompose(ts, model="additive", period=3)
""")
st.write("""
The decomposition gave deeper insight into each team's scoring pattern and helped prepare the forecast.
""")
st.markdown("**4. Rolling Average and Forecast**")
st.write("""
To estimate the next season’s average points, I applied a 3-year rolling average to smooth out the data and used the decomposition components to build a simple forecast. 3 year seemed appropriate for the model as we were initially dealing with a 9 year period and most contracts in the sporting era can vary between 1-5 years in length.

Because we didn’t have time to build a full model, I used a basic method where the forecast equals:
- The most recent rolling average
- Plus the latest seasonal effect
- Plus the mean of the residuals

Here’s the code for the calculation:
""")
st.code("""
forecast_trend = data["RollingAvg"].iloc[-1]
forecast_season = decomp.seasonal.iloc[-3]
forecast_resid = decomp.resid.mean(skipna=True)
forecast_val = forecast_trend + forecast_season + forecast_resid
""")
st.write("""
Although from my readings this model is not as robust as ARIMA or exponential smoothing, this method still gave a reasonable estimate and worked well for our projects scope.
""")
st.subheader("Step 3: Connecting Forecasts to Match Predictions")
st.write("""
Once I had forecasted average points for each team, I used this to simulate head-to-head matchups. The logic was simple: if Team A’s forecasted points were higher than Team B’s, Team A would be predicted to win.

To make this interactive, I built a dropdown system where users can select two teams to compare. The app then calculates the forecast for both and returns the expected winner.

Here’s a simplified version of the logic I used:
""")
st.code("""
score1 = round(forecast_avg_pts(team1))
score2 = round(forecast_avg_pts(team2))

winner = team1 if score1 > score2 else team2 if score2 > score1 else "Tie"
""")
st.write("""
This added a practical application to the forecasting work that turned raw time series data into a simple, interpretable decision tool.
""")
st.subheader("Technical Considerations")
st.write("""
There were several technical decisions I made during this process:

- I used `pd.date_range()` with `freq='Y'` to generate evenly spaced annual time points, aligning with the assumption of one observation per season.
- I selected a seasonal period of 3 in `seasonal_decompose` based on exploratory plotting, many teams showed multi-year performance cycles.
- I applied the same rolling average and decomposition-based forecast method to all teams for consistency, knowing that this wouldn’t be perfect for every case.

If I had more time, I would have liked to tried more advanced models for more accurate, team-specific forecasting, and experiment with different seasonal periods based on autocorrelation plots.
""")

@st.cache_data
def load_data(path="./data/Cleaned_NBA_All_Games_2015_2024.csv"):
    df = pd.read_csv(path)
    df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"])
    return df

regular_games = load_data()

# Aggregate seasonal PPG by team
team_season_stats = (
    regular_games
    .groupby([pd.Grouper(key="GAME_DATE", freq="Y"), "TEAM_NAME"])["PTS"]
    .mean()
    .reset_index()
    .rename(columns={"GAME_DATE": "SEASON", "PTS": "AVG_PTS"})
)

# Time Series Forecast — select a team to see it in action
st.header("Time Series Forecast")
teams = sorted(team_season_stats["TEAM_NAME"].unique())
selected_team = st.selectbox("Select Team:", [""] + teams)

if selected_team:
    # Filter down to the chosen team
    df = team_season_stats.query("TEAM_NAME == @selected_team").copy()
    df.set_index("SEASON", inplace=True)
    df.index = pd.to_datetime(df.index)

    # Compute a 3-year rolling average and year-over-year change
    df["RollingAvg"] = df["AVG_PTS"].rolling(window=3, min_periods=1).mean()
    df["ChangeYOY"] = df["AVG_PTS"].diff()

    # Decompose the PPG series into trend, seasonal and residual components
    ts = df["AVG_PTS"].copy()
    ts.index = pd.date_range(start=df.index.min(), periods=len(ts), freq="Y")
    decomp = seasonal_decompose(ts, model="additive", period=3)

    # Build a simple next-season forecast
    next_year = df.index.year.max() + 1
    forecast = (
        df["RollingAvg"].iloc[-1]
        + decomp.seasonal.iloc[-3]
        + decomp.resid.mean(skipna=True)
    )

    # 1) Average Points Per Game
    st.subheader("Average Points Per Game")
    st.markdown("How a team's average PPG evolves each season.")
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(df.index.year, df["AVG_PTS"], marker="o")
    ax1.set_title("Average PPG by Season")
    ax1.set_xlabel("Season")
    ax1.set_ylabel("Avg PPG")
    ax1.grid(True)
    st.pyplot(fig1)

    # 2) Year-over-Year Change
    st.subheader("Year-over-Year Change")
    st.markdown("Season-to-season delta in a team's average PPG.")
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.bar(df.index.year, df["ChangeYOY"], color="gray")
    ax2.set_title("Year-over-Year Change in PPG")
    ax2.set_xlabel("Season")
    ax2.set_ylabel("Δ Avg PPG")
    ax2.grid(True)
    st.pyplot(fig2)

    # 3) Time Series Decomposition
    st.subheader("Time Series Decomposition")
    st.markdown("Trend, seasonal and residual components of the PPG series.")
    fig3 = decomp.plot()
    fig3.set_size_inches(10, 8)
    fig3.suptitle("Decomposition of Average PPG", y=1.02)
    st.pyplot(fig3)

    # 4) Forecast for Next Season
    st.subheader("Forecast for Next Season")
    st.markdown("Projection combining 3-yr trend, seasonal effect and residual.")
    fig4, ax4 = plt.subplots(figsize=(10, 4))
    ax4.plot(df.index.year, df["RollingAvg"], marker="x", linestyle="--", label="3-Yr Rolling Avg")
    ax4.scatter([next_year], [forecast], color="red", s=100, label="Forecast")
    ax4.set_title("Rolling Average & Next Season Forecast")
    ax4.set_xlabel("Season")
    ax4.set_ylabel("Avg PPG")
    ax4.legend()
    ax4.grid(True)
    st.pyplot(fig4)

    st.success(f"Forecasted Avg PPG for {selected_team}: {forecast:.2f}")

st.divider()
st.divider()

st.header("Clustering")
st.write("""
This section focuses on completing unsupervised classification by clustering with K-Means. With this we are able to see if we can create clusters of players by position that perform similarly and have similar average game statistics. In this we way, we can also extend this to cluster NBA teams based on their play style/performance. For clustering with k-Means we want high within group similarity but low between group similarity. Sometimes there are clear groupings, sometimes there are no clear groupings and often we find something in between.
""")

st.subheader("Can we cluster players that play a particular position by their average play style/performance?")

st.markdown("""
    **Steps Included:**
    1. Feature Selection based on Position.
    2. Checking for missing values as Clustering with k-Means cannot be completed with NA values.
    3. Scale the data using MinMax. Variables on different scales are not suitable for Clustering with k-Means. 
    4. Perform clustering with k-Means using scikit-learn, setting the number of starting points and the method to choose these starting points via n_init and init.
    5. Identify the best value of k via Silhouette Score, Inertia, Davies–Bouldin Index Average and Calinski–Harabasz Index calculations and plots.
    6. Identifying features of the clusters to try and determine what these clusters represent through description tables and pairs plots of clusters.
    7. Visualise the data through UMAP projection to see the groupings of the multi-dimensional clusters and whether they are distinct.
""")

st.subheader("Player Cluster Viewer by Position")

position = st.selectbox("Select a Position", ["Shooting Guard", "Power Forward", "Point Guard", "Center", "Small Forward"])

file_map = {
    "Shooting Guard": "./data/playerinfo_df_SG.csv",
    "Power Forward": "./data/playerinfo_df_PF.csv",
    "Point Guard": "./data/playerinfo_df_PG.csv",
    "Center": "./data/playerinfo_df_C.csv",
    "Small Forward": "./data/playerinfo_df_SF.csv"
}

file_path = file_map[position]

try:
    df = pd.read_csv(file_path)

    player_names = df["Player"].unique()
    selected_player = st.selectbox("Select a Player", player_names)


    player_info = df[df["Player"] == selected_player].iloc[0,1:]
    cluster_id = player_info['Cluster']
    cluster_mates = df[(df['Cluster'] == cluster_id) & (df["Player"] != selected_player)]
    cluster_info = df[(df['Cluster'] == cluster_id)]

    st.subheader(f"Cluster {cluster_id}")
    st.subheader(f"Overview of Cluster {cluster_id}")
    st.write(cluster_info.iloc[:,1:-1].describe()[1:])

    st.subheader(f"Pairs Plot for Position {position}")
    pair_grid = sns.pairplot(df[df.columns[1:]], diag_kind="kde", hue="Cluster")
    st.pyplot(pair_grid.fig)

    st.subheader("Selected Player Information")
    st.write(player_info.to_frame().T)

    st.subheader(f"Other Players in Cluster {cluster_id}")
    st.dataframe(cluster_mates.iloc[:,1:-1])

except FileNotFoundError:
    st.error(f"The file for {position}s was not found. Make sure '{file_path}' exists.")


st.subheader("Can we cluster teams by their average game statistics/play performance?")

st.markdown("""
    **Steps Included:**
    1. Feature Selection based on Team Performance/Statistics.
    2. Checking for missing values as Clustering with k-Means cannot be completed with NA values.
    3. Scale the data using MinMax. Variables on different scales are not suitable for Clustering with k-Means. 
    4. Perform clustering with k-Means using scikit-learn, setting the number of starting points and the method to choose these starting points via n_init and init.
    5. Identify the best value of k via Silhouette Score, Inertia, Davies–Bouldin Index Average and Calinski–Harabasz Index calculations and plots.
    6. Identifying features of the clusters to try and determine what these clusters represent through description tables and pairs plots of clusters.
    7. Visualise the data through UMAP projection to see the groupings of the multi-dimensional clusters and whether they are distinct.
""")

st.subheader("Team Cluster Viewer")

file_path2 = "./data/teaminfo_df_Grouped.csv"

try:
    df2 = pd.read_csv(file_path2)

    team_names = df2["Team Name"].unique()
    selected_team = st.selectbox("Select a Team", team_names)

    team_info = df2[df2["Team Name"] == selected_team].iloc[0,1:]
    cluster_id2 = team_info['Cluster']
    cluster_mates2 = df2[(df2['Cluster'] == cluster_id2) & (df2["Team Name"] !=  selected_team)]
    cluster_info2 = df2[(df2['Cluster'] == cluster_id2)]

    st.subheader(f"Cluster {cluster_id2}")
    st.subheader(f"Overview of Cluster {cluster_id2}")
    st.write(cluster_info2.iloc[:,2:-1].describe()[1:])

    st.subheader(f"Pairs Plot")
    pair_grid2 = sns.pairplot(df2[df2.columns[2:]], diag_kind="kde", hue="Cluster")
    st.pyplot(pair_grid2.fig)

    st.subheader("Team Information")
    st.write(team_info.to_frame().T)

    st.subheader(f"Other Teams in Cluster {cluster_id2}")
    st.dataframe(cluster_mates2.iloc[:,1:-1])

except FileNotFoundError:
    st.error(f"The file for {position}s was not found. Make sure '{file_path}' exists.")

st.divider()
st.divider()

st.header("Regression")
st.write("""
In this section, I aimed to predict how many points an NBA team would score in a game using common game statistics. 
Rather than using actual scoring stats like `PTS`, `FGM`, or `3PM`, I selected features that could influence scoring 
without directly giving it away — this helps avoid what's known as **data leakage**.
""")

st.subheader("Step 1: Preparing the Data")
st.write("""
I started by selecting 12 features that teams usually influence through gameplay:
""")
st.code("""
features = [
    'MIN', 'FGA', 'FG3A', 'FTA', 'OREB', 
    'REB', 'DREB', 'AST', 'STL', 'BLK', 'TOV', 'PF'
]
X = regular_games[features]
y = regular_games['PTS']
""", language="python")
st.write("""
Here, `X` represents the predictor variables (our input stats), and `y` is the target variable — the points scored.
""")

st.subheader("Step 2: Splitting and Training the Model")
st.write("""
Next, I split the data into training and testing sets (80% training, 20% testing). 
This helps the model learn from past data and evaluate performance on unseen games.
""")
st.code("""
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

reg = RandomForestRegressor(n_estimators=100, random_state=42)
reg.fit(X_train, y_train)
y_pred = reg.predict(X_test)
""", language="python")
st.write("""
Random Forest is an ensemble model made up of many decision trees. Each tree gives a prediction, 
and the forest averages them for more accurate and stable results.
""")

st.subheader("Step 3: Evaluating the Model")
st.write("""
To evaluate how well the model predicted team points, I used three common metrics:
""")
st.code("""
rmse = mean_squared_error(y_test, y_pred, squared=False)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
""", language="python")

st.write("""
- **RMSE (Root Mean Squared Error):** Measures average prediction error. Lower is better.
- **MAE (Mean Absolute Error):** Average size of errors. Helps understand overall miss.
- **R² Score:** Measures how much variation is explained by the model. 1.0 is perfect.
""")

st.subheader("Step 4: Interpreting the Model")
st.write("""
One big benefit of Random Forest is that it tells you how important each feature was in predicting team points.
""")
st.code("""
importances = reg.feature_importances_
""", language="python")

st.write("""
In my case, the model showed:
- `AST` (assists) had the highest importance — logical, since assists lead directly to baskets.
- `FTA`, `FGA`, and `OREB` followed closely — these represent opportunities to score.
""")

st.header("Predicting NBA Team Season Rank Based on Game Stats")

st.write("""
Next, I tried predicting a team's final rank in a given NBA season using Random Forest Regression and aggregated season stats.
""")

st.subheader("Step 1: Data Preparation")
st.write("""
- Copied the original dataset to avoid modifying it directly.
- Created a binary `WIN` feature from the win/loss result.
- Calculated total wins and ranked teams by wins per season.
- Aggregated mean stats per team per season to serve as features.
""")
st.code("""
data = all_games.copy()

data['WIN'] = (data['WL'] == 'W').astype(int)

team_wins = data.groupby(['TEAM_NAME', 'SEASON'])['WIN'].sum().reset_index()
team_wins['TEAM_RANK'] = team_wins.groupby('SEASON')['WIN'].rank(ascending=False, method='dense')

group_stats = data.groupby(['TEAM_NAME', 'SEASON']).agg({
    'PTS': 'mean','AST': 'mean','REB': 'mean','FG_PCT': 'mean','FG3_PCT': 'mean',
    'FT_PCT': 'mean','TOV': 'mean','FGA': 'mean','FG3A': 'mean',
    'FTA': 'mean','OREB': 'mean','DREB': 'mean','STL': 'mean','BLK': 'mean','PF': 'mean',
}).reset_index()

complete_set = pd.merge(group_stats, team_wins[['TEAM_NAME', 'SEASON', 'TEAM_RANK']], on=['TEAM_NAME', 'SEASON'])
""")

st.subheader("Step 2: Feature Scaling and Model Training")
st.write("""
Scaled the features for consistent range, then split into train/test sets and trained the Random Forest model.
""")
st.code("""
X = complete_set.drop(['TEAM_NAME', 'SEASON', 'TEAM_RANK'], axis=1)
y = complete_set['TEAM_RANK']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

reg = RandomForestRegressor(n_estimators=100, random_state=42)
reg.fit(X_train, y_train)

y_pred = reg.predict(X_test)
""")

st.subheader("Step 3: Model Evaluation")
st.code("""
mse = root_mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
mean = mean_absolute_error(y_test, y_pred)

print(f"RMSE: {mse:.2f}")
print(f"R2: {r2:.4f}")
print(f"MAE: {mean:.2f}")
""")
st.write("""
- RMSE and MAE show the model's predicted rank is usually off by about 4 places, which is reasonable.
- R² around 0.51 means the model explains just over half the variance in team rankings, which is promising.
- Small difference between RMSE and MAE suggests consistent prediction errors without many outliers.
""")

st.subheader("Step 4: Model Improvements and Data Leakage")
st.write("""
Previously, I accidentally included `PLUS_MINUS` as a feature, which caused data leakage since it directly relates to point differentials and winning.

After removing it, model performance dropped but became more valid and trustworthy.
""")

st.subheader("Step 5: Insights on Feature Importance")
st.write("""
The model shows that `FG3_PCT` (3-point field goal percentage) is by far the most important predictor for team rank.

This matches NBA trends where strong 3-point shooting correlates strongly with winning and better rankings.
""")

st.write("Overall, both models demonstrate how game and season stats can be used to predict team scoring and ranking, highlighting key stats like assists and three-point shooting.")

st.subheader("Conclusion")
st.write("""
Random Forest turned out to be a solid choice. It:
- Captured relationships between stats and team performance
- Gave decent accuracy using just gameplay stats
- Helped explain what drives team scoring

This model could serve as a foundation for predicting future team performances, 
or be extended by adding contextual data like opponent strength or home/away effects.
""")


with st.sidebar:
    st.header("Contents")
    # Table of contents
    st.markdown("""
        <style>
            .toc a {
                display: block;
                text-decoration: none;
                color: var(--text-color);
                padding-left: 0px;
                margin: 0.25em 0;
                font-size: 0.95em;
                transition: opacity 0.1s;
            }
            .toc a:hover {
                opacity: 0.5;
            }
            .toc a.one {
                padding-left: 20px;
            }
        </style>

        <div class="toc">
            <a href="#classification">Classification</a>
            <a href="#time-series">Time Series</a>
            <a href="#clustering">Clustering</a>
            <a href="#regression">Regression</a>
        </div>
        """, unsafe_allow_html=True)