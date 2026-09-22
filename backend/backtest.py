from dataclasses import dataclass

from .agents.momentum import MomentumAgent
from .models import Portfolio
from .paper_broker import PaperBroker
from .risk import RiskEngine
from .trade_history import TradeHistory
from .equity import EquityTracker


@dataclass
class BacktestResult:
    initial_capital: float
    final_equity: float
    total_return_percent: float
    total_trades: int
    completed_trades: int
    max_drawdown: float
    max_drawdown_percent: float


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

                self.equity_tracker.update(equity)

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

                trade = self.broker.sell(
                    symbol="BTC",
                    quantity=exit_decision.quantity,
                    market_price=price,
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
                        )

                        self.trade_history.record(trade)

                    elif decision.action == "SELL":

                        trade = self.broker.sell(
                            symbol="BTC",
                            quantity=risk_decision.quantity,
                            market_price=price,
                        )

                        self.trade_history.record(trade)

            # =========================
            # EQUITY UPDATE
            # =========================

            equity = self.broker.portfolio_value(
                {"BTC": price}
            )

            self.equity_tracker.update(equity)

        # =========================
        # FINAL EQUITY
        # =========================

        final_equity = self.broker.portfolio_value(
            {"BTC": self.close_history[-1]}
        )

        total_return_percent = (
            (final_equity - self.initial_capital)
            / self.initial_capital
        ) * 100

        return BacktestResult(
            initial_capital=self.initial_capital,
            final_equity=final_equity,
            total_return_percent=total_return_percent,
            total_trades=self.trade_history.total_trades(),
            completed_trades=self.trade_history.completed_trade_count(),
            max_drawdown=self.equity_tracker.max_drawdown(),
            max_drawdown_percent=(
                self.equity_tracker.max_drawdown_percent()
            ),
        )                                                                     