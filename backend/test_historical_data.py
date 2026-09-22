from .market.historical import HistoricalMarketData


def main():

    market = HistoricalMarketData(
        symbol="BTCUSDT",
        interval="1m",
    )

    candles = market.fetch(limit=10)

    print("\n========== HISTORICAL DATA ==========")

    for candle in candles:
        print(
            f"Close: ${candle['close']:,.2f} "
            f"| Volume: {candle['volume']:.4f}"
        )

    print(f"\nCandles received: {len(candles)}")
    print("=====================================")


if __name__ == "__main__":
    main()