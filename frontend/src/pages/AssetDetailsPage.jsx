import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { api } from '../api/client';
import RiskBadge from '../components/RiskBadge';
import PriorityBadge from '../components/PriorityBadge';
import { LoadingState, ErrorState } from '../components/EmptyState';
import { 
  ShieldAlert, 
  Code, 
  Calculator, 
  Sparkles, 
  Save, 
  ArrowLeft,
  FileCode
} from 'lucide-react';

export const AssetDetailsPage = () => {
  const { id, assetId } = useParams();
  const navigate = useNavigate();

  const [assetDetail, setAssetDetail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  // Editable fields
  const [dataSensitivity, setDataSensitivity] = useState('Medium');
  const [businessCriticality, setBusinessCriticality] = useState('Medium');
  const [dataLifetimeYears, setDataLifetimeYears] = useState(10);
  const [migrationDifficulty, setMigrationDifficulty] = useState('Medium');

  const fetchAssetDetail = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.getAssetDetail(id, assetId);
      setAssetDetail(res.data);
      setDataSensitivity(res.data.data_sensitivity || 'Medium');
      setBusinessCriticality(res.data.business_criticality || 'Medium');
      setDataLifetimeYears(res.data.data_lifetime_years || 10);
      setMigrationDifficulty(res.data.migration_difficulty || 'Medium');
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to load asset details');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAssetDetail();
  }, [id, assetId]);

  const handleUpdateContext = async () => {
    setSaving(true);
    try {
      await api.updateAssetContext(id, assetId, {
        data_sensitivity: dataSensitivity,
        business_criticality: businessCriticality,
        data_lifetime_years: parseInt(dataLifetimeYears, 10),
        migration_difficulty: migrationDifficulty,
      });
      await fetchAssetDetail();
    } catch (err) {
      alert(`Failed to update context parameters: ${err.response?.data?.detail || err.message}`);
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="p-8"><LoadingState message="Fetching asset details & raw evidence code snippet..." /></div>;
  if (error) return <div className="p-8"><ErrorState message={error} onRetry={fetchAssetDetail} /></div>;
  if (!assetDetail) return null;

  const { risk_assessment, recommendation, raw_evidence } = assetDetail;

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-8">
      {/* Header Bar */}
      <div className="flex items-center space-x-4 border-b border-slate-800 pb-5">
        <button
          onClick={() => navigate(`/projects/${id}/assets`)}
          className="p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <div>
          <span className="text-xs font-mono uppercase text-purple-400 font-semibold">{assetDetail.language} Asset</span>
          <h2 className="text-2xl font-bold text-slate-100 mt-0.5">{assetDetail.algorithm} ({assetDetail.crypto_purpose})</h2>
          <p className="text-xs text-slate-400 font-mono mt-0.5">{assetDetail.file_path}:{assetDetail.line_number}</p>
        </div>
      </div>

      {/* Primary Summary Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-5 bg-[#111827] border border-slate-800 rounded-xl p-6 shadow-xl">
        <div>
          <p className="text-xs text-slate-400 uppercase font-semibold">Risk Classification</p>
          <div className="mt-2"><RiskBadge risk={assetDetail.risk_type} /></div>
        </div>

        <div>
          <p className="text-xs text-slate-400 uppercase font-semibold">Weighted Risk Score</p>
          <p className="text-2xl font-bold text-slate-100 mt-1">{assetDetail.risk_score} / 100</p>
        </div>

        <div>
          <p className="text-xs text-slate-400 uppercase font-semibold">Migration Priority</p>
          <div className="mt-2"><PriorityBadge priority={assetDetail.priority} /></div>
        </div>

        <div>
          <p className="text-xs text-slate-400 uppercase font-semibold">Purpose Confidence</p>
          <p className="text-2xl font-bold text-purple-400 mt-1">{Math.round(assetDetail.purpose_confidence * 100)}%</p>
        </div>
      </div>

      {/* WHY WAS THIS DETECTED? - Raw Evidence Code Snippets */}
      <div className="bg-[#111827] border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
        <div className="flex items-center space-x-2 text-sm font-semibold text-slate-200 uppercase tracking-wider">
          <Code className="w-5 h-5 text-purple-400" />
          <span>Why Was This Detected? (Raw Evidence)</span>
        </div>

        {raw_evidence && raw_evidence.length > 0 ? (
          raw_evidence.map((ev) => (
            <div key={ev.id} className="bg-slate-900 border border-slate-800 rounded-lg p-4 space-y-3">
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-400 font-semibold">Detector: <span className="text-slate-200">{ev.detector}</span></span>
                <span className="text-slate-400 font-mono">Confidence: <span className="text-purple-400 font-bold">{ev.confidence}</span></span>
              </div>

              <div>
                <p className="text-xs text-slate-400 mb-1">Matched Source Text:</p>
                <code className="block bg-slate-950 p-2.5 rounded text-xs text-rose-300 font-mono border border-slate-800">
                  {ev.matched_text}
                </code>
              </div>

              {ev.surrounding_context && (
                <div>
                  <p className="text-xs text-slate-400 mb-1">Surrounding Code Context:</p>
                  <pre className="bg-slate-950 p-3 rounded text-[11px] text-slate-300 font-mono border border-slate-800 overflow-x-auto whitespace-pre">
                    {ev.surrounding_context}
                  </pre>
                </div>
              )}
            </div>
          ))
        ) : (
          <p className="text-xs text-slate-400">No detailed raw evidence recorded for this asset.</p>
        )}
      </div>

      {/* Editable Context Inputs Section */}
      <div className="bg-[#111827] border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
        <div className="flex justify-between items-center border-b border-slate-800 pb-3">
          <h3 className="text-sm font-semibold text-slate-200 uppercase tracking-wider">Editable Contextual Input Parameters</h3>
          <button
            onClick={handleUpdateContext}
            disabled={saving}
            className="flex items-center space-x-2 bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold px-4 py-2 rounded-lg transition-colors shadow-md disabled:opacity-50"
          >
            <Save className="w-4 h-4" />
            <span>{saving ? 'Recalculating...' : 'Recalculate Risk & Priority'}</span>
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-5 pt-2">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Data Sensitivity</label>
            <select
              value={dataSensitivity}
              onChange={(e) => setDataSensitivity(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-purple-500"
            >
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
              <option value="Critical">Critical</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Business Criticality</label>
            <select
              value={businessCriticality}
              onChange={(e) => setBusinessCriticality(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-purple-500"
            >
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
              <option value="Critical">Critical</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Data Protection Lifetime (Years)</label>
            <input
              type="number"
              min="1"
              max="50"
              value={dataLifetimeYears}
              onChange={(e) => setDataLifetimeYears(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-purple-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Migration Difficulty</label>
            <select
              value={migrationDifficulty}
              onChange={(e) => setMigrationDifficulty(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-purple-500"
            >
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
            </select>
          </div>
        </div>
      </div>

      {/* Risk Breakdown Section */}
      {risk_assessment && (
        <div className="bg-[#111827] border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
          <div className="flex items-center space-x-2 text-sm font-semibold text-slate-200 uppercase tracking-wider">
            <Calculator className="w-5 h-5 text-amber-400" />
            <span>Weighted Risk Engine Breakdown</span>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-5 gap-3 text-center">
            <div className="bg-slate-900 p-3 rounded-lg border border-slate-800">
              <p className="text-[10px] text-slate-400 uppercase font-semibold">Quantum Vulnerability (35%)</p>
              <p className="text-lg font-bold text-rose-400 mt-1">{risk_assessment.quantum_vulnerability_score}</p>
            </div>
            <div className="bg-slate-900 p-3 rounded-lg border border-slate-800">
              <p className="text-[10px] text-slate-400 uppercase font-semibold">Data Sensitivity (20%)</p>
              <p className="text-lg font-bold text-amber-400 mt-1">{risk_assessment.data_sensitivity_score}</p>
            </div>
            <div className="bg-slate-900 p-3 rounded-lg border border-slate-800">
              <p className="text-[10px] text-slate-400 uppercase font-semibold">Data Lifetime (20%)</p>
              <p className="text-lg font-bold text-purple-400 mt-1">{risk_assessment.data_lifetime_score}</p>
            </div>
            <div className="bg-slate-900 p-3 rounded-lg border border-slate-800">
              <p className="text-[10px] text-slate-400 uppercase font-semibold">Business Criticality (15%)</p>
              <p className="text-lg font-bold text-blue-400 mt-1">{risk_assessment.business_criticality_score}</p>
            </div>
            <div className="bg-slate-900 p-3 rounded-lg border border-slate-800">
              <p className="text-[10px] text-slate-400 uppercase font-semibold">Migration Difficulty (10%)</p>
              <p className="text-lg font-bold text-slate-300 mt-1">{risk_assessment.migration_difficulty_score}</p>
            </div>
          </div>

          <p className="text-xs text-slate-300 bg-slate-900/60 p-3.5 rounded-lg border border-slate-800 leading-relaxed">
            {risk_assessment.explanation}
          </p>
        </div>
      )}

      {/* PQC Recommendation Card */}
      {recommendation && (
        <div className="bg-[#111827] border border-emerald-500/30 rounded-xl p-6 shadow-xl space-y-4">
          <div className="flex items-center space-x-2 text-sm font-semibold text-emerald-400 uppercase tracking-wider">
            <Sparkles className="w-5 h-5" />
            <span>NIST Post-Quantum Cryptography Candidate Recommendation</span>
          </div>

          <div className="bg-emerald-950/20 border border-emerald-500/20 p-4 rounded-lg space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-xs text-slate-400 font-semibold">Current Primitive: <span className="text-slate-200">{recommendation.current_algorithm} ({recommendation.current_purpose})</span></span>
              <span className="text-xs text-emerald-400 font-bold uppercase">Complexity: {recommendation.migration_complexity}</span>
            </div>

            <p className="text-sm font-bold text-emerald-300 mt-1">
              Target PQC Algorithm: {recommendation.candidate_algorithm}
            </p>

            <p className="text-xs text-slate-300 mt-2 leading-relaxed">
              {recommendation.reason}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div className="bg-slate-900 p-3 rounded-lg border border-slate-800">
              <p className="font-semibold text-slate-300 mb-1">Performance Considerations:</p>
              <p className="text-slate-400">{recommendation.performance_considerations}</p>
            </div>
            <div className="bg-slate-900 p-3 rounded-lg border border-slate-800">
              <p className="font-semibold text-slate-300 mb-1">Compatibility Considerations:</p>
              <p className="text-slate-400">{recommendation.compatibility_considerations}</p>
            </div>
          </div>

          <p className="text-[11px] text-slate-500 italic">
            Disclaimer: {recommendation.disclaimer}
          </p>
        </div>
      )}
    </div>
  );
};

export default AssetDetailsPage;
