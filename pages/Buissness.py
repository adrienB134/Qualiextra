import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import datetime
import calendar

st.set_page_config(page_title="Qualiextra", page_icon="🏝️", layout="wide")

data = st.session_state.data


#ajout au préprocessing existant
data = data[data["statuts"] != "annulé"]
data['Mois_WY'] = pd.DatetimeIndex(data['date_fin']).month
data ['Marge_sur_CA'] = data.apply(lambda x: x["marge"] - x["total HT"], axis=1)
data["Jour"] = data["date_fin"].dt.to_period("D").astype(str)
mois_auj = datetime.datetime.now().strftime("%Y-%m")
mois_année_précédente = datetime.datetime.now().replace(year=datetime.datetime.now().year - 1).strftime("%Y-%m")
ca_auj = sum(data[data['Mois']==mois_auj]['total HT'])
ca_année_précédente = sum(data[data['Mois']==mois_année_précédente]['total HT'])
marge_auj = sum(data[data['Mois']==mois_auj]['marge'])
marge_année_précédente = sum(data[data['Mois']==mois_année_précédente]['marge'])



st.title("Analyse chiffre d'affaires et de la marge Qualiextra")


col1, col2, col3 = st.columns(3)
col1.metric(f"Chiffre d'affaires prévisionnel à fin {datetime.datetime.now().strftime('%B %Y')}", f"{ca_auj: ,} €", f"{round(((ca_auj/ca_année_précédente-1)*100),2)}% par rapport à {datetime.datetime.now().replace(year=datetime.datetime.now().year - 1).strftime('%B %Y')}")
col2.metric(f"Marge prévisionnelle à fin {datetime.datetime.now().strftime('%B %Y')}", f"{marge_auj: ,} €", f"{round(((marge_auj/marge_année_précédente-1)*100),2)}% par rapport à {datetime.datetime.now().replace(year=datetime.datetime.now().year - 1).strftime('%B %Y')}")
col3.metric("Pipeline de Chiffre d'affaires", f"{sum(data[data['Mois']>mois_auj]['total HT']): ,} €", f"Jusqu'à {max(data['date_fin']).strftime('%B %Y')}")

# Création du graphique à barres empilées avec Plotly Express
    
fig = px.line(
        data.groupby(["Mois_WY", "Année"])["total HT"].sum().reset_index(),
        x="Mois_WY",
        y="total HT",
        color = "Année",
        text="total HT",
        labels={"total HT": "CA","Mois_WY":"Mois" },
        title=f"Évolution du chiffre d'affaires par mois",
    )

    # Mise en forme du graphique
fig.update_traces(textposition="bottom center")
fig.update_xaxes(type="category")
fig.update_yaxes(title_text="Marge")

st.plotly_chart(fig, use_container_width=True)


periode= st.selectbox("Sélectionnez la période", options=["Previsionnel", "M", "YTD", "6M", "N-1",  "Tout"],index=2)
granularité = st.selectbox("Sélectionnez la granularité", options=["Année", "Mois", "Semaine", "Jour"],index=1)
marge_ou_ca_clean = st.radio("",options=['CA', 'Marge'], horizontal=True, index=0)

if marge_ou_ca_clean == 'CA' :
    marge_ou_ca = 'total HT'
else:
    marge_ou_ca = 'marge'


col1, col2 = st.columns(2)
with col1:
    if periode == "Tout" : 
        fig = px.line(
            data.groupby([granularité])[marge_ou_ca].sum().reset_index(),
            x=granularité,
            y=marge_ou_ca,
            text=marge_ou_ca,
            labels={marge_ou_ca: marge_ou_ca_clean},
            title=f"Évolution du {marge_ou_ca_clean} - {periode}",
        )
    elif periode == "N-1" : 
        data = data[data["Année"] == datetime.datetime.now().replace(year=datetime.datetime.now().year - 1).strftime("%Y")]
        fig = px.line(
            data.groupby([granularité])[marge_ou_ca].sum().reset_index(),
            x=granularité,
            y=marge_ou_ca,
            text=marge_ou_ca,
            labels={marge_ou_ca: marge_ou_ca_clean},
            title=f"Évolution du {marge_ou_ca_clean} - {periode}",
        )
        
    elif periode == "6M" : 
        data = data[(data["Mois"] <= datetime.datetime.now().strftime("%Y-%m")) & (data["Mois"] > datetime.datetime.now().replace(month=datetime.datetime.now().month - 6).strftime("%Y-%m"))]
        fig = px.line(
            data.groupby([granularité])[marge_ou_ca].sum().reset_index(),
            x=granularité,
            y=marge_ou_ca,
            text=marge_ou_ca,
            labels={marge_ou_ca: marge_ou_ca_clean},
            title=f"Évolution du {marge_ou_ca_clean} - {periode}",
        )

    elif periode == "YTD" : 
        data = data[data["Année"] == datetime.datetime.now().strftime("%Y")]
        fig = px.line(
            data.groupby([granularité])[marge_ou_ca].sum().reset_index(),
            x=granularité,
            y=marge_ou_ca,
            text=marge_ou_ca,
            labels={marge_ou_ca: marge_ou_ca_clean},
            title=f"Évolution du {marge_ou_ca_clean} - {periode}",
        )

    elif periode == "M" : 
        data = data[data["Mois"] == mois_auj]
        fig = px.line(
            data.groupby([granularité])[marge_ou_ca].sum().reset_index(),
            x=granularité,
            y=marge_ou_ca,
            text=marge_ou_ca,
            labels={marge_ou_ca: marge_ou_ca_clean},
            title=f"Évolution du {marge_ou_ca_clean} - {periode}",
        )

    elif periode == "Previsionnel" : 
        data = data[data["Mois"] >= mois_auj]
        fig = px.line(
            data.groupby([granularité])[marge_ou_ca].sum().reset_index(),
            x=granularité,
            y=marge_ou_ca,
            text=marge_ou_ca,
            labels={marge_ou_ca: marge_ou_ca_clean},
            title=f"Évolution du {marge_ou_ca_clean} - {periode}",
        )

    # Mise en forme du graphique
    fig.update_xaxes(type="category", tickformat="%b-%Y")
    fig.update_yaxes(title_text=marge_ou_ca_clean)
    fig.update_traces(textposition='bottom center')

    # Affichage du graphique avec Streamlit
    st.plotly_chart(fig)


with col2:
    # Création du graphique à barres empilées avec Plotly Express

    fig = px.bar(
        data.groupby([granularité])["marge","total HT"].sum().reset_index(),
        x=granularité,
        y="total HT",
        color = "marge",
        labels={"total HT": "CA"},
        title=f"Évolution CA / Marge - {periode}",
    )

    # Mise en forme du graphique
    fig.update_xaxes(type="category", tickformat="%b-%Y")
    fig.update_yaxes(title_text="CA/Marge")

    st.plotly_chart(fig)

