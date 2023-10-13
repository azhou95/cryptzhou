import abc


class StreamingDataProvider(abc.ABC):
    @abc.abstractmethod
    async def start(self):
        pass

    @abc.abstractmethod
    async def __aiter__(self):
        pass
