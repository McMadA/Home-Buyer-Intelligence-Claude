from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from .risk import RiskScore
from .bidding import BiddingAdvice
from ..enums import AnalysisStatus, BiddingStrategyType


@dataclass
class AnalysisResult:
    session_id: UUID
    id: UUID = field(default_factory=uuid4)
    status: AnalysisStatus = AnalysisStatus.PENDING
    property_data: dict | None = None
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    risk_score: RiskScore | None = None
    market_position: dict | None = None
    bidding_advice: dict[BiddingStrategyType, BiddingAdvice] | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: datetime | None = None
    error_message: str | None = None
