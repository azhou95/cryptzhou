import abc
from datetime import datetime, timedelta

import pandas as pd


class HistoricalDataProvider(abc.ABC):
    @abc.abstractmethod
    def get_historical_data(self, start: datetime, end: datetime, interval: timedelta) -> pd.DataFrame:
        pass
