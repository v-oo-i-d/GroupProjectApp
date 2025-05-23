import streamlit as st
import pandas as pd

st.set_page_config(page_title="Home", layout="wide")

team_stats_df = pd.read_csv("./data/Cleaned_NBA_Per_Game_Stats_2015_2024.csv")
regular_df = pd.read_csv("./data/Cleaned_NBA_Regular_Season_Games_2015_2024.csv")
playoff_df = pd.read_csv("./data/Cleaned_NBA_Playoff_Games_2015_2024.csv")
all_games_df = pd.read_csv("./data/Cleaned_NBA_All_Games_2015_2024.csv")

st.header("Exploring NBA Statistics")

st.markdown(
    """
    <style>
        p {
            display: block;
            margin: 0;
        }
        i {
            padding-right: 1em;
        }
        .idk {
            color: var(--text-color);
            opacity: 0.5;
        }
    </style>
    
    <p class="idk">Project 3, Group 3, 297201</p>
    <br>
    
    <p><i class="idk">23013368</i>Michael Graham</p>
    <p><i class="idk">19037138</i>AJ Stone</p>
    <p><i class="idk">9036628&nbsp;&nbsp;</i>Amanda Hawkins</p>
    <p><i class="idk">24004428</i>Kobe Spring</p>
""", unsafe_allow_html=True)
st.divider()

# Abstract
st.header("Abstract")
st.write("""
    This article explores how NBA player performance data from multiple seasons was collected, cleaned, and analyzed to uncover meaningful insights. 
    It explains how the raw data was organized and prepared for use, then used to answer important questions about players, teams, and trends across seasons. 
    Alongside the analysis, a range of visualizations are included to help tell the story behind the numbers and highlight key takeaways. 
    The goal is to show how data can be used to better understand the game and its players.
""")

# Introduction
st.header("Introduction")
st.markdown("""
    Working with real world sports data, especially from an immensely popular sport like basketball, is either a hit or miss when it comes to extracting data. 
    Across seasons, data can vary in format, contain missing or inconsistent values, and often includes an overwhelming number of features and player records. 
    These issues can hinder the ability to draw insights or use the data effectively for deeper analysis or visualization.
    The primary goal of this project was to take raw NBA performance data and turn it into something clean, structured, and ready for analysis. 
    This involved, honestly, very minimal inconsistency resolving and cleaning. The work here differs in that it focuses solely on actual data wrangling stages particular to sports analytics. 
    This project walks through all of the steps, from acquiring the data, cleaning it, potential feature engineering, and eventually visualization, 
    to demonstrate how the demands data preparation may lead to insightful findings and enable intricate modelling in the future.
""", unsafe_allow_html=True)

# Dataset Overview
st.header("Dataset Overview")
st.write("""
    The data we are working with consists of 3 separate datasets, all originating from the NBA. 
    The first dataset contains player data from 1425 players, every row containing a player, season, and average stats for that season.\n
""")
st.divider()
st.dataframe(team_stats_df)

st.write("The seconds dataset contains regular games from every team and every season, along with the same metrics as the player dataset.")
st.divider()
st.dataframe(regular_df)

st.write("Our last dataset is the exact same as the previous, except it contains playoff games.")
st.divider()
st.dataframe(playoff_df)

st.write("These last two datasets were combined into a larger games dataset containing every game for easier use.")

# Wrangling Methodology
st.header("Wrangling Methodology")
st.write("""
    The dataset was compiled from NBA player statistics across multiple seasons using the NBA API. Due to the 
    robustness of the NBA datasets and the abundance of available documentation, the raw data required minimal 
    preprocessing. However, several foundational cleaning steps were performed using pandas to ensure consistency and reliability for analysis.
""")

st.subheader("Date Formatting")
st.write("Game dates were initially provided as strings. These were converted into proper datetime format to facilitate time-based filtering and analysis.")
st.code("regular_games['GAME_DATE'] = pd.to_datetime(regular_games['GAME_DATE'], errors='coerce')")

