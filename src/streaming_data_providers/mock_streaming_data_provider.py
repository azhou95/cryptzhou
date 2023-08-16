import asyncio
import logging

from base_classes.streaming_data_provider import StreamingDataProvider


class MockStreamingDataProvider(StreamingDataProvider):
    def __init__(self, period: int, value_gen):
        self.period = period
        self.value_gen = value_gen
        self._logger = logging.getLogger(self.__class__.__name__)

    async def __aiter__(self):
        while True:
            val = next(self.value_gen)
            self._logger.info(f"Got value {val}")
            yield val
            await asyncio.sleep(self.period)

    async def __anext__(self):
        return next(self.value_gen)
