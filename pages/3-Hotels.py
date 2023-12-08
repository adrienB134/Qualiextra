import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import locale
from pathlib import Path

# Config
st.set_page_config(page_title="Hôtels", page_icon="🏨", layout="wide")

my_file = Path("missions_processed.csv")
if my_file.is_file():
    # Load data
    locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
    data = pd.read_csv("missions_processed.csv")
    data["date_debut"] = pd.to_datetime(data["date_debut"])
    data["periode_debut"] = data["date_debut"].dt.strftime("%b-%Y")
    data["date_fin"] = pd.to_datetime(data["date_fin"])
    data["statuts"] = data["statuts"].replace("annulé", "annulée")
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

    # Body
    st.header("Classement des hôtels sur la totalité de la période")
    st.markdown("---")

    top = st.text_input("Nombre d'hôtels à afficher", 5)

    ca_missions = st.radio(
        "Classement", ["Nombre de missions", "Chiffre d'affaires"], horizontal=True
    )

    if ca_missions == "Nombre de missions":
        df = (
            data.groupby("Propriété")
            .count()
            .sort_values(by="hôtel", ascending=False)
            .reset_index()[["Propriété", "hôtel"]]
        )

        df.index = np.arange(1, len(df) + 1)
        df.index = df.index.rename("Rang")
        df.columns = ["Hôtels", "Missions (nb)"]
        st.dataframe(df.iloc[0 : int(top), :], use_container_width=True)

        st.header("Evolution du nombre de missions par hôtel et par an")
        st.markdown("---")

        years = st.selectbox(
            "Année", data["date_debut"].dt.year.astype(str).unique(), index=1, key=1
        )

        by_year = data.loc[
            data["date_debut"].dt.year.astype(str) == years,
            ["Propriété", "mois"],
        ]

        by_year["count"] = 1

        by_year = by_year.pivot_table(
            index="mois",
            values="count",
            columns=["Propriété"],
            aggfunc="count",
            fill_value=0,
        )

        top_hotels = (
            by_year.sum().sort_values(ascending=False)[: int(top)].index.to_list()
        )

        top_by_year = by_year.loc[:, top_hotels]
        top_by_year = pd.melt(
            top_by_year.reset_index(), id_vars="mois", value_name="Missions"
        )

        fig = px.line(
            top_by_year, x="mois", y="Missions", color="Propriété", markers=True
        )
        fig.update_traces(hovertemplate=None)
        fig.update_layout(hovermode="x unified")
        fig.update_xaxes(title_text="Temps")
        fig.update_yaxes(title_text="Nombre de missions")

        st.plotly_chart(fig, use_container_width=True)

        st.header("Nombre de missions et leur statut par hôtel sur une période")

        st.markdown("---")

        year = st.selectbox(
            "Choisissez une année",
            data["date_debut"].dt.strftime("%Y").unique(),
            index=1,
        )

        month = st.selectbox(
            "Choisissez un mois",
            [
                "Tous mois confondus",
                *data.loc[data["date_debut"].dt.year.astype(str) == year, "date_debut"]
                .dt.strftime("%b")
                .unique(),
            ],
            index=0,
        )

        if month != "Tous mois confondus":
            date = month + "-" + year
            monthly_missions_status = (
                data[(data["periode_debut"] == date)]
                .groupby(["Propriété", "statuts"])
                .count()
                .reset_index()
                .sort_values(by="Propriété", ascending=False)
                .iloc[:, :3]
            )

        else:
            monthly_missions_status = (
                data[(data["date_debut"].dt.year.astype(str) == year)]
                .groupby(["Propriété", "statuts"])
                .count()
                .reset_index()
                .sort_values(by="Propriété", ascending=False)
                .iloc[:, :3]
            )

        monthly_missions_status.columns = ["Propriété", "Statut", "Missions"]
        sorter = (
            monthly_missions_status.groupby("Propriété")
            .sum()
            .sort_values(by="Missions", ascending=False)
            .index
        )
        sorter = sorter.to_list()

        monthly_missions_status["Propriété_cat"] = pd.Categorical(
            monthly_missions_status["Propriété"], categories=sorter, ordered=True
        )

        monthly_missions_status = monthly_missions_status.sort_values(
            by="Propriété_cat"
        )

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=monthly_missions_status[
                    monthly_missions_status["Statut"] == "standard"
                ]["Propriété"],
                y=monthly_missions_status[
                    monthly_missions_status["Statut"] == "standard"
                ]["Missions"],
                name="Standard",
            )
        )

        fig.add_trace(
            go.Bar(
                x=monthly_missions_status[
                    monthly_missions_status["Statut"] == "urgente"
                ]["Propriété"],
                y=monthly_missions_status[
                    monthly_missions_status["Statut"] == "urgente"
                ]["Missions"],
                name="Urgente",
            )
        )

        fig.add_trace(
            go.Bar(
                x=monthly_missions_status[
                    monthly_missions_status["Statut"] == "annulée"
                ]["Propriété"],
                y=monthly_missions_status[
                    monthly_missions_status["Statut"] == "annulée"
                ]["Missions"],
                name="Annulée",
            )
        )
        fig.update_layout(barmode="stack")

        fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))

        fig.update_xaxes(title_text="Hôtels")
        fig.update_yaxes(title_text="Nombre de missions")

        st.plotly_chart(fig, use_container_width=True)

    else:
        df = (
            data.groupby("Propriété")
            .sum(numeric_only=True)
            .sort_values(by="total HT", ascending=False)
            .reset_index()[["Propriété", "total HT"]]
        )
        df.index = np.arange(1, len(df) + 1)
        df.index = df.index.rename("Rang")
        df.columns = ["Hôtels", "Chiffre d'affaires (€)"]
        st.dataframe(df.iloc[0 : int(top), :], use_container_width=True)

        st.header("Evolution du CA par hôtel et par an")
        st.markdown("---")

        years = st.selectbox(
            "Année", data["date_debut"].dt.year.astype(str).unique(), index=1, key=2
        )

        by_year = data.loc[
            data["date_debut"].dt.year.astype(str) == years,
            ["Propriété", "mois", "total HT"],
        ]
        by_year = by_year.pivot_table(
            index="mois",
            values="total HT",
            columns=["Propriété"],
            aggfunc="sum",
            fill_value=0,
        )

        top_hotels = (
            by_year.sum().sort_values(ascending=False)[: int(top)].index.to_list()
        )

        top_by_year = by_year.loc[:, top_hotels]
        top_by_year = pd.melt(
            top_by_year.reset_index(), id_vars="mois", value_name="CA"
        )

        fig = px.line(top_by_year, x="mois", y="CA", color="Propriété", markers=True)
        fig.update_traces(hovertemplate=None)
        fig.update_layout(hovermode="x unified")
        fig.update_xaxes(title_text="Temps")
        fig.update_yaxes(title_text="Chiffre d'affaires")

        st.plotly_chart(fig, use_container_width=True)

        st.header("Marge par hôtel sur une période")
        st.markdown("---")

        year = st.selectbox(
            "Choisissez une année",
            data["date_debut"].dt.strftime("%Y").unique(),
            index=1,
        )

        month = st.selectbox(
            "Choisissez un mois",
            [
                "Tous mois confondus",
                *data.loc[data["date_debut"].dt.year.astype(str) == year, "date_debut"]
                .dt.strftime("%b")
                .unique(),
            ],
            index=0,
        )

        if month != "Tous mois confondus":
            date = month + "-" + year
            marge_df = (
                data.loc[
                    data["periode_debut"] == date, ["Propriété", "total HT", "marge"]
                ]
                .groupby("Propriété")
                .mean()
            )

        else:
            marge_df = (
                data.loc[
                    data["date_debut"].dt.year.astype(str) == year,
                    ["Propriété", "total HT", "marge"],
                ]
                .groupby("Propriété")
                .mean()
            )

        marge_df["pourcent"] = marge_df.apply(
            lambda x: round(x["marge"] / x["total HT"] * 100, 1), axis=1
        )
        marge_df = marge_df.reset_index().sort_values(by="pourcent", ascending=False)

        fig = px.bar(
            marge_df,
            x="Propriété",
            y="pourcent",
            text=[str(x) + "%" for x in marge_df["pourcent"]],
        )

        fig.update_xaxes(title_text="Hôtels")
        fig.update_yaxes(title_text="Marge en % de CA")
        fig.update_traces(textposition="outside")
        fig.update_layout(yaxis_range=[0, max(marge_df["pourcent"]) + 10])

        st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Merci de bien vouloir charger des données !")
