import streamlit as st
import pandas as pd
from geopy.geocoders import BANFrance
import plotly.express as px
from pathlib import Path
import utils.preprocess as preprocess
import datetime

@st.cache_data
def load_csv(file, sep=","):
    return pd.read_csv(file, sep=sep)


def geolocation(data, hotel_data):
    info = hotel_data
    info["Adresse"] = (
        info["adresse"] + " " + info["code"].astype("str") + " " + info["ville"]
    )
    hotel = pd.DataFrame(data["Propriété"].unique(), columns=["nom"])
    hotel = pd.merge(hotel, info[["nom", "Adresse"]], on="nom", how="outer")

    hotel["Adresse"] = hotel["Adresse"].fillna("Paris")
    geolocator = BANFrance()
    hotel["location"] = hotel["Adresse"].apply(geolocator.geocode)
    hotel["latitude"] = hotel["location"].apply(
        lambda loc: tuple(loc.point)[0] if loc else None
    )
    hotel["longitude"] = hotel["location"].apply(
        lambda loc: tuple(loc.point)[1] if loc else None
    )
    hotel = pd.merge(
        hotel,
        data.groupby("Propriété")["extra_clean"].count().to_frame(),
        left_on="nom",
        right_on="Propriété",
    )
    hotel = hotel.rename(columns={"extra_clean": "Nombre de missions"})
    return hotel


if __name__ == "__main__":
    st.set_page_config(
        page_title="Qualiextra",
        page_icon="👋",
        layout="wide",
    )

    upload = st.file_uploader("Déposer votre csv issu de notion")
    my_file = Path("./missions_processed.csv")

    if upload != None:
        preprocess.load_data(upload)

    if my_file.is_file():
        data = load_csv("./missions_processed.csv")
        hôtel_upload = st.file_uploader(
            "Vous pouvez actualiser la carte en déposant \
                un nouveau csv avec les adresses des hôtels"
        )
        hotel_file = Path("./hotels.csv")

        if hôtel_upload != None:
            with open("./hotels.csv", "wb") as file:
                file.write(hôtel_upload.read())

        if hotel_file.is_file():
            hotel_data = load_csv("./hotels.csv", sep=";")
            hotel = geolocation(data, hotel_data)
            st.empty()
            st.write("# Welcome to Qualiextra! 👋")
            st.markdown("---")

            col1, col2, col3 = st.columns(3)
            # Création des variables necessaires pour affficher les métrics
            aujd = datetime.datetime.now()
            mois_précédent = aujd.replace(month=aujd.month - 1).strftime("%Y-%m")
            mois_précédent_clean = aujd.replace(month=aujd.month - 1).strftime("%B %Y")  
            mois_année_précédente = (aujd.replace(month=aujd.month - 1)
                                     .replace(year=aujd.year - 1).strftime("%Y-%m"))
            mois_année_précédente_clean = (aujd.replace(month=aujd.month - 1)
                                     .replace(year=aujd.year - 1).strftime("%B %Y"))
            data_mois_prec = data[data["Mois"]== mois_précédent] 

            col1.metric(
                f"🏨 Hôtel du mois ({mois_précédent_clean})",
                f"{data_mois_prec.groupby('Propriété')['total HT'].sum().idxmax()}",
                )
            col1.markdown(f"<div style='margin-top: -18px; color: green;'> Pour un CA total de {max(data_mois_prec.groupby(['Propriété'])['total HT'].sum()): ,} € </div>", unsafe_allow_html=True)

            col2.metric(
                f"🧑 Extra du mois ({mois_précédent_clean})",
                f"{data_mois_prec.groupby('extra_clean')['total HT'].sum().idxmax()}"
                )
            col2.markdown(f"<div style='margin-top: -18px; color: green;'> Pour un CA total de {max(data_mois_prec.groupby('extra_clean')['total HT'].sum()): ,} € </div>", unsafe_allow_html=True)

            ca_mois_précédent = sum(data[data["Mois"] == mois_précédent]["total HT"])
            ca_année_précédente = sum(data[data["Mois"] == mois_année_précédente]["total HT"])
            col3.metric(
                f"💸 CA à fin {mois_précédent_clean}",
                f"{ca_mois_précédent: ,} €",
            )
            col3.markdown(f"<div style='margin-top: -18px; color: green;'> + {round(((ca_mois_précédent/ca_année_précédente)*100),0)}% vs. {mois_année_précédente_clean} </div>", unsafe_allow_html=True)

            fig = px.scatter_mapbox(
                hotel,
                lat="latitude",
                lon="longitude",
                mapbox_style="carto-positron",
                zoom=11,
                hover_name="nom",
                hover_data=["Adresse"],
                height=800,
                size="Nombre de missions",
            )

            st.plotly_chart(fig, use_container_width=True)
