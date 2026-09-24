from dataclasses import dataclass


@dataclass
class RegimePerformance:
    regime: str
    trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    total_pnl: float
    average_pnl: float
    expectancy: float


class RegimePerformanceAnalyzer:

    def analyze(self, completed_trades):

        regimes = [
            "TRENDING",
            "RANGING",
            "HIGH_VOLATILITY",
        ]

        results = {}

        for regime in regimes:

            trades = [
                trade
                for trade in completed_trades
                if trade.regime == regime
            ]

            winning_trades = [
                trade
                for trade in trades
                if trade.realized_pnl > 0
            ]

            losing_trades = [
                trade
                for trade in trades
                if trade.realized_pnl < 0
            ]

            trade_count = len(trades)

            winning_count = len(winning_trades)
            losing_count = len(losing_trades)

            win_rate = (
                winning_count / trade_count * 100
                if trade_count
                else 0.0
            )

            total_pnl = sum(
                trade.realized_pnl
                for trade in trades
            )

            average_pnl = (
                total_pnl / trade_count
                if trade_count
                else 0.0
            )

            expectancy = average_pnl

            results[regime] = RegimePerformance(
                regime=regime,
                trades=trade_count,
                winning_trades=winning_count,
                losing_trades=losing_count,
                win_rate=win_rate,
                total_pnl=total_pnl,
                average_pnl=average_pnl,
                expectancy=expectancy,
            )

        return results