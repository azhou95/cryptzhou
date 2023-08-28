import logging

from base_classes.streaming_data_provider import StreamingDataProvider
from binance import AsyncClient, BinanceSocketManager


class BinanceStreamingDataProvider(StreamingDataProvider):
    def __init__(self):
        self.bsm = None
        self._logger = logging.getLogger(self.__class__.__name__)

    async def start(self):
        client = await AsyncClient.create()
        self.bsm = BinanceSocketManager(client)

    async def __aiter__(self):
        # TODO: (azhou) handle errors
        async with self.bsm.depth_socket('ETHBTC') as ts:
            res = await ts.recv()
            self._logger.info(res)
            yield res
