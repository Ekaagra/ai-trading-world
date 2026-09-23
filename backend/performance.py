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

    average_winning_trade: float
    average_losing_trade: float

    largest_winning_trade: float
    largest_losing_trade: float

    total_winning_pnl: float
    total_losing_pnl: float

    average_holding_time_seconds: float

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

        winning_trade_pnls = [
            trade.realized_pnl
            for trade in completed_trades
            if trade.realized_pnl > 0
        ]

        losing_trade_pnls = [
            trade.realized_pnl
            for trade in completed_trades
            if trade.realized_pnl < 0
        ]

        total_winning_pnl = sum(winning_trade_pnls)

        total_losing_pnl = sum(losing_trade_pnls)

        average_winning_trade = (
            total_winning_pnl / len(winning_trade_pnls)
            if winning_trade_pnls
            else 0.0
        )

        average_losing_trade = (
            total_losing_pnl / len(losing_trade_pnls)
            if losing_trade_pnls
            else 0.0
        )

        largest_winning_trade = (
            max(winning_trade_pnls)
            if winning_trade_pnls
            else 0.0
        )

        largest_losing_trade = (
            min(losing_trade_pnls)
            if losing_trade_pnls
            else 0.0
        )

        holding_times = [
            (
                trade.exit_timestamp - trade.entry_timestamp
            ).total_seconds()
            for trade in completed_trades
        ]

        average_holding_time_seconds = (
            sum(holding_times) / len(holding_times)
            if holding_times
            else 0.0
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
            execution_count=len(self.trade_history.get_trades()),
            completed_trades=len(completed_trades),
            open_trades=len(self.trade_history.get_open_trades()),

            total_realized_pnl=total_realized_pnl,

            winning_trades=winning_trades,
            losing_trades=losing_trades,
            win_rate=win_rate,

            profit_factor=profit_factor,
            average_trade_pnl=average_trade_pnl,

            average_winning_trade=average_winning_trade,
            average_losing_trade=average_losing_trade,

            largest_winning_trade=largest_winning_trade,
            largest_losing_trade=largest_losing_trade,

            total_winning_pnl=total_winning_pnl,
            total_losing_pnl=total_losing_pnl,

            average_holding_time_seconds=average_holding_time_seconds,

            return_percent=return_percent,

            current_equity=current_equity,
            peak_equity=peak_equity,
            current_drawdown=current_drawdown,
            current_drawdown_percent=current_drawdown_percent,

            max_drawdown=max_drawdown,
            max_drawdown_percent=max_drawdown_percent,
        )