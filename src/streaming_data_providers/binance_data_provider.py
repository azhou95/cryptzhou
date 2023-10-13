import json
import logging

import pandas as pd

from base_classes.streaming_data_provider import StreamingDataProvider
from binance import AsyncClient, BinanceSocketManager

from utils.data_models import TradeNotification


class BinanceStreamingDataProvider(StreamingDataProvider):
    def __init__(self, ticker: str):
        self._ticker = ticker
        self.bsm = None
        self._logger = logging.getLogger(f"{ticker}::{self.__class__.__name__}")

    async def start(self):
        client = await AsyncClient.create()
        self.bsm = BinanceSocketManager(client)

    async def __aiter__(self) -> TradeNotification:
        # TODO: (azhou) handle errors
        async with self.bsm.kline_socket(self._ticker) as ts:
            res = await ts.recv()
            res = json.loads(res)
            trade_notification = TradeNotification(
                time=pd.to_datetime(res["E"], unit="ms"),
                close_price=float(res["k"]["c"])
            )
            yield trade_notification
