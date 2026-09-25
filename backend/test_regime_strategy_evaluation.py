from backend.market.historical import (
    HistoricalMarketData,
)

from backend.agents.momentum import (
    MomentumAgent,
)

from backend.backtest import BacktestEngine

from backend.regime_strategy_evaluation import (
    RegimeStrategyEvaluator,
)


def main():

    market_data = HistoricalMarketData(
        symbol="BTCUSDT",
        interval="1m",
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

    evaluator = RegimeStrategyEvaluator()

    evaluation = evaluator.evaluate(
        strategy_name=strategy.name,
        result=result,
    )

    print(
        "\n========== STRATEGY "
        "REGIME EVALUATION =========="
    )

    print(
        f"Strategy: "
        f"{evaluation.strategy_name}"
    )

    for regime in evaluation.regime_results:

        print(
            f"\n---------- "
            f"{regime.regime} ----------"
        )

        print(
            f"Trades: "
            f"{regime.completed_trades}"
        )

        print(
            f"Wins: "
            f"{regime.winning_trades}"
        )

        print(
            f"Losses: "
            f"{regime.losing_trades}"
        )

        print(
            f"Total P&L: "
            f"${regime.total_pnl:,.2f}"
        )

        print(
            f"Average Trade P&L: "
            f"${regime.average_trade_pnl:.2f}"
        )

        print(
            f"Win Rate: "
            f"{regime.win_rate:.2f}%"
        )

        print(
            f"Profit Factor: "
            f"{regime.profit_factor:.2f}"
        )

        print(
            f"Expectancy: "
            f"${regime.expectancy:.2f}"
        )

    print(
        "\n========================================"
    )


if __name__ == "__main__":
    main()