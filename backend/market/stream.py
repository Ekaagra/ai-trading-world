import asyncio
import json
from datetime import datetime

import websockets


class MarketStream:

    SYMBOL_MAP = {
        "BTC": "btcusdt",
        "ETH": "ethusdt",
        "SOL": "solusdt",
    }

    def __init__(self, symbols: list[str]):
        self.symbols = symbols

        streams = "/".join(
            f"{self.SYMBOL_MAP[symbol]}@trade"
            for symbol in symbols
        )

        self.url = (
            f"wss://stream.binance.com:9443/stream"
            f"?streams={streams}"
        )

    async def connect(self):

        print("Connecting to market stream...")

        async with websockets.connect(
            self.url
        ) as websocket:

            print("Connected to Binance market stream.")

            while True:

                message = await websocket.recv()

                data = json.loads(message)

                stream_data = data["data"]

                exchange_symbol = stream_data["s"]

                price = float(
                    stream_data["p"]
                )

                quantity = float(
                    stream_data["q"]
                )

                timestamp = datetime.fromtimestamp(
                    stream_data["T"] / 1000
                )

                symbol = next(
                    key
                    for key, value in self.SYMBOL_MAP.items()
                    if value.upper() == exchange_symbol
                )

                yield {
                    "symbol": symbol,
                    "price": price,
                    "quantity": quantity,
                    "timestamp": timestamp,
                }


async def main():

    stream = MarketStream(
        symbols=[
            "BTC",
            "ETH",
            "SOL",
        ]
    )

    async for event in stream.connect():

        print(
            f"{event['symbol']}: "
            f"${event['price']:,.2f}"
        )


if __name__ == "__main__":
    asyncio.run(main())