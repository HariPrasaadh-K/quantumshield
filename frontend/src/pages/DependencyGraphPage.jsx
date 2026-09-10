import React, { useEffect, useState, useCallback, useMemo } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  ReactFlow, 
  Controls, 
  Background, 
  useNodesState, 
  useEdgesState 
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { api } from '../api/client';
import CustomNode from '../components/CustomNode';
import { LoadingState, EmptyState, ErrorState } from '../components/EmptyState';
import { Network, Filter, ZoomIn, Info } from 'lucide-react';

export const DependencyGraphPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [rawGraph, setRawGraph] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Filters
  const [riskFilter, setRiskFilter] = useState('');
  const [nodeTypeFilter, setNodeTypeFilter] = useState('');

  const nodeTypes = useMemo(() => ({ custom: CustomNode }), []);

  const fetchGraph = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.getDependencyGraph(id);
      setRawGraph(res.data);
      setNodes(res.data.nodes || []);
      setEdges(res.data.edges || []);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to load dependency graph');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGraph();
  }, [id]);

  // Apply filters
  useEffect(() => {
    if (!rawGraph) return;

    let filteredNodes = rawGraph.nodes || [];

    if (riskFilter) {
      filteredNodes = filteredNodes.filter(
        (n) => n.data.risk === riskFilter || n.data.type === 'project'
      );
    }

    if (nodeTypeFilter) {
      filteredNodes = filteredNodes.filter(
        (n) => n.data.type === nodeTypeFilter || n.data.type === 'project'
      );
    }

    const validNodeIds = new Set(filteredNodes.map((n) => n.id));
    const filteredEdges = (rawGraph.edges || []).filter(
      (e) => validNodeIds.has(e.source) && validNodeIds.has(e.target)
    );

    setNodes(filteredNodes);
    setEdges(filteredEdges);
  }, [riskFilter, nodeTypeFilter, rawGraph]);

  const onNodeClick = useCallback((event, node) => {
    if (node.data.type === 'crypto_asset' && node.data.id) {
      const assetDbId = node.data.id.replace('asset-', '');
      navigate(`/projects/${id}/assets/${assetDbId}`);
    }
  }, [id, navigate]);

  if (loading) return <div className="p-8"><LoadingState message="Building interactive React Flow dependency graph..." /></div>;
  if (error) return <div className="p-8"><ErrorState message={error} onRetry={fetchGraph} /></div>;

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-slate-100 flex items-center space-x-2">
            <span>Cryptographic Dependency & Blast Radius Graph</span>
            <Network className="w-6 h-6 text-purple-400" />
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Visual representation mapping relationships between project repositories, files, cryptographic primitives, and imported libraries.
          </p>
        </div>
      </div>

      {/* Filter Controls Bar */}
      <div className="bg-[#111827] border border-slate-800 rounded-xl p-4 flex flex-wrap gap-4 items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">
            <Filter className="w-4 h-4 text-purple-400" />
            <span>Filter Graph:</span>
          </div>

          <select
            value={riskFilter}
            onChange={(e) => setRiskFilter(e.target.value)}
            className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-purple-500"
          >
            <option value="">All Risk Levels</option>
            <option value="Quantum">Quantum Vulnerable</option>
            <option value="Classical">Classical Weakness</option>
            <option value="Monitor">Monitor Items</option>
          </select>

          <select
            value={nodeTypeFilter}
            onChange={(e) => setNodeTypeFilter(e.target.value)}
            className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-purple-500"
          >
            <option value="">All Node Types</option>
            <option value="crypto_asset">Crypto Assets</option>
            <option value="file">Source Files</option>
            <option value="library">Libraries</option>
          </select>
        </div>

        {/* Legend */}
        <div className="flex items-center space-x-4 text-xs">
          <div className="flex items-center space-x-1.5">
            <span className="w-3 h-3 rounded-full bg-red-500"></span>
            <span className="text-slate-300">Quantum (P0/P1)</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-3 h-3 rounded-full bg-amber-500"></span>
            <span className="text-slate-300">Classical</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-3 h-3 rounded-full bg-emerald-500"></span>
            <span className="text-slate-300">Monitor</span>
          </div>
        </div>
      </div>

      {/* React Flow Graph Canvas Container */}
      <div className="bg-[#0B0F19] border border-slate-800 rounded-xl h-[650px] shadow-2xl relative overflow-hidden">
        {nodes.length === 0 ? (
          <EmptyState title="Empty Graph" description="No nodes to display." />
        ) : (
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onNodeClick={onNodeClick}
            nodeTypes={nodeTypes}
            fitView
            className="bg-slate-950"
          >
            <Controls className="!bg-slate-900 !border-slate-800 !text-slate-200 fill-slate-200" />
            <Background color="#1E293B" gap={24} size={1} />
          </ReactFlow>
        )}
      </div>
    </div>
  );
};

export default DependencyGraphPage;
