import requests


class HistoricalMarketData:

    def __init__(
        self,
        symbol="BTCUSDT",
        interval="1m",
    ):
        self.symbol = symbol
        self.interval = interval

        self.url = (
            "https://api.binance.com/api/v3/klines"
        )

    def fetch(self, limit=500):

        if limit <= 0:
            raise ValueError(
                "limit must be greater than 0"
            )

        candles = []

        remaining = limit
        end_time = None

        while remaining > 0:

            batch_size = min(
                remaining,
                1000,
            )

            params = {
                "symbol": self.symbol,
                "interval": self.interval,
                "limit": batch_size,
            }

            if end_time is not None:
                params["endTime"] = end_time

            response = requests.get(
                self.url,
                params=params,
                timeout=10,
            )

            response.raise_for_status()

            data = response.json()

            if not data:
                break

            batch = []

            for candle in data:

                batch.append(
                    {
                        "timestamp": candle[0],
                        "open": float(candle[1]),
                        "high": float(candle[2]),
                        "low": float(candle[3]),
                        "close": float(candle[4]),
                        "volume": float(candle[5]),
                    }
                )

            candles = batch + candles

            remaining -= len(batch)

            end_time = data[0][0] - 1

            if len(data) < batch_size:
                break

        return candles[-limit:]