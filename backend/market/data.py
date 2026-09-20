import yfinance as yf


class MarketDataProvider:

    SYMBOL_MAP = {
        "BTC": "BTC-USD",
        "ETH": "ETH-USD",
        "SOL": "SOL-USD",
    }

    def get_price(self, symbol: str) -> float:

        if symbol not in self.SYMBOL_MAP:
            raise ValueError(
                f"Unsupported symbol: {symbol}"
            )

        ticker_symbol = self.SYMBOL_MAP[symbol]

        ticker = yf.Ticker(ticker_symbol)

        data = ticker.history(
            period="1d",
            interval="1m",
        )

        if data.empty:
            raise RuntimeError(
                f"No market data available for {symbol}"
            )

        return float(data["Close"].iloc[-1])

    def get_prices(
        self,
        symbols: list[str],
    ) -> dict[str, float]:

        prices = {}

        for symbol in symbols:
            prices[symbol] = self.get_price(symbol)

        return prices