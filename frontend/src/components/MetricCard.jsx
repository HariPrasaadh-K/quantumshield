import React from 'react';

export const MetricCard = ({ title, value, icon: Icon, color = 'purple', subtitle, subValue }) => {
  const colorStyles = {
    purple: 'text-purple-400 bg-purple-500/10 border-purple-500/20',
    red: 'text-red-400 bg-red-500/10 border-red-500/20',
    amber: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
    blue: 'text-blue-400 bg-blue-500/10 border-blue-500/20',
    emerald: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
  };

  const currentStyle = colorStyles[color] || colorStyles.purple;

  return (
    <div className="bg-[#111827] border border-slate-800 rounded-xl p-5 hover:border-slate-700 transition-all shadow-lg">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">{title}</p>
          <p className="text-3xl font-bold text-slate-100 mt-2">{value}</p>
          {subtitle && (
            <p className="text-xs text-slate-400 mt-1">
              {subtitle} <span className="font-semibold text-slate-200">{subValue}</span>
            </p>
          )}
        </div>
        {Icon && (
          <div className={`p-3 rounded-lg border ${currentStyle}`}>
            <Icon className="w-6 h-6" />
          </div>
        )}
      </div>
    </div>
  );
};

export default MetricCard;
