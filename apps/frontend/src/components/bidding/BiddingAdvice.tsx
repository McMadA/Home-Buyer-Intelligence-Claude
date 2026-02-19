import { useState } from 'react';
import type { BiddingAdvice as BiddingAdviceType } from '../../types';
import StrategySelector from './StrategySelector';

interface Props {
  advice: Record<string, BiddingAdviceType>;
}

function formatEuro(n: number): string {
  return new Intl.NumberFormat('nl-NL', {
    style: 'currency',
    currency: 'EUR',
    maximumFractionDigits: 0,
  }).format(n);
}

export default function BiddingAdvice({ advice }: Props) {
  const [strategy, setStrategy] = useState('competitive');
  const current = advice[strategy];

  if (!current) return null;

  const range = current.max_price - current.min_price;
  const recommendedPos = range > 0 ? ((current.recommended_price - current.min_price) / range) * 100 : 50;

  return (
    <div className="card">
      <h2 className="text-xl font-bold text-gray-900 mb-6">Bidding Strategy</h2>
      <StrategySelector selected={strategy} onChange={setStrategy} />

      <div className="mt-8">
        {/* Price Range Bar */}
        <div className="mb-6">
          <div className="flex justify-between text-sm text-gray-500 mb-2">
            <span>{formatEuro(current.min_price)}</span>
            <span>{formatEuro(current.max_price)}</span>
          </div>
          <div className="relative h-4 bg-gray-200 rounded-full">
            <div className="absolute inset-0 bg-gradient-to-r from-primary-200 to-primary-400 rounded-full" />
            {/* Recommended price marker */}
            <div
              className="absolute top-1/2 -translate-y-1/2 w-6 h-6 bg-accent-400 border-2 border-white rounded-full shadow-md"
              style={{ left: `calc(${recommendedPos}% - 12px)` }}
            />
          </div>
          <div className="text-center mt-3">
            <span className="text-xs text-gray-400">Recommended</span>
            <p className="text-2xl font-bold text-primary-500">{formatEuro(current.recommended_price)}</p>
          </div>
        </div>

        {/* Explanation */}
        <div className="bg-gray-50 rounded-lg p-4">
          <p className="text-sm text-gray-600 leading-relaxed">{current.explanation}</p>
        </div>
      </div>
    </div>
  );
}
