from src.domain.models.risk import RiskFinding, RiskScore
from src.domain.enums import RiskCategory, Severity


class RiskScoringService:
    def compute_score(
        self, findings: list[RiskFinding], market_data: dict | None = None
    ) -> RiskScore:
        """Compute risk score from findings and optional market data."""
        all_findings = list(findings)

        if market_data:
            energy_data = market_data.get("energy_label_data")
            if energy_data and energy_data.get("energy_label"):
                label = energy_data["energy_label"]
                if label in ("F", "G"):
                    all_findings.append(
                        RiskFinding(
                            category=RiskCategory.FINANCIAL,
                            severity=Severity.MEDIUM,
                            title="Poor energy label",
                            description=f"Energy label {label} indicates high energy costs and potential mandatory renovation requirements.",
                            source="ep_online",
                        )
                    )
                elif label in ("D", "E"):
                    all_findings.append(
                        RiskFinding(
                            category=RiskCategory.FINANCIAL,
                            severity=Severity.LOW,
                            title="Below-average energy label",
                            description=f"Energy label {label} means moderate energy costs. Consider insulation improvements.",
                            source="ep_online",
                        )
                    )

        return RiskScore.compute(all_findings)
