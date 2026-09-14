from dataclasses import dataclass, field


@dataclass
class Position:
    symbol: str
    quantity: float = 0.0
    average_price: float = 0.0


@dataclass
class Portfolio:
    initial_cash: float
    cash: float
    positions: dict[str, Position] = field(default_factory=dict)
    realized_pnl: float = 0.0

    def get_position(self, symbol: str) -> Position:
        if symbol not in self.positions:
            self.positions[symbol] = Position(symbol=symbol)

        return self.positions[symbol]