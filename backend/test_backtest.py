from .backtest import BacktestEngine


def main():

    candles = [
        {"close": 100},
        {"close": 101},
        {"close": 102},
        {"close": 103},
        {"close": 104},
        {"close": 106},
        {"close": 108},
        {"close": 110},
        {"close": 109},
        {"close": 107},
        {"close": 105},
    ]

    engine = BacktestEngine(
        initial_capital=100_000
    )

    result = engine.run(
        candles
    )

    print(
        "\n========== BACKTEST =========="
    )

    print(
        f"Initial capital: "
        f"${result.initial_capital:,.2f}"
    )

    print(
        f"Final equity:    "
        f"${result.final_equity:,.2f}"
    )

    print(
        f"Return:          "
        f"{result.total_return_percent:.2f}%"
    )

    print(
        f"Executions:      "
        f"{result.total_trades}"
    )

    print(
        f"Completed trades:"
        f" {result.completed_trades}"
    )
    print(
        f"Max drawdown:    "
        f"${result.max_drawdown:,.2f}"
    )

    print(
        f"Max DD %:        "
        f"{result.max_drawdown_percent:.2f}%"
    )

    print(
        "=============================="
    )


if __name__ == "__main__":
    main()