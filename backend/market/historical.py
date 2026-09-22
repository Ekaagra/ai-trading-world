import requests


class HistoricalMarketData:

    def __init__(self, symbol="BTCUSDT", interval="1m"):
        self.symbol = symbol
        self.interval = interval
        self.url = "https://api.binance.com/api/v3/klines"

    def fetch(self, limit=500):
        params = {
            "symbol": self.symbol,
            "interval": self.interval,
            "limit": limit,
        }

        response = requests.get(
            self.url,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        candles = []

        for candle in data:
            candles.append(
                {
                    "timestamp": candle[0],
                    "open": float(candle[1]),
                    "high": float(candle[2]),
                    "low": float(candle[3]),
                    "close": float(candle[4]),
                    "volume": float(candle[5]),
                }
            )

        return candles