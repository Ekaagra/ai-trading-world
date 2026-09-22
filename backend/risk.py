from dataclasses import dataclass

from .agents.momentum import TradeDecision
from .models import Portfolio


@dataclass
class RiskDecision:
    approved: bool
    reason: str
    quantity: float


class RiskEngine:

    def __init__(
        self,
        max_position_value: float = 10_000,
        min_order_value: float = 10,
        stop_loss_percent: float = 0.01,
        take_profit_percent: float = 0.02,
    ):
        self.max_position_value = max_position_value
        self.min_order_value = min_order_value

        self.stop_loss_percent = stop_loss_percent
        self.take_profit_percent = take_profit_percent

    def check(
        self,
        decision: TradeDecision,
        portfolio: Portfolio,
        market_price: float,
    ) -> RiskDecision:

        if decision.action == "HOLD":
            return RiskDecision(
                approved=False,
                reason="Agent decided to HOLD",
                quantity=0.0,
            )

        position = portfolio.get_position(
            decision.symbol
        )

        current_position_value = (
            position.quantity * market_price
        )

        # =========================
        # BUY
        # =========================

        if decision.action == "BUY":

            remaining_value = (
                self.max_position_value
                - current_position_value
            )

            if remaining_value <= 0:
                return RiskDecision(
                    approved=False,
                    reason="Maximum position size reached",
                    quantity=0.0,
                )

            position_value = (
                remaining_value
                * decision.confidence
            )

            if position_value < self.min_order_value:
                return RiskDecision(
                    approved=False,
                    reason=(
                        "Confidence-adjusted "
                        "order below minimum size"
                    ),
                    quantity=0.0,
                )

            quantity = (
                position_value
                / market_price
            )

            return RiskDecision(
                approved=True,
                reason=(
                    f"BUY approved "
                    f"(confidence="
                    f"{decision.confidence:.2f})"
                ),
                quantity=quantity,
            )

        # =========================
        # SELL
        # =========================

        if decision.action == "SELL":

            if position.quantity <= 0:
                return RiskDecision(
                    approved=False,
                    reason="No position to sell",
                    quantity=0.0,
                )

            order_value = (
                position.quantity
                * market_price
            )

            if order_value < self.min_order_value:
                return RiskDecision(
                    approved=False,
                    reason=(
                        "Position value below "
                        "minimum order size"
                    ),
                    quantity=0.0,
                )

            return RiskDecision(
                approved=True,
                reason="SELL approved",
                quantity=position.quantity,
            )

        return RiskDecision(
            approved=False,
            reason="Unknown action",
            quantity=0.0,
        )

    # =========================
    # EXIT CONDITIONS
    # =========================

    def check_exit_conditions(
        self,
        symbol: str,
        portfolio: Portfolio,
        market_price: float,
    ) -> RiskDecision:

        position = portfolio.get_position(symbol)

        if position.quantity <= 0:
            return RiskDecision(
                approved=False,
                reason="No open position",
                quantity=0.0,
            )

        entry_price = position.average_price

        stop_loss_price = (
            entry_price
            * (1 - self.stop_loss_percent)
        )

        take_profit_price = (
            entry_price
            * (1 + self.take_profit_percent)
        )

        # Stop loss
        if market_price <= stop_loss_price:

            return RiskDecision(
                approved=True,
                reason=(
                    f"Stop-loss triggered "
                    f"(price=${market_price:,.2f}, "
                    f"stop=${stop_loss_price:,.2f})"
                ),
                quantity=position.quantity,
            )

        # Take profit
        if market_price >= take_profit_price:

            return RiskDecision(
                approved=True,
                reason=(
                    f"Take-profit triggered "
                    f"(price=${market_price:,.2f}, "
                    f"target=${take_profit_price:,.2f})"
                ),
                quantity=position.quantity,
            )

        return RiskDecision(
            approved=False,
            reason="No exit condition triggered",
            quantity=0.0,
        )