from dataclasses import dataclass

from .backtest import BacktestResult, BacktestEngine
from .parameter_analysis import ParameterAnalyzer
from .strategy_evaluation import (
    StrategyEvaluation,
    StrategyEvaluator,
)
from .strategies.base import Strategy
from .robust_parameter_selection import (
    RobustParameterSelector,
)


@dataclass
class RollingWindowResult:
    window_number: int

    train_start: int
    train_end: int

    test_start: int
    test_end: int

    selected_parameters: dict

    train_result: BacktestResult
    test_result: BacktestResult

    evaluation: StrategyEvaluation

    robust_selection_failed: bool


@dataclass
class RollingWalkForwardResult:
    strategy_name: str
    windows: list[RollingWindowResult]

    total_test_trades: int
    total_test_pnl: float

    average_test_return_percent: float
    average_test_expectancy: float
    average_test_drawdown_percent: float


class RollingWalkForwardTester:

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

    def run(
        self,
        candles: list[dict],
        strategy_factory,
        parameter_configurations: list[dict],
    ) -> RollingWalkForwardResult:

        minimum_required = (
            self.train_size + self.test_size
        )

        if len(candles) < minimum_required:
            raise ValueError(
                f"Need at least {minimum_required} candles, "
                f"but received {len(candles)}."
            )

        parameter_analyzer = ParameterAnalyzer()
        strategy_evaluator = StrategyEvaluator()
        parameter_selector = RobustParameterSelector()

        windows = []

        window_number = 1
        start = 0

        while (
            start
            + self.train_size
            + self.test_size
            <= len(candles)
        ):

            train_start = start

            train_end = (
                start + self.train_size
            )

            test_start = train_end

            test_end = (
                test_start + self.test_size
            )

            train_candles = candles[
                train_start:train_end
            ]

            test_candles = candles[
                test_start:test_end
            ]

            # =========================
            # TRAINING
            # =========================

            parameter_results = []

            for parameters in parameter_configurations:

                strategy = strategy_factory(
                    parameters
                )

                engine = BacktestEngine(
                    initial_capital=self.initial_capital,
                    strategy=strategy,
                )

                result = engine.run(
                    train_candles
                )

                parameter_results.append(
                    (
                        strategy.name,
                        parameters,
                        result,
                    )
                )

            analyzed_results = (
                parameter_analyzer.analyze(
                    parameter_results
                )
            )

            if not analyzed_results:
                raise ValueError(
                    "No parameter configurations "
                    "were evaluated."
                )

            # =========================
            # ROBUST PARAMETER SELECTION
            # =========================

            robust_selection = (
                parameter_selector.select(
                    analyzed_results
                )
            )

            selected_parameters = (
                robust_selection.parameters
            )

            # =========================
            # SELECTED TRAINING RESULT
            # =========================

            selected_train_strategy = (
                strategy_factory(
                    selected_parameters
                )
            )

            selected_train_engine = (
                BacktestEngine(
                    initial_capital=(
                        self.initial_capital
                    ),
                    strategy=(
                        selected_train_strategy
                    ),
                )
            )

            selected_train_result = (
                selected_train_engine.run(
                    train_candles
                )
            )

            # =========================
            # OUT-OF-SAMPLE TEST
            # =========================

            test_strategy = strategy_factory(
                selected_parameters
            )

            test_engine = BacktestEngine(
                initial_capital=self.initial_capital,
                strategy=test_strategy,
            )

            test_result = test_engine.run(
                test_candles
            )

            # =========================
            # EVALUATION
            # =========================

            evaluation = (
                strategy_evaluator.evaluate(
                    strategy_name=test_strategy.name,
                    result=test_result,
                )
            )

            # =========================
            # WINDOW RESULT
            # =========================

            window_result = RollingWindowResult(
                window_number=window_number,

                train_start=train_start,
                train_end=train_end,

                test_start=test_start,
                test_end=test_end,

                selected_parameters=(
                    selected_parameters
                ),

                train_result=(
                    selected_train_result
                ),

                test_result=(
                    test_result
                ),

                evaluation=(
                    evaluation
                ),

                robust_selection_failed=(
                    robust_selection
                    .all_candidates_failed_filters
                ),
            )

            windows.append(
                window_result
            )

            window_number += 1

            start += self.step_size

        # =========================
        # AGGREGATED RESULTS
        # =========================

        total_test_trades = sum(
            window.test_result.completed_trades
            for window in windows
        )

        total_test_pnl = sum(
            window.test_result.total_realized_pnl
            for window in windows
        )

        average_test_return = (
            sum(
                window.test_result
                .total_return_percent
                for window in windows
            )
            / len(windows)
        )

        average_test_expectancy = (
            sum(
                window.test_result
                .expectancy
                for window in windows
            )
            / len(windows)
        )

        average_test_drawdown = (
            sum(
                window.test_result
                .max_drawdown_percent
                for window in windows
            )
            / len(windows)
        )

        return RollingWalkForwardResult(
            strategy_name=(
                windows[0]
                .evaluation
                .strategy_name
            ),

            windows=windows,

            total_test_trades=(
                total_test_trades
            ),

            total_test_pnl=(
                total_test_pnl
            ),

            average_test_return_percent=(
                average_test_return
            ),

            average_test_expectancy=(
                average_test_expectancy
            ),

            average_test_drawdown_percent=(
                average_test_drawdown
            ),
        )