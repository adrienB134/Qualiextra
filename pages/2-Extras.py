import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Extras", page_icon="🧑", layout="wide")
my_file = Path("missions_processed.csv")
if my_file.is_file():
    data = pd.read_csv("missions_processed.csv")
    data["date_debut"] = pd.to_datetime(data["date_debut"])
    data["date_fin"] = pd.to_datetime(data["date_fin"])
    data["mois"] = data["date_fin"].dt.strftime("%B")
    data["mois"] = pd.Categorical(
        data["mois"],
        categories=[
            "janvier",
            "février",
            "mars",
            "avril",
            "mai",
            "juin",
            "juillet",
            "août",
            "septembre",
            "octobre",
            "novembre",
            "décembre",
        ],
        ordered=True,
    )

    data = data[data["statuts"] != "annulé"]

    st.header("Classements des extras sur la totalité de la période")

    ##Main
    col1, col2 = st.columns(2)

    ca_missions = col1.radio(
        "Classement", ["Chiffre d'affaires", "Nombre de Missions"], horizontal=True
    )
    top = col1.text_input("Nombre de rangs a afficher", 5)
    timeframe = col2.radio("Granularité", ["Année", "Mois", "Semaine"], horizontal=True)
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

    data2 = data.groupby(["mois", "Année"])["extra_clean"].nunique().reset_index()
    mask = data2["extra_clean"] != 0
    data2 = data2[mask]

    st.header("Nombre d'extras uniques par mois")

    fig = px.line(
        data2,
        x="mois",
        y="extra_clean",
        color="Année",
        text=data2["extra_clean"],
        labels={"extra_clean": "Nombre d'extras uniques", "mois": "Mois"},
        title=f"Nombre d'extras uniques par mois",
    )

    fig.update_layout(xaxis_title="Mois", yaxis_title="Nombre d'extras uniques")
    fig.update_traces(textposition="bottom center")

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Merci de bien vouloir charger des données !")
