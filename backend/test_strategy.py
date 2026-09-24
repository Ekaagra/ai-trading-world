from .agents.momentum import MomentumAgent


def main():

    strategy = MomentumAgent(
        symbol="BTC",
        short_window=3,
        long_window=5
    )

    prices = [
        80000,
        80100,
        80200,
        80400,
        80600,
        80800
    ]

    decision = strategy.decide(prices)

    print("========== STRATEGY TEST ==========")
    print(f"Strategy:   {strategy.name}")
    print(f"Symbol:     {decision.symbol}")
    print(f"Action:     {decision.action}")
    print(f"Confidence: {decision.confidence:.4f}")
    print(f"Momentum:   {decision.momentum:.6f}")
    print("===================================")


if __name__ == "__main__":
    main()