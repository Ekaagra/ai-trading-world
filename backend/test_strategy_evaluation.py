from backend.market.historical import HistoricalMarketData
from backend.backtest import BacktestEngine
from backend.agents.momentum import MomentumAgent
from backend.strategy_evaluation import StrategyEvaluator


def main():

    market_data = HistoricalMarketData(
        symbol="BTCUSDT",
        interval="1m"
    )

    candles = market_data.fetch(
        limit=5000
    )

    strategy = MomentumAgent(
        symbol="BTC",
        short_window=3,
        long_window=5,
        signal_threshold=0.0005,
    )

    engine = BacktestEngine(
        initial_capital=100_000,
        strategy=strategy,
    )

    result = engine.run(
        candles
    )

    evaluator = StrategyEvaluator()

    evaluation = evaluator.evaluate(
        strategy_name=strategy.name,
        result=result,
    )

    print(
        "\n========== STRATEGY EVALUATION =========="
    )

    print(
        f"Strategy: "
        f"{evaluation.strategy_name}"
    )

    print(
        f"Return: "
        f"{evaluation.total_return_percent:.2f}%"
    )

    print(
        f"Profit Factor: "
        f"{evaluation.profit_factor:.2f}"
    )

    print(
        f"Expectancy: "
        f"${evaluation.expectancy:.2f}"
    )

    print(
        f"Win Rate: "
        f"{evaluation.win_rate:.2f}%"
    )

    print(
        f"Payoff Ratio: "
        f"{evaluation.payoff_ratio:.2f}"
    )

    print(
        f"Completed Trades: "
        f"{evaluation.completed_trades}"
    )

    print(
        f"Max Drawdown: "
        f"${evaluation.max_drawdown:,.2f}"
    )

    print(
        f"Max Drawdown %: "
        f"{evaluation.max_drawdown_percent:.2f}%"
    )

    print(
        f"Average Trade P&L: "
        f"${evaluation.average_trade_pnl:.2f}"
    )

    print(
        "\nRobustness Flags:"
    )

    if evaluation.robustness_flags:

        for flag in evaluation.robustness_flags:
            print(
                f"  - {flag}"
            )

    else:

        print(
            "  None"
        )

    print(
        "\n=========================================="
    )


if __name__ == "__main__":
    main()