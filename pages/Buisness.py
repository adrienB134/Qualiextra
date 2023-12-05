import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import datetime
import calendar
from pathlib import Path
import locale

def format_currency(value):
    return f"{value:,} €"


st.set_page_config(page_title="Qualiextra", page_icon="💸", layout="wide")

my_file = Path("missions_processed.csv")
if my_file.is_file():
    locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
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

    # Création des variables necessaires pour affficher les métrics
    aujd = datetime.datetime.now()
    mois_auj = aujd.strftime("%Y-%m")
    premier_jour_du_mois =  aujd.replace(day=1).strftime("%Y-%m-%d")
    mois_précédent = (
        aujd.now()
        .replace(month=aujd.month - 1)
        .strftime("%Y-%m")
    )
    mois_auj_clean = aujd.strftime("%B %Y") #utile pour un affiche en format nom du mois année
    mois_année_précédente = (
        aujd
        .replace(year=aujd.year - 1)
        .strftime("%Y-%m")
    )
    mois_année_précédente_clean = ( #utile pour un affiche en format nom du mois année
        aujd
        .replace(year=aujd.year - 1)
        .strftime("%B %Y")
    )

    #calcul du CA et de la marge en comparaison avec l'année précédente à la même période
    ca_auj = sum(data[data["Mois"] == mois_auj]["total HT"])
    ca_année_précédente = sum(data[data["Mois"] == mois_année_précédente]["total HT"])

    marge_auj = sum(data[data["Mois"] == mois_auj]["marge"])
    marge_année_précédente = sum(data[data["Mois"] == mois_année_précédente]["marge"])


    #Mise en place du calcul du flus de trésorerie 
    mask = (data['Jour']<=  aujd.strftime("%Y-%m-%d")) & (data['Jour']>= premier_jour_du_mois)
    data_month_to_date  = data[mask]

    st.header("Analyse du chiffre d'affaires")

    # Affichage des métrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        f"Trésorerie décaissée au {aujd.strftime('%d-%m-%Y')}",
        f"{sum(data_month_to_date['montant HT']): ,} €"

    )
    col2.metric(
        f"CA à fin {mois_auj_clean}",
        f"{ca_auj: ,} €",
        f"{round(((ca_auj/ca_année_précédente)*100),0)}% de {mois_année_précédente_clean}",
    )
    col3.metric(
        f"Marge à fin {mois_auj_clean}",
        f"{marge_auj: ,} €",
        f"{round(((marge_auj/marge_année_précédente)*100),0)}% de {mois_année_précédente_clean}",
    )
    col4.metric(
        f"CA signé à {max(data['date_fin']).strftime('%B %Y')}",
        f"{sum(data[data['Jour']>aujd.strftime('%Y-%m-%d')]['total HT']): ,} €",

    )

    # Création du graphique en ligne pour chaque année
    data_grouby_CA = data.groupby(["mois", "Mois", "Année"])["total HT"].sum().reset_index()
    mask = data_grouby_CA["total HT"] != 0
    data_grouby_CA = data_grouby_CA[mask]
    annees = data_grouby_CA["Année"].unique()


    couleur_dict={}
    for i, annee in enumerate(annees):    
        couleur = px.colors.qualitative.Set1[i]
        couleur_dict.update({annee:couleur})


    mask = data_grouby_CA["Mois"] <= mois_précédent
    annees_prec = data_grouby_CA[mask]["Année"].unique()
    couleurs_annees_prec = [couleur_dict.get(annee, "valeur_par_défaut") for annee in annees_prec]

    fig = px.line(
        data_grouby_CA[mask],
        x="mois",
        y="total HT",
        text = data_grouby_CA[mask]["total HT"].map(format_currency),
        color="Année",  
        labels={"total HT": "CA", "mois": "Mois"},
        title="Évolution du chiffre d'affaires par mois",
        color_discrete_sequence=couleurs_annees_prec,
    )

    fig.update_layout(
        legend=dict(traceorder='reversed'),
    )


    for i, annee in enumerate(annees):
        mask = (data_grouby_CA["Mois"] >= mois_précédent) & (data_grouby_CA["Année"] == annee)
        color = couleur_dict[annee]
        fig.add_trace(
            go.Scatter(name = f"En cours pour {annee}",
                x=data_grouby_CA[mask]["mois"],
                y=data_grouby_CA[mask]["total HT"],
                mode="lines+markers+text",
                line=dict(color=color, width=2, dash="dash"),
                text=data_grouby_CA[mask]["total HT"].map(format_currency),
                textposition="top center",
            )
        )


    fig.update_traces(textposition="bottom center")
    fig.update_xaxes(type="category")
    fig.update_yaxes(title_text="CA en k€")


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
                == aujd
                .replace(year=aujd.year - 1)
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
                    > aujd
                    .replace(month=aujd.month - 6)
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
                (data["Année"].astype(str) >= aujd.strftime("%Y"))
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
