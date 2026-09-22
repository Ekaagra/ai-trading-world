from dataclasses import dataclass


@dataclass
class EquitySnapshot:
    equity: float
    peak_equity: float
    drawdown: float
    drawdown_percent: float


class EquityTracker:

    def __init__(self, initial_equity: float):
        self.peak_equity = initial_equity
        self.snapshots: list[EquitySnapshot] = []

    def update(self, equity: float) -> EquitySnapshot:

        if equity > self.peak_equity:
            self.peak_equity = equity

        drawdown = (
            self.peak_equity - equity
        )

        if self.peak_equity > 0:
            drawdown_percent = (
                drawdown / self.peak_equity
            ) * 100
        else:
            drawdown_percent = 0.0

        snapshot = EquitySnapshot(
            equity=equity,
            peak_equity=self.peak_equity,
            drawdown=drawdown,
            drawdown_percent=drawdown_percent,
        )

        self.snapshots.append(snapshot)

        return snapshot

    def current(self) -> EquitySnapshot | None:

        if not self.snapshots:
            return None

        return self.snapshots[-1]

    def max_drawdown(self) -> float:

        if not self.snapshots:
            return 0.0

        return max(
            snapshot.drawdown
            for snapshot in self.snapshots
        )

    def max_drawdown_percent(self) -> float:

        if not self.snapshots:
            return 0.0

        return max(
            snapshot.drawdown_percent
            for snapshot in self.snapshots
        )