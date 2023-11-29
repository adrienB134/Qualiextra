import streamlit as st
import pandas as pd

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
        data["date_debut"] = data.apply(lambda x: x["date"].split(" →")[0], axis=1)
        data["date_debut"] = data["date_debut"].apply(
            lambda x: x.replace(" (UTC+3)", "")
        )
        data["date_debut"] = data["date_debut"].apply(lambda x: x.replace(" (UTC)", ""))
        data["date_debut"] = pd.to_datetime(data["date_debut"], format="%d/%m/%Y %H:%M")
        data["time_delta"] = data["nbre d'heures"].apply(lambda x: pd.to_timedelta(x))
        data["date_fin"] = data.apply(
            lambda x: x["date_debut"] + x["time_delta"], axis=1
        )
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
        return data

    st.session_state.data = load_data()

    st.write("# Welcome to Qualiextra! 👋")
