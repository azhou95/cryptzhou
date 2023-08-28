import asyncio
import json

from binance import AsyncClient, DepthCacheManager, BinanceSocketManager

async def main():

    # initialise the client
    client = await AsyncClient.create()

    # run some simple requests
    # print(json.dumps(await client.get_exchange_info(), indent=2))
    #
    # print(json.dumps(await client.get_symbol_ticker(symbol="BTCUSDT"), indent=2))

    # initialise websocket factory manager
    bsm = BinanceSocketManager(client)

    # create listener using async with
    # this will exit and close the connection after 5 messages
    async with bsm.trade_socket('ETHBTC') as ts:
        for _ in range(5):
            res = await ts.recv()
            print(res)
            # print(f'recv {res["price"]}')


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
