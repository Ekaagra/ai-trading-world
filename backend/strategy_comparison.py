from dataclasses import dataclass

from .backtest import BacktestResult


@dataclass
class StrategyComparison:
    strategy_name: str
    final_equity: float
    total_return_percent: float
    completed_trades: int
    win_rate: float
    profit_factor: float
    average_trade_pnl: float
    max_drawdown: float
    max_drawdown_percent: float
    expectancy: float
    payoff_ratio: float


class StrategyComparisonEngine:

    def compare(
        self,
        results: dict[str, BacktestResult]
    ) -> list[StrategyComparison]:

        comparisons = []

        for strategy_name, result in results.items():

            comparison = StrategyComparison(
                strategy_name=strategy_name,
                final_equity=result.final_equity,
                total_return_percent=result.total_return_percent,
                completed_trades=result.completed_trades,
                win_rate=result.win_rate,
                profit_factor=result.profit_factor,
                average_trade_pnl=result.average_trade_pnl,
                max_drawdown=result.max_drawdown,
                max_drawdown_percent=result.max_drawdown_percent,
                expectancy=result.expectancy,
                payoff_ratio=result.payoff_ratio,
            )

            comparisons.append(comparison)

        return comparisons