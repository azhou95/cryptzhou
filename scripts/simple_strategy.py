import asyncio
import logging

import pandas as pd

from base_classes.strategies import BaseStrategy
from base_classes.streaming_data_provider import StreamingDataProvider
from exchange_handlers.mock_exchange_handler import MockExchangeHandler
from strategies.ma_crossover_strategy import SimpleStrategy
from streaming_data_providers.historical_binance_data_provider import HistoricalBinanceStreamingDataProvider
from utils.data_models import TradeNotification
from utils.enums import Signal
import plotly.express as px


class StrategyOrchestrator:
    def __init__(self, data_stream: StreamingDataProvider, strategy: BaseStrategy, exchange_handler):
        self._data_stream = data_stream
        self._strategy = strategy
        self._exchange_handler = exchange_handler
        self._trade_data = pd.DataFrame()
        self._max_data = strategy.parameters.max_data_rows

        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.DEBUG)

    async def start(self):
        await self._data_stream.start()

    async def run(self):
        while True:
            try:
                async for trade in self._data_stream:
                    self._logger.info(f"Received Trade {trade}")
                    self.on_trade(trade)
            except Exception as e:
                self._logger.warning(f"Stream ended with error: {e}")
                self.end_session()
                break

    def end_session(self):
        fig = px.line(x=self._trade_data.index, y=self._trade_data["ClosePrice"])
        # TODO: (azhou) add some visualisation for signals
        # fig.add_vline(x=self._trade_data.index[10], line_dash="dot")
        fig.show()

    def on_trade(self, trade: TradeNotification):
        # TODO: (azhou) faster to keep a deque and transform to a df?
        # TODO: (azhou) when do we trim the df?
        new_trade_df = self._append_new_trade_data(trade)
        signal = self._strategy.on_trade(new_trade_df)
        if signal == Signal.BUY:
            self._exchange_handler.buy(trade.time)
        elif signal == Signal.SELL:
            self._exchange_handler.sell(trade.time)

    def _append_new_trade_data(self, trade_row: TradeNotification) -> pd.DataFrame:
        new_trade_df = pd.concat([self._trade_data, trade_row.to_df_row()], axis=0)
        # new_trade_df = new_trade_df[-self._max_data:]
        self._trade_data = new_trade_df
        return self._trade_data.copy()


async def main():
    orch = StrategyOrchestrator(
        HistoricalBinanceStreamingDataProvider(
            ticker="ETHBTC",
            interval="1m",
            start="2023-10-02",
            end="2023-10-03",
        ),
        SimpleStrategy(),
        MockExchangeHandler(),
    )
    await orch.start()
    await orch.run()

if __name__ == "__main__":
    asyncio.run(main())
