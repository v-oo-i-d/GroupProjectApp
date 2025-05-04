import streamlit as st

st.set_page_config(page_title="Analyses", page_icon="🔎", layout="wide")

st.write("# Intro")
st.write("# Analysis")
st.write("## Section 1")
st.write("### 1a")
st.write("#### 1aa")
st.write("#### 1ab")
st.write("## Section 2")
st.write("### 2a")
st.write("#### 2aa")
st.write("## Section 3")
st.write("### 3a")
st.write("#### 3aa")
st.write("# Conclusion")

with st.sidebar:
    st.write("## Contents")
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
                font-weight: bold;
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
            <a class="one" href="#intro">Intro</a>
            <a class="one" href="#analysis">Analysis</a>
                <a class="two" href="#section-1">Section 1</a>
                     <a class="three" href="#1a">1a</a>
                         <a class="four" href="#1aa">1aa</a>
                         <a class="four" href="#1ab">1ab</a>
                <a class="two" href="#section-2">Section 2</a>
                     <a class="three" href="#2a">2a</a>
                         <a class="four" href="#2aa">2aa</a>
                <a class="two" href="#section-3">Section 3</a>
                     <a class="three" href="#3a">3a</a>
                         <a class="four" href="#3aa">3aa</a>
            <a class="one" href="#conclusion">Conclusion</a>
        </div>
        """, unsafe_allow_html=True)