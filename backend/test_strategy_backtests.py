from backend.market.historical import HistoricalMarketData
from backend.backtest import BacktestEngine
from backend.strategy_comparison import StrategyComparisonEngine

from backend.agents.momentum import MomentumAgent
from backend.strategies.mean_reversion import MeanReversionStrategy


def run_strategy(strategy):

    market_data = HistoricalMarketData(
        symbol="BTCUSDT",
        interval="1m"
    )

    candles = market_data.fetch(
        limit=5000
    )

    engine = BacktestEngine(
        initial_capital=100_000,
        strategy=strategy
    )

    return engine.run(candles)

def main():

    market_data = HistoricalMarketData(
        symbol="BTCUSDT",
        interval="1m"
    )

    candles = market_data.fetch(
        limit=5000
    )

    momentum = MomentumAgent(
        symbol="BTC",
        short_window=3,
        long_window=5
    )

    mean_reversion = MeanReversionStrategy(
        symbol="BTC",
        window=5,
        deviation_threshold=0.001
    )

    momentum_engine = BacktestEngine(
        initial_capital=100_000,
        strategy=momentum
    )

    mean_reversion_engine = BacktestEngine(
        initial_capital=100_000,
        strategy=mean_reversion
    )

    momentum_result = momentum_engine.run(candles)

    mean_reversion_result = mean_reversion_engine.run(candles)

    results = {
        momentum.name: momentum_result,
        mean_reversion.name: mean_reversion_result,
    }

    comparison_engine = StrategyComparisonEngine()

    comparisons = comparison_engine.compare(
        results
    )

    print("\n========== STRATEGY COMPARISON ==========")

    for comparison in comparisons:

        print(
            f"\n{comparison.strategy_name}"
        )

        print(
            f"Final Equity:       "
            f"${comparison.final_equity:,.2f}"
        )

        print(
            f"Return:             "
            f"{comparison.total_return_percent:.2f}%"
        )

        print(
            f"Completed Trades:   "
            f"{comparison.completed_trades}"
        )

        print(
            f"Win Rate:           "
            f"{comparison.win_rate:.2f}%"
        )

        print(
            f"Profit Factor:      "
            f"{comparison.profit_factor:.2f}"
        )

        print(
            f"Average Trade P&L:  "
            f"${comparison.average_trade_pnl:.2f}"
        )

        print(
            f"Max Drawdown:       "
            f"${comparison.max_drawdown:.2f}"
        )

        print(
            f"Max Drawdown %:     "
            f"{comparison.max_drawdown_percent:.2f}%"
        )

        print(
            f"Expectancy:         "
            f"${comparison.expectancy:.2f}"
        )

        print(
            f"Payoff Ratio:       "
            f"{comparison.payoff_ratio:.2f}"
        )

    print("\n==========================================")


if __name__ == "__main__":
    main()