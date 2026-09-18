from .agents.momentum import MomentumAgent
from .market.engine import MarketEngine
from .models import Portfolio
from .paper_broker import PaperBroker
from .risk import RiskEngine


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

    # -------------------------
    # MARKET
    # -------------------------

    market = MarketEngine(
        initial_prices={
            "BTC": 115_000,
            "ETH": 4_500,
            "SOL": 200,
        }
    )

    # -------------------------
    # AGENT
    # -------------------------

    btc_agent = MomentumAgent(
        symbol="BTC",
        short_window=3,
        long_window=5,
    )

    btc_price_history = [
        market.get_price("BTC")
    ]

    # -------------------------
    # PORTFOLIO
    # -------------------------

    portfolio = Portfolio(
        initial_cash=100_000,
        cash=100_000,
    )

    broker = PaperBroker(portfolio)

    # -------------------------
    # RISK ENGINE
    # -------------------------

    risk_engine = RiskEngine(
        max_position_value=10_000
    )

    # -------------------------
    # INITIAL STATE
    # -------------------------

    print("Initial market:")
    print(market.get_prices())

    print_portfolio(
        portfolio,
        broker,
        market.get_prices(),
    )

    # -------------------------
    # MARKET LOOP
    # -------------------------

    for i in range(10):

        # Update market prices
        market.update_prices()

        # Add new BTC price to history
        btc_price_history.append(
            market.get_price("BTC")
        )

        # -------------------------
        # AGENT DECISION
        # -------------------------

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

        # -------------------------
        # RISK CHECK
        # -------------------------

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

        # -------------------------
        # EXECUTE TRADE
        # -------------------------

        if risk_decision.approved:

            if decision.action == "BUY":

                trade = broker.buy(
                    symbol=decision.symbol,
                    quantity=risk_decision.quantity,
                    market_price=market.get_price(
                        decision.symbol
                    ),
                )

                print(
                    f"Trade executed: "
                    f"BUY {trade['quantity']:.6f} "
                    f"{trade['symbol']} "
                    f"@ ${trade['execution_price']:,.2f}"
                )

            elif decision.action == "SELL":

                trade = broker.sell(
                    symbol=decision.symbol,
                    quantity=risk_decision.quantity,
                    market_price=market.get_price(
                        decision.symbol
                    ),
                )

                print(
                    f"Trade executed: "
                    f"SELL {trade['quantity']:.6f} "
                    f"{trade['symbol']} "
                    f"@ ${trade['execution_price']:,.2f}"
                )

        # -------------------------
        # PORTFOLIO AFTER UPDATE
        # -------------------------

        print_portfolio(
            portfolio,
            broker,
            market.get_prices(),
        )


if __name__ == "__main__":
    main()