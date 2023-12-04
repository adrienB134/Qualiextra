import streamlit as st
import pandas as pd
import plotly.express as px
from neuralforecast import NeuralForecast
from datetime import datetime
from neuralforecast.models import NBEATS, NHITS, TimesNet
from pathlib import Path


my_file = Path("missions_processed.csv")
if my_file.is_file():

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

    data = pd.read_csv("missions_processed.csv")
    data["date_debut"] = pd.to_datetime(data["date_debut"])
    data["date_fin"] = pd.to_datetime(data["date_fin"])

    st.title(" 📈 Prédiction du nombre d'extras pour les prochain mois")
    plot_df = forecasting(data)

    plot = px.line(plot_df, height=600)

    st.plotly_chart(plot, use_container_width=True)
else:
    st.warning("Merci de bien vouloir charger des données !")
