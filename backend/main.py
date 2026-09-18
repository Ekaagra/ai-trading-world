from .agents.momentum import MomentumAgent
from .market.engine import MarketEngine
from .models import Portfolio
from .paper_broker import PaperBroker
from .risk import RiskEngine
from .trade_history import TradeHistory


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

    market = MarketEngine(
        initial_prices={
            "BTC": 115_000,
            "ETH": 4_500,
            "SOL": 200,
        }
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

        # Update market prices
        market.update_prices()

        # Add latest BTC price to history
        btc_price_history.append(
            market.get_price("BTC")
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


if __name__ == "__main__":
    main()