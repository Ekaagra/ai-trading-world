from dataclasses import dataclass

from .backtest import BacktestResult


@dataclass
class StrategyEvaluation:
    strategy_name: str

    total_return_percent: float
    profit_factor: float
    expectancy: float

    win_rate: float
    payoff_ratio: float

    completed_trades: int

    max_drawdown: float
    max_drawdown_percent: float

    average_trade_pnl: float

    robustness_flags: list[str]


class StrategyEvaluator:

    def evaluate(
        self,
        strategy_name: str,
        result: BacktestResult,
    ) -> StrategyEvaluation:

        flags = []

        # =========================
        # SAMPLE SIZE
        # =========================

        if result.completed_trades < 30:
            flags.append(
                "LOW_TRADE_COUNT"
            )

        # =========================
        # PROFITABILITY
        # =========================

        if result.profit_factor < 1.0:
            flags.append(
                "PROFIT_FACTOR_BELOW_1"
            )

        if result.expectancy <= 0:
            flags.append(
                "NEGATIVE_EXPECTANCY"
            )

        # =========================
        # DRAWDOWN
        # =========================

        if result.max_drawdown_percent > 10:
            flags.append(
                "HIGH_DRAWDOWN"
            )

        # =========================
        # WIN RATE
        # =========================

        if result.win_rate < 30:
            flags.append(
                "LOW_WIN_RATE"
            )

        # =========================
        # PAYOFF
        # =========================

        if result.payoff_ratio < 1.0:
            flags.append(
                "PAYOFF_RATIO_BELOW_1"
            )

        return StrategyEvaluation(
            strategy_name=strategy_name,

            total_return_percent=(
                result.total_return_percent
            ),

            profit_factor=(
                result.profit_factor
            ),

            expectancy=(
                result.expectancy
            ),

            win_rate=(
                result.win_rate
            ),

            payoff_ratio=(
                result.payoff_ratio
            ),

            completed_trades=(
                result.completed_trades
            ),

            max_drawdown=(
                result.max_drawdown
            ),

            max_drawdown_percent=(
                result.max_drawdown_percent
            ),

            average_trade_pnl=(
                result.average_trade_pnl
            ),

            robustness_flags=flags,
        )