import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import datetime
import calendar
from pathlib import Path


st.set_page_config(page_title="Qualiextra", page_icon="💸", layout="wide")

my_file = Path("missions_processed.csv")
if my_file.is_file():
    data = pd.read_csv("missions_processed.csv")
    data["date_debut"] = pd.to_datetime(data["date_debut"])
    data["date_fin"] = pd.to_datetime(data["date_fin"])
    data["mois"] = data["date_fin"].dt.strftime("%B")
    data["mois"] = pd.Categorical(
        data["mois"],
        categories=[
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
        ordered=True,
    )

    data = data[data["statuts"] != "annulé"]

    def format_currency(value):
        return f"{value:,} €"

    # Création des variables de mois
    mois_auj = datetime.datetime.now().strftime("%Y-%m")
    mois_auj_clean = datetime.datetime.now().strftime("%B %Y")
    mois_année_précédente = (
        datetime.datetime.now()
        .replace(year=datetime.datetime.now().year - 1)
        .strftime("%Y-%m")
    )
    mois_année_précédente_clean = (
        datetime.datetime.now()
        .replace(year=datetime.datetime.now().year - 1)
        .strftime("%B %Y")
    )
    ca_auj = sum(data[data["Mois"] == mois_auj]["total HT"])
    ca_année_précédente = sum(data[data["Mois"] == mois_année_précédente]["total HT"])
    marge_auj = sum(data[data["Mois"] == mois_auj]["marge"])
    marge_année_précédente = sum(data[data["Mois"] == mois_année_précédente]["marge"])

    st.header("Analyse du chiffre d'affaires")

    col1, col2, col3 = st.columns(3)
    col1.metric(
        f"Chiffre d'affaires prévisionnel à fin {mois_auj_clean}",
        f"{ca_auj: ,} €",
        f"{round(((ca_auj/ca_année_précédente-1)*100),2)}% par rapport à {mois_année_précédente_clean}",
    )
    col2.metric(
        f"Marge prévisionnelle à fin {mois_auj_clean}",
        f"{marge_auj: ,} €",
        f"{round(((marge_auj/marge_année_précédente-1)*100),2)}% par rapport à {mois_année_précédente_clean}",
    )
    col3.metric(
        "Pipeline de Chiffre d'affaires",
        f"{sum(data[data['Mois']>mois_auj]['total HT']): ,} €",
        f"Jusqu'à {max(data['date_fin']).strftime('%B %Y')}",
    )

    # Création du graphique en ligne pour chaque année
    data2 = data.groupby(["mois", "Année"])["total HT"].sum().reset_index()
    mask = data2["total HT"] != 0
    data2 = data2[mask]

    fig = px.line(
        data2,
        x="mois",
        y="total HT",
        color="Année",
        text=data2["total HT"].map(format_currency),
        labels={"total HT": "CA", "mois": "Mois"},
        title=f"Évolution du chiffre d'affaires par mois",
    )

    # Mise en forme du graphique
    fig.update_traces(textposition="bottom center")
    fig.update_xaxes(type="category")
    fig.update_yaxes(title_text="Marge en k€")

    st.plotly_chart(fig, use_container_width=True)

    # Création d'un graphique pour le chiffre d'affaires et la marge selon une période indiquée

    st.header("Analyse du chiffre d'affaires et de la marge par période")

    periode = st.selectbox(
        "Sélectionnez la période",
        options=["Previsionnel", "M", "YTD", "6M", "N-1", "Tout"],
        index=2,
    )
    granularité = st.selectbox(
        "Sélectionnez la granularité",
        options=["Année", "Mois", "Semaine", "Jour"],
        index=1,
    )
    marge_ou_ca_clean = st.radio("", options=["CA", "Marge"], horizontal=True, index=0)

    if marge_ou_ca_clean == "CA":
        marge_ou_ca = "total HT"
    else:
        marge_ou_ca = "marge"

    col1, col2 = st.columns(2)
    with col1:
        if periode == "Tout":
            data_filtre = data.groupby([granularité])[marge_ou_ca].sum().reset_index()
            fig = px.line(
                data_filtre,
                x=granularité,
                y=marge_ou_ca,
                text=data_filtre[marge_ou_ca].map(format_currency),
                labels={marge_ou_ca: marge_ou_ca_clean},
                title=f"Évolution du {marge_ou_ca_clean} - {periode}",
            )
        elif periode == "N-1":
            data = data[
                data["Année"]
                == datetime.datetime.now()
                .replace(year=datetime.datetime.now().year - 1)
                .strftime("%Y")
            ]
            data_filtre = data.groupby([granularité])[marge_ou_ca].sum().reset_index()
            fig = px.line(
                data_filtre,
                x=granularité,
                y=marge_ou_ca,
                text=data_filtre[marge_ou_ca].map(format_currency),
                labels={marge_ou_ca: marge_ou_ca_clean},
                title=f"Évolution du {marge_ou_ca_clean} - {periode}",
            )

        elif periode == "6M":
            data = data[
                (data["Mois"] <= mois_auj)
                & (
                    data["Mois"]
                    > datetime.datetime.now()
                    .replace(month=datetime.datetime.now().month - 6)
                    .strftime("%Y-%m")
                )
            ]
            data_filtre = data.groupby([granularité])[marge_ou_ca].sum().reset_index()
            fig = px.line(
                data_filtre,
                x=granularité,
                y=marge_ou_ca,
                text=data_filtre[marge_ou_ca].map(format_currency),
                labels={marge_ou_ca: marge_ou_ca_clean},
                title=f"Évolution du {marge_ou_ca_clean} - {periode}",
            )

        elif periode == "YTD":
            data = data[
                (data["Année"].astype(str) >= datetime.datetime.now().strftime("%Y"))
                & (data["Mois"] <= mois_auj)
            ]
            data_filtre = data.groupby([granularité])[marge_ou_ca].sum().reset_index()
            fig = px.line(
                data_filtre,
                x=granularité,
                y=marge_ou_ca,
                text=data_filtre[marge_ou_ca].map(format_currency),
                labels={marge_ou_ca: marge_ou_ca_clean},
                title=f"Évolution du {marge_ou_ca_clean} - {periode}",
            )

        elif periode == "M":
            data = data[data["Mois"] == mois_auj]
            data_filtre = data.groupby([granularité])[marge_ou_ca].sum().reset_index()
            fig = px.line(
                data_filtre,
                x=granularité,
                y=marge_ou_ca,
                text=data_filtre[marge_ou_ca].map(format_currency),
                labels={marge_ou_ca: marge_ou_ca_clean},
                title=f"Évolution du {marge_ou_ca_clean} - {periode}",
            )

        elif periode == "Previsionnel":
            data = data[data["Mois"] >= mois_auj]
            data_filtre = data.groupby([granularité])[marge_ou_ca].sum().reset_index()
            fig = px.line(
                data_filtre,
                x=granularité,
                y=marge_ou_ca,
                text=data_filtre[marge_ou_ca].map(format_currency),
                labels={marge_ou_ca: marge_ou_ca_clean},
                title=f"Évolution du {marge_ou_ca_clean} - {periode}",
            )

        # Mise en forme du graphique
        fig.update_xaxes(type="category", tickformat="%b-%Y")
        fig.update_yaxes(title_text=marge_ou_ca_clean)
        fig.update_traces(textposition="top center")

        # Affichage du graphique avec Streamlit
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Création du graphique à barres empilées avec Plotly Express
        data = data.groupby(granularité)[["marge", "montant HT"]].sum().reset_index()
        data["Marge_sur_CA"] = data.apply(
            lambda x: x["marge"] * 100 / (x["montant HT"] + x["marge"]), axis=1
        )
        data["Couts_sur_CA"] = data.apply(
            lambda x: x["montant HT"] * 100 / (x["montant HT"] + x["marge"]), axis=1
        )

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=data[granularité],
                y=data["marge"],
                text=data["Marge_sur_CA"].apply(lambda x: "{0:1.2f}%".format(x)),
                name="Marge",
            )
        )
        fig.add_trace(
            go.Bar(
                x=data[granularité],
                y=data["montant HT"],
                text=data["Couts_sur_CA"].apply(lambda x: "{0:1.2f}%".format(x)),
                name="Rémunération Extra",
            )
        )

        # Mise en forme du graphique
        fig.update_layout(
            barmode="relative",
            title_text="Relative Barmode",
            title=f"Évolution de la répartition du CA - {periode}",
            legend=dict(x=0.5, y=1.1, orientation="h"),
        )
        fig.update_xaxes(type="category", title_text=f"{granularité}")
        fig.update_yaxes(title_text="CA en k€")
        fig.update_traces(textposition="auto")

        st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Merci de bien vouloir charger des données !")
