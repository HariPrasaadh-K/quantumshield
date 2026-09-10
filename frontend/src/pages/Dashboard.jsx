import React, { useEffect, useState } from 'react';
import { useProject } from '../context/ProjectContext';
import { api } from '../api/client';
import MetricCard from '../components/MetricCard';
import RiskBadge from '../components/RiskBadge';
import PriorityBadge from '../components/PriorityBadge';
import { LoadingState, EmptyState, ErrorState } from '../components/EmptyState';
import { 
  ShieldAlert, 
  AlertOctagon, 
  Flame, 
  CheckCircle2, 
  Layers, 
  Lock,
  ArrowRight
} from 'lucide-react';
import { 
  PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer 
} from 'recharts';
import { useNavigate, Link } from 'react-router-dom';

export const Dashboard = () => {
  const { currentProject } = useProject();
  const navigate = useNavigate();

  const [riskSummary, setRiskSummary] = useState(null);
  const [recentAssets, setRecentAssets] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchDashboardData = async () => {
    if (!currentProject) return;
    setLoading(true);
    setError(null);
    try {
      const [sumRes, assetsRes] = await Promise.all([
        api.getRiskSummary(currentProject.id),
        api.getAssets(currentProject.id)
      ]);
      setRiskSummary(sumRes.data);
      setRecentAssets(assetsRes.data.slice(0, 5));
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, [currentProject]);

  if (!currentProject) {
    return (
      <div className="p-8">
        <EmptyState
          title="No Project Selected"
          description="Create or select a project to discover cryptographic assets and analyze post-quantum readiness."
          actionText="Manage Projects"
          onAction={() => navigate('/projects')}
        />
      </div>
    );
  }

  if (loading) return <div className="p-8"><LoadingState message="Fetching real-time cryptographic intelligence..." /></div>;
  if (error) return <div className="p-8"><ErrorState message={error} onRetry={fetchDashboardData} /></div>;
  if (!riskSummary || riskSummary.total_crypto_assets === 0) {
    return (
      <div className="p-8">
        <EmptyState
          title="No Cryptographic Assets Discovered"
          description={`Project "${currentProject.name}" has not completed a scan yet or contains zero detected cryptographic primitives.`}
          actionText="Run Initial Scan"
          onAction={async () => {
            setLoading(true);
            await api.startScan(currentProject.id);
            fetchDashboardData();
          }}
        />
      </div>
    );
  }

  // Data for Charts
  const riskPieData = [
    { name: 'Quantum Vulnerable', value: riskSummary.quantum_vulnerable, color: '#EF4444' },
    { name: 'Classical Weakness', value: riskSummary.classical_weakness, color: '#F59E0B' },
    { name: 'Monitor Items', value: riskSummary.monitor_items, color: '#10B981' },
  ].filter(d => d.value > 0);

  const priorityPieData = [
    { name: 'P0 Immediate', value: riskSummary.priority_distribution.P0 || 0, color: '#F43F5E' },
    { name: 'P1 High', value: riskSummary.priority_distribution.P1 || 0, color: '#FB923C' },
    { name: 'P2 Planned', value: riskSummary.priority_distribution.P2 || 0, color: '#3B82F6' },
    { name: 'P3 Monitor', value: riskSummary.priority_distribution.P3 || 0, color: '#64748B' },
  ].filter(d => d.value > 0);

  const algoBarData = Object.entries(riskSummary.algorithm_distribution || {}).map(([algo, count]) => ({
    name: algo,
    count
  }));

  const purposeBarData = Object.entries(riskSummary.purpose_distribution || {}).map(([purpose, count]) => ({
    name: purpose,
    count
  }));

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* Header Banner */}
      <div className="flex justify-between items-end border-b border-slate-800 pb-5">
        <div>
          <span className="text-xs font-semibold text-purple-400 uppercase tracking-widest">Executive Dashboard</span>
          <h2 className="text-2xl font-bold text-slate-100 mt-1">{currentProject.name}</h2>
          <p className="text-xs text-slate-400 mt-0.5">Post-Quantum Cryptography Readiness & CBOM Summary</p>
        </div>
        <Link
          to={`/projects/${currentProject.id}/assets`}
          className="flex items-center space-x-2 text-xs text-purple-400 hover:text-purple-300 font-semibold bg-purple-500/10 border border-purple-500/20 px-3 py-2 rounded-lg transition-colors"
        >
          <span>View All ({riskSummary.total_crypto_assets}) Assets</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>

      {/* Top 4 Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        <MetricCard
          title="Total Crypto Assets"
          value={riskSummary.total_crypto_assets}
          icon={Layers}
          color="purple"
          subtitle="Discovered in CBOM"
        />
        <MetricCard
          title="Quantum Vulnerable"
          value={riskSummary.quantum_vulnerable}
          icon={ShieldAlert}
          color="red"
          subtitle="Shor's Algorithm Risk"
        />
        <MetricCard
          title="Critical & High Risk"
          value={riskSummary.critical_risk + riskSummary.high_risk}
          icon={Flame}
          color="amber"
          subtitle="Weighted Risk Score > 60"
        />
        <MetricCard
          title="P0 Immediate Planning"
          value={riskSummary.priority_distribution.P0 || 0}
          icon={AlertOctagon}
          color="red"
          subtitle="Highest Priority Migration"
        />
      </div>

      {/* Analytics Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Risk Distribution Donut */}
        <div className="bg-[#111827] border border-slate-800 rounded-xl p-6 shadow-lg">
          <h3 className="text-sm font-semibold text-slate-200 uppercase tracking-wider mb-4">Risk Categorization</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={riskPieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {riskPieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#1E293B', borderColor: '#334155', borderRadius: '8px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex justify-center space-x-6 text-xs mt-2">
            {riskPieData.map(item => (
              <div key={item.name} className="flex items-center space-x-2">
                <span className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }}></span>
                <span className="text-slate-300">{item.name} ({item.value})</span>
              </div>
            ))}
          </div>
        </div>

        {/* Priority Distribution Chart */}
        <div className="bg-[#111827] border border-slate-800 rounded-xl p-6 shadow-lg">
          <h3 className="text-sm font-semibold text-slate-200 uppercase tracking-wider mb-4">Migration Priority Levels</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={priorityPieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {priorityPieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#1E293B', borderColor: '#334155', borderRadius: '8px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex justify-center space-x-4 text-xs mt-2">
            {priorityPieData.map(item => (
              <div key={item.name} className="flex items-center space-x-1.5">
                <span className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }}></span>
                <span className="text-slate-300">{item.name} ({item.value})</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Algorithm & Purpose Bar Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-[#111827] border border-slate-800 rounded-xl p-6 shadow-lg">
          <h3 className="text-sm font-semibold text-slate-200 uppercase tracking-wider mb-4">Algorithm Breakdown</h3>
          <div className="h-60">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={algoBarData}>
                <XAxis dataKey="name" stroke="#64748B" fontSize={11} />
                <YAxis stroke="#64748B" fontSize={11} />
                <Tooltip contentStyle={{ backgroundColor: '#1E293B', borderColor: '#334155' }} />
                <Bar dataKey="count" fill="#8B5CF6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-[#111827] border border-slate-800 rounded-xl p-6 shadow-lg">
          <h3 className="text-sm font-semibold text-slate-200 uppercase tracking-wider mb-4">Cryptographic Purpose Distribution</h3>
          <div className="h-60">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={purposeBarData}>
                <XAxis dataKey="name" stroke="#64748B" fontSize={11} />
                <YAxis stroke="#64748B" fontSize={11} />
                <Tooltip contentStyle={{ backgroundColor: '#1E293B', borderColor: '#334155' }} />
                <Bar dataKey="count" fill="#3B82F6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Recent Findings Preview Table */}
      <div className="bg-[#111827] border border-slate-800 rounded-xl p-6 shadow-lg">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-sm font-semibold text-slate-200 uppercase tracking-wider">Top Priority Cryptographic Assets</h3>
          <Link to={`/projects/${currentProject.id}/assets`} className="text-xs text-purple-400 hover:underline">
            View All Assets →
          </Link>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 uppercase font-semibold">
                <th className="py-3 px-3">Algorithm</th>
                <th className="py-3 px-3">Purpose</th>
                <th className="py-3 px-3">Risk Type</th>
                <th className="py-3 px-3">Risk Score</th>
                <th className="py-3 px-3">Priority</th>
                <th className="py-3 px-3">Location</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {recentAssets.map((asset) => (
                <tr
                  key={asset.id}
                  onClick={() => navigate(`/projects/${currentProject.id}/assets/${asset.id}`)}
                  className="hover:bg-slate-800/50 cursor-pointer transition-colors"
                >
                  <td className="py-3 px-3 font-semibold text-slate-200">{asset.algorithm}</td>
                  <td className="py-3 px-3 text-slate-400">{asset.crypto_purpose}</td>
                  <td className="py-3 px-3"><RiskBadge risk={asset.risk_type} /></td>
                  <td className="py-3 px-3 font-mono font-bold text-slate-200">{asset.risk_score}</td>
                  <td className="py-3 px-3"><PriorityBadge priority={asset.priority} /></td>
                  <td className="py-3 px-3 font-mono text-slate-400 truncate max-w-[200px]">{asset.file_path}:{asset.line_number}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
