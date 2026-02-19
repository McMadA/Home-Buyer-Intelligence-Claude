from dataclasses import dataclass
from ..enums import BiddingStrategyType


@dataclass
class BiddingAdvice:
    strategy: BiddingStrategyType
    min_price: float
    max_price: float
    recommended_price: float
    explanation: str
