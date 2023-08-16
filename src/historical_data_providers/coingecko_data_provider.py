import json
from datetime import datetime, timedelta

import pandas as pd
import requests

from base_classes import HistoricalDataProvider


class CoingeckoDataProvider(HistoricalDataProvider):
    """
    Note that Coingecko historical_data_providers only has 5 minute granularity for the last 24 hours.
    Beyond this point we only have 1 hour granularity.
    """
    COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from=%s&to=%s"

    def get_historical_data(self, start: datetime, end: datetime, interval: timedelta) -> pd.DataFrame:
        # TODO (azhou) make this variable per asset
        url = self.COINGECKO_URL % (start.timestamp(), end.timestamp())
        response = requests.get(url)
        data = json.loads(response.text)
        prices = data["prices"]
        # Convert the price historical_data_providers to a Pandas dataframe
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df = df[['timestamp', 'price']].rename(columns={'price': 'Coingecko BTC', 'timestamp': 'Timestamp'})

        # Convert the timestamp to a datetime object
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
        df = df.set_index("Timestamp").resample("5T").last().reset_index()
        return df


if __name__ == "__main__":
    res = CoingeckoDataProvider().get_historical_data(datetime(2023, 8, 16), datetime(2023, 8, 17), timedelta(minutes=5))
    print(res.head(10))
