import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Qualiextra", page_icon="🏝️", layout="wide")

data = st.session_state.data


st.title("Analyse des performances")

# Sélection de la période
period = st.radio("Sélectionnez la période", options=["Année", "Mois", "Semaine"])

# Création du graphique à barres empilées avec Plotly Express
fig = px.bar(
    data.groupby(period)["marge"].sum().reset_index(),
    x=period,
    y="marge",
    labels={"Marge": "Marge"},
    title=f"Évolution de la marge par {period}",
)

# Mise en forme du graphique
fig.update_xaxes(type="category", categoryorder="total ascending")
fig.update_yaxes(title_text="Marge")

# Affichage du graphique avec Streamlit
st.plotly_chart(fig)
