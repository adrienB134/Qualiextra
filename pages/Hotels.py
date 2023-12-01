import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np


@st.cache_data
def load_data():
    data = pd.read_csv("./Missions.csv", sep=";")
    mask = data["hôtel"].notna()
    data = data[mask]
    data["date_debut"] = data.apply(lambda x: x["date"].split(" →")[0], axis=1)
    data["date_debut"] = data["date_debut"].apply(lambda x: x.replace(" (UTC+3)", ""))
    data["date_debut"] = data["date_debut"].apply(lambda x: x.replace(" (UTC)", ""))
    data["date_debut"] = pd.to_datetime(data["date_debut"], format="%d/%m/%Y %H:%M")
    data["time_delta"] = data["nbre d'heures"].apply(lambda x: pd.to_timedelta(x))
    data["date_fin"] = data.apply(lambda x: x["date_debut"] + x["time_delta"], axis=1)
    data["Propriété"] = data.apply(
        lambda x: x["hôtel"].split(" (")[0] if "www" in x["Propriété"] else x,
        axis=1,
    )["Propriété"]
    data["Propriété_clean"] = data["hôtel"].apply(lambda x: x.split(" (")[0])
    data["extra_clean"] = data["extra"].apply(lambda x: x.split(" (")[0])
    data["periode_debut"] = data["date_debut"].dt.strftime("%m-%Y")
    data["periode_fin"] = data["date_fin"].dt.strftime("%m-%Y")
    data["Année"] = data["date_fin"].dt.year.astype(str)
    data["Mois"] = data["date_fin"].dt.to_period("M").astype(str)
    data["Semaine"] = data["date_fin"].dt.to_period("W-Mon").astype(str)
    data["marge"] = data.apply(lambda x: x["total HT"] - x["montant HT"], axis=1)
    data["mois"] = data["date_fin"].dt.strftime("%m")
    data["Jour"] = data["date_fin"].dt.to_period("D").astype(str)
    data["statuts"] = data["statuts"].fillna("standard")

    return data


# Config
st.set_page_config(page_title="Qualiextra", page_icon="🏨", layout="wide")

# Load data
data = load_data()
data["statuts"] = data["statuts"].replace("annulé", "annulée")

# Body
st.header("Classements des hôtels sur la totalité de la période")
st.markdown("---")

top = st.text_input("Nombre d'hôtels a afficher", 5)

df = (
    data.groupby("Propriété_clean")
    .count()
    .sort_values(by="hôtel", ascending=False)
    .reset_index()[["Propriété_clean", "Propriété"]]
)

df.index = np.arange(1, len(df) + 1)
df.index = df.index.rename("Rang")
df.columns = ["Hôtels", "Missions (nb)"]
st.dataframe(df.iloc[0 : int(top), :], use_container_width=True)


st.header("Evolution du nombre de missions par hôtel et par an")
st.markdown("---")

years = st.selectbox("Année", data["date_debut"].dt.year.astype(str).unique(), index=1)

by_year = data.loc[
    data["date_debut"].dt.year.astype(str) == years,
    ["Propriété_clean", "periode_debut"],
]

by_year["count"] = 1

by_year = by_year.pivot_table(
    index="periode_debut",
    values="count",
    columns=["Propriété_clean"],
    aggfunc="count",
    fill_value=0,
)

top_hotels = by_year.sum().sort_values(ascending=False)[: int(top)].index.to_list()

top_by_year = by_year.loc[:, top_hotels]
top_by_year = pd.melt(
    top_by_year.reset_index(), id_vars="periode_debut", value_name="Missions"
)

fig = px.line(
    top_by_year, x="periode_debut", y="Missions", color="Propriété_clean", markers=True
)
fig.update_traces(hovertemplate=None)
fig.update_layout(hovermode="x unified")
fig.update_xaxes(title_text="Temps")
fig.update_yaxes(title_text="Nombre de missions")

st.plotly_chart(fig, use_container_width=True)


st.header("Nombre de missions et leur statut par hôtel sur une période")

st.markdown("---")


year = st.selectbox(
    "Choisissez une année", data["date_debut"].dt.strftime("%Y").unique(), index=1
)

month = st.selectbox(
    "Choisissez un mois",
    [
        "Tous mois confondus",
        *data.loc[data["date_debut"].dt.year.astype(str) == year, "date_debut"]
        .dt.strftime("%m")
        .unique(),
    ],
    index=0,
)

if month != "Tous mois confondus":
    date = month + "-" + year
    monthly_missions_status = (
        data[(data["periode_debut"] == date)]
        .groupby(["Propriété_clean", "statuts"])
        .count()
        .reset_index()
        .sort_values(by="Propriété", ascending=False)
        .iloc[:, :3]
    )

else:
    monthly_missions_status = (
        data[(data["date_debut"].dt.year.astype(str) == year)]
        .groupby(["Propriété_clean", "statuts"])
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

monthly_missions_status = monthly_missions_status.sort_values(by="Propriété_cat")

fig = px.bar(
    monthly_missions_status,
    x="Propriété",
    y="Missions",
    color="Statut",
    hover_name="Propriété",
    hover_data=["Missions", "Statut"],
)

fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))

fig.update_xaxes(title_text="Hôtels")
fig.update_yaxes(title_text="Nombre de missions")

st.plotly_chart(fig, use_container_width=True)
