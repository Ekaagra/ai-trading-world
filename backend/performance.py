from dataclasses import dataclass

from .equity import EquityTracker
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

    current_equity: float
    peak_equity: float
    current_drawdown: float
    current_drawdown_percent: float
    max_drawdown: float
    max_drawdown_percent: float


class PerformanceAnalyzer:

    def __init__(
        self,
        initial_capital: float,
        trade_history: TradeHistory,
        equity_tracker: EquityTracker,
    ):
        self.initial_capital = initial_capital
        self.trade_history = trade_history
        self.equity_tracker = equity_tracker

    def calculate(self) -> PerformanceReport:

        execution_count = (
            self.trade_history.total_trades()
        )

        completed_trades = (
            self.trade_history.get_completed_trades()
        )

        completed_trade_count = len(
            completed_trades
        )

        open_trade_count = (
            self.trade_history.open_trade_count()
        )

        realized_pnls = [
            trade.realized_pnl
            for trade in completed_trades
        ]

        total_realized_pnl = sum(
            realized_pnls
        )

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

        if completed_trade_count > 0:

            win_rate = (
                winning_trades
                / completed_trade_count
            ) * 100

        else:
            win_rate = 0.0

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

        if completed_trade_count > 0:

            average_trade_pnl = (
                total_realized_pnl
                / completed_trade_count
            )

        else:

            average_trade_pnl = 0.0


        # ==============================
        # EQUITY METRICS
        # ==============================

        current_snapshot = (
            self.equity_tracker.current()
        )

        if current_snapshot is None:

            current_equity = (
                self.initial_capital
            )

            peak_equity = (
                self.initial_capital
            )

            current_drawdown = 0.0
            current_drawdown_percent = 0.0

        else:

            current_equity = (
                current_snapshot.equity
            )

            peak_equity = (
                current_snapshot.peak_equity
            )

            current_drawdown = (
                current_snapshot.drawdown
            )

            current_drawdown_percent = (
                current_snapshot.drawdown_percent
            )

        max_drawdown = (
            self.equity_tracker.max_drawdown()
        )

        max_drawdown_percent = (
            self.equity_tracker
            .max_drawdown_percent()
        )

        return_percent = (
            (current_equity - self.initial_capital)
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

            winning_trades=winning_trades,

            losing_trades=losing_trades,

            win_rate=win_rate,

            profit_factor=profit_factor,

            average_trade_pnl=(
                average_trade_pnl
            ),

            return_percent=return_percent,

            current_equity=current_equity,

            peak_equity=peak_equity,

            current_drawdown=current_drawdown,

            current_drawdown_percent=(
                current_drawdown_percent
            ),

            max_drawdown=max_drawdown,

            max_drawdown_percent=(
                max_drawdown_percent
            ),
        )