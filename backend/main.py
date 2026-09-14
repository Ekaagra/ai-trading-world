from backend.models import Portfolio
from backend.paper_broker import PaperBroker


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
    portfolio = Portfolio(
        initial_cash=100_000,
        cash=100_000,
    )

    broker = PaperBroker(portfolio)

    market_prices = {
        "BTC": 115_000,
        "ETH": 4_500,
    }

    print("Initial state:")
    print_portfolio(
        portfolio,
        broker,
        market_prices,
    )

    print("Buying BTC...")

    trade = broker.buy(
        symbol="BTC",
        quantity=0.05,
        market_price=market_prices["BTC"],
    )

    print(trade)

    print_portfolio(
        portfolio,
        broker,
        market_prices,
    )

    print("BTC price moves...")

    market_prices["BTC"] = 117_000

    print_portfolio(
        portfolio,
        broker,
        market_prices,
    )

    print("Selling BTC...")

    trade = broker.sell(
        symbol="BTC",
        quantity=0.05,
        market_price=market_prices["BTC"],
    )

    print(trade)

    print_portfolio(
        portfolio,
        broker,
        market_prices,
    )


if __name__ == "__main__":
    main()