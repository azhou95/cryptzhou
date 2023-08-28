import json

import websockets

from base_classes.streaming_data_provider import StreamingDataProvider


class CoinbaseStreamingDataProvider(StreamingDataProvider):
    URI = "wss://ws-feed.prime.coinbase.com"
    # TODO (azhou) need to create an account and authenticate

    async def __aiter__(self):
        async with websockets.connect(self.URI, ping_interval=None, max_size=None) as ws:
            response = await ws.recv()
            parsed = json.loads(response)
            yield parsed
