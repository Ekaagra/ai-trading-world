from dataclasses import dataclass


@dataclass
class MarketState:
    prices: dict[str, float]


class MarketEngine:

    def __init__(
        self,
        symbols: list[str],
    ):
        self.symbols = symbols

        self.state = MarketState(
            prices={}
        )

    def update_price(
        self,
        symbol: str,
        price: float,
    ):

        self.state.prices[symbol] = price

    def get_price(
        self,
        symbol: str,
    ) -> float:

        if symbol not in self.state.prices:
            raise ValueError(
                f"No price available for {symbol}"
            )

        return self.state.prices[symbol]

    def get_prices(self) -> dict[str, float]:

        return self.state.prices.copy()