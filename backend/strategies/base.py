from abc import ABC, abstractmethod

from backend.strategies.types import TradeDecision


class Strategy(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def decide(self, prices: list[float]) -> TradeDecision:
        pass