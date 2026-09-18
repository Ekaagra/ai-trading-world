from dataclasses import dataclass
from datetime import datetime


@dataclass
class TradeRecord:
    timestamp: datetime
    symbol: str
    side: str
    quantity: float
    market_price: float
    execution_price: float
    fee: float
    realized_pnl: float = 0.0


class TradeHistory:

    def __init__(self):
        self.trades: list[TradeRecord] = []

    def record(self, trade: dict):
        record = TradeRecord(
            timestamp=datetime.now(),
            symbol=trade["symbol"],
            side=trade["side"],
            quantity=trade["quantity"],
            market_price=trade["market_price"],
            execution_price=trade["execution_price"],
            fee=trade["fee"],
            realized_pnl=trade.get("realized_pnl", 0.0),
        )

        self.trades.append(record)

    def get_trades(self):
        return self.trades.copy()

    def total_trades(self):
        return len(self.trades)

    def total_realized_pnl(self):
        return sum(
            trade.realized_pnl
            for trade in self.trades
        )