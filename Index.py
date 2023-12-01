import streamlit as st
import pandas as pd
from geopy.geocoders import BANFrance
import plotly.express as px

if __name__ == "__main__":
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    @st.cache_data
    def load_data():
        data = pd.read_csv("./Missions.csv", sep=";")
        mask = data["hôtel"].notna()
        data = data[mask]
        data["Propriété"] = data.apply(
            lambda x: x["hôtel"].split(" (")[0] if "www" in x["Propriété"] else x,
            axis=1,
        )["Propriété"]
        data["Propriété_clean"] = data["hôtel"].apply(lambda x: x.split(" (")[0])

        return data


def geolocation(data):
    info = pd.read_csv("./hotels.csv", sep=";")
    info["Adresse"] = (
        info["adresse"] + " " + info["code"].astype("str") + " " + info["ville"]
    )
    hotel = pd.DataFrame(data["Propriété_clean"].unique(), columns=["nom"])
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
    # hotel["total_extras"] = (
    #     data.groupby("Propriété_clean")["extra_clean"].unique().apply(lambda x: len(x))
    # )
    return hotel


data = load_data()

hotel = geolocation(data)
st.write("# Welcome to Qualiextra! 👋")

fig = px.scatter_mapbox(
    hotel,
    lat="latitude",
    lon="longitude",
    mapbox_style="carto-positron",
    zoom=10,
    hover_name="nom",
    hover_data=["Adresse"],
    # size=data["hôtel"].value_counts(),
)

fig.update_layout(mapbox=dict())

st.plotly_chart(fig)
