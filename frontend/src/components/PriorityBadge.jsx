import React from 'react';

export const PriorityBadge = ({ priority }) => {
  const p = (priority || '').toUpperCase();
  
  let style = 'bg-slate-800 text-slate-300 border-slate-700';
  let label = p;

  if (p === 'P0') {
    style = 'bg-rose-600/20 text-rose-300 border-rose-500/40 font-bold animate-pulse';
    label = 'P0 (Immediate)';
  } else if (p === 'P1') {
    style = 'bg-orange-500/20 text-orange-300 border-orange-500/40 font-semibold';
    label = 'P1 (High)';
  } else if (p === 'P2') {
    style = 'bg-blue-500/20 text-blue-300 border-blue-500/40';
    label = 'P2 (Planned)';
  } else if (p === 'P3') {
    style = 'bg-slate-500/20 text-slate-400 border-slate-500/30';
    label = 'P3 (Monitor)';
  }

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-md text-xs border ${style}`}>
      {label}
    </span>
  );
};

export default PriorityBadge;
