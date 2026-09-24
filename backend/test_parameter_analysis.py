from backend.market.historical import HistoricalMarketData
from backend.backtest import BacktestEngine
from backend.agents.momentum import MomentumAgent
from backend.parameter_analysis import ParameterAnalyzer


def main():

    market_data = HistoricalMarketData(
        symbol="BTCUSDT",
        interval="1m"
    )

    candles = market_data.fetch(
        limit=5000
    )

    configurations = [
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

    results = []

    for config in configurations:

        print(
            f"\nRunning Momentum "
            f"short={config['short_window']} "
            f"long={config['long_window']} "
            f"threshold={config['signal_threshold']}"
        )

        strategy = MomentumAgent(
            symbol="BTC",
            short_window=config["short_window"],
            long_window=config["long_window"],
            signal_threshold=config["signal_threshold"],
        )

        engine = BacktestEngine(
            initial_capital=100_000,
            strategy=strategy,
        )

        result = engine.run(candles)

        results.append(
            (
                strategy.name,
                config,
                result,
            )
        )

    analyzer = ParameterAnalyzer()

    parameter_results = analyzer.analyze(
        results
    )

    print(
        "\n========== PARAMETER ANALYSIS =========="
    )

    for result in parameter_results:

        print(
            f"\nStrategy: {result.strategy_name}"
        )

        print(
            f"Parameters: {result.parameters}"
        )

        print(
            f"Final Equity: "
            f"${result.final_equity:,.2f}"
        )

        print(
            f"Return: "
            f"{result.total_return_percent:.2f}%"
        )

        print(
            f"Trades: "
            f"{result.completed_trades}"
        )

        print(
            f"Win Rate: "
            f"{result.win_rate:.2f}%"
        )

        print(
            f"Profit Factor: "
            f"{result.profit_factor:.2f}"
        )

        print(
            f"Average Trade P&L: "
            f"${result.average_trade_pnl:.2f}"
        )

        print(
            f"Max Drawdown: "
            f"${result.max_drawdown:.2f}"
        )

        print(
            f"Max Drawdown %: "
            f"{result.max_drawdown_percent:.2f}%"
        )

        print(
            f"Expectancy: "
            f"${result.expectancy:.2f}"
        )

        print(
            f"Payoff Ratio: "
            f"{result.payoff_ratio:.2f}"
        )

    print(
        "\n========================================="
    )


if __name__ == "__main__":
    main()