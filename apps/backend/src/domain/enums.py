from enum import StrEnum


class DocumentType(StrEnum):
    PURCHASE_AGREEMENT = "purchase_agreement"
    ENERGY_LABEL = "energy_label"
    INSPECTION_REPORT = "inspection_report"
    HOA_DOCUMENTS = "hoa_documents"
    PROPERTY_LISTING = "property_listing"
    OTHER = "other"


class RiskCategory(StrEnum):
    STRUCTURAL = "structural"
    LEGAL = "legal"
    FINANCIAL = "financial"
    MARKET = "market"


class RiskLevel(StrEnum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class BiddingStrategyType(StrEnum):
    CONSERVATIVE = "conservative"
    COMPETITIVE = "competitive"
    AGGRESSIVE = "aggressive"


class AnalysisStatus(StrEnum):
    PENDING = "pending"
    EXTRACTING = "extracting"
    ANALYZING = "analyzing"
    ENRICHING = "enriching"
    SCORING = "scoring"
    COMPLETE = "complete"
    FAILED = "failed"
