import datetime
import logging


class MockExchangeHandler:
    def __init__(self):
        self._buys = []
        self._sells = []
        self._logger = logging.getLogger(self.__class__.__name__)

    def buy(self, buy_time: datetime.datetime):
        self._logger.info(f"Buying at {buy_time}")
        self._buys.append(buy_time)

    def sell(self, sell_time: datetime.datetime):
        self._logger.info(f"Selling at {sell_time}")
        self._sells.append(sell_time)
