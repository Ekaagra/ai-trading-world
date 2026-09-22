import asyncio

from .market.stream import MarketStream
from .market.aggregator import CandleAggregator


async def main():

    stream = MarketStream(
        symbols=["BTC"]
    )

    aggregator = CandleAggregator(
        interval_seconds=60
    )

    print("Starting candle aggregator...")

    async for event in stream.connect():

        candle = aggregator.update(
            symbol=event["symbol"],
            price=event["price"],
            quantity=event["quantity"],
            timestamp=event["timestamp"],
        )

        if candle is not None:

            print(
                "\n========== CANDLE =========="
            )

            print(
                f"Symbol:    {candle.symbol}"
            )

            print(
                f"Time:      {candle.timestamp}"
            )

            print(
                f"Open:      ${candle.open:,.2f}"
            )

            print(
                f"High:      ${candle.high:,.2f}"
            )

            print(
                f"Low:       ${candle.low:,.2f}"
            )

            print(
                f"Close:     ${candle.close:,.2f}"
            )

            print(
                f"Volume:    {candle.volume:.6f}"
            )

            print(
                "============================"
            )


if __name__ == "__main__":
    asyncio.run(main())