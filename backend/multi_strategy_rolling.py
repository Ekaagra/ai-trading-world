from dataclasses import dataclass

from .rolling_walk_forward import (
    RollingWalkForwardTester,
    RollingWalkForwardResult,
)


@dataclass
class MultiStrategyResult:
    strategy_name: str
    result: RollingWalkForwardResult


class MultiStrategyRollingEvaluator:

    def __init__(
        self,
        initial_capital: float = 100_000,
        train_size: int = 2000,
        test_size: int = 1000,
        step_size: int = 1000,
    ):
        self.initial_capital = initial_capital
        self.train_size = train_size
        self.test_size = test_size
        self.step_size = step_size

    def evaluate(
        self,
        candles: list[dict],
        strategies: list[tuple],
        parameter_configurations: dict[str, list[dict]],
    ) -> list[MultiStrategyResult]:

        results = []

        for strategy_name, strategy_factory in strategies:

            tester = RollingWalkForwardTester(
                initial_capital=self.initial_capital,
                train_size=self.train_size,
                test_size=self.test_size,
                step_size=self.step_size,
            )

            result = tester.run(
                candles=candles,
                strategy_factory=strategy_factory,
                parameter_configurations=(
                    parameter_configurations[
                        strategy_name
                    ]
                ),
            )

            results.append(
                MultiStrategyResult(
                    strategy_name=strategy_name,
                    result=result,
                )
            )

        return results