from dataclasses import dataclass

from .backtest import BacktestResult


@dataclass
class ParameterResult:
    strategy_name: str
    parameters: dict
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


class ParameterAnalyzer:

    def analyze(
        self,
        results: list[tuple[str, dict, BacktestResult]]
    ) -> list[ParameterResult]:

        parameter_results = []

        for strategy_name, parameters, result in results:

            parameter_result = ParameterResult(
                strategy_name=strategy_name,
                parameters=parameters,
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

            parameter_results.append(
                parameter_result
            )

        return parameter_results