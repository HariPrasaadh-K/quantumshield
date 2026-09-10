import React from 'react';
import { useProject } from '../context/ProjectContext';
import { Download, FileCode, Play, FolderKanban } from 'lucide-react';
import { api } from '../api/client';

export const Topbar = ({ onTriggerScan, scanning }) => {
  const { projects, currentProject, setCurrentProject } = useProject();

  const handleExportJson = () => {
    if (!currentProject) return;
    window.open(api.getCbomJsonUrl(currentProject.id), '_blank');
  };

  const handleExportPdf = () => {
    if (!currentProject) return;
    window.open(api.getPdfReportUrl(currentProject.id), '_blank');
  };

  return (
    <header className="h-16 bg-[#0F172A] border-b border-slate-800 flex items-center justify-between px-8 sticky top-0 z-30">
      {/* Active Project Switcher */}
      <div className="flex items-center space-x-3">
        <FolderKanban className="w-5 h-5 text-slate-400" />
        <select
          value={currentProject?.id || ''}
          onChange={(e) => {
            const p = projects.find((item) => item.id === e.target.value);
            if (p) setCurrentProject(p);
          }}
          className="bg-slate-900 text-slate-200 border border-slate-700 rounded-lg px-3 py-1.5 text-sm font-medium focus:outline-none focus:border-purple-500"
        >
          {projects.length === 0 && <option value="">No projects available</option>}
          {projects.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name} ({p.source_type.toUpperCase()})
            </option>
          ))}
        </select>
      </div>

      {/* Action Buttons */}
      <div className="flex items-center space-x-3">
        {currentProject && (
          <>
            {onTriggerScan && (
              <button
                onClick={onTriggerScan}
                disabled={scanning}
                className="flex items-center space-x-2 bg-purple-600 hover:bg-purple-500 text-white px-4 py-1.5 rounded-lg text-sm font-medium transition-all shadow-md disabled:opacity-50"
              >
                <Play className="w-4 h-4 fill-current" />
                <span>{scanning ? 'Scanning...' : 'Run Scan'}</span>
              </button>
            )}

            <button
              onClick={handleExportJson}
              className="flex items-center space-x-2 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors"
              title="Export CycloneDX CBOM JSON"
            >
              <FileCode className="w-4 h-4 text-purple-400" />
              <span>CBOM JSON</span>
            </button>

            <button
              onClick={handleExportPdf}
              className="flex items-center space-x-2 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors"
              title="Export Full PDF Report"
            >
              <Download className="w-4 h-4 text-emerald-400" />
              <span>PDF Report</span>
            </button>
          </>
        )}
      </div>
    </header>
  );
};

export default Topbar;
