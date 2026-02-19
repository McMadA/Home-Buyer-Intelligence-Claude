from dataclasses import dataclass, field
from ..enums import RiskCategory, RiskLevel, Severity

SEVERITY_POINTS = {
    Severity.LOW: 5,
    Severity.MEDIUM: 15,
    Severity.HIGH: 30,
    Severity.CRITICAL: 50,
}

CATEGORY_WEIGHTS = {
    RiskCategory.STRUCTURAL: 0.30,
    RiskCategory.LEGAL: 0.20,
    RiskCategory.FINANCIAL: 0.25,
    RiskCategory.MARKET: 0.25,
}


@dataclass
class RiskFinding:
    category: RiskCategory
    severity: Severity
    title: str
    description: str
    source: str  # "ai_extraction", "bag_api", "energy_label", etc.


@dataclass
class RiskScore:
    overall_score: float = 0.0
    category_scores: dict[RiskCategory, float] = field(default_factory=dict)
    findings: list[RiskFinding] = field(default_factory=list)

    @property
    def risk_level(self) -> RiskLevel:
        if self.overall_score <= 25:
            return RiskLevel.LOW
        elif self.overall_score <= 50:
            return RiskLevel.MODERATE
        elif self.overall_score <= 75:
            return RiskLevel.HIGH
        return RiskLevel.CRITICAL

    @staticmethod
    def compute(findings: list[RiskFinding]) -> "RiskScore":
        category_points: dict[RiskCategory, float] = {cat: 0.0 for cat in RiskCategory}
        for f in findings:
            category_points[f.category] += SEVERITY_POINTS[f.severity]

        category_scores = {cat: min(100.0, pts) for cat, pts in category_points.items()}
        overall = sum(
            category_scores[cat] * weight
            for cat, weight in CATEGORY_WEIGHTS.items()
        )
        return RiskScore(
            overall_score=round(overall, 1),
            category_scores=category_scores,
            findings=findings,
        )
