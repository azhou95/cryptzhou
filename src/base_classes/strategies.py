import abc
from typing import Optional

import pandas as pd

from utils.data_models import StrategyParams
from utils.enums import Signal


class BaseStrategy(abc.ABC):

    @property
    @abc.abstractmethod
    def parameters(self) -> StrategyParams:
        pass

    @abc.abstractmethod
    async def on_trade(self, trade_data: pd.DataFrame) -> Optional[Signal]:
        pass

