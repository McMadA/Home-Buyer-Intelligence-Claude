from src.domain.enums import BiddingStrategyType
from src.domain.models.bidding import BiddingAdvice
from src.domain.models.risk import RiskScore


class BiddingStrategyService:
    def generate_advice(
        self,
        asking_price: float,
        risk_score: RiskScore,
        market_data: dict | None = None,
    ) -> dict[BiddingStrategyType, BiddingAdvice]:
        """Generate bidding advice for all strategy types."""
        risk_adj = self._risk_adjustment(risk_score.overall_score)
        market_adj = self._market_adjustment(market_data)
        base_adj = risk_adj + market_adj

        return {
            BiddingStrategyType.CONSERVATIVE: BiddingAdvice(
                strategy=BiddingStrategyType.CONSERVATIVE,
                min_price=round(asking_price * (0.88 + base_adj)),
                max_price=round(asking_price * (0.95 + base_adj)),
                recommended_price=round(asking_price * (0.92 + base_adj)),
                explanation=self._conservative_explanation(risk_score),
            ),
            BiddingStrategyType.COMPETITIVE: BiddingAdvice(
                strategy=BiddingStrategyType.COMPETITIVE,
                min_price=round(asking_price * (0.96 + base_adj)),
                max_price=round(asking_price * (1.04 + base_adj)),
                recommended_price=round(asking_price * (1.00 + base_adj)),
                explanation=self._competitive_explanation(risk_score),
            ),
            BiddingStrategyType.AGGRESSIVE: BiddingAdvice(
                strategy=BiddingStrategyType.AGGRESSIVE,
                min_price=round(asking_price * (1.02 + base_adj)),
                max_price=round(asking_price * (1.13 + base_adj)),
                recommended_price=round(asking_price * (1.07 + base_adj)),
                explanation=self._aggressive_explanation(risk_score),
            ),
        }

    def _risk_adjustment(self, overall_score: float) -> float:
        if overall_score >= 75:
            return -0.05
        elif overall_score >= 50:
            return -0.03
        elif overall_score >= 25:
            return -0.01
        return 0.0

    def _market_adjustment(self, market_data: dict | None) -> float:
        if not market_data:
            return 0.0
        price_index = (market_data.get("area_statistics") or {}).get("price_index")
        if price_index and isinstance(price_index, (int, float)):
            if price_index > 110:
                return 0.02
            elif price_index < 95:
                return -0.02
        return 0.0

    def _conservative_explanation(self, risk_score: RiskScore) -> str:
        parts = ["Conservative strategy: bid below asking price."]
        if risk_score.overall_score >= 50:
            parts.append(
                f"Risk score is {risk_score.overall_score}/100 ({risk_score.risk_level.value}), justifying a lower bid."
            )
        parts.append(
            "This approach is suitable for properties with notable risks or in a buyer's market."
        )
        return " ".join(parts)

    def _competitive_explanation(self, risk_score: RiskScore) -> str:
        parts = ["Competitive strategy: bid around asking price."]
        parts.append("Balanced approach for average market conditions.")
        if risk_score.overall_score < 30:
            parts.append(
                "The low risk profile supports bidding at or near asking price."
            )
        return " ".join(parts)

    def _aggressive_explanation(self, risk_score: RiskScore) -> str:
        parts = ["Aggressive strategy: bid above asking price."]
        parts.append(
            "Suitable for high-demand properties or when you want to maximize your chances."
        )
        if risk_score.overall_score < 25:
            parts.append(
                "The property's low risk score makes it a strong candidate for a premium bid."
            )
        return " ".join(parts)
