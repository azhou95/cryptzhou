import logging

import pandas as pd
from binance import Client

from base_classes.streaming_data_provider import StreamingDataProvider
from utils.data_models import TradeNotification


class HistoricalBinanceStreamingDataProvider(StreamingDataProvider):
    def __init__(self, ticker: str, interval: str, start: str, end: str):
        self._ticker = ticker
        self._interval = interval
        self._start = start
        self._end = end

        self._historical_data = None
        self._logger = logging.getLogger(f"{ticker}::{self.__class__.__name__}")

    async def start(self):
        client = Client()
        # Returns list of OHLCV values (Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore)
        historical_data = client.get_historical_klines(
            symbol=self._ticker,
            interval=self._interval,
            start_str=self._start,
            end_str=self._end,
        )
        self._historical_data = iter(historical_data)

    async def __aiter__(self) -> TradeNotification:
        res = next(self._historical_data)
        trade_notification = TradeNotification(
            time=pd.to_datetime(res[0], unit="ms"),
            close_price=float(res[4])
        )
        yield trade_notification


async def tester():
    provider = HistoricalBinanceStreamingDataProvider(
        ticker="ETHBTC",
        interval="1m",
        start="2023-10-02",
        end="2023-10-03",
    )
    await provider.start()
    while True:
        try:
            async for value in provider:
                print(value)
        except Exception:
            print("end")
            break

if __name__ == "__main__":
    import asyncio
    asyncio.run(tester())

