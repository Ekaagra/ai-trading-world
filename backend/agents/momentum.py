from dataclasses import dataclass


@dataclass
class TradeDecision:
    symbol: str
    action: str
    confidence: float
    momentum: float


class MomentumAgent:

    def __init__(
        self,
        symbol: str,
        short_window: int = 3,
        long_window: int = 5,
        signal_threshold: float = 0.0005,
    ):
        self.symbol = symbol
        self.short_window = short_window
        self.long_window = long_window
        self.signal_threshold = signal_threshold

    def decide(
        self,
        prices: list[float],
    ) -> TradeDecision:

        if len(prices) < self.long_window:
            return TradeDecision(
                symbol=self.symbol,
                action="HOLD",
                confidence=0.0,
                momentum=0.0,
            )

        short_prices = prices[-self.short_window:]
        long_prices = prices[-self.long_window:]

        short_average = (
            sum(short_prices)
            / self.short_window
        )

        long_average = (
            sum(long_prices)
            / self.long_window
        )

        momentum = (
            short_average - long_average
        ) / long_average

        if momentum > self.signal_threshold:
            action = "BUY"

        elif momentum < -self.signal_threshold:
            action = "SELL"

        else:
            action = "HOLD"

        confidence = min(
            abs(momentum)
            / self.signal_threshold,
            1.0,
        )

        return TradeDecision(
            symbol=self.symbol,
            action=action,
            confidence=confidence,
            momentum=momentum,
        )