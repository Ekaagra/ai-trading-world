from backend.market.historical import HistoricalMarketData
from backend.agents.momentum import MomentumAgent
from backend.walk_forward import WalkForwardTester


def create_momentum_strategy(parameters):

    return MomentumAgent(
        symbol="BTC",
        short_window=parameters["short_window"],
        long_window=parameters["long_window"],
        signal_threshold=parameters["signal_threshold"],
    )


def main():

    market_data = HistoricalMarketData(
        symbol="BTCUSDT",
        interval="1m"
    )

    candles = market_data.fetch(
        limit=5000
    )

    parameter_configurations = [
        {
            "short_window": 3,
            "long_window": 5,
            "signal_threshold": 0.0005,
        },
        {
            "short_window": 5,
            "long_window": 10,
            "signal_threshold": 0.0005,
        },
        {
            "short_window": 10,
            "long_window": 20,
            "signal_threshold": 0.0005,
        },
    ]

    tester = WalkForwardTester(
        initial_capital=100_000,
        train_size=3500,
        test_size=1500,
    )

    result = tester.run(
        candles=candles,
        strategy_factory=create_momentum_strategy,
        parameter_configurations=parameter_configurations,
    )

    print(
        "\n========== WALK-FORWARD TEST =========="
    )

    print(
        f"Strategy: "
        f"{result.strategy_name}"
    )

    print(
        f"Train Candles: "
        f"{result.train_candles}"
    )

    print(
        f"Test Candles: "
        f"{result.test_candles}"
    )

    print(
        f"\nSelected Parameters:"
    )

    print(
        result.selected_parameters
    )

    print(
        "\n========== TRAINING RESULT =========="
    )

    print(
        f"Train Return: "
        f"{result.train_result.total_return_percent:.2f}%"
    )

    print(
        f"Train Trades: "
        f"{result.train_result.completed_trades}"
    )

    print(
        f"Train Profit Factor: "
        f"{result.train_result.profit_factor:.2f}"
    )

    print(
        f"Train Expectancy: "
        f"${result.train_result.expectancy:.2f}"
    )

    print(
        "\n========== OUT-OF-SAMPLE RESULT =========="
    )

    print(
        f"Test Final Equity: "
        f"${result.test_result.final_equity:,.2f}"
    )

    print(
        f"Test Return: "
        f"{result.test_result.total_return_percent:.2f}%"
    )

    print(
        f"Test Trades: "
        f"{result.test_result.completed_trades}"
    )

    print(
        f"Test Win Rate: "
        f"{result.test_result.win_rate:.2f}%"
    )

    print(
        f"Test Profit Factor: "
        f"{result.test_result.profit_factor:.2f}"
    )

    print(
        f"Test Max Drawdown: "
        f"${result.test_result.max_drawdown:,.2f}"
    )

    print(
        f"Test Expectancy: "
        f"${result.test_result.expectancy:.2f}"
    )

    print(
        "\n=========================================="
    )


if __name__ == "__main__":
    main()