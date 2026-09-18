from dataclasses import dataclass


@dataclass
class TradeDecision:
    symbol: str
    action: str
    confidence: float


class MomentumAgent:

    def __init__(
        self,
        symbol: str,
        short_window: int = 3,
        long_window: int = 5,
    ):
        self.symbol = symbol
        self.short_window = short_window
        self.long_window = long_window

    def decide(self, prices: list[float]) -> TradeDecision:

        if len(prices) < self.long_window:
            return TradeDecision(
                symbol=self.symbol,
                action="HOLD",
                confidence=0.0,
            )

        short_prices = prices[-self.short_window:]
        long_prices = prices[-self.long_window:]

        short_average = sum(short_prices) / self.short_window
        long_average = sum(long_prices) / self.long_window

        if short_average > long_average:
            action = "BUY"

        elif short_average < long_average:
            action = "SELL"

        else:
            action = "HOLD"

        difference = abs(
            short_average - long_average
        )

        confidence = min(
            difference / long_average,
            1.0,
        )

        return TradeDecision(
            symbol=self.symbol,
            action=action,
            confidence=confidence,
        )