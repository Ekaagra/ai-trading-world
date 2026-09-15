import random
from dataclasses import dataclass


@dataclass
class MarketState:
    prices: dict[str, float]


class MarketEngine:

    def __init__(self, initial_prices: dict[str, float]):
        self.state = MarketState(
            prices=initial_prices.copy()
        )

    def get_price(self, symbol: str) -> float:
        if symbol not in self.state.prices:
            raise ValueError(f"Unknown symbol: {symbol}")

        return self.state.prices[symbol]

    def get_prices(self) -> dict[str, float]:
        return self.state.prices.copy()

    def update_prices(self):
        for symbol, price in self.state.prices.items():

            # Random price movement between -1% and +1%
            change_percent = random.uniform(-0.01, 0.01)

            new_price = price * (1 + change_percent)

            self.state.prices[symbol] = new_price