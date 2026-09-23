from dataclasses import dataclass

from .agents.momentum import MomentumAgent
from .models import Portfolio
from .paper_broker import PaperBroker
from .risk import RiskEngine
from .trade_history import TradeHistory
from .equity import EquityTracker
from .performance import PerformanceAnalyzer

@dataclass
class BacktestResult:
    initial_capital: float
    final_equity: float
    total_return_percent: float

    total_trades: int
    completed_trades: int

    winning_trades: int
    losing_trades: int

    win_rate: float
    profit_factor: float
    average_trade_pnl: float
    total_realized_pnl: float

    max_drawdown: float
    max_drawdown_percent: float

    completed_trade_details: list
    equity_curve: list


class BacktestEngine:

    def __init__(
        self,
        initial_capital: float = 100_000,
    ):
        self.initial_capital = initial_capital

        self.portfolio = Portfolio(
            initial_cash=initial_capital,
            cash=initial_capital,
        )

        self.broker = PaperBroker(
            self.portfolio
        )

        self.risk_engine = RiskEngine(
            max_position_value=10_000,
            min_order_value=10,
            stop_loss_percent=0.01,
            take_profit_percent=0.02,
        )

        self.trade_history = TradeHistory()

        self.agent = MomentumAgent(
            symbol="BTC",
            short_window=3,
            long_window=5,
        )

        self.close_history: list[float] = []

        self.equity_tracker = EquityTracker(
            initial_equity=initial_capital
        )

    def _normalize_exit_reason(
        self,
        reason: str,
    ) -> str:

        reason_upper = reason.upper()

        if "TAKE-PROFIT" in reason_upper:
            return "TAKE_PROFIT"

        if "STOP-LOSS" in reason_upper:
            return "STOP_LOSS"

        return "SIGNAL"


    def run(
        self,
        candles: list[dict],
    ) -> BacktestResult:

        for candle in candles:

            price = candle["close"]

            self.close_history.append(price)

            if len(self.close_history) < 5:
                equity = self.broker.portfolio_value(
                    {"BTC": price}
                )

                self.equity_tracker.update(equity,timestamp=candle["timestamp"])

                continue

            # =========================
            # EXIT CONDITIONS
            # =========================

            exit_decision = (
                self.risk_engine
                .check_exit_conditions(
                    symbol="BTC",
                    portfolio=self.portfolio,
                    market_price=price,
                )
            )

            if exit_decision.approved:

                normalized_reason = (
                    self._normalize_exit_reason(
                        exit_decision.reason
                    )
                )

                trade = self.broker.sell(
                    symbol="BTC",
                    quantity=exit_decision.quantity,
                    market_price=price,
                    timestamp=candle["timestamp"],
                    exit_reason=normalized_reason,
                    exit_message=exit_decision.reason,
                )

                self.trade_history.record(trade)

            else:

                # =========================
                # AGENT
                # =========================

                decision = self.agent.decide(
                    self.close_history
                )

                # =========================
                # RISK
                # =========================

                risk_decision = (
                    self.risk_engine.check(
                        decision=decision,
                        portfolio=self.portfolio,
                        market_price=price,
                    )
                )

                # =========================
                # EXECUTION
                # =========================

                if risk_decision.approved:

                    if decision.action == "BUY":

                        trade = self.broker.buy(
                            symbol="BTC",
                            quantity=risk_decision.quantity,
                            market_price=price,
                            timestamp=candle["timestamp"],
                        )

                        self.trade_history.record(trade)

                    elif decision.action == "SELL":

                        trade = self.broker.sell(
                            symbol="BTC",
                            quantity=risk_decision.quantity,
                            market_price=price,
                            timestamp=candle["timestamp"],
                            exit_reason="SIGNAL",
                            exit_message="Momentum agent sell signal",
                        )

                        self.trade_history.record(trade)

            # =========================
            # EQUITY UPDATE
            # =========================

            equity = self.broker.portfolio_value(
                {"BTC": price}
            )

            self.equity_tracker.update(equity,timestamp=candle["timestamp"])

        # =========================
        # FINAL EQUITY
        # =========================

        final_equity = self.broker.portfolio_value(
            {"BTC": self.close_history[-1]}
        )

        performance = PerformanceAnalyzer(
            initial_capital=self.initial_capital,
            trade_history=self.trade_history,
            equity_tracker=self.equity_tracker,
        )

        report = performance.calculate()

        total_return_percent = (
            (final_equity - self.initial_capital)
            / self.initial_capital
        ) * 100

        completed_trade_details=self.trade_history.completed_trades,

        return BacktestResult(
            initial_capital=self.initial_capital,
            final_equity=final_equity,
            total_return_percent=(
                (final_equity - self.initial_capital)
                / self.initial_capital
            ) * 100,

            total_trades=report.execution_count,
            completed_trades=report.completed_trades,

            winning_trades=report.winning_trades,
            losing_trades=report.losing_trades,

            win_rate=report.win_rate,
            profit_factor=report.profit_factor,
            average_trade_pnl=report.average_trade_pnl,
            total_realized_pnl=report.total_realized_pnl,

            max_drawdown=report.max_drawdown,
            max_drawdown_percent=report.max_drawdown_percent,

            completed_trade_details=(
                self.trade_history.completed_trades
            ),

            equity_curve=(
                self.equity_tracker.snapshots.copy()
            ),
        )                                              