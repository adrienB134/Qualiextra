import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px


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
    data["mois"] = data["date_fin"].dt.strftime("%B")
    data["Jour"] = data["date_fin"].dt.to_period("D").astype(str)
    data["statuts"] = data["statuts"].fillna("standard")
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

    return data


st.set_page_config(page_title="Qualiextra", page_icon="🧑", layout="wide")
data = load_data()

data = data[data["statuts"] != "annulé"]


st.header("Classements des extras sur la totalité de la période")

##Main
col1, col2 = st.columns(2)
ca_missions = col1.radio(
    "Classement", ["Chiffre d'affaires", "Nombre de missions"], horizontal=True
)
top = col1.text_input("Nombre de rangs a afficher", 5)
timeframe = col2.radio("Granularité", ["Année", "Mois", "Semaine"], horizontal=True)
option = col2.selectbox("Période", (data[timeframe].unique()))

df = data[data[timeframe] == option]

if ca_missions == "Nombre de missions":
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
    title=f"Nombre d'extras par mois",
)

fig.update_layout(xaxis_title="Mois", yaxis_title="Nombre d'extras uniques")
fig.update_traces(textposition="bottom center")


st.plotly_chart(fig, use_container_width=True)
