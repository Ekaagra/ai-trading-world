from dataclasses import dataclass
from datetime import datetime


@dataclass
class Candle:
    symbol: str
    timestamp: datetime

    open: float
    high: float
    low: float
    close: float

    volume: float


class CandleAggregator:

    def __init__(
        self,
        interval_seconds: int = 60,
    ):
        if interval_seconds <= 0:
            raise ValueError(
                "interval_seconds must be greater than 0"
            )

        self.interval_seconds = interval_seconds

        self.current_candles: dict[str, Candle] = {}

    def _get_bucket_time(
        self,
        timestamp: datetime,
    ) -> datetime:

        timestamp_seconds = int(
            timestamp.timestamp()
        )

        bucket_seconds = (
            timestamp_seconds
            // self.interval_seconds
        ) * self.interval_seconds

        return datetime.fromtimestamp(
            bucket_seconds
        )

    def update(
        self,
        symbol: str,
        price: float,
        quantity: float,
        timestamp: datetime,
    ) -> Candle | None:

        bucket_time = self._get_bucket_time(
            timestamp
        )

        current = self.current_candles.get(
            symbol
        )

        # ==============================
        # FIRST TRADE
        # ==============================

        if current is None:

            self.current_candles[symbol] = Candle(
                symbol=symbol,
                timestamp=bucket_time,
                open=price,
                high=price,
                low=price,
                close=price,
                volume=quantity,
            )

            return None

        # ==============================
        # SAME TIME BUCKET
        # ==============================

        if bucket_time == current.timestamp:

            current.high = max(
                current.high,
                price,
            )

            current.low = min(
                current.low,
                price,
            )

            current.close = price

            current.volume += quantity

            return None

        # ==============================
        # NEW TIME BUCKET
        # ==============================

        completed_candle = current

        self.current_candles[symbol] = Candle(
            symbol=symbol,
            timestamp=bucket_time,
            open=price,
            high=price,
            low=price,
            close=price,
            volume=quantity,
        )

        return completed_candle