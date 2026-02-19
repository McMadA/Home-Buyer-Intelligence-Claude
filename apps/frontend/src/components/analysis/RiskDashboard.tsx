import type { RiskScore } from '../../types';
import RiskScoreGauge from './RiskScoreGauge';
import CategoryBreakdown from './CategoryBreakdown';

interface Props {
  riskScore: RiskScore;
}

export default function RiskDashboard({ riskScore }: Props) {
  return (
    <div className="card">
      <h2 className="text-xl font-bold text-gray-900 mb-6">Risk Assessment</h2>
      <div className="grid md:grid-cols-2 gap-8 items-start">
        <div className="flex justify-center">
          <RiskScoreGauge score={riskScore.overall_score} riskLevel={riskScore.risk_level} />
        </div>
        <CategoryBreakdown
          categoryScores={riskScore.category_scores}
          findings={riskScore.findings}
        />
      </div>
    </div>
  );
}
