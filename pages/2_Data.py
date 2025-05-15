import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data", page_icon="📚", layout="wide")

st.write("# Data")

with st.sidebar:
    st.write("Data")
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
                color: var(--text-color);
                opacity: 0.5;
            }
        </style>
        
        <div class="toc">
            <a href="#dataset-1">Dataset 1</a>
            <a href="#dataset-2">Dataset 2</a>
            <a href="#dataset-3">Dataset 3</a>
        </div>
    """, unsafe_allow_html=True)


import os

for file in os.listdir("./data"):
    if file.endswith("Cleaned.csv"):
        df = pd.read_csv(os.path.join("./data", file), index_col=0).reset_index(drop=True)
        st.dataframe(df)


# st.markdown("## Games.csv")
# st.write("Description about this data")
# st.dataframe(pd.read_csv("./data/Games.csv"))
#
# st.markdown("## Merged_RegularSeason_WithWinner.csv")
# st.write("Description about this data")
# st.dataframe(pd.read_csv("./data/Merged_RegularSeason_WithWinner.csv"))