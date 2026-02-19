interface Props {
  selected: string;
  onChange: (strategy: string) => void;
}

const strategies = [
  { key: 'conservative', label: 'Conservative', description: 'Lower risk, below asking' },
  { key: 'competitive', label: 'Competitive', description: 'Balanced, around asking' },
  { key: 'aggressive', label: 'Aggressive', description: 'Maximize chances, above asking' },
];

export default function StrategySelector({ selected, onChange }: Props) {
  return (
    <div className="flex gap-2">
      {strategies.map((s) => (
        <button
          key={s.key}
          onClick={() => onChange(s.key)}
          className={`flex-1 px-4 py-3 rounded-lg border-2 text-center transition-all ${
            selected === s.key
              ? 'border-primary-500 bg-primary-50 text-primary-700'
              : 'border-gray-200 bg-white text-gray-600 hover:border-gray-300'
          }`}
        >
          <span className="text-sm font-semibold block">{s.label}</span>
          <span className="text-xs text-gray-400">{s.description}</span>
        </button>
      ))}
    </div>
  );
}
