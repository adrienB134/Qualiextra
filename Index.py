import streamlit as st
import pandas as pd
from geopy.geocoders import BANFrance
import plotly.express as px


if __name__ == "__main__":
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
        layout="wide",
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

        data["extra_clean"] = data["extra"].apply(lambda x: x.split(" (")[0])
        data["periode_debut"] = data["date_debut"].dt.strftime("%m-%Y")
        data["periode_fin"] = data["date_fin"].dt.strftime("%m-%Y")
        data["Année"] = data["date_fin"].dt.year.astype(str)
        data["Mois"] = data["date_fin"].dt.to_period("M").astype(str)
        data["Semaine"] = data["date_fin"].dt.to_period("W-Mon").astype(str)
        data["marge"] = data.apply(lambda x: x["total HT"] - x["montant HT"], axis=1)
        data["mois"] = data["date_fin"].dt.strftime("%B")
        data["mois"] = pd.Categorical(data["mois"], 
                                      categories=["January",
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
                                                    "December"], ordered=True)
    
        # data["Adresse"] = data["Propriété_clean"].apply(
        #     lambda x: hotel[hotel["nom"] == x]["Adresse"].iloc[0]
        # )
        # data["latitude"] = data["Propriété_clean"].apply(
        #     lambda x: hotel[hotel["nom"] == x]["latitude"].iloc[0]
        # )
        # data["longitude"] = data["Propriété_clean"].apply(
        #     lambda x: hotel[hotel["nom"] == x]["longitude"].iloc[0]
        # )
        data["Jour"] = data["date_fin"].dt.to_period("D").astype(str)

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
    hotel = pd.merge(
        hotel,
        data.groupby("Propriété_clean")["extra_clean"].count().to_frame(),
        left_on="nom",
        right_on="Propriété_clean",
    )
    hotel = hotel.rename(columns={"extra_clean": "Nombre de missions"})
    return hotel


data = load_data()

hotel = geolocation(data)
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

fig.update_layout(mapbox=dict())

st.plotly_chart(fig, use_container_width=True)
