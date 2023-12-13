import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path
import datetime

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
    aujd = datetime.datetime.now()
    mois_auj = aujd.strftime("%Y-%m")
    premier_jour_du_mois = aujd.replace(day=1).strftime("%Y-%m-%d")
    mois_précédent = aujd.replace(month=aujd.month - 1).strftime("%Y-%m")
    data = data[data["statuts"] != "annulé"]

    st.header("Classement des extras sur la totalité de la période")
    st.markdown("---")

    ##Main
    col1, col2 = st.columns(2)

    ca_missions = col1.radio(
        "Classement", ["Chiffre d'affaires", "Nombre de Missions"], horizontal=True
    )
    top = col1.text_input("Nombre de rangs à afficher", 5)
    timeframe = col2.radio("Granularité", ["Année", "Mois", "Semaine"], horizontal=True)
    option = col2.selectbox("Période", (data[timeframe].unique()))

    df = data[data[timeframe] == option]

    if ca_missions == "Nombre de Missions":
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
            .reset_index()[["extra_clean", "montant HT"]]
        )
        df.index = np.arange(1, len(df) + 1)
        df.index = df.index.rename("Rang")
        df.columns = ["Extra", "Chiffre d'affaires (€)"]

    st.dataframe(df.iloc[0 : int(top), :], use_container_width=True)

    # Création du graphique représentant le nb d'extra uniques par mois au cours des années
    st.header("Nombre d'extras uniques par mois")
    st.markdown("---")

    data_grouby_extra = (
        data.groupby(["mois", "Mois", "Année"])["extra_clean"].nunique().reset_index()
    )
    mask = data_grouby_extra["extra_clean"] != 0
    data_grouby_extra = data_grouby_extra[mask]
    annees = data_grouby_extra["Année"].unique()

    couleur_dict = {}
    for i, annee in enumerate(annees):
        couleur = px.colors.qualitative.Set1[i]
        couleur_dict.update({annee: couleur})

    mask = data_grouby_extra["Mois"] <= mois_précédent
    annees_prec = data_grouby_extra[mask]["Année"].unique()
    couleurs_annees_prec = [
        couleur_dict.get(annee, "valeur_par_défaut") for annee in annees_prec
    ]

    fig = px.line(
        data_grouby_extra[mask],
        x="mois",
        y="extra_clean",
        text=data_grouby_extra[mask]["extra_clean"],
        color="Année",
        labels={"extra_clean": "Nombre d'extras uniques", "mois": "Mois"},
        title="Évolution du nombre d'extras uniques par mois",
        color_discrete_sequence=couleurs_annees_prec,
    )

    fig.update_layout(
        legend=dict(traceorder="reversed"),
    )

    for i, annee in enumerate(annees):
        mask = (data_grouby_extra["Mois"] >= mois_précédent) & (
            data_grouby_extra["Année"] == annee
        )
        color = couleur_dict[annee]
        fig.add_trace(
            go.Scatter(
                name=f"En cours pour {annee}",
                x=data_grouby_extra[mask]["mois"],
                y=data_grouby_extra[mask]["extra_clean"],
                mode="lines+markers+text",
                line=dict(color=color, width=2, dash="dash"),
                text=data_grouby_extra[mask]["extra_clean"],
                textposition="top center",
            )
        )

    fig.update_traces(textposition="bottom center")
    fig.update_xaxes(type="category")
    fig.update_yaxes(title_text="Nombre d'extras uniques")

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Merci de bien vouloir charger des données !")
