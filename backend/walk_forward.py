from dataclasses import dataclass
from typing import Callable

from .backtest import BacktestResult, BacktestEngine
from .parameter_analysis import ParameterAnalyzer
from .strategies.base import Strategy
from .robust_parameter_selection import RobustParameterSelector

@dataclass
class WalkForwardResult:
    strategy_name: str
    train_candles: int
    test_candles: int
    selected_parameters: dict
    train_result: BacktestResult
    test_result: BacktestResult


class WalkForwardTester:

    def __init__(
        self,
        initial_capital: float = 100_000,
        train_size: int = 3500,
        test_size: int = 1500,
    ):
        self.initial_capital = initial_capital
        self.train_size = train_size
        self.test_size = test_size

    def run(
        self,
        candles: list[dict],
        strategy_factory: Callable[[dict], Strategy],
        parameter_configurations: list[dict],
    ) -> WalkForwardResult:

        required_candles = (
            self.train_size + self.test_size
        )

        if len(candles) < required_candles:
            raise ValueError(
                f"Need at least {required_candles} candles, "
                f"but received {len(candles)}."
            )

        train_candles = candles[
            :self.train_size
        ]

        test_candles = candles[
            self.train_size:
            self.train_size + self.test_size
        ]

        # =========================
        # TRAINING / PARAMETER SEARCH
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

        analyzer = ParameterAnalyzer()

        analyzed_results = analyzer.analyze(
            parameter_results
        )

        if not analyzed_results:
            raise ValueError(
                "No parameter configurations were evaluated."
            )

        # =========================
        # SELECT TRAINING CONFIG
        # =========================

        selector = RobustParameterSelector(
            minimum_trades=10,
            minimum_profit_factor=0.8,
        )

        robust_selection = selector.select(
            analyzed_results
        )

        selected_parameters = (
            robust_selection.parameters
        )

        selected_train_strategy = strategy_factory(
            selected_parameters
        )

        selected_train_engine = BacktestEngine(
            initial_capital=self.initial_capital,
            strategy=selected_train_strategy,
        )

        selected_train_result = selected_train_engine.run(
            train_candles
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

        return WalkForwardResult(
            strategy_name=test_strategy.name,
            train_candles=len(train_candles),
            test_candles=len(test_candles),
            selected_parameters=selected_parameters,
            train_result=selected_train_result,
            test_result=test_result,
        )