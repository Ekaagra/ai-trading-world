from backend.models import Portfolio


class PaperBroker:

    def __init__(
        self,
        portfolio: Portfolio,
        fee_rate: float = 0.001,
        slippage_rate: float = 0.0005,
        
    ):
        self.portfolio = portfolio
        self.fee_rate = fee_rate
        self.slippage_rate = slippage_rate

    def buy(self, symbol: str, quantity: float, market_price: float,timestamp=None):
        execution_price = market_price * (1 + self.slippage_rate)

        gross_cost = execution_price * quantity
        fee = gross_cost * self.fee_rate
        total_cost = gross_cost + fee

        if total_cost > self.portfolio.cash:
            raise ValueError("Insufficient cash")

        position = self.portfolio.get_position(symbol)

        old_quantity = position.quantity
        old_average = position.average_price

        new_quantity = old_quantity + quantity

        if new_quantity > 0:
            position.average_price = (
                (old_quantity * old_average)
                + (quantity * execution_price)
            ) / new_quantity

        position.quantity = new_quantity

        self.portfolio.cash -= total_cost

        return {
            "symbol": symbol,
            "side": "BUY",
            "quantity": quantity,
            "market_price": market_price,
            "execution_price": execution_price,
            "fee": fee,
            "total_cost": total_cost,
            "timestamp": timestamp,
        }

    def sell(self, symbol: str, quantity: float, market_price: float,timestamp=None,exit_reason="SIGNAL",exit_message=""):
        position = self.portfolio.get_position(symbol)

        if quantity > position.quantity:
            raise ValueError("Insufficient position")

        execution_price = market_price * (1 - self.slippage_rate)

        gross_value = execution_price * quantity
        fee = gross_value * self.fee_rate
        net_value = gross_value - fee

        pnl = (
            execution_price - position.average_price
        ) * quantity - fee

        position.quantity -= quantity

        self.portfolio.cash += net_value
        self.portfolio.realized_pnl += pnl

        if position.quantity == 0:
            position.average_price = 0.0

        return {
            "symbol": symbol,
            "side": "SELL",
            "quantity": quantity,
            "market_price": market_price,
            "execution_price": execution_price,
            "fee": fee,
            "realized_pnl": pnl,
            "net_value": net_value,
            "timestamp": timestamp,
            "exit_reason": exit_reason,
            "exit_message": exit_message,
        }

    def portfolio_value(self, market_prices: dict[str, float]):
        value = self.portfolio.cash

        for symbol, position in self.portfolio.positions.items():
            price = market_prices.get(symbol)

            if price is None:
                continue

            value += position.quantity * price

        return value

    def unrealized_pnl(self, market_prices: dict[str, float]):
        pnl = 0.0

        for symbol, position in self.portfolio.positions.items():
            if position.quantity <= 0:
                continue

            price = market_prices.get(symbol)

            if price is None:
                continue

            pnl += (
                price - position.average_price
            ) * position.quantity

        return pnl