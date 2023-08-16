# Simple script to observe the difference in price between one
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd

import historical_data_providers


def main(start: datetime, end: datetime, interval: timedelta):
    coingecko_data = historical_data_providers.CoingeckoDataProvider().get_historical_data(start, end, interval)
    yfinance_data = historical_data_providers.YfinanceDataProvider().get_historical_data(start, end, interval)

    df = coingecko_data.join(yfinance_data['YFinance BTC'])
    df.dropna(inplace=True)

    print("max earnings in one day: ", sum(abs(df["Coingecko BTC"] - df["YFinance BTC"])))
    df["Difference"] = df["Coingecko BTC"] - df["YFinance BTC"]
    df["Fees"] = df["Coingecko BTC"] * 0.001 + df["YFinance BTC"] * 0.0006
    df["Potential Profit"] = df["Difference"] - df["Fees"]
    print(sum(df[df["Potential Profit"] > 0]["Potential Profit"]))


def plot_data(df: pd.DataFrame):
    # TODO: (azhou) use seaborn?
    fig, ax = plt.subplots(figsize=(8, 4), dpi=200)
    ax.plot(df['Timestamp'], df['Coingecko BTC'], label='Coingecko BTC (Exchange I)')
    ax.plot(df['Timestamp'], df['YFinance BTC'], label='YFinance BTC (Exchange II)')
    plt.title('BTC Price (Coingecko vs YFinance)')
    plt.legend()

    fig, ax = plt.subplots(figsize=(8, 4), dpi=200)
    plt.plot(df['Timestamp'], abs(df['Coingecko BTC'] - df['YFinance BTC']), label='Spread | Coingecko - YFinance')
    plt.title('Spread | Coingecko - YFinance')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    import pytz
    main(
        datetime.now(tz=pytz.UTC) - timedelta(hours=24), datetime.now(tz=pytz.UTC), timedelta(minutes=5)
    )
