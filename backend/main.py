from .agents.momentum import MomentumAgent
from .market.engine import MarketEngine
from .market.data import MarketDataProvider
from .models import Portfolio
from .paper_broker import PaperBroker
from .risk import RiskEngine
from .trade_history import TradeHistory
from .performance import PerformanceAnalyzer
import time

def print_portfolio(
    portfolio: Portfolio,
    broker: PaperBroker,
    market_prices: dict[str, float],
):
    value = broker.portfolio_value(market_prices)
    unrealized = broker.unrealized_pnl(market_prices)

    print("\n========== PORTFOLIO ==========")
    print(f"Cash:           ${portfolio.cash:,.2f}")
    print(f"Portfolio:      ${value:,.2f}")
    print(f"Realized P&L:   ${portfolio.realized_pnl:,.2f}")
    print(f"Unrealized P&L: ${unrealized:,.2f}")

    print("\nPositions:")

    for symbol, position in portfolio.positions.items():
        if position.quantity > 0:
            print(
                f"  {symbol}: "
                f"{position.quantity:.6f} units "
                f"@ ${position.average_price:,.2f}"
            )

    print("===============================\n")


def main():

    # ==============================
    # 1. MARKET ENGINE
    # ==============================

    data_provider = MarketDataProvider()

    market = MarketEngine(
        symbols=["BTC", "ETH", "SOL"],
        data_provider=data_provider,
    )

    # ==============================
    # 2. TRADING AGENT
    # ==============================

    btc_agent = MomentumAgent(
        symbol="BTC",
        short_window=3,
        long_window=5,
    )

    btc_price_history = [
        market.get_price("BTC")
    ]

    # ==============================
    # 3. PORTFOLIO
    # ==============================

    portfolio = Portfolio(
        initial_cash=100_000,
        cash=100_000,
    )

    # ==============================
    # 4. PAPER BROKER
    # ==============================

    broker = PaperBroker(portfolio)

    # ==============================
    # 5. RISK ENGINE
    # ==============================

    risk_engine = RiskEngine(
        max_position_value=10_000
    )

    # ==============================
    # 6. TRADE HISTORY
    # ==============================

    trade_history = TradeHistory()


    performance = PerformanceAnalyzer(
        initial_capital=portfolio.initial_cash,
        trade_history=trade_history,
    )

    # ==============================
    # INITIAL STATE
    # ==============================

    print("Initial market:")
    print(market.get_prices())

    print_portfolio(
        portfolio,
        broker,
        market.get_prices(),
    )

    # ==============================
    # MARKET LOOP
    # ==============================

    for i in range(10):

        time.sleep(10)

         # ==============================
        # UPDATE MARKET
        # ==============================

        prices = market.update_prices()

        previous_btc_price = btc_price_history[-1]

        current_btc_price = prices["BTC"]

        price_change = (
            current_btc_price
            - previous_btc_price
        )

        price_change_percent = (
            price_change
            / previous_btc_price
        ) * 100

        btc_price_history.append(
            current_btc_price
        )

        print(
            f"BTC change: "
            f"{price_change:+.2f} "
            f"({price_change_percent:+.4f}%)"
        )
        # ==============================
        # AGENT DECISION
        # ==============================

        decision = btc_agent.decide(
            btc_price_history
        )

        print(
            f"\nMarket update #{i + 1}:"
        )

        print(
            market.get_prices()
        )

        print(
            f"Agent decision: "
            f"{decision.action} "
            f"{decision.symbol} "
            f"(confidence={decision.confidence:.4f})"
        )

        # ==============================
        # RISK CHECK
        # ==============================

        risk_decision = risk_engine.check(
            decision=decision,
            portfolio=portfolio,
            market_price=market.get_price(
                decision.symbol
            ),
        )

        print(
            f"Risk: "
            f"{'APPROVED' if risk_decision.approved else 'REJECTED'} "
            f"| {risk_decision.reason}"
        )

        # ==============================
        # TRADE EXECUTION
        # ==============================

        if risk_decision.approved:

            # --------------------------
            # BUY
            # --------------------------

            if decision.action == "BUY":

                trade = broker.buy(
                    symbol=decision.symbol,
                    quantity=risk_decision.quantity,
                    market_price=market.get_price(
                        decision.symbol
                    ),
                )

                # Save trade
                trade_history.record(trade)

                print(
                    f"Trade executed: "
                    f"BUY {trade['quantity']:.6f} "
                    f"{trade['symbol']} "
                    f"@ ${trade['execution_price']:,.2f}"
                )

            # --------------------------
            # SELL
            # --------------------------

            elif decision.action == "SELL":

                trade = broker.sell(
                    symbol=decision.symbol,
                    quantity=risk_decision.quantity,
                    market_price=market.get_price(
                        decision.symbol
                    ),
                )

                # Save trade
                trade_history.record(trade)

                print(
                    f"Trade executed: "
                    f"SELL {trade['quantity']:.6f} "
                    f"{trade['symbol']} "
                    f"@ ${trade['execution_price']:,.2f}"
                )

        # ==============================
        # CURRENT PORTFOLIO
        # ==============================

        print_portfolio(
            portfolio,
            broker,
            market.get_prices(),
        )

    # ==============================
    # TRADE HISTORY
    # ==============================

    print(
        "\n========== TRADE HISTORY =========="
    )

    for i, trade in enumerate(
        trade_history.get_trades(),
        start=1,
    ):
        print(
            f"{i}. "
            f"{trade.side} "
            f"{trade.quantity:.6f} "
            f"{trade.symbol} "
            f"@ ${trade.execution_price:,.2f} "
            f"| Fee: ${trade.fee:.2f} "
            f"| P&L: ${trade.realized_pnl:.2f}"
        )

    print(
        f"\nTotal trades: "
        f"{trade_history.total_trades()}"
    )

    print(
        f"Total realized P&L: "
        f"${trade_history.total_realized_pnl():,.2f}"
    )

    print(
        "==================================="
    )


    # ==============================
    # PERFORMANCE
    # ==============================

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
        f"Winning trades:     "
        f"{report.winning_trades}"
    )

    print(
        f"Losing trades:      "
        f"{report.losing_trades}"
    )

    print(
        f"Win rate:           "
        f"{report.win_rate:.2f}%"
    )

    if report.profit_factor == float("inf"):

        profit_factor_display = "∞"

    else:

        profit_factor_display = (
            f"{report.profit_factor:.2f}"
        )

    print(
        f"Profit factor:      "
        f"{profit_factor_display}"
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


if __name__ == "__main__":
    main()