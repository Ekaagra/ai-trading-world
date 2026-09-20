from dataclasses import dataclass

from .data import MarketDataProvider


@dataclass
class MarketState:
    prices: dict[str, float]


class MarketEngine:

    def __init__(
        self,
        symbols: list[str],
        data_provider: MarketDataProvider,
    ):
        self.symbols = symbols
        self.data_provider = data_provider

        initial_prices = (
            self.data_provider.get_prices(
                self.symbols
            )
        )

        self.state = MarketState(
            prices=initial_prices
        )

    def get_price(self, symbol: str) -> float:

        if symbol not in self.state.prices:
            raise ValueError(
                f"Unknown symbol: {symbol}"
            )

        return self.state.prices[symbol]

    def get_prices(self) -> dict[str, float]:

        return self.state.prices.copy()

    def update_prices(self) -> dict[str, float]:

        new_prices = (
            self.data_provider.get_prices(
                self.symbols
            )
        )

        self.state.prices = new_prices

        return self.state.prices.copy()