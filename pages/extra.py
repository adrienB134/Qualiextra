import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px


data = st.session_state.data
data = data[data["statuts"] != "annulé"]

##sidebar
with st.sidebar:
    timeframe = st.radio("Timeframe", ["Année", "Mois", "Semaine"])
    ca_missions = st.radio("Classement", ["Chiffre d'affaire", "Missions"])

##computation
col1, col2 = st.columns(2)
top = col1.text_input("Nombre de rangs a afficher", 5)
option = col2.selectbox("Période", (data[timeframe].unique()))
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


fig = go.Figure(
    layout=go.Layout(title=go.layout.Title(text="Nombre d'extras par mois"))
)

for period in data["Année"].unique():
    fig.add_trace(
        go.Scatter(
            x=data[data["Année"] == period]["mois"].unique(),
            y=data[data["Année"] == period]
            .groupby("mois")["extra_clean"]
            .unique()
            .apply(lambda x: len(x)),
            name=f"{period}",
            text=data[data["Année"] == period]
            .groupby("mois")["extra_clean"]
            .unique()
            .apply(lambda x: len(x)),
        )
    )

fig2 = px.density_heatmap(data, x="extra_clean", y="Propriété_clean")
# fig.update_traces(dict(marker_line_width=0))

##main

st.plotly_chart(fig)
st.plotly_chart(fig2)
