import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { api } from '../api/client';
import { LoadingState, EmptyState, ErrorState } from '../components/EmptyState';
import { Sparkles, ShieldCheck, Filter } from 'lucide-react';

export const RecommendationsPage = () => {
  const { id } = useParams();

  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Filters
  const [complexityFilter, setComplexityFilter] = useState('');
  const [algoFilter, setAlgoFilter] = useState('');

  const fetchRecommendations = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.getRecommendations(id);
      setRecommendations(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to fetch PQC recommendations');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendations();
  }, [id]);

  const filtered = recommendations.filter((r) => {
    if (complexityFilter && r.migration_complexity !== complexityFilter) return false;
    if (algoFilter && !r.current_algorithm.toLowerCase().includes(algoFilter.toLowerCase())) return false;
    return true;
  });

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-slate-100 flex items-center space-x-2">
          <span>NIST Post-Quantum Cryptography Recommendations</span>
          <Sparkles className="w-6 h-6 text-emerald-400" />
        </h2>
        <p className="text-sm text-slate-400 mt-1">
          Automated migration targets mapped directly to NIST FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), and FIPS 205 (SLH-DSA) standards.
        </p>
      </div>

      {/* Prominent Disclaimer Banner */}
      <div className="bg-emerald-500/10 border border-emerald-500/30 p-4 rounded-xl flex items-center space-x-3 text-xs text-emerald-300">
        <ShieldCheck className="w-5 h-5 shrink-0 text-emerald-400" />
        <span className="font-semibold">Candidate migration guidance — validate in non-production environments before production deployment.</span>
      </div>

      {/* Filter Bar */}
      <div className="bg-[#111827] border border-slate-800 rounded-xl p-4 flex flex-wrap gap-4 items-center">
        <div className="flex items-center space-x-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">
          <Filter className="w-4 h-4 text-emerald-400" />
          <span>Filter Guidance:</span>
        </div>

        <input
          type="text"
          placeholder="Filter primitive (e.g. RSA)..."
          value={algoFilter}
          onChange={(e) => setAlgoFilter(e.target.value)}
          className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
        />

        <select
          value={complexityFilter}
          onChange={(e) => setComplexityFilter(e.target.value)}
          className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
        >
          <option value="">All Migration Complexities</option>
          <option value="Low">Low</option>
          <option value="Medium">Medium</option>
          <option value="High">High</option>
        </select>
      </div>

      {/* Recommendation Cards */}
      {loading ? (
        <LoadingState message="Generating NIST PQC recommendations..." />
      ) : error ? (
        <ErrorState message={error} onRetry={fetchRecommendations} />
      ) : filtered.length === 0 ? (
        <EmptyState
          title="No Recommendations Available"
          description="No cryptographic primitives require recommendations or match the selected filters."
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filtered.map((rec) => (
            <div key={rec.id} className="bg-[#111827] border border-slate-800 rounded-xl p-6 shadow-xl space-y-4 flex flex-col justify-between">
              <div className="space-y-3">
                <div className="flex justify-between items-start">
                  <div>
                    <span className="text-[10px] uppercase font-bold text-slate-400 font-mono">Current Primitive</span>
                    <h3 className="text-base font-bold text-slate-100">{rec.current_algorithm} ({rec.current_purpose})</h3>
                  </div>
                  <span className={`px-2.5 py-0.5 rounded text-xs font-bold uppercase ${
                    rec.migration_complexity === 'High'
                      ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                      : rec.migration_complexity === 'Medium'
                      ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                      : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                  }`}>
                    {rec.migration_complexity} Complexity
                  </span>
                </div>

                <div className="bg-emerald-950/20 border border-emerald-500/30 p-3.5 rounded-lg">
                  <span className="text-[10px] uppercase font-bold text-emerald-400 tracking-wider">Target Post-Quantum Standard</span>
                  <p className="text-sm font-bold text-emerald-300 mt-0.5">{rec.candidate_algorithm}</p>
                </div>

                <p className="text-xs text-slate-300 leading-relaxed">{rec.reason}</p>

                <div className="space-y-2 pt-2 text-xs">
                  {rec.performance_considerations && (
                    <div className="bg-slate-900 p-2.5 rounded border border-slate-800">
                      <span className="font-semibold text-slate-300">Performance: </span>
                      <span className="text-slate-400">{rec.performance_considerations}</span>
                    </div>
                  )}
                  {rec.compatibility_considerations && (
                    <div className="bg-slate-900 p-2.5 rounded border border-slate-800">
                      <span className="font-semibold text-slate-300">Compatibility: </span>
                      <span className="text-slate-400">{rec.compatibility_considerations}</span>
                    </div>
                  )}
                </div>
              </div>

              <div className="pt-2 border-t border-slate-800 flex justify-between text-[11px] text-slate-500">
                <span>Confidence Score: {(rec.confidence * 100).toFixed(0)}%</span>
                <span className="italic">NIST FIPS Standardized</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default RecommendationsPage;
