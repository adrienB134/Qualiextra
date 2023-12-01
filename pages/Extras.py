import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Qualiextra", page_icon="🏝️", layout="wide")
data = st.session_state.data
data = data[data["statuts"] != "annulé"]


st.header("Classements des extras sur la totalité de la période")

##Main
col1, col2 = st.columns(2)
top = col1.text_input("Nombre de rangs a afficher", 5)
timeframe = col1.radio("Timeframe", ["Année", "Mois", "Semaine"],horizontal=True)
option = col2.selectbox("Période", (data[timeframe].unique()))
ca_missions = col2.radio("Classement", ["Chiffre d'affaire", "Missions"], horizontal=True)
df = data[data[timeframe] == option]

if ca_missions == "Missions":
    df = (
        df.groupby("extra_clean")
        .count()
        .sort_values(by="extra", ascending=False)
        .reset_index()[["extra_clean", "extra"]]
    )
    df.index = np.arange(1, len(df) + 1)
    df.index = df.index.rename("Rang")
    df.columns = ["Extra", "Missions (nb)"]

else:
    df = (
        df.groupby("extra_clean")
        .sum(numeric_only=True)
        .sort_values(by="total HT", ascending=False)
        .reset_index()[["extra_clean", "total HT"]]
    )
    df.index = np.arange(1, len(df) + 1)
    df.index = df.index.rename("Rang")
    df.columns = ["Extra", "Chiffre d'affaires (€)"]


st.dataframe(df.iloc[0 : int(top), :], use_container_width=True)


data2 = data.groupby(["mois", "Année"])["extra_clean"].nunique().reset_index()
mask = data2["extra_clean"] != 0
data2 = data2 [mask]

st.header("Nombre d'extras par mois")

fig = px.line(
    data2,
    x="mois",
    y="extra_clean",
    color="Année",
    text=data2["extra_clean"],
    labels={"extra_clean": "Nombre d'extras uniques", "mois": "Mois"},
    title=f"Nombre d'extras par mois",
    
)

fig.update_layout(xaxis_title="Mois", yaxis_title="Nombre d'extras uniques")
fig.update_traces(textposition="bottom center")


st.plotly_chart(fig, use_container_width=True)