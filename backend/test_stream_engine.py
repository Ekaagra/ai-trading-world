import asyncio

from .market.stream import MarketStream
from .market.engine import MarketEngine


async def main():

    symbols = [
        "BTC",
        "ETH",
        "SOL",
    ]

    stream = MarketStream(
        symbols=symbols
    )

    market = MarketEngine(
        symbols=symbols
    )

    async for event in stream.connect():

        symbol = event["symbol"]
        price = event["price"]

        # Update market state
        market.update_price(
            symbol=symbol,
            price=price,
        )

        print(
            f"Updated: "
            f"{symbol} = ${price:,.2f}"
        )

        print(
            "Current market:",
            market.get_prices()
        )


if __name__ == "__main__":
    asyncio.run(main())