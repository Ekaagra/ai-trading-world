from dataclasses import dataclass


@dataclass
class TradeDecision:
    symbol: str
    action: str
    confidence: float
    momentum: float