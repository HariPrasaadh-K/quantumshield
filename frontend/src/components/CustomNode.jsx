import React, { memo } from 'react';
import { Handle, Position } from '@xyflow/react';
import { Shield, FileCode, Package, Layers } from 'lucide-react';

const CustomNode = ({ data }) => {
  const { label, type, risk, priority, algorithm, purpose } = data;

  const nodeIcons = {
    project: Layers,
    file: FileCode,
    crypto_asset: Shield,
    library: Package,
  };

  const Icon = nodeIcons[type] || Shield;

  let borderColor = 'border-slate-700 bg-slate-900';
  let badgeColor = 'text-slate-400 bg-slate-800';

  if (type === 'crypto_asset') {
    if (risk === 'Quantum' || priority === 'P0') {
      borderColor = 'border-red-500/80 bg-red-950/30 text-red-300';
      badgeColor = 'bg-red-500/20 text-red-400';
    } else if (risk === 'Classical' || priority === 'P1') {
      borderColor = 'border-amber-500/80 bg-amber-950/30 text-amber-300';
      badgeColor = 'bg-amber-500/20 text-amber-400';
    } else {
      borderColor = 'border-emerald-500/80 bg-emerald-950/30 text-emerald-300';
      badgeColor = 'bg-emerald-500/20 text-emerald-400';
    }
  } else if (type === 'project') {
    borderColor = 'border-purple-500/80 bg-purple-950/40 text-purple-200';
  }

  return (
    <div className={`px-4 py-3 rounded-lg border-2 shadow-xl min-w-[200px] ${borderColor}`}>
      <Handle type="target" position={Position.Top} className="w-2 h-2 !bg-slate-400" />
      
      <div className="flex items-center space-x-2">
        <Icon className="w-4 h-4 shrink-0" />
        <span className="font-semibold text-xs truncate max-w-[150px]">{label}</span>
      </div>

      {type === 'crypto_asset' && (
        <div className="mt-2 space-y-1 text-[10px]">
          <div className="flex justify-between items-center">
            <span className="text-slate-400 font-mono">{algorithm}</span>
            <span className={`px-1.5 py-0.5 rounded font-bold uppercase ${badgeColor}`}>{priority}</span>
          </div>
          <p className="text-slate-500 truncate">{purpose}</p>
        </div>
      )}

      <Handle type="source" position={Position.Bottom} className="w-2 h-2 !bg-slate-400" />
    </div>
  );
};

export default memo(CustomNode);
