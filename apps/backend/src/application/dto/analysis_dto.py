from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class RiskFindingDTO(BaseModel):
    category: str
    severity: str
    title: str
    description: str
    source: str


class RiskScoreDTO(BaseModel):
    overall_score: float
    risk_level: str
    category_scores: dict[str, float]
    findings: list[RiskFindingDTO]


class BiddingAdviceDTO(BaseModel):
    strategy: str
    min_price: float
    max_price: float
    recommended_price: float
    explanation: str


class PropertyDTO(BaseModel):
    address: str | None = None
    postal_code: str | None = None
    city: str | None = None
    square_meters: float | None = None
    year_built: int | None = None
    energy_label: str | None = None
    property_type: str | None = None
    asking_price: float | None = None
    hoa_monthly_cost: float | None = None
    num_rooms: int | None = None
    has_garden: bool | None = None
    has_parking: bool | None = None


class AnalysisResponse(BaseModel):
    id: UUID
    session_id: UUID
    status: str
    property_data: PropertyDTO | None = None
    strengths: list[str] = []
    weaknesses: list[str] = []
    risk_score: RiskScoreDTO | None = None
    market_position: dict | None = None
    bidding_advice: dict[str, BiddingAdviceDTO] | None = None
    created_at: datetime
    completed_at: datetime | None = None
    error_message: str | None = None


class AnalysisStatusResponse(BaseModel):
    session_id: UUID
    status: str
    progress_message: str
