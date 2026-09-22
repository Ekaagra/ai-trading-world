from unittest import result
from .backtest import BacktestEngine
from .market.historical import HistoricalMarketData


def main():

    # =========================
    # GET HISTORICAL DATA
    # =========================

    market = HistoricalMarketData(
        symbol="BTCUSDT",
        interval="1m",
    )

    candles = market.fetch(
        limit=500
    )

    print("\n========== HISTORICAL BACKTEST ==========")
    print(f"Candles: {len(candles)}")

    # =========================
    # RUN BACKTEST
    # =========================

    engine = BacktestEngine(
        initial_capital=100_000
    )

    result = engine.run(
        candles
    )

    # =========================
    # RESULTS
    # =========================

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
        f"Winning trades:   "
        f"{result.winning_trades}"
    )

    print(
        f"Losing trades:    "
        f"{result.losing_trades}"
    )

    print(
        f"Win rate:         "
        f"{result.win_rate:.2f}%"
    )

    print(
        f"Profit factor:    "
        f"{result.profit_factor:.2f}"
    )

    print(
        f"Average trade:    "
        f"${result.average_trade_pnl:,.2f}"
    )

    print(
        f"Realized P&L:     "
        f"${result.total_realized_pnl:,.2f}"
    )

    print(
        f"Max drawdown:    "
        f"${result.max_drawdown:,.2f}"
    )

    print(
        f"Max DD %:        "
        f"{result.max_drawdown_percent:.2f}%"
    )

    print("==========================================")


if __name__ == "__main__":
    main()