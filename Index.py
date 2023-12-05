import streamlit as st
import pandas as pd
from geopy.geocoders import BANFrance
import plotly.express as px
from pathlib import Path
import utils.preprocess as preprocess


def geolocation(data):
    info = pd.read_csv("./hotels.csv", sep=";")
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
        page_title="Hello",
        page_icon="👋",
        layout="wide",
    )

    upload = st.file_uploader("Déposer votre csv issu de notion")
    my_file = Path("./missions_processed.csv")

    if upload != None:
        preprocess.load_data(upload)
        st.session_state.data_geo = pd.read_csv("missions_processed.csv")

    if my_file.is_file():
        hotel = geolocation(st.session_state.data_geo)
        st.write("# Welcome to Qualiextra! 👋")

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

        hôtel_upload = st.file_uploader(
            "Vous pouver actualiser la carte en déposant un nouceau csv avec les adresses des hôtels"
        )
