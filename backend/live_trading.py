import asyncio

from .agents.momentum import MomentumAgent
from .market.aggregator import CandleAggregator
from .market.engine import MarketEngine
from .market.stream import MarketStream
from .models import Portfolio
from .paper_broker import PaperBroker
from .risk import RiskEngine
from .trade_history import TradeHistory
from .equity import EquityTracker
from .performance import PerformanceAnalyzer

def print_performance(performance):

    report = performance.calculate()

    print("\n========== PERFORMANCE ==========")

    print(
        f"Executions:         "
        f"{report.execution_count}"
    )

    print(
        f"Completed trades:   "
        f"{report.completed_trades}"
    )

    print(
        f"Open trades:        "
        f"{report.open_trades}"
    )

    print(
        f"Realized P&L:       "
        f"${report.total_realized_pnl:,.2f}"
    )

    print(
        f"Current equity:     "
        f"${report.current_equity:,.2f}"
    )

    print(
        f"Peak equity:        "
        f"${report.peak_equity:,.2f}"
    )

    print(
        f"Current drawdown:   "
        f"${report.current_drawdown:,.2f}"
    )

    print(
        f"Current DD %:       "
        f"{report.current_drawdown_percent:.2f}%"
    )

    print(
        f"Maximum drawdown:   "
        f"${report.max_drawdown:,.2f}"
    )

    print(
        f"Maximum DD %:       "
        f"{report.max_drawdown_percent:.2f}%"
    )

    print(
        f"Win rate:           "
        f"{report.win_rate:.2f}%"
    )

    if report.profit_factor == float("inf"):
        profit_factor = "∞"
    else:
        profit_factor = (
            f"{report.profit_factor:.2f}"
        )

    print(
        f"Profit factor:      "
        f"{profit_factor}"
    )

    print(
        f"Average trade P&L:  "
        f"${report.average_trade_pnl:,.2f}"
    )

    print(
        f"Return:             "
        f"{report.return_percent:.4f}%"
    )

    print(
        "================================="
    )
