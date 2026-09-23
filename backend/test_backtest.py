from unittest import result
from .backtest import BacktestEngine
from .market.historical import HistoricalMarketData
from collections import Counter
import matplotlib.pyplot as plt


def main():

    # =========================
    # GET HISTORICAL DATA
    # =========================

    market = HistoricalMarketData(
        symbol="BTCUSDT",
        interval="1m",
    )

    candles = market.fetch(
        limit=5000
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

    print("\n========== COMPLETED TRADES ==========")

    for i, trade in enumerate(
        result.completed_trade_details,
        start=1,
    ):

        duration = (
            trade.exit_timestamp
            - trade.entry_timestamp
        )

        print(
            f"Trade #{i} | "
            f"{trade.symbol} | "
            f"Entry: ${trade.entry_price:,.2f} | "
            f"Exit: ${trade.exit_price:,.2f} | "
            f"P&L: ${trade.realized_pnl:,.2f} | "
            f"Duration: {duration} | "
            f"Reason: {trade.exit_reason}"
        )

    print("=======================================")

    exit_reasons = Counter(
        trade.exit_reason
        for trade in result.completed_trade_details
    )

    print("\n========== EXIT REASONS ==========")

    for reason in [
        "SIGNAL",
        "STOP_LOSS",
        "TAKE_PROFIT",
    ]:
        print(
            f"{reason}: "
            f"{exit_reasons.get(reason, 0)}"
        )

    print("==================================")

    print("\n========== EQUITY CURVE ==========")

    print(
        f"Snapshots: "
        f"{len(result.equity_curve)}"
    )

    if result.equity_curve:

        first = result.equity_curve[0]
        last = result.equity_curve[-1]

        print(
            f"Start: {first.timestamp} | "
            f"Equity: ${first.equity:,.2f}"
        )

        print(
            f"End:   {last.timestamp} | "
            f"Equity: ${last.equity:,.2f}"
        )

    print("==================================")

    timestamps = [snapshot.timestamp for snapshot in result.equity_curve]
    equity_values = [snapshot.equity for snapshot in result.equity_curve]

    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, equity_values)

    plt.title("Backtest Equity Curve")
    plt.xlabel("Time")
    plt.ylabel("Equity ($)")
    plt.grid(True)
    plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    main()