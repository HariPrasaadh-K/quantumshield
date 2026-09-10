import React from 'react';
import { ShieldAlert, AlertTriangle, RefreshCw } from 'lucide-react';

export const EmptyState = ({ title, description, actionText, onAction }) => (
  <div className="flex flex-col items-center justify-center py-16 px-4 border border-dashed border-slate-800 rounded-xl bg-slate-900/30 text-center">
    <div className="p-4 bg-purple-500/10 border border-purple-500/20 rounded-full mb-4">
      <ShieldAlert className="w-8 h-8 text-purple-400" />
    </div>
    <h3 className="text-lg font-semibold text-slate-200">{title}</h3>
    <p className="text-sm text-slate-400 max-w-md mt-1 mb-6">{description}</p>
    {actionText && onAction && (
      <button
        onClick={onAction}
        className="bg-purple-600 hover:bg-purple-500 text-white font-medium text-sm px-5 py-2 rounded-lg transition-colors shadow-lg"
      >
        {actionText}
      </button>
    )}
  </div>
);

export const LoadingState = ({ message = 'Analyzing cryptographic assets...' }) => (
  <div className="flex flex-col items-center justify-center py-20 text-center">
    <div className="animate-spin p-3 bg-purple-500/10 border border-purple-500/20 rounded-full mb-4 text-purple-400">
      <RefreshCw className="w-8 h-8" />
    </div>
    <p className="text-sm font-medium text-slate-300">{message}</p>
  </div>
);

export const ErrorState = ({ message = 'An unexpected error occurred.', onRetry }) => (
  <div className="flex flex-col items-center justify-center py-12 px-4 border border-red-500/20 rounded-xl bg-red-500/5 text-center">
    <AlertTriangle className="w-8 h-8 text-red-400 mb-3" />
    <h4 className="text-base font-semibold text-red-300">Scanning & Analysis Error</h4>
    <p className="text-sm text-slate-400 max-w-md mt-1 mb-4">{message}</p>
    {onRetry && (
      <button
        onClick={onRetry}
        className="bg-red-600 hover:bg-red-500 text-white text-xs font-medium px-4 py-2 rounded-lg transition-colors"
      >
        Try Again
      </button>
    )}
  </div>
);

export default EmptyState;
