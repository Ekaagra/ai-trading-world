from .market.data import MarketDataProvider


def main():

    provider = MarketDataProvider()

    prices = provider.get_prices(
        ["BTC", "ETH", "SOL"]
    )

    print("Real market prices:")

    for symbol, price in prices.items():
        print(
            f"{symbol}: ${price:,.2f}"
        )


if __name__ == "__main__":
    main()