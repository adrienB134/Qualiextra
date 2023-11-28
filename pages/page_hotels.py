import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import numpy as np

# Config
st.set_page_config(page_title="GetAround Delay", page_icon="🚗 ", layout="wide")


data = st.session_state.data


# change text from "Loading data..." to "" once the the load_data function has run


st.header("Classements des hôtels sur la période")

st.markdown("---")

top = st.text_input("Nombre de lignes a afficher", 5)

df = (
    data.groupby("Propriété_clean")
    .count()
    .sort_values(by="hôtel", ascending=False)
    .reset_index()[["Propriété_clean", "Propriété"]]
)
df.index = np.arange(1, len(df) + 1)
df.index = df.index.rename("Rang")
df.columns = ["Hôtels", "Missions (nb)"]

st.table(df.iloc[0 : int(top), :])

st.header("Nombre de missions par hôtel et par mois")

st.markdown("---")

months = data["periode_debut"].unique()
custom_palette = sns.color_palette(
    "tab10", len(data["periode_debut"].unique())
).as_hex()
fig = go.Figure()


for i in range(len(months)):
    if i == 1:
        fig.add_trace(
            go.Bar(
                x=data[data["periode_debut"] == months[i]]
                .groupby("Propriété_clean")
                .count()
                .sort_values(by="hôtel", ascending=False)
                .index,
                y=data[data["periode_debut"] == months[i]]
                .groupby("Propriété_clean")
                .count()
                .sort_values(by="hôtel", ascending=False)
                .hôtel,
                visible=True,
                marker_color=custom_palette[i],
            )
        )

    else:
        fig.add_trace(
            go.Bar(
                x=data[data["periode_debut"] == months[i]]
                .groupby("Propriété_clean")
                .count()
                .sort_values(by="hôtel", ascending=False)
                .index,
                y=data[data["periode_debut"] == months[i]]
                .groupby("Propriété_clean")
                .count()
                .sort_values(by="hôtel", ascending=False)
                .hôtel,
                visible=False,
                marker_color=custom_palette[i],
            )
        )

fig.update_layout(
    title=go.layout.Title(text="Nombre de missions par hôtel", x=0.5),
    autosize=False,
    showlegend=False,
    width=1500,
    height=700,
)

buttons = [
    go.layout.updatemenu.Button(
        label=month, method="update", args=[{"visible": [m == month for m in months]}]
    )
    for month in months
]


fig.update_layout(updatemenus=[go.layout.Updatemenu(active=1, buttons=buttons)])

fig.update_xaxes(title_text="Hôtels")
fig.update_yaxes(title_text="Nombre de missions")

st.plotly_chart(fig, use_container_width=True, theme=None)


st.header("Nombre de missions par hôtel et par an")

st.markdown("---")


years = data["date_debut"].dt.year.astype(str).unique()
custom_palette = sns.color_palette(
    "tab10", len(data["date_debut"].dt.year.unique())
).as_hex()
fig = go.Figure()


for i in range(len(years)):
    if i == 1:
        fig.add_trace(
            go.Bar(
                x=data[data["date_debut"].dt.year.astype(str) == years[i]]
                .groupby("Propriété_clean")
                .count()
                .sort_values(by="hôtel", ascending=False)
                .index,
                y=data[data["date_debut"].dt.year.astype(str) == years[i]]
                .groupby("Propriété_clean")
                .count()
                .sort_values(by="hôtel", ascending=False)
                .hôtel,
                visible=True,
                marker_color=custom_palette[i],
            )
        )

    else:
        fig.add_trace(
            go.Bar(
                x=data[data["date_debut"].dt.year.astype(str) == years[i]]
                .groupby("Propriété_clean")
                .count()
                .sort_values(by="hôtel", ascending=False)
                .index,
                y=data[data["date_debut"].dt.year.astype(str) == years[i]]
                .groupby("Propriété_clean")
                .count()
                .sort_values(by="hôtel", ascending=False)
                .hôtel,
                visible=False,
                marker_color=custom_palette[i],
            )
        )

fig.update_layout(
    title=go.layout.Title(text="Nombre de missions par hôtel", x=0.5),
    autosize=False,
    showlegend=False,
    width=1500,
    height=700,
)

buttons = [
    go.layout.updatemenu.Button(
        label=year, method="update", args=[{"visible": [y == year for y in years]}]
    )
    for year in years
]


fig.update_layout(updatemenus=[go.layout.Updatemenu(active=1, buttons=buttons)])

fig.update_xaxes(title_text="Hôtels")
fig.update_yaxes(title_text="Nombre de missions")

st.plotly_chart(fig, use_container_width=True, theme=None)
