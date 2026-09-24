from backend.strategies.mean_reversion import MeanReversionStrategy


def main():

    strategy = MeanReversionStrategy(
        symbol="BTC",
        window=5,
        deviation_threshold=0.001
    )

    prices = [
        80000,
        80100,
        80200,
        80150,
        79800,
        79500
    ]

    decision = strategy.decide(prices)

    print("========== MEAN REVERSION TEST ==========")
    print(f"Strategy:   {strategy.name}")
    print(f"Symbol:     {decision.symbol}")
    print(f"Action:     {decision.action}")
    print(f"Confidence: {decision.confidence:.4f}")
    print(f"Deviation:  {decision.momentum:.6f}")
    print("==========================================")


if __name__ == "__main__":
    main()