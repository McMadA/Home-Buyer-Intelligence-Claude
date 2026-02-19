interface Props {
  score: number;
  riskLevel: string;
}

function getColor(score: number): string {
  if (score <= 25) return '#22c55e';
  if (score <= 50) return '#eab308';
  if (score <= 75) return '#f97316';
  return '#ef4444';
}

export default function RiskScoreGauge({ score, riskLevel }: Props) {
  const color = getColor(score);
  const radius = 70;
  const circumference = 2 * Math.PI * radius;
  const progress = (score / 100) * circumference;

  return (
    <div className="flex flex-col items-center">
      <svg width="180" height="180" viewBox="0 0 180 180">
        {/* Background circle */}
        <circle cx="90" cy="90" r={radius} fill="none" stroke="#e5e7eb" strokeWidth="12" />
        {/* Progress circle */}
        <circle
          cx="90"
          cy="90"
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth="12"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={circumference - progress}
          transform="rotate(-90 90 90)"
          className="transition-all duration-1000 ease-out"
        />
        {/* Score text */}
        <text x="90" y="82" textAnchor="middle" className="text-4xl font-bold" fill={color}>
          {Math.round(score)}
        </text>
        <text x="90" y="105" textAnchor="middle" className="text-sm" fill="#6b7280">
          / 100
        </text>
      </svg>
      <p className="mt-2 text-sm font-semibold uppercase tracking-wide" style={{ color }}>
        {riskLevel} Risk
      </p>
    </div>
  );
}
