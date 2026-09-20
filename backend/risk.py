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
    ):
        self.max_position_value = max_position_value
        self.min_order_value = min_order_value

    def check(
        self,
        decision: TradeDecision,
        portfolio: Portfolio,
        market_price: float,
    ) -> RiskDecision:

        # ==============================
        # HOLD
        # ==============================

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

        # ==============================
        # BUY
        # ==============================

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

            # Check minimum order value
            if remaining_value < self.min_order_value:

                return RiskDecision(
                    approved=False,
                    reason="Trade value below minimum order size",
                    quantity=0.0,
                )

            quantity = (
                remaining_value
                / market_price
            )

            return RiskDecision(
                approved=True,
                reason="BUY approved",
                quantity=quantity,
            )

        # ==============================
        # SELL
        # ==============================

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
                    reason="Position value below minimum order size",
                    quantity=0.0,
                )

            return RiskDecision(
                approved=True,
                reason="SELL approved",
                quantity=position.quantity,
            )

        # ==============================
        # UNKNOWN ACTION
        # ==============================

        return RiskDecision(
            approved=False,
            reason="Unknown action",
            quantity=0.0,
        )