from collections import Counter
import statistics

from backend.market.historical import HistoricalMarketData
from backend.regime import MarketRegimeDetector


def main():

    market_data = HistoricalMarketData(
        symbol="BTCUSDT",
        interval="1m",
    )

    candles = market_data.fetch(limit=5000)

    detector = MarketRegimeDetector()

    prices = []
    regimes = []
    volatility_values = []

    for candle in candles:

        prices.append(candle["close"])

        result = detector.detect(prices)

        regimes.append(
            result.regime.value
        )

        volatility_values.append(
            result.volatility
        )

    regime_counts = Counter(regimes)

    print("\n========== MARKET REGIME ANALYSIS ==========")

    print(
        f"Total candles: {len(candles)}"
    )

    for regime in [
        "TRENDING",
        "RANGING",
        "HIGH_VOLATILITY",
    ]:

        count = regime_counts.get(
            regime,
            0,
        )

        percentage = (
            count / len(regimes) * 100
            if regimes
            else 0
        )

        print(
            f"{regime:18} "
            f"{count:5} candles "
            f"({percentage:6.2f}%)"
        )

    print("============================================")

    print("\n========== VOLATILITY STATISTICS ==========")

    if volatility_values:

        print(
            f"Minimum volatility: "
            f"{min(volatility_values):.6f}"
        )

        print(
            f"Average volatility: "
            f"{statistics.mean(volatility_values):.6f}"
        )

        print(
            f"Maximum volatility: "
            f"{max(volatility_values):.6f}"
        )

    else:

        print("No volatility data available.")

    print("============================================")


if __name__ == "__main__":
    main()