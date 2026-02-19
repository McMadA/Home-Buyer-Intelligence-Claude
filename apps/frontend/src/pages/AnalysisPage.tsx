import { useParams, useNavigate } from 'react-router-dom';
import { useAnalysisStatus, useAnalysis, useDeleteSession, useExportData } from '../hooks/useAnalysis';
import RiskDashboard from '../components/analysis/RiskDashboard';
import StrengthsWeaknesses from '../components/analysis/StrengthsWeaknesses';
import MarketPosition from '../components/market/MarketPosition';
import BiddingAdvice from '../components/bidding/BiddingAdvice';
import type { PropertyData } from '../types';

function PropertySummary({ data }: { data: PropertyData }) {
  const fields = [
    { label: 'Address', value: data.address },
    { label: 'City', value: data.city },
    { label: 'Postal Code', value: data.postal_code },
    {
      label: 'Asking Price',
      value: data.asking_price
        ? new Intl.NumberFormat('nl-NL', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }).format(data.asking_price)
        : null,
    },
    { label: 'Size', value: data.square_meters ? `${data.square_meters} m2` : null },
    { label: 'Year Built', value: data.year_built },
    { label: 'Energy Label', value: data.energy_label },
    { label: 'Rooms', value: data.num_rooms },
    { label: 'HOA/month', value: data.hoa_monthly_cost ? `EUR ${data.hoa_monthly_cost}` : null },
  ].filter((f) => f.value);

  return (
    <div className="card">
      <h2 className="text-xl font-bold text-gray-900 mb-4">Property Summary</h2>
      <dl className="grid grid-cols-2 sm:grid-cols-3 gap-4">
        {fields.map((f) => (
          <div key={f.label}>
            <dt className="text-xs text-gray-400 uppercase tracking-wide">{f.label}</dt>
            <dd className="text-sm font-semibold text-gray-900">{String(f.value)}</dd>
          </div>
        ))}
      </dl>
    </div>
  );
}

export default function AnalysisPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const navigate = useNavigate();

  const statusQuery = useAnalysisStatus(sessionId, true);
  const isComplete = statusQuery.data?.status === 'complete';
  const isFailed = statusQuery.data?.status === 'failed';

  const analysisQuery = useAnalysis(isComplete ? sessionId : undefined);
  const deleteSession = useDeleteSession();
  const exportData = useExportData();

  const handleDelete = async () => {
    if (!sessionId || !confirm('Delete all data for this session? This cannot be undone.')) return;
    await deleteSession.mutateAsync(sessionId);
    navigate('/');
  };

  const handleExport = async () => {
    if (!sessionId) return;
    const data = await exportData.mutateAsync(sessionId);
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `session-${sessionId}-export.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Loading state
  if (!isComplete && !isFailed) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-20 text-center">
        <svg className="animate-spin h-12 w-12 mx-auto mb-6 text-primary-500" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
        <h2 className="text-2xl font-bold text-primary-500 mb-2">Analyzing Your Documents</h2>
        <p className="text-gray-500 text-lg">
          {statusQuery.data?.progress_message || 'Starting analysis...'}
        </p>
      </div>
    );
  }

  // Error state
  if (isFailed) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-20 text-center">
        <div className="bg-red-50 border border-red-200 rounded-xl p-8">
          <h2 className="text-2xl font-bold text-red-700 mb-2">Analysis Failed</h2>
          <p className="text-red-600">{statusQuery.data?.progress_message}</p>
          <button onClick={() => navigate('/upload')} className="btn-primary mt-6">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  const analysis = analysisQuery.data;
  if (!analysis || analysisQuery.isLoading) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-20 text-center">
        <p className="text-gray-500">Loading results...</p>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-primary-500">Analysis Results</h1>
        <div className="flex gap-2">
          <button onClick={handleExport} className="btn-outline text-sm px-4 py-2">
            Export Data
          </button>
          <button
            onClick={handleDelete}
            className="border-2 border-red-300 text-red-600 px-4 py-2 rounded-lg text-sm font-semibold hover:bg-red-50 transition-colors"
          >
            Delete All Data
          </button>
        </div>
      </div>

      {analysis.property_data && <PropertySummary data={analysis.property_data} />}

      {analysis.risk_score && <RiskDashboard riskScore={analysis.risk_score} />}

      <StrengthsWeaknesses strengths={analysis.strengths} weaknesses={analysis.weaknesses} />

      {analysis.market_position && <MarketPosition data={analysis.market_position} />}

      {analysis.bidding_advice && <BiddingAdvice advice={analysis.bidding_advice} />}
    </div>
  );
}
