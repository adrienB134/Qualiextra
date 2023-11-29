import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import numpy as np

# Config
st.set_page_config(page_title="Qualiextra", 
                   page_icon="🏝️", 
                   layout="wide")

# Load data
data = st.session_state.data
full = data
annulations = data[data["statuts"] == "annulé"]
data = data[data["statuts"] != "annulé"]

# Body
st.header("Classements des hôtels sur la totalité de la période")
st.markdown("---")

top = st.text_input("Nombre d'hôtels a afficher", 5)

df = (data.groupby("Propriété_clean")
    .count()
    .sort_values(by="hôtel", 
                 ascending=False)
    .reset_index()[["Propriété_clean", "Propriété"]])

df.index = np.arange(1, len(df) + 1)
df.index = df.index.rename("Rang")
df.columns = ["Hôtels", "Missions (nb)"]
st.dataframe(df.iloc[0 : int(top), :], use_container_width=True)


st.header("Evolution du nombre de missions par hôtel et par an")
st.markdown("---")

years = st.selectbox("Année", data["date_debut"].dt.year\
                     .astype(str)
                     .unique(), index=1)

by_year = data.loc[data["date_debut"].dt.year\
                   .astype(str) == years, ["Propriété_clean","periode_debut"]]

by_year["count"] = 1

by_year = by_year.pivot_table(index="periode_debut", 
                              values="count",
                              columns=['Propriété_clean'], 
                              aggfunc="count", 
                              fill_value=0)

top_hotels = by_year.sum()\
    .sort_values(ascending=False)[:int(top)]\
    .index.to_list()

top_by_year = by_year.loc[:,top_hotels]
top_by_year = pd.melt(top_by_year.reset_index(), 
                      id_vars="periode_debut", 
                      value_name="Missions")

fig = px.line(top_by_year, 
              x="periode_debut", 
              y ="Missions", 
              color="Propriété_clean", 
              markers=True)

fig.update_xaxes(title_text="Temps")
fig.update_yaxes(title_text="Nombre de missions")

st.plotly_chart(fig, use_container_width=True)


st.header("Nombre de missions et annulations par hôtel et par mois")

st.markdown("---")

data["statuts"] = data["statuts"].fillna("standard")

year = st.selectbox("Choisissez une année", 
                    data["date_debut"].dt.strftime("%Y").unique(), 
                    index=1)

month = st.selectbox("Choisissez un mois", 
                     ["Tous mois confondus", 
                      *data.loc[data["date_debut"].dt.year.astype(str) == year, 
                                "date_debut"].dt.strftime("%m").unique()], 
                     index=0)

if month != "Tous mois confondus":
    date = month+'-'+year
    monthly_missions_status = data[(data["periode_debut"] == date)]\
        .groupby(["Propriété_clean", "statuts"])\
        .count()\
        .sort_values(by="hôtel", ascending=False)\
        .reset_index().iloc[:,:3]
    
    pourcent_annulations = pd.DataFrame()

    pourcent_annulations["total"] = full[full["periode_debut"] == date]\
        .groupby("Propriété_clean")\
        .count().loc[:,"hôtel"]
    
    pourcent_annulations["annule"] = \
        annulations[annulations["periode_debut"] == date]\
        .groupby("Propriété_clean")\
        .count()\
        .loc[:,"hôtel"]
    
else : 
    monthly_missions_status = data[(data["date_debut"].dt.year\
                                    .astype(str) == year)]\
                                .groupby(["Propriété_clean", "statuts"])\
                                .count().sort_values(by="hôtel", 
                                                     ascending=False)\
                                .reset_index()\
                                .iloc[:,:3]
    
    pourcent_annulations = pd.DataFrame()

    pourcent_annulations["total"] = full[(full["date_debut"].dt.year\
                                          .astype(str) == year)]\
                                        .groupby("Propriété_clean")\
                                        .count()\
                                        .loc[:,"hôtel"]
    
    pourcent_annulations["annule"] = annulations[(annulations["date_debut"]\
                                                  .dt.year\
                                                  .astype(str) == year)]\
                                            .groupby("Propriété_clean")\
                                            .count()\
                                            .loc[:,"hôtel"]


tab1, tab2 = st.tabs(["Missions", "Annulations"])

with tab1:
    st.subheader("Missions")

    fig = px.bar(monthly_missions_status, 
                 x="Propriété_clean", 
                 y="Propriété", 
                 color="statuts")
    
    fig.update_layout(legend=dict(
                          yanchor="top",
                          y=0.99,
                          xanchor="right",
                          x=0.99
                      ))
    
    fig.update_xaxes(title_text="Hôtels")
    fig.update_yaxes(title_text="Nombre de missions")

    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Annulations")
    pourcent_annulations = pourcent_annulations\
        .fillna(0)\
        .sort_values(by="annule",
                     ascending=False)

    if pourcent_annulations["annule"].sum() != 0:
        fig = px.bar(pourcent_annulations, 
                     x=pourcent_annulations.index, 
                     y="annule")
        
        fig.update_xaxes(title_text="Hôtels")
        fig.update_yaxes(title_text="Nombre d'annulations")
        st.plotly_chart(fig, use_container_width=True)
    else:
        with st.columns(3)[1]:
            st.caption("Pas d'annulations pour cette période")