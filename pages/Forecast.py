import streamlit as st
import pandas as pd
import plotly.express as px
from neuralforecast import NeuralForecast
from datetime import datetime
from neuralforecast.models import NBEATS, NHITS, TimesNet


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


@st.cache_data
def forecasting(data):
    # Preprocessing
    data["ds"] = pd.to_datetime(data["date_debut"], format="%d/%m/%Y").dt.date
    data_ts = data.groupby("ds")["extra_clean"].count().to_frame()
    data_ts = data_ts.rename(columns={"extra_clean": "y"})
    data_ts = data_ts.reset_index()
    data_ts["ds"] = data_ts["ds"].apply(lambda x: pd.Timestamp(x))
    data_ts["y"] = data_ts["y"].astype("int")
    split_date = pd.Timestamp(datetime.today())

    # training set
    Y_df = data_ts
    Y_df = Y_df[Y_df.ds <= split_date]
    Y_df["unique_id"] = 1.0

    # Load model
    nf = NeuralForecast.load("./models/")

    # Training
    nf.fit(df=Y_df)

    # Prediction
    Y_hat_df = nf.predict().reset_index()

    # Plotting
    plot_df = pd.concat([Y_df, Y_hat_df]).set_index("ds").drop("unique_id", axis=1)

    return plot_df


data = load_data()

st.title(" 📈 Prédiction du nombre d'extras pour les prochain mois")
plot_df = forecasting(data)

plot = px.line(plot_df, height=600)

st.plotly_chart(plot, use_container_width=True)
