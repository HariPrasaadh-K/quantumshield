import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { api } from '../api/client';
import { useProject } from '../context/ProjectContext';
import MetricCard from '../components/MetricCard';
import { LoadingState, ErrorState } from '../components/EmptyState';
import { 
  Play, 
  ShieldAlert, 
  Flame, 
  Layers, 
  FileText, 
  Map, 
  Network, 
  Sparkles,
  ArrowRight,
  Clock
} from 'lucide-react';

export const ProjectOverview = () => {
  const { id } = useParams();
  const { setCurrentProject, projects } = useProject();
  const navigate = useNavigate();

  const [project, setProject] = useState(null);
  const [scans, setScans] = useState([]);
  const [riskSummary, setRiskSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [scanning, setScanning] = useState(false);
  const [error, setError] = useState(null);

  const loadOverview = async () => {
    setLoading(true);
    setError(null);
    try {
      const [projRes, scansRes, riskRes] = await Promise.all([
        api.getProject(id),
        api.getProjectScans(id),
        api.getRiskSummary(id)
      ]);
      setProject(projRes.data);
      setCurrentProject(projRes.data);
      setScans(scansRes.data);
      setRiskSummary(riskRes.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to load project details');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadOverview();
  }, [id]);

  const handleRunScan = async () => {
    setScanning(true);
    try {
      await api.startScan(id);
      await loadOverview();
    } catch (err) {
      alert(`Scan failed: ${err.response?.data?.detail || err.message}`);
    } finally {
      setScanning(false);
    }
  };

  if (loading) return <div className="p-8"><LoadingState message="Loading project workspace..." /></div>;
  if (error) return <div className="p-8"><ErrorState message={error} onRetry={loadOverview} /></div>;

  const latestScan = scans.length > 0 ? scans[0] : null;

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8">
      {/* Top Header & Run Scan Button */}
      <div className="flex justify-between items-center bg-[#111827] border border-slate-800 rounded-xl p-6 shadow-xl">
        <div>
          <span className="text-xs font-mono uppercase text-purple-400 font-semibold">{project.source_type} Repository</span>
          <h2 className="text-2xl font-bold text-slate-100 mt-1">{project.name}</h2>
          <p className="text-xs text-slate-400 mt-1">ID: {project.id}</p>
        </div>

        <div className="flex items-center space-x-4">
          <button
            onClick={handleRunScan}
            disabled={scanning}
            className="flex items-center space-x-2 bg-purple-600 hover:bg-purple-500 text-white font-semibold px-5 py-2.5 rounded-lg shadow-lg transition-all disabled:opacity-50"
          >
            <Play className="w-4 h-4 fill-current" />
            <span>{scanning ? 'Running Static Analysis...' : 'Run Scan'}</span>
          </button>
        </div>
      </div>

      {/* Metrics Row */}
      {riskSummary && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
          <MetricCard
            title="Discovered Assets"
            value={riskSummary.total_crypto_assets}
            icon={Layers}
            color="purple"
          />
          <MetricCard
            title="Quantum Vulnerable"
            value={riskSummary.quantum_vulnerable}
            icon={ShieldAlert}
            color="red"
          />
          <MetricCard
            title="Critical Risk Assets"
            value={riskSummary.critical_risk}
            icon={Flame}
            color="amber"
          />
          <MetricCard
            title="P0 Immediate Priority"
            value={riskSummary.priority_distribution.P0 || 0}
            icon={Clock}
            color="red"
          />
        </div>
      )}

      {/* Quick Navigation Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
        <Link
          to={`/projects/${id}/assets`}
          className="bg-[#111827] border border-slate-800 hover:border-purple-500/50 p-5 rounded-xl transition-all shadow-md group"
        >
          <ShieldAlert className="w-6 h-6 text-purple-400 mb-2 group-hover:scale-110 transition-transform" />
          <h4 className="font-semibold text-slate-200 text-sm">Crypto Asset Inventory</h4>
          <p className="text-xs text-slate-400 mt-1">Explore findings, raw context code snippets, and evidence.</p>
        </Link>

        <Link
          to={`/projects/${id}/recommendations`}
          className="bg-[#111827] border border-slate-800 hover:border-emerald-500/50 p-5 rounded-xl transition-all shadow-md group"
        >
          <Sparkles className="w-6 h-6 text-emerald-400 mb-2 group-hover:scale-110 transition-transform" />
          <h4 className="font-semibold text-slate-200 text-sm">PQC Recommendations</h4>
          <p className="text-xs text-slate-400 mt-1">NIST FIPS 203/204 candidate migration alternatives.</p>
        </Link>

        <Link
          to={`/projects/${id}/roadmap`}
          className="bg-[#111827] border border-slate-800 hover:border-blue-500/50 p-5 rounded-xl transition-all shadow-md group"
        >
          <Map className="w-6 h-6 text-blue-400 mb-2 group-hover:scale-110 transition-transform" />
          <h4 className="font-semibold text-slate-200 text-sm">Migration Roadmap</h4>
          <p className="text-xs text-slate-400 mt-1">Mosca theorem timeline & phased security window analysis.</p>
        </Link>

        <Link
          to={`/projects/${id}/graph`}
          className="bg-[#111827] border border-slate-800 hover:border-purple-500/50 p-5 rounded-xl transition-all shadow-md group"
        >
          <Network className="w-6 h-6 text-purple-400 mb-2 group-hover:scale-110 transition-transform" />
          <h4 className="font-semibold text-slate-200 text-sm">Dependency Graph</h4>
          <p className="text-xs text-slate-400 mt-1">Interactive React Flow visual graph of asset relationships.</p>
        </Link>
      </div>

      {/* Latest Scan Details */}
      <div className="bg-[#111827] border border-slate-800 rounded-xl p-6 shadow-xl">
        <h3 className="text-sm font-semibold text-slate-200 uppercase tracking-wider mb-4">Scan Execution History</h3>
        {scans.length === 0 ? (
          <p className="text-xs text-slate-400">No scans executed yet. Click "Run Scan" above to analyze this project.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400 uppercase font-semibold">
                  <th className="py-3 px-3">Scan ID</th>
                  <th className="py-3 px-3">Status</th>
                  <th className="py-3 px-3">Files Scanned</th>
                  <th className="py-3 px-3">Findings</th>
                  <th className="py-3 px-3">Assets Created</th>
                  <th className="py-3 px-3">Started At</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {scans.map((s) => (
                  <tr key={s.id} className="hover:bg-slate-800/50">
                    <td className="py-3 px-3 font-mono text-slate-300">{s.id.substring(0, 8)}...</td>
                    <td className="py-3 px-3">
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-purple-500/10 text-purple-400 border border-purple-500/20">
                        {s.status}
                      </span>
                    </td>
                    <td className="py-3 px-3 text-slate-300 font-bold">{s.files_scanned}</td>
                    <td className="py-3 px-3 text-slate-300 font-bold">{s.findings_found}</td>
                    <td className="py-3 px-3 text-slate-300 font-bold">{s.assets_found}</td>
                    <td className="py-3 px-3 text-slate-400">{new Date(s.started_at).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProjectOverview;
