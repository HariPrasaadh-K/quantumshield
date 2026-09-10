import React from 'react';

export const RiskBadge = ({ risk, score }) => {
  const r = (risk || '').toUpperCase();
  
  let colors = 'bg-slate-800 text-slate-300 border-slate-700';
  if (r === 'QUANTUM' || r === 'CRITICAL') {
    colors = 'bg-red-500/10 text-red-400 border-red-500/30';
  } else if (r === 'HIGH' || r === 'CLASSICAL') {
    colors = 'bg-amber-500/10 text-amber-400 border-amber-500/30';
  } else if (r === 'MEDIUM') {
    colors = 'bg-yellow-500/10 text-yellow-400 border-yellow-500/30';
  } else if (r === 'MONITOR' || r === 'LOW') {
    colors = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
  }

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${colors}`}>
      {risk} {score !== undefined && score !== null ? `(${score})` : ''}
    </span>
  );
};

export default RiskBadge;
