from dataclasses import dataclass
import datetime

import pandas as pd


@dataclass
class TradeNotification:
    time: datetime.datetime
    close_price: float

    def to_df_row(self) -> pd.DataFrame:
        return pd.DataFrame(
            data=[self.close_price],
            index=[self.time],
            columns=["ClosePrice"],
        )


@dataclass
class StrategyParams:
    max_data_rows: int
