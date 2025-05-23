import streamlit as st

st.set_page_config(page_title="Home", layout="wide")

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
""")

# Wrangling Methodology
st.header("Wrangling Methodology")

# Results & Evaluation
st.header("Results & Evaluation")

# Discussion
st.header("Discussion")

# Conclusion
st.header("Conclusion")