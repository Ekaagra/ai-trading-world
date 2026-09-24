from backend.strategies.base import Strategy
from backend.strategies.types import TradeDecision


class MeanReversionStrategy(Strategy):

    def __init__(
        self,
        symbol: str,
        window: int = 5,
        deviation_threshold: float = 0.001
    ):
        self.symbol = symbol
        self.window = window
        self.deviation_threshold = deviation_threshold

    @property
    def name(self) -> str:
        return "Mean Reversion"

    def decide(
        self,
        prices: list[float]
    ) -> TradeDecision:

        if len(prices) < self.window:
            return TradeDecision(
                symbol=self.symbol,
                action="HOLD",
                confidence=0.0,
                momentum=0.0
            )

        recent_prices = prices[-self.window:]

        moving_average = (
            sum(recent_prices) / self.window
        )

        current_price = prices[-1]

        deviation = (
            (current_price - moving_average)
            / moving_average
        )

        # Price is sufficiently below the mean.
        # Expectation: price may revert upward.
        if deviation < -self.deviation_threshold:
            action = "BUY"

        # Price is sufficiently above the mean.
        # Expectation: price may revert downward.
        elif deviation > self.deviation_threshold:
            action = "SELL"

        else:
            action = "HOLD"

        confidence = min(
            abs(deviation) / self.deviation_threshold,
            1.0
        )

        return TradeDecision(
            symbol=self.symbol,
            action=action,
            confidence=confidence,
            momentum=deviation
        )