async def main():

    symbols = [
        "BTC",
        "ETH",
        "SOL",
    ]

    # ==============================
    # MARKET
    # ==============================

    stream = MarketStream(
        symbols=symbols
    )

    aggregator = CandleAggregator(
        interval_seconds=60
    )

    market = MarketEngine(
        symbols=symbols
    )

    # ==============================
    # AGENT
    # ==============================

    btc_agent = MomentumAgent(
        symbol="BTC",
        short_window=3,
        long_window=5,
    )

    btc_close_history = []

    # ==============================
    # PORTFOLIO
    # ==============================

    portfolio = Portfolio(
        initial_cash=100_000,
        cash=100_000,
    )

    equity_tracker = EquityTracker(
        initial_equity=portfolio.initial_cash
    )

    broker = PaperBroker(
        portfolio
    )

    # ==============================
    # RISK
    # ==============================

    risk_engine = RiskEngine(
        max_position_value=10_000,
        min_order_value=10,
        stop_loss_percent=0.01,
        take_profit_percent=0.02,
    )

    # ==============================
    # TRADE HISTORY
    # ==============================

    trade_history = TradeHistory()

    # ==============================
    # PERFORMANCE
    # ==============================

    performance = PerformanceAnalyzer(
        initial_capital=portfolio.initial_cash,
        trade_history=trade_history,
        equity_tracker=equity_tracker,
    )

    print(
        "Starting live candle trading system..."
    )

    print(
        "Waiting for market data..."
    )

    # ==============================
    # LIVE MARKET STREAM
    # ==============================

    async for event in stream.connect():

        symbol = event["symbol"]
        price = event["price"]

        # ==============================
        # UPDATE MARKET STATE
        # ==============================

        market.update_price(
            symbol=symbol,
            price=price,
        )

        # ==============================
        # AGGREGATE TRADE
        # ==============================

        candle = aggregator.update(
            symbol=symbol,
            price=price,
            quantity=event["quantity"],
            timestamp=event["timestamp"],
        )

        # No completed candle yet
        if candle is None:
            continue

        print(
            "\n========== NEW CANDLE =========="
        )

        print(
            f"Symbol: {candle.symbol}"
        )

        print(
            f"Time:   {candle.timestamp}"
        )

        print(
            f"Open:   ${candle.open:,.2f}"
        )

        print(
            f"High:   ${candle.high:,.2f}"
        )

        print(
            f"Low:    ${candle.low:,.2f}"
        )

        print(
            f"Close:  ${candle.close:,.2f}"
        )

        print(
            f"Volume: {candle.volume:.6f}"
        )

        print(
            "================================"
        )

        # ==============================
        # ONLY BTC FOR CURRENT AGENT
        # ==============================

        if candle.symbol != "BTC":
            continue

        equity = broker.portfolio_value(
            market_prices={
                "BTC": candle.close
            }
        )

        equity_snapshot = equity_tracker.update(
            equity
        )

        print(
            f"Equity: ${equity_snapshot.equity:,.2f} | "
            f"Drawdown: "
            f"{equity_snapshot.drawdown_percent:.2f}%"
        )

        # Use candle close for strategy
        btc_close_history.append(
            candle.close
        )

        # ==============================
        # WAIT FOR ENOUGH DATA
        # ==============================

        if len(btc_close_history) < 5:

            print(
                f"Waiting for history: "
                f"{len(btc_close_history)}/5"
            )

            continue

        exit_decision = risk_engine.check_exit_conditions(
            symbol="BTC",
            portfolio=portfolio,
            market_price=candle.close,
        )

        if exit_decision.approved:

            trade = broker.sell(
                symbol="BTC",
                quantity=exit_decision.quantity,
                market_price=candle.close,
            )

            trade_history.record(trade)

            print(
                f"RISK EXIT: {exit_decision.reason}"
            )

            print(
                f"EXECUTED SELL: "
                f"{trade['quantity']:.6f} BTC "
                f"at ${trade['execution_price']:,.2f}"
            )

            continue

        # ==============================
        # AGENT DECISION
        # ==============================

        decision = btc_agent.decide(
            btc_close_history
        )

        print(
            f"Agent: {decision.action} "
            f"{decision.symbol} | "
            f"momentum={decision.momentum * 100:.4f}% | "
            f"confidence={decision.confidence:.4f}"
        )

        # ==============================
        # RISK CHECK
        # ==============================

        risk_decision = risk_engine.check(
            decision=decision,
            portfolio=portfolio,
            market_price=candle.close,
        )

        print(
            f"Risk: "
            f"{'APPROVED' if risk_decision.approved else 'REJECTED'} "
            f"| {risk_decision.reason}"
        )

        # ==============================
        # TRADE EXECUTION
        # ==============================

        if not risk_decision.approved:
            continue

        # ------------------------------
        # BUY
        # ------------------------------

        if decision.action == "BUY":

            trade = broker.buy(
                symbol=decision.symbol,
                quantity=risk_decision.quantity,
                market_price=candle.close,
            )

            trade_history.record(
                trade
            )

            print(
                f"EXECUTED BUY: "
                f"{trade['quantity']:.6f} "
                f"{trade['symbol']} "
                f"@ ${trade['execution_price']:,.2f}"
            )

        # ------------------------------
        # SELL
        # ------------------------------

        elif decision.action == "SELL":

            trade = broker.sell(
                symbol=decision.symbol,
                quantity=risk_decision.quantity,
                market_price=candle.close,
            )

            trade_history.record(
                trade
            )

            print(
                f"EXECUTED SELL: "
                f"{trade['quantity']:.6f} "
                f"{trade['symbol']} "
                f"@ ${trade['execution_price']:,.2f}"
            )


if __name__ == "__main__":
    asyncio.run(main())