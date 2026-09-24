from unittest import result
from .backtest import BacktestEngine
from .market.historical import HistoricalMarketData
from .regime_performance import RegimePerformanceAnalyzer

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
            f"Reason: {trade.exit_reason} | "
            f"Regime: {trade.regime}"
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


    # =========================
    # PLOT EQUITY CURVE
    # =========================

    timestamps = [
        snapshot.timestamp
        for snapshot in result.equity_curve
    ]

    equity_values = [
        snapshot.equity
        for snapshot in result.equity_curve
    ]

    plt.figure(figsize=(14, 7))

    plt.plot(
        timestamps,
        equity_values,
        label="Equity"
    )

    for trade in result.completed_trade_details:

        entry_time = trade.entry_timestamp
        exit_time = trade.exit_timestamp

        entry_snapshot = min(
            result.equity_curve,
            key=lambda snapshot: abs(
                (snapshot.timestamp - entry_time).total_seconds()
            )
        )

        exit_snapshot = min(
            result.equity_curve,
            key=lambda snapshot: abs(
                (snapshot.timestamp - exit_time).total_seconds()
            )
        )

        plt.scatter(
            entry_snapshot.timestamp,
            entry_snapshot.equity,
            marker="^",
            s=80,
            label="BUY" if "BUY" not in plt.gca().get_legend_handles_labels()[1] else ""
        )

        if trade.exit_reason == "STOP_LOSS":
            marker = "v"
            label = "STOP_LOSS"
        elif trade.exit_reason == "TAKE_PROFIT":
            marker = "v"
            label = "TAKE_PROFIT"
        else:
            marker = "v"
            label = "SELL"

        existing_labels = plt.gca().get_legend_handles_labels()[1]

        plt.scatter(
            exit_snapshot.timestamp,
            exit_snapshot.equity,
            marker=marker,
            s=80,
            label=label if label not in existing_labels else ""
        )

    plt.title("Backtest Equity Curve with Trade Markers")
    plt.xlabel("Time")
    plt.ylabel("Equity ($)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.show()


    # =========================
    # PLOT DRAWDOWN
    # =========================

    drawdown_values = [
        snapshot.drawdown_percent
        for snapshot in result.equity_curve
    ]

    plt.figure(figsize=(14, 6))
    plt.plot(timestamps, drawdown_values)

    plt.title("Backtest Drawdown")
    plt.xlabel("Time")
    plt.ylabel("Drawdown (%)")
    plt.grid(True)
    plt.tight_layout()

    plt.show()

    print("\n========== TRADE ANALYTICS ==========")

    print(
        f"Average winning trade: "
        f"${result.average_winning_trade:,.2f}"
    )

    print(
        f"Average losing trade:  "
        f"${result.average_losing_trade:,.2f}"
    )

    print(
        f"Largest winning trade: "
        f"${result.largest_winning_trade:,.2f}"
    )

    print(
        f"Largest losing trade:  "
        f"${result.largest_losing_trade:,.2f}"
    )

    print(
        f"Total winning P&L:     "
        f"${result.total_winning_pnl:,.2f}"
    )

    print(
        f"Total losing P&L:      "
        f"${result.total_losing_pnl:,.2f}"
    )

    average_holding_time = result.average_holding_time_seconds

    hours = int(average_holding_time // 3600)
    minutes = int((average_holding_time % 3600) // 60)
    seconds = int(average_holding_time % 60)

    print(
        f"Average holding time:  "
        f"{hours}:{minutes:02d}:{seconds:02d}"
    )

    print("======================================")

    print("\n========== STRATEGY DIAGNOSTICS ==========")

    print(
        f"Expectancy per trade: "
        f"${result.expectancy:,.2f}"
    )

    print(
        f"Payoff ratio:         "
        f"{result.payoff_ratio:.2f}"
    )

    print(
        f"Profit factor:        "
        f"{result.profit_factor:.2f}"
    )

    print(
        f"Win rate:             "
        f"{result.win_rate:.2f}%"
    )

    print(
        f"Total winning P&L:    "
        f"${result.total_winning_pnl:,.2f}"
    )

    print(
        f"Total losing P&L:     "
        f"${result.total_losing_pnl:,.2f}"
    )

    print("==========================================")

    regime_analyzer = RegimePerformanceAnalyzer()

    regime_results = regime_analyzer.analyze(
        result.completed_trade_details
    )

    print("\n========== REGIME PERFORMANCE ==========")

    for regime in [
        "TRENDING",
        "RANGING",
        "HIGH_VOLATILITY",
    ]:

        performance = regime_results[regime]

        print(f"\n{regime}")

        print(
            f"Trades:          {performance.trades}"
        )

        print(
            f"Winning trades:  {performance.winning_trades}"
        )

        print(
            f"Losing trades:   {performance.losing_trades}"
        )

        print(
            f"Win rate:        "
            f"{performance.win_rate:.2f}%"
        )

        print(
            f"Total P&L:       "
            f"${performance.total_pnl:,.2f}"
        )

        print(
            f"Average P&L:     "
            f"${performance.average_pnl:,.2f}"
        )

        print(
            f"Expectancy:      "
            f"${performance.expectancy:,.2f}"
        )

    print("\n=========================================")

if __name__ == "__main__":
    main()