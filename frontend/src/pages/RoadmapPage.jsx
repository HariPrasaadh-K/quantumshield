import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { api } from '../api/client';
import { LoadingState, EmptyState, ErrorState } from '../components/EmptyState';
import { Map, Clock, AlertOctagon, CheckCircle2, ChevronRight, RefreshCw } from 'lucide-react';

export const RoadmapPage = () => {
  const { id } = useParams();

  const [roadmap, setRoadmap] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState(null);

  // User configurable controls
  const [horizonYears, setHorizonYears] = useState(10);
  const [migrationYears, setMigrationYears] = useState(2);

  const fetchRoadmap = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.getRoadmap(id);
      setRoadmap(res.data);
      if (res.data.planning_threat_horizon_years) {
        setHorizonYears(res.data.planning_threat_horizon_years);
      }
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to load migration roadmap');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRoadmap();
  }, [id]);

  const handleRecalculateRoadmap = async () => {
    setGenerating(true);
    try {
      const res = await api.generateRoadmap(id, {
        planning_threat_horizon_years: parseInt(horizonYears, 10),
        default_migration_time_years: parseInt(migrationYears, 10),
      });
      setRoadmap(res.data);
    } catch (err) {
      alert(`Roadmap generation failed: ${err.response?.data?.detail || err.message}`);
    } finally {
      setGenerating(false);
    }
  };

  if (loading) return <div className="p-8"><LoadingState message="Evaluating Mosca Theorem & building migration roadmap..." /></div>;
  if (error) return <div className="p-8"><ErrorState message={error} onRetry={fetchRoadmap} /></div>;
  if (!roadmap) return null;

  const getMoscaBadge = (status) => {
    if (status === 'URGENT') {
      return <span className="px-3 py-1 rounded-md text-xs font-bold bg-rose-500/20 text-rose-300 border border-rose-500/40 animate-pulse">URGENT</span>;
    } else if (status === 'ACCELERATE') {
      return <span className="px-3 py-1 rounded-md text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40">ACCELERATE</span>;
    }
    return <span className="px-3 py-1 rounded-md text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">PLANNED</span>;
  };

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-8">
      <div>
        <h2 className="text-2xl font-bold text-slate-100 flex items-center space-x-2">
          <span>Mosca-Based Post-Quantum Migration Roadmap</span>
          <Map className="w-6 h-6 text-blue-400" />
        </h2>
        <p className="text-sm text-slate-400 mt-1">
          Strategic timeline planning evaluating Michele Mosca’s theorem: $Y + Z &gt; X$ where $Y$ is Data Lifetime, $Z$ is Migration Time, and $X$ is Threat Horizon.
        </p>
      </div>

      {/* Configurable Parameters Bar */}
      <div className="bg-[#111827] border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
        <div className="flex justify-between items-center border-b border-slate-800 pb-3">
          <h3 className="text-sm font-semibold text-slate-200 uppercase tracking-wider">Mosca Parameter Controls</h3>
          <button
            onClick={handleRecalculateRoadmap}
            disabled={generating}
            className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold px-4 py-2 rounded-lg transition-colors shadow-md disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${generating ? 'animate-spin' : ''}`} />
            <span>Recalculate Roadmap</span>
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
              Planning Threat Horizon (X Years)
            </label>
            <input
              type="number"
              min="1"
              max="30"
              value={horizonYears}
              onChange={(e) => setHorizonYears(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-blue-500"
            />
            <p className="text-[11px] text-slate-500 mt-1">Configurable planning horizon for quantum readiness evaluation.</p>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
              Estimated Migration Duration (Z Years)
            </label>
            <input
              type="number"
              min="1"
              max="10"
              value={migrationYears}
              onChange={(e) => setMigrationYears(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-blue-500"
            />
            <p className="text-[11px] text-slate-500 mt-1">Estimated organization-wide PQC re-engineering timeline.</p>
          </div>
        </div>
      </div>

      {/* Mosca Evaluation Card */}
      <div className="bg-[#111827] border border-slate-800 rounded-xl p-6 shadow-xl space-y-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-3">
            <Clock className="w-6 h-6 text-purple-400" />
            <h3 className="text-base font-bold text-slate-100">Mosca Theorem Status Evaluation</h3>
          </div>
          {getMoscaBadge(roadmap.mosca_status)}
        </div>

        <div className="bg-slate-900 p-4 rounded-lg border border-slate-800 space-y-2 text-xs">
          <p className="text-slate-300 leading-relaxed font-medium">
            {roadmap.explanation}
          </p>
          <p className="text-[11px] text-slate-500 italic border-t border-slate-800 pt-2">
            Notice: The planning threat horizon is a configurable planning parameter and is not a prediction of when a cryptographically relevant quantum computer will arrive.
          </p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
          <div className="bg-slate-900 p-3 rounded-lg border border-slate-800">
            <p className="text-[10px] text-slate-400 uppercase font-semibold">Required Security Window</p>
            <p className="text-lg font-bold text-purple-400 mt-1">{roadmap.required_security_window_years || (horizonYears + migrationYears)} Yrs</p>
          </div>
          <div className="bg-slate-900 p-3 rounded-lg border border-slate-800">
            <p className="text-[10px] text-slate-400 uppercase font-semibold">Threat Horizon (X)</p>
            <p className="text-lg font-bold text-blue-400 mt-1">{roadmap.planning_threat_horizon_years} Yrs</p>
          </div>
          <div className="bg-slate-900 p-3 rounded-lg border border-slate-800">
            <p className="text-[10px] text-slate-400 uppercase font-semibold">P0 Immediate Assets</p>
            <p className="text-lg font-bold text-rose-400 mt-1">{roadmap.urgent_asset_count}</p>
          </div>
          <div className="bg-slate-900 p-3 rounded-lg border border-slate-800">
            <p className="text-[10px] text-slate-400 uppercase font-semibold">P1 High Priority Assets</p>
            <p className="text-lg font-bold text-amber-400 mt-1">{roadmap.high_priority_count}</p>
          </div>
        </div>
      </div>

      {/* Phased Roadmap Timeline */}
      <div className="bg-[#111827] border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
        <h3 className="text-sm font-semibold text-slate-200 uppercase tracking-wider">7-Phase Post-Quantum Migration Timeline</h3>

        <div className="space-y-4">
          {roadmap.phases.map((phase) => (
            <div
              key={phase.order}
              className={`p-4 rounded-lg border transition-all ${
                phase.status === 'completed'
                  ? 'bg-emerald-950/20 border-emerald-500/30'
                  : phase.status === 'in_progress'
                  ? 'bg-purple-950/20 border-purple-500/30'
                  : 'bg-slate-900/60 border-slate-800'
              }`}
            >
              <div className="flex justify-between items-start">
                <div className="flex items-center space-x-3">
                  <div className={`p-1.5 rounded-full ${
                    phase.status === 'completed' ? 'bg-emerald-500/20 text-emerald-400' :
                    phase.status === 'in_progress' ? 'bg-purple-500/20 text-purple-400' : 'bg-slate-800 text-slate-500'
                  }`}>
                    {phase.status === 'completed' ? <CheckCircle2 className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
                  </div>
                  <h4 className="font-bold text-sm text-slate-200">{phase.name}</h4>
                </div>

                <span className={`text-[10px] font-bold uppercase px-2.5 py-0.5 rounded ${
                  phase.status === 'completed' ? 'bg-emerald-500/20 text-emerald-300' :
                  phase.status === 'in_progress' ? 'bg-purple-500/20 text-purple-300' : 'bg-slate-800 text-slate-400'
                }`}>
                  {phase.status}
                </span>
              </div>

              <p className="text-xs text-slate-400 mt-2 ml-8 leading-relaxed">
                {phase.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default RoadmapPage;
