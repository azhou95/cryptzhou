from datetime import datetime, timedelta
import pytz

import pandas as pd
import yfinance as yf

from base_classes import HistoricalDataProvider


class YfinanceDataProvider(HistoricalDataProvider):
    def get_historical_data(self, start: datetime, end: datetime, interval: timedelta) -> pd.DataFrame:
        # (azhou) yfinance assumes the historical_data_providers is in UTC without doing any sanity checks, so we perform them  here
        assert start.tzinfo == pytz.UTC, "start time must be in UTC"
        assert end.tzinfo == pytz.UTC, "end time must be in UTC"

        # TODO (azhou) make this variable per asset
        btc = yf.Ticker("BTC-USD")
        df = btc.history(start=start, end=end, interval=f"{int(interval.seconds / 60)}m")
        df = df[['Close']]
        df = df[['Close']].rename(columns={'Close': 'YFinance BTC'})
        df.index = pd.to_datetime(df.index, utc=False).tz_localize(None)
        df = df.reset_index()
        return df


if __name__ == "__main__":
    res = YfinanceDataProvider().get_historical_data(datetime.now() - timedelta(hours=24), datetime.now(), timedelta(minutes=5))
    print(res.head(10))
