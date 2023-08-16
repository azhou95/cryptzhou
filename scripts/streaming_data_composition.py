import asyncio
import logging

from streaming_data_providers.mock_streaming_data_provider import MockStreamingDataProvider


class StreamComposer:
    # TODO: error handling in the streams, managing data rate etc.
    def __init__(self, stream_provider_1, stream_provider_2):
        self.stream_provider_1 = stream_provider_1
        self.stream_provider_2 = stream_provider_2
        self.event = asyncio.Event()
        self.state = [None, None]  # TODO: this should be a queue

        self._logger = logging.getLogger(self.__class__.__name__)

    async def read_gen(self, stream_provider, index):
        async for value in stream_provider:
            self.state[index] = value
            self.event.set()

    async def read_combined(self):
        while True:
            await self.event.wait()
            self.event.clear()
            if all(state_value is not None for state_value in self.state):
                print(self.state)
            else:
                self._logger.warning("No data yet!")

    async def start(self):
        await asyncio.gather(
            self.read_gen(self.stream_provider_1, 0),
            self.read_gen(self.stream_provider_2, 1),
            self.read_combined(),
        )


def brownian(start=0, delta=0.25, dt=0.1):
    """
    naive brownian motion gen
    """
    from scipy.stats import norm
    x = start
    while True:
        x = x + norm.rvs(scale=delta ** 2 * dt)
        yield x


async def main():
    streaming_data_provider_1 = MockStreamingDataProvider(1, brownian(20000))
    streaming_data_provider_2 = MockStreamingDataProvider(2, brownian(20000))

    stream_composer = StreamComposer(streaming_data_provider_1, streaming_data_provider_2)
    await stream_composer.start()

if __name__ == "__main__":
    asyncio.run(main())
