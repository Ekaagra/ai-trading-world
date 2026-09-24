from backend.market.historical import HistoricalMarketData
from backend.backtest import BacktestEngine

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

    print("\n========== MOMENTUM ==========")

    momentum = MomentumAgent(
        symbol="BTC",
        short_window=3,
        long_window=5
    )

    momentum_result = run_strategy(momentum)

    print(
        f"Final Equity: "
        f"${momentum_result.final_equity:,.2f}"
    )

    print(
        f"Return: "
        f"{momentum_result.total_return_percent:.2f}%"
    )

    print(
        f"Trades: "
        f"{momentum_result.completed_trades}"
    )

    print(
        f"Win Rate: "
        f"{momentum_result.win_rate:.2f}%"
    )

    print(
        f"Profit Factor: "
        f"{momentum_result.profit_factor:.2f}"
    )

    print("\n========== MEAN REVERSION ==========")

    mean_reversion = MeanReversionStrategy(
        symbol="BTC",
        window=5,
        deviation_threshold=0.001
    )

    mean_result = run_strategy(mean_reversion)

    print(
        f"Final Equity: "
        f"${mean_result.final_equity:,.2f}"
    )

    print(
        f"Return: "
        f"{mean_result.total_return_percent:.2f}%"
    )

    print(
        f"Trades: "
        f"{mean_result.completed_trades}"
    )

    print(
        f"Win Rate: "
        f"{mean_result.win_rate:.2f}%"
    )

    print(
        f"Profit Factor: "
        f"{mean_result.profit_factor:.2f}"
    )


if __name__ == "__main__":
    main()