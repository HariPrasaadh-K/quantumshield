import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { api } from '../api/client';
import RiskBadge from '../components/RiskBadge';
import PriorityBadge from '../components/PriorityBadge';
import { LoadingState, EmptyState, ErrorState } from '../components/EmptyState';
import { Filter, ArrowUpDown } from 'lucide-react';

export const AssetsPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Filters
  const [algorithmFilter, setAlgorithmFilter] = useState('');
  const [purposeFilter, setPurposeFilter] = useState('');
  const [riskFilter, setRiskFilter] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('');
  const [languageFilter, setLanguageFilter] = useState('');

  // Sorting
  const [sortBy, setSortBy] = useState('risk_score'); // risk_score, priority, algorithm
  const [sortOrder, setSortOrder] = useState('desc');

  const fetchAssets = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.getAssets(id, {
        algorithm: algorithmFilter || undefined,
        purpose: purposeFilter || undefined,
        risk: riskFilter || undefined,
        priority: priorityFilter || undefined,
        language: languageFilter || undefined,
      });
      setAssets(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to fetch assets');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAssets();
  }, [id, algorithmFilter, purposeFilter, riskFilter, priorityFilter, languageFilter]);

  // Handle client-side sorting
  const sortedAssets = [...assets].sort((a, b) => {
    let valA = a[sortBy];
    let valB = b[sortBy];

    if (sortBy === 'priority') {
      const pMap = { P0: 4, P1: 3, P2: 2, P3: 1 };
      valA = pMap[a.priority] || 0;
      valB = pMap[b.priority] || 0;
    }

    if (valA < valB) return sortOrder === 'asc' ? -1 : 1;
    if (valA > valB) return sortOrder === 'asc' ? 1 : -1;
    return 0;
  });

  const toggleSort = (field) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(field);
      setSortOrder('desc');
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-slate-100">Cryptographic Assets Inventory (CBOM)</h2>
        <p className="text-sm text-slate-400 mt-1">
          Complete bill of materials listing every cryptographic algorithm, key size, signature scheme, and hashing function discovered in source files.
        </p>
      </div>

      {/* Filter Controls Bar */}
      <div className="bg-[#111827] border border-slate-800 rounded-xl p-4 flex flex-wrap gap-4 items-center">
        <div className="flex items-center space-x-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">
          <Filter className="w-4 h-4 text-purple-400" />
          <span>Filter CBOM:</span>
        </div>

        <input
          type="text"
          placeholder="Filter algorithm (e.g. RSA)..."
          value={algorithmFilter}
          onChange={(e) => setAlgorithmFilter(e.target.value)}
          className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-purple-500"
        />

        <select
          value={riskFilter}
          onChange={(e) => setRiskFilter(e.target.value)}
          className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-purple-500"
        >
          <option value="">All Risk Types</option>
          <option value="Quantum">Quantum</option>
          <option value="Classical">Classical</option>
          <option value="Monitor">Monitor</option>
          <option value="Unknown">Unknown</option>
        </select>

        <select
          value={priorityFilter}
          onChange={(e) => setPriorityFilter(e.target.value)}
          className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-purple-500"
        >
          <option value="">All Priorities</option>
          <option value="P0">P0 (Immediate)</option>
          <option value="P1">P1 (High)</option>
          <option value="P2">P2 (Planned)</option>
          <option value="P3">P3 (Monitor)</option>
        </select>

        <select
          value={purposeFilter}
          onChange={(e) => setPurposeFilter(e.target.value)}
          className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-purple-500"
        >
          <option value="">All Purposes</option>
          <option value="Key Establishment">Key Establishment</option>
          <option value="Digital Signature">Digital Signature</option>
          <option value="Encryption">Encryption</option>
          <option value="Hashing">Hashing</option>
          <option value="TLS">TLS</option>
          <option value="Unknown">Unknown</option>
        </select>
      </div>

      {/* Main Assets Table */}
      {loading ? (
        <LoadingState message="Fetching cryptographic assets from database..." />
      ) : error ? (
        <ErrorState message={error} onRetry={fetchAssets} />
      ) : sortedAssets.length === 0 ? (
        <EmptyState
          title="No Matching Assets Discovered"
          description="No cryptographic findings match the selected filter criteria."
        />
      ) : (
        <div className="bg-[#111827] border border-slate-800 rounded-xl overflow-hidden shadow-xl">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400 uppercase font-semibold bg-[#0F172A]">
                  <th className="py-3.5 px-4 cursor-pointer" onClick={() => toggleSort('algorithm')}>
                    <div className="flex items-center space-x-1">
                      <span>Algorithm</span>
                      <ArrowUpDown className="w-3 h-3 text-slate-500" />
                    </div>
                  </th>
                  <th className="py-3.5 px-4">Purpose</th>
                  <th className="py-3.5 px-4">Risk Type</th>
                  <th className="py-3.5 px-4 cursor-pointer" onClick={() => toggleSort('risk_score')}>
                    <div className="flex items-center space-x-1">
                      <span>Risk Score</span>
                      <ArrowUpDown className="w-3 h-3 text-slate-500" />
                    </div>
                  </th>
                  <th className="py-3.5 px-4 cursor-pointer" onClick={() => toggleSort('priority')}>
                    <div className="flex items-center space-x-1">
                      <span>Priority</span>
                      <ArrowUpDown className="w-3 h-3 text-slate-500" />
                    </div>
                  </th>
                  <th className="py-3.5 px-4">Language</th>
                  <th className="py-3.5 px-4">File Location</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {sortedAssets.map((asset) => (
                  <tr
                    key={asset.id}
                    onClick={() => navigate(`/projects/${id}/assets/${asset.id}`)}
                    className="hover:bg-slate-800/50 cursor-pointer transition-colors"
                  >
                    <td className="py-3.5 px-4 font-semibold text-slate-200">{asset.algorithm}</td>
                    <td className="py-3.5 px-4 text-slate-300">{asset.crypto_purpose}</td>
                    <td className="py-3.5 px-4"><RiskBadge risk={asset.risk_type} /></td>
                    <td className="py-3.5 px-4 font-mono font-bold text-slate-200">{asset.risk_score}</td>
                    <td className="py-3.5 px-4"><PriorityBadge priority={asset.priority} /></td>
                    <td className="py-3.5 px-4 text-slate-400 font-mono">{asset.language || 'N/A'}</td>
                    <td className="py-3.5 px-4 text-purple-400 font-mono hover:underline truncate max-w-[250px]">
                      {asset.file_path}:{asset.line_number}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default AssetsPage;
