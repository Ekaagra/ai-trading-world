from dataclasses import dataclass

from .backtest import BacktestResult
from .regime import MarketRegime


@dataclass
class RegimePerformance:
    regime: str

    completed_trades: int
    winning_trades: int
    losing_trades: int

    total_pnl: float
    average_trade_pnl: float

    win_rate: float
    profit_factor: float
    expectancy: float


@dataclass
class StrategyRegimeEvaluation:
    strategy_name: str
    regime_results: list[RegimePerformance]


class RegimeStrategyEvaluator:

    def evaluate(
        self,
        strategy_name: str,
        result: BacktestResult,
    ) -> StrategyRegimeEvaluation:

        regime_trades = {}

        for trade in result.completed_trade_details:

            regime = trade.entry_regime

            if not regime:
                regime = "UNKNOWN"

            if regime not in regime_trades:
                regime_trades[regime] = []

            regime_trades[regime].append(
                trade
            )

        regime_results = []

        for regime, trades in regime_trades.items():

            completed_trades = len(trades)

            winning_trades = sum(
                1
                for trade in trades
                if trade.realized_pnl > 0
            )

            losing_trades = sum(
                1
                for trade in trades
                if trade.realized_pnl < 0
            )

            total_pnl = sum(
                trade.realized_pnl
                for trade in trades
            )

            average_trade_pnl = (
                total_pnl / completed_trades
                if completed_trades
                else 0.0
            )

            win_rate = (
                winning_trades
                / completed_trades
                * 100
                if completed_trades
                else 0.0
            )

            winning_pnl = sum(
                trade.realized_pnl
                for trade in trades
                if trade.realized_pnl > 0
            )

            losing_pnl = sum(
                trade.realized_pnl
                for trade in trades
                if trade.realized_pnl < 0
            )

            if losing_pnl == 0:

                if winning_pnl > 0:
                    profit_factor = float("inf")
                else:
                    profit_factor = 0.0

            else:

                profit_factor = (
                    winning_pnl
                    / abs(losing_pnl)
                )

            expectancy = average_trade_pnl

            regime_results.append(
                RegimePerformance(
                    regime=regime,

                    completed_trades=(
                        completed_trades
                    ),

                    winning_trades=(
                        winning_trades
                    ),

                    losing_trades=(
                        losing_trades
                    ),

                    total_pnl=total_pnl,

                    average_trade_pnl=(
                        average_trade_pnl
                    ),

                    win_rate=win_rate,

                    profit_factor=(
                        profit_factor
                    ),

                    expectancy=expectancy,
                )
            )

        return StrategyRegimeEvaluation(
            strategy_name=strategy_name,
            regime_results=regime_results,
        )