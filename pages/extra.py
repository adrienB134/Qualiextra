import streamlit as st
import plotly.graph_objects as go
import pandas as pd

data = st.session_state.data

##sidebar
with st.sidebar:
    timeframe = st.radio("Timeframe", ["Mois", "Années", "semaines"])

##computation

fig = go.Figure()
fig.add_trace(
    go.Histogram(x=data["periode_debut"].sort_values(), y=data["extra_clean"])
)
fig.update_traces(dict(marker_line_width=0))

##main

st.plotly_chart(fig)