st.subheader("Header Row Removal")
st.write("Some datasets included repeated headers within the data. These were removed to prevent type mismatches and ensure clean numeric operations.")
st.code("team_stats = team_stats[team_stats['Player'] != 'Player']")

st.subheader("Data Type Correction")
st.write("Numeric values such as points, assists, and rebounds were sometimes parsed as strings. We ensured that all columns containing numeric-like values were properly cast:")
st.code("""
    for col in team_stats.columns:
        team_stats[col] = pd.to_numeric(team_stats[col], errors='ignore')
""")

st.subheader("Feature Engineering")
st.write("""
    Additional features were engineered to support downstream analysis, these included binary columns, team rank, z-scores, Euclidean distances from average metrics, rolling averages, and more.
    Feature engineering plays a crucial role in developing machine learning models. By generating new features from existing data, you can uncover hidden patterns, trends, or relationships between variables
    that may not have been immediately apparent beforehand. These new columns can help the models distinguish between classes, predict outcomes, and generalize unseen data more accurately.
    Ultimately, thoughtful engineering, often leads to simpler and more accurate machine learning models, making it a key step in the process.
""")


# Results & Evaluation
# st.header("Results & Evaluation")

# Discussion
st.header("Discussion (add your own sections)")
st.subheader("Classification")
st.markdown("""
    This section of the discussion serves to discuss the classification models used in the analyses section of this research.
    It weighs the pros and cons and nature of each classification model and its u
    
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;K Nearest Neighbors (KNN) is a basic classification algorithm which makes predictions based on the similarity between data points. 
    KNN represents each game as a vector in multidimensional space; looking for the K most similar games using euclidean distance by default. 
    The algorithm then looks at what happened in the K most similar games and predicts the most frequent outcome as the outcome for the new game. 
    KNN is an all round safe bet when it comes to classifying numerical data, but may not be the best suited in every case. 
    For this example, we achieved an accuracy of 71% which is decent and means its classifying correctly most of the time.
    
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Random Forest is a powerful classifier that constructs several decision trees on several random subsets of the data and the features. 
    To predict, it takes all of the sub-trees and forms a prediction on the grounds of majority voting to provide a more precise and stable prediction than a single decision tree. 
    Random Forest is designed to reduce overfitting and improve generalization by combining the predictions of multiple decision trees trained on different subsets of the data. 
    This has proved successful, as we have a much better accuracy of 80.3%, meaning it's classifying correctly four fifths of the time.

    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Support Vector Classification (SVC) is an algorithm for machine learning which tries to separate the data into classes by learning the best boundary between them. 
    SVC tries to find not just the line that separates the classes, but the line as far as it can from the closest points in each set. 
    These are called support vectors, and are the defining points which make the line of separation. If the data cannot be divided neatly using a line, SVC can apply what's called a kernel function to transform the data so it can be divided. 
    Once it's trained, the model uses the boundary to determine into what grouping a new item of data fits. With an accuracy of 75.2% it's proving to be a decent choice.

    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Gradient Boosting Classification is another ensemble ML process where it builds an efficient prediction model by aggregating multiple weak decision trees in an iterative process. 
    Each iteration entails trying to minimize the previous iterations' residual errors as much as possible. This process is performed by training the new learner on the errors of previous decision trees. 
    Gradient boosting works well for many classification problems and can be adjusted to perform even better by choosing different ways to measure errors (loss functions) and by using techniques that help prevent the model from becoming too complicated. 
    This resulted in an accuracy of 80.2%.
    
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;To summarise, each of the classifiers performed as anticipated and in line with the type and quality of the dataset. From the observed performance, each of the models was suited for the task and was capable of dealing with the information in a satisfactory manner. 
    Differences in performance did occur, but were primarily a result of the nature of each of the classifiers and how it operates on the patterns in the information.
""")

# Conclusion
st.header("Conclusion?")