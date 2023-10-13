from typing import Optional

import pandas as pd

from base_classes.strategies import BaseStrategy
from utils.data_models import StrategyParams
from utils.enums import Signal


class SimpleStrategy(BaseStrategy):
    def __init__(self):
        self._has_position = False  # TODO: we will have to get position from exchange

    @property
    def parameters(self) -> StrategyParams:
        return StrategyParams(
            max_data_rows=30
        )

    def on_trade(self, trade_data: pd.DataFrame) -> Optional[Signal]:
        if len(trade_data) <= 20:
            return

        trade_data["MA5"] = trade_data["ClosePrice"].rolling(5).mean()
        trade_data["MA10"] = trade_data["ClosePrice"].rolling(10).mean()
        trade_data["MA20"] = trade_data["ClosePrice"].rolling(20).mean()

        for trade_time, trade_details in trade_data.iterrows():
            if (trade_details["MA5"] > trade_details["MA10"]) and (trade_details["MA5"] > trade_details["MA20"]) and not self._has_position:
                self._has_position = True
                return Signal.BUY
            elif (trade_details["MA5"] < trade_details["MA10"]) and (trade_details["MA5"] < trade_details["MA20"]) and self._has_position:
                self._has_position = False
                return Signal.SELL
