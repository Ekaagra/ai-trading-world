from dataclasses import dataclass

from .parameter_analysis import ParameterResult

@dataclass
class RobustParameterResult:
    strategy_name: str
    parameters: dict

    score: float

    final_equity: float
    total_return_percent: float
    profit_factor: float
    expectancy: float
    win_rate: float
    payoff_ratio: float
    completed_trades: int
    max_drawdown_percent: float

    selection_flags: list[str]

    all_candidates_failed_filters: bool


class RobustParameterSelector:

    def __init__(
        self,
        minimum_trades: int = 10,
        minimum_profit_factor: float = 0.8,
    ):
        self.minimum_trades = minimum_trades
        self.minimum_profit_factor = (
            minimum_profit_factor
        )

    def select(
        self,
        results: list[ParameterResult],
    ) -> RobustParameterResult:

        if not results:
            raise ValueError(
                "No parameter results provided."
            )

        candidates = []

        for result in results:

            flags = []

            if (
                result.completed_trades
                < self.minimum_trades
            ):
                flags.append(
                    "LOW_TRADE_COUNT"
                )

            if (
                result.profit_factor
                < self.minimum_profit_factor
            ):
                flags.append(
                    "LOW_PROFIT_FACTOR"
                )

            if result.expectancy <= 0:
                flags.append(
                    "NEGATIVE_EXPECTANCY"
                )

            candidates.append(
                (
                    result,
                    flags,
                )
            )

        valid_candidates = [
            (result, flags)
            for result, flags in candidates
            if not flags
        ]

        all_candidates_failed_filters = (
            len(valid_candidates) == 0
        )

        if all_candidates_failed_filters:
            valid_candidates = candidates

        scored_candidates = []

        for result, flags in valid_candidates:

            score = self._calculate_score(
                result
            )

            scored_candidates.append(
                (
                    result,
                    flags,
                    score,
                )
            )

        selected = max(
            scored_candidates,
            key=lambda item: item[2]
        )

        result, flags, score = selected

        return RobustParameterResult(
            strategy_name=result.strategy_name,
            parameters=result.parameters,

            score=score,

            final_equity=result.final_equity,
            total_return_percent=(
                result.total_return_percent
            ),
            profit_factor=result.profit_factor,
            expectancy=result.expectancy,
            win_rate=result.win_rate,
            payoff_ratio=result.payoff_ratio,
            completed_trades=(
                result.completed_trades
            ),
            max_drawdown_percent=(
                result.max_drawdown_percent
            ),
            selection_flags=flags,
            all_candidates_failed_filters=(
                all_candidates_failed_filters
            ),
        )

    def _calculate_score(
        self,
        result: ParameterResult,
    ) -> float:

        score = 0.0

        # Positive return
        score += (
            result.total_return_percent
            * 2.0
        )

        # Reward profit factor
        score += (
            result.profit_factor
            * 10.0
        )

        # Reward positive expectancy
        score += (
            result.expectancy
            / 10.0
        )

        # Reward reasonable win rate
        score += (
            result.win_rate
            * 0.05
        )

        # Reward payoff ratio
        score += (
            result.payoff_ratio
            * 5.0
        )

        # Penalize drawdown
        score -= (
            result.max_drawdown_percent
            * 2.0
        )

        return score