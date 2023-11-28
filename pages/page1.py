import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np

st.set_page_config(
    page_title="Qualiextra",
    page_icon="🏝️",
    layout="wide"
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

        return data

data = load_data()

data["periode_fin"] = data["date_fin"].dt.strftime('%m-%Y')
data['Annee'] = data['date_fin'].dt.year.astype(str)
data['Mois'] = data['date_fin'].dt.to_period('M').astype(str)
data['Semaine'] = data['date_fin'].dt.to_period('W-Mon').astype(str)
data["marge"] = data.apply(lambda x: x["total HT"] - x["montant HT"], axis=1)

st.title('Analyse des performances')

# Sélection de la période
period = st.radio("Sélectionnez la période", options=['Année', 'Mois', 'Semaine'])

# Création du graphique à barres empilées avec Plotly Express
fig = px.bar(data.groupby(period)['marge'].sum().reset_index(), x=period, y='marge', 
             labels={'Marge': 'Marge'}, title=f'Évolution de la marge par {period}')

# Mise en forme du graphique
fig.update_xaxes(type='category', categoryorder='total ascending')
fig.update_yaxes(title_text='Marge')

# Affichage du graphique avec Streamlit
st.plotly_chart(fig)