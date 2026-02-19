import type { MarketPosition as MarketPositionType } from '../../types';

interface Props {
  data: MarketPositionType;
}

function formatPrice(price: number | null | undefined): string {
  if (!price) return '-';
  return new Intl.NumberFormat('nl-NL', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }).format(price);
}

export default function MarketPosition({ data }: Props) {
  const area = data.area_statistics as Record<string, unknown> | null;
  const bag = data.bag_data as Record<string, unknown> | null;
  const energy = data.energy_label_data as Record<string, unknown> | null;

  return (
    <div className="card">
      <h2 className="text-xl font-bold text-gray-900 mb-6">Market Context</h2>
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Area Statistics */}
        {area && (
          <div>
            <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">
              Area Statistics
            </h3>
            <dl className="space-y-2">
              {area.municipality && (
                <div>
                  <dt className="text-xs text-gray-400">Municipality</dt>
                  <dd className="text-sm font-medium">{String(area.municipality)}</dd>
                </div>
              )}
              {area.avg_purchase_price && (
                <div>
                  <dt className="text-xs text-gray-400">Avg. Purchase Price</dt>
                  <dd className="text-sm font-medium">{formatPrice(area.avg_purchase_price as number)}</dd>
                </div>
              )}
              {area.num_transactions && (
                <div>
                  <dt className="text-xs text-gray-400">Transactions</dt>
                  <dd className="text-sm font-medium">{String(area.num_transactions)}</dd>
                </div>
              )}
            </dl>
          </div>
        )}

        {/* BAG Data */}
        {bag && (
          <div>
            <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">
              Building Data (BAG)
            </h3>
            <dl className="space-y-2">
              {bag.year_built && (
                <div>
                  <dt className="text-xs text-gray-400">Year Built</dt>
                  <dd className="text-sm font-medium">{String(bag.year_built)}</dd>
                </div>
              )}
              {bag.floor_area && (
                <div>
                  <dt className="text-xs text-gray-400">Floor Area</dt>
                  <dd className="text-sm font-medium">{String(bag.floor_area)} m2</dd>
                </div>
              )}
              {bag.usage_purpose && (
                <div>
                  <dt className="text-xs text-gray-400">Usage</dt>
                  <dd className="text-sm font-medium">{String(bag.usage_purpose)}</dd>
                </div>
              )}
            </dl>
          </div>
        )}

        {/* Energy Label */}
        {energy && (
          <div>
            <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">
              Energy Label
            </h3>
            <dl className="space-y-2">
              {energy.energy_label && (
                <div>
                  <dt className="text-xs text-gray-400">Label</dt>
                  <dd className="text-2xl font-bold text-primary-500">{String(energy.energy_label)}</dd>
                </div>
              )}
              {energy.valid_until && (
                <div>
                  <dt className="text-xs text-gray-400">Valid Until</dt>
                  <dd className="text-sm font-medium">{String(energy.valid_until)}</dd>
                </div>
              )}
            </dl>
          </div>
        )}

        {!area && !bag && !energy && (
          <p className="text-sm text-gray-400 col-span-full">No market data available.</p>
        )}
      </div>
    </div>
  );
}
