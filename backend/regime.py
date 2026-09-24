from dataclasses import dataclass
from enum import Enum


class MarketRegime(str, Enum):
    TRENDING = "TRENDING"
    RANGING = "RANGING"
    HIGH_VOLATILITY = "HIGH_VOLATILITY"


@dataclass
class RegimeResult:
    regime: MarketRegime
    trend_strength: float
    volatility: float


class MarketRegimeDetector:

    def __init__(
        self,
        trend_window: int = 20,
        volatility_window: int = 20,
        trend_threshold: float = 0.002,
        volatility_threshold: float = 0.0015,
    ):
        self.trend_window = trend_window
        self.volatility_window = volatility_window
        self.trend_threshold = trend_threshold
        self.volatility_threshold = volatility_threshold

    def detect(self, prices: list[float]) -> RegimeResult:

        minimum_window = max(
            self.trend_window,
            self.volatility_window,
        )

        if len(prices) < minimum_window:
            return RegimeResult(
                regime=MarketRegime.RANGING,
                trend_strength=0.0,
                volatility=0.0,
            )

        recent_prices = prices[-self.trend_window:]

        start_price = recent_prices[0]
        end_price = recent_prices[-1]

        trend_strength = (
            (end_price - start_price)
            / start_price
        )

        returns = []

        for i in range(1, self.volatility_window):
            previous_price = prices[-self.volatility_window + i - 1]
            current_price = prices[-self.volatility_window + i]

            price_return = (
                current_price - previous_price
            ) / previous_price

            returns.append(price_return)

        if returns:
            mean_return = sum(returns) / len(returns)

            variance = sum(
                (r - mean_return) ** 2
                for r in returns
            ) / len(returns)

            volatility = variance ** 0.5

        else:
            volatility = 0.0

        if volatility >= self.volatility_threshold:
            regime = MarketRegime.HIGH_VOLATILITY

        elif abs(trend_strength) >= self.trend_threshold:
            regime = MarketRegime.TRENDING

        else:
            regime = MarketRegime.RANGING

        return RegimeResult(
            regime=regime,
            trend_strength=trend_strength,
            volatility=volatility,
        )