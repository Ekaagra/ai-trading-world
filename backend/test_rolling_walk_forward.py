from backend.market.historical import HistoricalMarketData
from backend.agents.momentum import MomentumAgent
from backend.rolling_walk_forward import (
    RollingWalkForwardTester,
)


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

    tester = RollingWalkForwardTester(
        initial_capital=100_000,
        train_size=2000,
        test_size=1000,
        step_size=1000,
    )

    result = tester.run(
        candles=candles,
        strategy_factory=create_momentum_strategy,
        parameter_configurations=(
            parameter_configurations
        ),
    )

    print(
        "\n========== ROLLING "
        "WALK-FORWARD =========="
    )

    print(
        f"Strategy: "
        f"{result.strategy_name}"
    )

    print(
        f"Windows: "
        f"{len(result.windows)}"
    )

    for window in result.windows:

        print(
            f"\n---------- WINDOW "
            f"{window.window_number} ----------"
        )

        print(
            f"Train: "
            f"{window.train_start} → "
            f"{window.train_end}"
        )

        print(
            f"Test:  "
            f"{window.test_start} → "
            f"{window.test_end}"
        )

        print(
            f"Selected Parameters: "
            f"{window.selected_parameters}"
        )

        print(
            f"Robust Selection Failed: "
            f"{window.robust_selection_failed}"
        )

        print(
            f"Test Return: "
            f"{window.test_result.total_return_percent:.2f}%"
        )

        print(
            f"Test Trades: "
            f"{window.test_result.completed_trades}"
        )

        print(
            f"Test Win Rate: "
            f"{window.test_result.win_rate:.2f}%"
        )

        print(
            f"Test Profit Factor: "
            f"{window.test_result.profit_factor:.2f}"
        )

        print(
            f"Test Expectancy: "
            f"${window.test_result.expectancy:.2f}"
        )

        print(
            f"Test Max Drawdown: "
            f"${window.test_result.max_drawdown:,.2f}"
        )

        print(
            "Flags:"
        )

        if window.evaluation.robustness_flags:

            for flag in (
                window.evaluation.robustness_flags
            ):
                print(
                    f"  - {flag}"
                )

        else:

            print(
                "  None"
            )

    print(
        "\n========== AGGREGATED =========="
    )

    print(
        f"Total Test Trades: "
        f"{result.total_test_trades}"
    )

    print(
        f"Total Test P&L: "
        f"${result.total_test_pnl:,.2f}"
    )

    print(
        f"Average Test Return: "
        f"{result.average_test_return_percent:.2f}%"
    )

    print(
        f"Average Test Expectancy: "
        f"${result.average_test_expectancy:.2f}"
    )

    print(
        f"Average Test Drawdown: "
        f"{result.average_test_drawdown_percent:.2f}%"
    )

    print(
        "\n================================"
    )


if __name__ == "__main__":
    main()