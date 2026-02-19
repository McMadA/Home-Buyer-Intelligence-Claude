import { useState } from 'react';
import type { RiskFinding } from '../../types';

interface Props {
  categoryScores: Record<string, number>;
  findings: RiskFinding[];
}

function getBarColor(score: number): string {
  if (score <= 25) return 'bg-risk-low';
  if (score <= 50) return 'bg-risk-moderate';
  if (score <= 75) return 'bg-risk-elevated';
  return 'bg-risk-high';
}

const categoryLabels: Record<string, string> = {
  structural: 'Structural',
  legal: 'Legal',
  financial: 'Financial',
  market: 'Market',
};

export default function CategoryBreakdown({ categoryScores, findings }: Props) {
  const [expanded, setExpanded] = useState<string | null>(null);

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-900">Risk by Category</h3>
      {Object.entries(categoryScores).map(([category, score]) => {
        const catFindings = findings.filter((f) => f.category === category);
        const isExpanded = expanded === category;

        return (
          <div key={category}>
            <button
              onClick={() => setExpanded(isExpanded ? null : category)}
              className="w-full text-left"
            >
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm font-medium text-gray-700">
                  {categoryLabels[category] || category}
                  {catFindings.length > 0 && (
                    <span className="ml-2 text-xs text-gray-400">
                      ({catFindings.length} finding{catFindings.length !== 1 ? 's' : ''})
                    </span>
                  )}
                </span>
                <span className="text-sm font-semibold text-gray-900">{Math.round(score)}</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2.5">
                <div
                  className={`h-2.5 rounded-full transition-all duration-700 ${getBarColor(score)}`}
                  style={{ width: `${Math.min(score, 100)}%` }}
                />
              </div>
            </button>
            {isExpanded && catFindings.length > 0 && (
              <div className="mt-2 ml-2 space-y-2">
                {catFindings.map((finding, i) => (
                  <div key={i} className="border-l-2 border-gray-200 pl-3 py-1">
                    <div className="flex items-center gap-2">
                      <span
                        className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                          finding.severity === 'critical'
                            ? 'bg-red-100 text-red-700'
                            : finding.severity === 'high'
                              ? 'bg-orange-100 text-orange-700'
                              : finding.severity === 'medium'
                                ? 'bg-yellow-100 text-yellow-700'
                                : 'bg-green-100 text-green-700'
                        }`}
                      >
                        {finding.severity}
                      </span>
                      <span className="text-sm font-medium text-gray-800">{finding.title}</span>
                    </div>
                    <p className="text-xs text-gray-500 mt-1">{finding.description}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
