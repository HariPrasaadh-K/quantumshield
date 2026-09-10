import React from 'react';
import { NavLink, useParams } from 'react-router-dom';
import { 
  LayoutDashboard, 
  FolderKanban, 
  ShieldAlert, 
  Sparkles, 
  Map, 
  Network, 
  FileText, 
  ShieldCheck 
} from 'lucide-react';
import { useProject } from '../context/ProjectContext';

export const Sidebar = () => {
  const { currentProject } = useProject();
  const projectId = currentProject?.id;

  const baseNavs = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Projects', path: '/projects', icon: FolderKanban },
  ];

  const projectNavs = projectId ? [
    { name: 'Overview', path: `/projects/${projectId}`, icon: FolderKanban },
    { name: 'Crypto Assets', path: `/projects/${projectId}/assets`, icon: ShieldAlert },
    { name: 'Recommendations', path: `/projects/${projectId}/recommendations`, icon: Sparkles },
    { name: 'Migration Roadmap', path: `/projects/${projectId}/roadmap`, icon: Map },
    { name: 'Dependency Graph', path: `/projects/${projectId}/graph`, icon: Network },
  ] : [];

  return (
    <aside className="w-64 bg-[#0F172A] border-r border-slate-800 flex flex-col justify-between h-screen sticky top-0">
      <div>
        {/* Brand Header */}
        <div className="h-16 flex items-center px-6 border-b border-slate-800 space-x-3">
          <div className="p-2 bg-purple-600/20 border border-purple-500/30 rounded-lg">
            <ShieldCheck className="w-6 h-6 text-purple-400" />
          </div>
          <div>
            <h1 className="font-bold text-slate-100 text-lg leading-tight tracking-tight">QuantumShield</h1>
            <span className="text-[10px] text-purple-400 font-mono uppercase tracking-widest">PQC CBOM Engine</span>
          </div>
        </div>

        {/* Global Navigation */}
        <div className="p-4 space-y-1">
          <p className="px-3 text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-2">Main Menu</p>
          {baseNavs.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-purple-600/15 text-purple-400 border border-purple-500/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`
              }
            >
              <item.icon className="w-4 h-4" />
              <span>{item.name}</span>
            </NavLink>
          ))}
        </div>

        {/* Project Specific Navigation */}
        {projectId && (
          <div className="p-4 pt-2 space-y-1">
            <p className="px-3 text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-2">Active Project</p>
            {projectNavs.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-purple-600/15 text-purple-400 border border-purple-500/30'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                  }`
                }
              >
                <item.icon className="w-4 h-4" />
                <span>{item.name}</span>
              </NavLink>
            ))}
          </div>
        )}
      </div>

      {/* Footer Info */}
      <div className="p-4 border-t border-slate-800 bg-[#0B0F19]/50 text-xs text-slate-500">
        <p className="font-semibold text-slate-400">SIH 2026 PS 26164</p>
        <p className="text-[11px] mt-0.5">NIST PQC Standards (FIPS 203/204)</p>
      </div>
    </aside>
  );
};

export default Sidebar;
