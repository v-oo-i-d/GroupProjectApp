import streamlit as st
import pandas as pd
import os

st.header("Our Datasets")

# Path to the directory containing the data
data_dir = "data"

# Ensure the directory exists
if not os.path.exists(data_dir):
    st.error(f"The directory '{data_dir}' does not exist.")
else:
    # List only CSV files in the /data directory
    csv_files = [file for file in os.listdir(data_dir) if file.endswith('.csv')]

    if not csv_files:
        st.write("No CSV files found in the /data directory.")
    else:
        for file in csv_files:
            st.subheader(f"{file}")
            try:
                df = pd.read_csv(os.path.join(data_dir, file))
                st.dataframe(df)
            except Exception as e:
                st.error(f"Could not read {file}: {e}")
