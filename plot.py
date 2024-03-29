import xml.etree.ElementTree as ET
from typing import Tuple

import pandas as pd
import plotly.graph_objs as go
from pandas import DataFrame


def parse_ecb_exchange_rates(filename: str) -> Tuple[DataFrame, DataFrame, DataFrame]:
    tree = ET.parse(filename)

    root = tree.getroot()

    dates = []
    exchange_rates = []

    for obs in root.findall(".//{http://www.ecb.europa.eu/vocabulary/stats/exr/1}Obs"):
        date = obs.get("TIME_PERIOD")
        exchange_rate = float(obs.get("OBS_VALUE"))
        dates.append(date)
        exchange_rates.append(exchange_rate)

    df = pd.DataFrame({"Date": dates, "ExchangeRate": exchange_rates})
    df["Date"] = pd.to_datetime(df["Date"])

    df_monthly_max = df.loc[
        df.groupby(df["Date"].dt.to_period("M"))["ExchangeRate"].idxmax()
    ]
    df_monthly_min = df.loc[
        df.groupby(df["Date"].dt.to_period("M"))["ExchangeRate"].idxmin()
    ]
    df_monthly_mean = df.groupby(df["Date"].dt.to_period("M"))["ExchangeRate"].mean()

    df_monthly_mean = df_monthly_mean.reset_index()

    # Convert Period index to string
    df_monthly_mean["Date"] = df_monthly_mean["Date"].astype(str)

    return df_monthly_max, df_monthly_min, df_monthly_mean


def plot_exchange_rates(
    maximum: DataFrame, minimum: DataFrame, mean: DataFrame, currency: str, y_ticks=None
):
    fig = go.Figure()

    # Add trace for Max Exchange Rate
    fig.add_trace(
        go.Scatter(
            x=maximum["Date"],
            y=maximum["ExchangeRate"],
            mode="markers+lines",
            name="Max Exchange Rate",
            marker=dict(color="green"),
        )
    )

    # Add trace for Min Exchange Rate
    fig.add_trace(
        go.Scatter(
            x=minimum["Date"],
            y=minimum["ExchangeRate"],
            mode="markers+lines",
            name="Min Exchange Rate",
            marker=dict(color="red"),
        )
    )

    # Add trace for Mean Exchange Rate
    fig.add_trace(
        go.Scatter(
            x=mean["Date"],
            y=mean["ExchangeRate"],
            mode="markers+lines",
            name="Mean Exchange Rate",
            marker=dict(color="yellow"),
        )
    )

    fig.update_layout(
        title=f"Max, Min, and Mean Exchange Rate per Month, {currency.upper()} to EUR",
        title_font_size=28,
        xaxis_title="Date",
        xaxis_title_font_size=20,
        yaxis_title="Exchange Rate",
        yaxis_title_font_size=20,
        yaxis=dict(
            tickfont=dict(size=18, color="black"), dtick=y_ticks, gridcolor="white"
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=18),
        ),
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=18, color="black"),
            dtick="M12",
            gridcolor="white",
        ),
        plot_bgcolor="grey",
        paper_bgcolor="lightgrey",
    )

    fig.show()
