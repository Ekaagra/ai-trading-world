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


@dataclass
class CompletedTrade:
    symbol: str
    quantity: float

    entry_price: float
    exit_price: float

    entry_fee: float
    exit_fee: float

    realized_pnl: float


class TradeHistory:

    def __init__(self):
        # Every BUY/SELL execution
        self.trades: list[TradeRecord] = []

        # Currently open positions
        self.open_trades: dict[str, TradeRecord] = {}

        # Completed BUY → SELL trades
        self.completed_trades: list[CompletedTrade] = []

    def record(self, trade: dict):

        record = TradeRecord(
            timestamp=datetime.now(),
            symbol=trade["symbol"],
            side=trade["side"],
            quantity=trade["quantity"],
            market_price=trade["market_price"],
            execution_price=trade["execution_price"],
            fee=trade["fee"],
            realized_pnl=trade.get(
                "realized_pnl",
                0.0
            ),
        )

        # Store every execution
        self.trades.append(record)

        # ==============================
        # BUY
        # ==============================

        if record.side == "BUY":

            self.open_trades[record.symbol] = record

        # ==============================
        # SELL
        # ==============================

        elif record.side == "SELL":

            entry = self.open_trades.get(
                record.symbol
            )

            if entry is None:
                return

            completed_trade = CompletedTrade(
                symbol=record.symbol,
                quantity=record.quantity,

                entry_price=entry.execution_price,
                exit_price=record.execution_price,

                entry_fee=entry.fee,
                exit_fee=record.fee,

                realized_pnl=record.realized_pnl,
            )

            self.completed_trades.append(
                completed_trade
            )

            # Position is now closed
            del self.open_trades[
                record.symbol
            ]

    def get_trades(self):
        return self.trades.copy()

    def get_completed_trades(self):
        return self.completed_trades.copy()

    def get_open_trades(self):
        return self.open_trades.copy()

    def total_trades(self):
        return len(self.trades)

    def completed_trade_count(self):
        return len(self.completed_trades)

    def open_trade_count(self):
        return len(self.open_trades)

    def total_realized_pnl(self):
        return sum(
            trade.realized_pnl
            for trade in self.completed_trades
        )