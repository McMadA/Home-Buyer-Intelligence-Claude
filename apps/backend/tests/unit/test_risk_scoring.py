from src.domain.models.risk import RiskScore, RiskFinding
from src.domain.enums import RiskCategory, Severity, RiskLevel


def test_empty_findings_score_zero():
    score = RiskScore.compute([])
    assert score.overall_score == 0.0
    assert score.risk_level == RiskLevel.LOW


def test_single_low_finding():
    findings = [
        RiskFinding(
            category=RiskCategory.STRUCTURAL,
            severity=Severity.LOW,
            title="Minor crack",
            description="Small hairline crack in wall",
            source="ai_extraction",
        )
    ]
    score = RiskScore.compute(findings)
    # structural weight = 0.30, LOW = 5 points
    assert score.overall_score == 1.5
    assert score.risk_level == RiskLevel.LOW


def test_critical_finding_high_score():
    findings = [
        RiskFinding(
            category=RiskCategory.STRUCTURAL,
            severity=Severity.CRITICAL,
            title="Foundation damage",
            description="Severe foundation issues",
            source="ai_extraction",
        )
    ]
    score = RiskScore.compute(findings)
    # structural weight = 0.30, CRITICAL = 50 points
    assert score.overall_score == 15.0


def test_multiple_findings_across_categories():
    findings = [
        RiskFinding(RiskCategory.STRUCTURAL, Severity.HIGH, "Roof", "Bad roof", "ai"),
        RiskFinding(RiskCategory.LEGAL, Severity.MEDIUM, "Erfpacht", "Ground lease", "ai"),
        RiskFinding(RiskCategory.FINANCIAL, Severity.LOW, "HOA", "High HOA", "ai"),
        RiskFinding(RiskCategory.MARKET, Severity.MEDIUM, "Slow", "Slow market", "ai"),
    ]
    score = RiskScore.compute(findings)
    # structural: 30*0.30=9, legal: 15*0.20=3, financial: 5*0.25=1.25, market: 15*0.25=3.75
    assert score.overall_score == 17.0
    assert score.risk_level == RiskLevel.LOW
    assert len(score.findings) == 4


def test_category_score_capped_at_100():
    findings = [
        RiskFinding(RiskCategory.STRUCTURAL, Severity.CRITICAL, "A", "", "ai"),
        RiskFinding(RiskCategory.STRUCTURAL, Severity.CRITICAL, "B", "", "ai"),
        RiskFinding(RiskCategory.STRUCTURAL, Severity.CRITICAL, "C", "", "ai"),
    ]
    score = RiskScore.compute(findings)
    assert score.category_scores[RiskCategory.STRUCTURAL] == 100.0
