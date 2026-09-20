from dataclasses import dataclass

from .trade_history import TradeHistory


@dataclass
class PerformanceReport:
    execution_count: int

    completed_trades: int
    open_trades: int

    total_realized_pnl: float

    winning_trades: int
    losing_trades: int

    win_rate: float
    profit_factor: float

    average_trade_pnl: float
    return_percent: float


class PerformanceAnalyzer:

    def __init__(
        self,
        initial_capital: float,
        trade_history: TradeHistory,
    ):
        self.initial_capital = initial_capital
        self.trade_history = trade_history

    def calculate(self) -> PerformanceReport:

        # ==================================
        # EXECUTIONS
        # ==================================

        execution_count = (
            self.trade_history.total_trades()
        )

        # ==================================
        # COMPLETED TRADES
        # ==================================

        completed_trades = (
            self.trade_history
            .get_completed_trades()
        )

        completed_trade_count = len(
            completed_trades
        )

        open_trade_count = (
            self.trade_history
            .open_trade_count()
        )

        # ==================================
        # P&L
        # ==================================

        realized_pnls = [
            trade.realized_pnl
            for trade in completed_trades
        ]

        total_realized_pnl = sum(
            realized_pnls
        )

        # ==================================
        # WIN / LOSS
        # ==================================

        winning_trades = sum(
            1
            for pnl in realized_pnls
            if pnl > 0
        )

        losing_trades = sum(
            1
            for pnl in realized_pnls
            if pnl < 0
        )

        # ==================================
        # WIN RATE
        # ==================================

        if completed_trade_count > 0:

            win_rate = (
                winning_trades
                / completed_trade_count
            ) * 100

        else:

            win_rate = 0.0

        # ==================================
        # PROFIT FACTOR
        # ==================================

        gross_profit = sum(
            pnl
            for pnl in realized_pnls
            if pnl > 0
        )

        gross_loss = abs(
            sum(
                pnl
                for pnl in realized_pnls
                if pnl < 0
            )
        )

        if gross_loss > 0:

            profit_factor = (
                gross_profit
                / gross_loss
            )

        elif gross_profit > 0:

            profit_factor = float("inf")

        else:

            profit_factor = 0.0

        # ==================================
        # AVERAGE TRADE P&L
        # ==================================

        if completed_trade_count > 0:

            average_trade_pnl = (
                total_realized_pnl
                / completed_trade_count
            )

        else:

            average_trade_pnl = 0.0

        # ==================================
        # RETURN
        # ==================================

        return_percent = (
            total_realized_pnl
            / self.initial_capital
        ) * 100

        return PerformanceReport(

            execution_count=execution_count,

            completed_trades=(
                completed_trade_count
            ),

            open_trades=open_trade_count,

            total_realized_pnl=(
                total_realized_pnl
            ),

            winning_trades=(
                winning_trades
            ),

            losing_trades=(
                losing_trades
            ),

            win_rate=win_rate,

            profit_factor=profit_factor,

            average_trade_pnl=(
                average_trade_pnl
            ),

            return_percent=(
                return_percent
            ),
        )