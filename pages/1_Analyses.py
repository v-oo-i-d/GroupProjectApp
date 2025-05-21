import streamlit as st

st.set_page_config(page_title="Analyses", page_icon="🔎", layout="wide")

st.header("Analyses")
st.write("""
    This page's goal is to go into greater depth regarding the steps that are taken to transform our cleaned NBA performance datasets into a form that is analytically ready. 
    These processes typically include, but are not limited to, dealing with missing values, inconsistencies in formats, duplicate records, and correcting data types. 
    In addition to demonstrating our wrangling skills, this part describes the approach we utilised to formulate and examine many research problems. 
    These questions prompted our investigation into player performance patterns, team statistics, and other relevant insights, all backed by well-presented data visualisations and summaries.
""")
st.divider()

st.header("Regression")
st.write("""
    Kobe's section
""")


st.header("Classification")
st.write("""
    Michael's section
""")

st.header("Time Series")
st.write("""
    A.J's section
""")

st.header("Clustering")
st.write("""
    Amanda's section
""")

with st.sidebar:
    st.write("## Contents")
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
            .toc a.two {
                padding-left: 40px;
            }
            .toc a.three {
                padding-left: 60px;
            }
            .toc a.four {
                padding-left: 80px;
            }
        </style>
        
        <div class="toc">
            <a class="one" href="#regression">Regression</a>
            <a class="one" href="#classification">Classification</a>
            <a class="one" href="#timeseries">Time Series</a>
            <a class="one" href="#clustering">Clustering</a>
        </div>
        """, unsafe_allow_html=True)