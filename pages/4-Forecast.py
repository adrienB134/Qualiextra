import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from neuralforecast import NeuralForecast
from datetime import datetime
from neuralforecast.models import NBEATS, NHITS, TimesNet

from statsmodels.tsa.holtwinters import ExponentialSmoothing
from pathlib import Path

st.set_page_config(
    page_title="Forecast",
    page_icon="📈",
    layout="wide",
)


@st.cache_data
def forecasting(data):
    # Preprocessing
    data["ds"] = pd.to_datetime(data["date_debut"]).dt.date
    data_ts = data.groupby("ds")["extra_clean"].count().to_frame()
    data_ts = data_ts.rename(columns={"extra_clean": "y"})
    data_ts = data_ts.reset_index()
    data_ts["ds"] = data_ts["ds"].apply(lambda x: pd.Timestamp(x))

    TES = ExponentialSmoothing(data_ts["y"], trend="add")
    TES_fit = TES.fit()
    TES_predict = TES_fit.predict(start=0, end=len(data_ts))
    data_ts["y"] = data_ts["y"].astype("int")
    y = data_ts["y"]
    MA7 = y.rolling(window=14)
    data_ts["y_7"] = round(MA7.mean())
    data_ts["y_upper"] = MA7.std()
    data_ts["y_lower"] = MA7.std()
    data_ts["TES"] = TES_predict
    data_ts["max"] = data_ts["TES"] + 1.5 * data_ts["y_upper"]
    data_ts["min"] = data_ts["TES"] - 1.5 * data_ts["y_lower"]
    data_ts["residual"] = data_ts["y"] - data_ts["TES"]

    Y1 = data_ts[["ds", "y"]]
    Y1["unique_id"] = "pred"
    Y3 = data_ts[["ds", "TES"]].rename(columns={"TES": "y"})
    Y3["unique_id"] = "pred_TES"
    Y4 = data_ts[["ds", "max"]].rename(columns={"max": "y"})
    Y4["unique_id"] = "max"
    Y5 = data_ts[["ds", "min"]].rename(columns={"min": "y"})
    Y5["unique_id"] = "min"

    split_date = pd.Timestamp(datetime.today())
    Y_hat_df2 = Y1[Y1.ds <= split_date].drop("unique_id", axis=1).copy()

    ts = [Y1, Y3, Y4, Y5]

    for Y in ts:
        Y["y"] = Y["y"].fillna(0)
        Y["y"] = round(Y["y"], 0)
        Y["y"] = Y["y"].astype("int")

        # split_date = pd.Timestamp("2023-08-31")
        Y_train_df = Y[Y.ds <= split_date]

        # Y_test_df = Y[Y.ds > split_date]
        # horizon = 90
        models = [
            # NBEATS(input_size=2 * horizon, h=horizon, max_steps=785),
            NBEATS(input_size=260, h=128, max_steps=200),
        ]
        nf = NeuralForecast(models=models, freq="D")
        nf.fit(
            df=Y_train_df,
            verbose=True,
        )
        Y_hat_df = nf.predict().reset_index().drop("unique_id", axis=1)

        Y_hat_df2 = pd.merge(Y_hat_df2, Y_hat_df, how="outer").rename(
            columns={
                "NBEATS": f'{Y["unique_id"].iloc[0]}',
            }
        )

    plot_df = Y_hat_df2.sort_values("ds").set_index("ds").rename(columns={"y": "réel"})
    return plot_df


my_file = Path("missions_processed.csv")
if my_file.is_file():
    data = pd.read_csv("missions_processed.csv")

    st.title(" 📈 Prédiction du nombre d'extras pour les prochains mois")
    plot_df = forecasting(data)

    plot_df["pred_lissé"] = round(plot_df["pred_TES"].rolling(window=7).max())
    plot_df["max_lissé"] = round(plot_df["max"].rolling(window=7).max())
    plot_df["min_lissé"] = round(plot_df["min"].rolling(window=7).min())
    plot_df["réel_lissé"] = round(plot_df["réel"].rolling(window=7).mean())

    plot = go.Figure()
    for column in plot_df.columns:
        plot.add_trace(
            go.Scatter(
                x=plot_df.index,
                y=plot_df[column],
                visible="legendonly",
                name=column,
            )
        )
    plot.for_each_trace(
        lambda trace: trace.update(visible=True)
        if trace.name == "réel_lissé"
        or trace.name == "pred_lissé"
        or trace.name == "max_lissé"
        or trace.name == "min_lissé"
        or trace.name == "réel"
        or trace.name == "pred"
        else (),
    )
    plot.for_each_trace(
        lambda trace: trace.update({"line": {"color": "indianred"}})
        if trace.name == "pred_lissé"
        or trace.name == "max_lissé"
        or trace.name == "min_lissé"
        else (),
    )
    plot.for_each_trace(
        lambda trace: trace.update(opacity=0.5)
        if trace.name == "max_lissé" or trace.name == "min_lissé"
        else (),
    )
    plot.update_traces(hovertemplate=None)
    plot.update_layout(
        height=700,
        hovermode="x unified",
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(
                            count=4, label="4 mois", step="month", stepmode="backward"
                        ),
                        dict(
                            count=6, label="6 mois", step="month", stepmode="backward"
                        ),
                        dict(count=1, label="1 an", step="year", stepmode="backward"),
                        dict(label="tout", step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
            type="date",
        ),
    )
    plot.update_xaxes(title_text="Date")
    plot.update_yaxes(title_text="Nombre d'extras uniques")
    st.plotly_chart(plot, use_container_width=True)


else:
    st.warning("Merci de bien vouloir charger des données !")
