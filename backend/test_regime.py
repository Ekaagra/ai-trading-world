from backend.regime import MarketRegimeDetector


def main():
    detector = MarketRegimeDetector()

    test_cases = {
        "TRENDING": [
            100,
            100.3,
            100.7,
            101.2,
            101.8,
            102.3,
            102.9,
            103.5,
            104.1,
            104.8,
            105.4,
            106.0,
            106.7,
            107.3,
            108.0,
            108.6,
            109.3,
            110.0,
            110.7,
            111.4,
        ],
        "RANGING": [
            100,
            100.2,
            99.9,
            100.1,
            100.0,
            100.3,
            99.8,
            100.1,
            99.9,
            100.2,
            100.0,
            100.1,
            99.8,
            100.2,
            100.0,
            100.1,
            99.9,
            100.2,
            100.0,
            100.1,
        ],
        "HIGH_VOLATILITY": [
            100,
            102,
            98,
            103,
            97,
            104,
            96,
            105,
            95,
            106,
            94,
            107,
            93,
            108,
            92,
            109,
            91,
            110,
            90,
            111,
        ],
    }

    for expected, prices in test_cases.items():

        result = detector.detect(prices)

        print(
            f"{expected:18} → "
            f"{result.regime.value:18} "
            f"Trend: {result.trend_strength:+.4f} "
            f"Volatility: {result.volatility:.4f}"
        )


if __name__ == "__main__":
    main()