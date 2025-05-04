import streamlit as st

st.set_page_config(page_title="Overview", page_icon="🎯", layout="wide")

st.write("# Project Name")

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
    
    <p class="idk">Project 3, 297201</p>
    <br>
    
    <p><i class="idk">23013368</i>Michael Graham</p>
    <p><i class="idk">19037138</i>AJ Stone</p>
    <p><i class="idk">9036628&nbsp;&nbsp;</i>Amanda Hawkins</p>
    <p><i class="idk">24004428</i>Kobe Spring</p>
    <hr>
    
    <p>Landing page overview blah blah blah</p>
""", unsafe_allow_html=True
)