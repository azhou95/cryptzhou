import json
import logging

import websockets

from base_classes.streaming_data_provider import StreamingDataProvider


class CoinbaseStreamingDataProvider(StreamingDataProvider):
    URI = "wss://ws-feed.prime.coinbase.com"
    # TODO (azhou) need to create an account and authenticate

    def __init__(self):
        self.ws = None
        self._logger = logging.getLogger(self.__class__.__name__)

    async def start(self):
        # TODO (azhou) disgusting, but I can't think of any solution other than adding a callback to the websockets API to pipe the result to a queue, which is arguably worse
        self.ws = await websockets.connect(self.URI, ping_interval=None, max_size=None).__aenter__

    async def __aiter__(self):
        while True:
            response = await self.ws.recv()
            parsed = json.loads(response)
            yield parsed
