from time import time
from xml.dom.expatbuilder import parseString
import altair as alt
import pandas as pd
import streamlit as st
import re

def parse_timestamps(time_string: str) -> int:
    """
    Parse their plain english into ~minutes
    """
    t = max(re.findall("\d+", time_string), key=int)

    if "min" not in time_string:
        t *= 60
    
    return t

@st.cache
def get_data(path: str = "../data/YYZ.csv"):
    source = pd.read_csv(path)
    source = source.applymap(parse_timestamps)
    source = source.reset_index()
    return source

source = get_data()

# Original time series chart. Omitted `get_chart` for clarity
chart = alt.Chart(source).mark_line().encode(
    x='index:T',
    y='T1 International:Q'
)

# Display both charts together
st.title("Wait time trends at YYZ")
st.altair_chart(chart.interactive(), use_container_width=True)