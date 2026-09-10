import React, { useState } from 'react';
import { useProject } from '../context/ProjectContext';
import { api } from '../api/client';
import { useNavigate } from 'react-router-dom';
import { 
  FolderPlus, 
  UploadCloud, 
  Github, 
  Sparkles, 
  FolderKanban, 
  ArrowRight,
  Play
} from 'lucide-react';
import { LoadingState } from '../components/EmptyState';

export const Projects = () => {
  const { projects, fetchProjects, setCurrentProject } = useProject();
  const navigate = useNavigate();

  const [activeTab, setActiveTab] = useState('demo'); // demo, zip, github
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Form states
  const [zipName, setZipName] = useState('');
  const [zipFile, setZipFile] = useState(null);
  const [ghName, setGhName] = useState('');
  const [ghUrl, setGhUrl] = useState('');

  const handleDemoProject = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.createDemoProject();
      await fetchProjects();
      setCurrentProject(res.data);
      // Immediately run scan on demo project
      await api.startScan(res.data.id);
      navigate(`/projects/${res.data.id}`);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to initialize Demo project');
    } finally {
      setLoading(false);
    }
  };

  const handleZipUpload = async (e) => {
    e.preventDefault();
    if (!zipFile) {
      setError('Please select a ZIP archive to upload.');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append('name', zipName || zipFile.name.replace('.zip', ''));
      formData.append('file', zipFile);

      const res = await api.uploadProjectZip(formData);
      await fetchProjects();
      setCurrentProject(res.data);
      // Run scan immediately
      await api.startScan(res.data.id);
      navigate(`/projects/${res.data.id}`);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to upload ZIP archive');
    } finally {
      setLoading(false);
    }
  };

  const handleGithubSubmit = async (e) => {
    e.preventDefault();
    if (!ghUrl) {
      setError('Please provide a valid public GitHub repository URL.');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await api.createGithubProject({
        name: ghName || ghUrl.split('/').pop().replace('.git', ''),
        github_url: ghUrl
      });
      await fetchProjects();
      setCurrentProject(res.data);
      // Run scan immediately
      await api.startScan(res.data.id);
      navigate(`/projects/${res.data.id}`);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to clone & scan GitHub repository');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-8">
      <div>
        <h2 className="text-2xl font-bold text-slate-100">Project Management</h2>
        <p className="text-sm text-slate-400 mt-1">
          Ingest target software repositories to perform automated static scanning and build a Quantum-Safe CBOM inventory.
        </p>
      </div>

      {/* Creation Card */}
      <div className="bg-[#111827] border border-slate-800 rounded-xl overflow-hidden shadow-xl">
        {/* Tabs */}
        <div className="flex border-b border-slate-800 bg-[#0F172A]">
          <button
            onClick={() => setActiveTab('demo')}
            className={`flex items-center space-x-2 px-6 py-3.5 text-sm font-semibold border-b-2 transition-all ${
              activeTab === 'demo'
                ? 'border-purple-500 text-purple-400 bg-purple-500/10'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Sparkles className="w-4 h-4" />
            <span>Instant Demo Project</span>
          </button>

          <button
            onClick={() => setActiveTab('zip')}
            className={`flex items-center space-x-2 px-6 py-3.5 text-sm font-semibold border-b-2 transition-all ${
              activeTab === 'zip'
                ? 'border-purple-500 text-purple-400 bg-purple-500/10'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <UploadCloud className="w-4 h-4" />
            <span>Upload ZIP Archive</span>
          </button>

          <button
            onClick={() => setActiveTab('github')}
            className={`flex items-center space-x-2 px-6 py-3.5 text-sm font-semibold border-b-2 transition-all ${
              activeTab === 'github'
                ? 'border-purple-500 text-purple-400 bg-purple-500/10'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Github className="w-4 h-4" />
            <span>GitHub Repository</span>
          </button>
        </div>

        {/* Tab Body */}
        <div className="p-6">
          {error && (
            <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 text-red-400 rounded-lg text-xs font-medium">
              {error}
            </div>
          )}

          {loading ? (
            <LoadingState message="Processing project ingestion & executing static scanning pipeline..." />
          ) : (
            <>
              {activeTab === 'demo' && (
                <div className="space-y-4">
                  <div className="p-4 bg-purple-500/10 border border-purple-500/20 rounded-lg">
                    <h4 className="font-semibold text-sm text-purple-300">Quick Test with Demo Suite</h4>
                    <p className="text-xs text-slate-300 mt-1">
                      Instantly load QuantumShield's multi-language demo project containing pre-packaged RSA-2048, ECDSA, ECDH, AES-256-GCM, MD5, and SHA-256 primitives across Java, Python, and Node.js files.
                    </p>
                  </div>
                  <button
                    onClick={handleDemoProject}
                    className="flex items-center space-x-2 bg-purple-600 hover:bg-purple-500 text-white font-semibold text-sm px-5 py-2.5 rounded-lg transition-colors shadow-lg"
                  >
                    <Play className="w-4 h-4 fill-current" />
                    <span>Launch & Scan Demo Project</span>
                  </button>
                </div>
              )}

              {activeTab === 'zip' && (
                <form onSubmit={handleZipUpload} className="space-y-4 max-w-lg">
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                      Project Name (Optional)
                    </label>
                    <input
                      type="text"
                      placeholder="My Secure App"
                      value={zipName}
                      onChange={(e) => setZipName(e.target.value)}
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-purple-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                      ZIP Archive (.zip)
                    </label>
                    <input
                      type="file"
                      accept=".zip"
                      onChange={(e) => setZipFile(e.target.files[0])}
                      className="w-full text-xs text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-purple-600/20 file:text-purple-300 hover:file:bg-purple-600/30"
                    />
                  </div>

                  <button
                    type="submit"
                    className="flex items-center space-x-2 bg-purple-600 hover:bg-purple-500 text-white font-semibold text-sm px-5 py-2.5 rounded-lg transition-colors shadow-lg"
                  >
                    <UploadCloud className="w-4 h-4" />
                    <span>Upload & Scan ZIP</span>
                  </button>
                </form>
              )}

              {activeTab === 'github' && (
                <form onSubmit={handleGithubSubmit} className="space-y-4 max-w-lg">
                  <div>
                    <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                      Project Name
                    </label>
                    <input
                      type="text"
                      placeholder="OpenSSL Repository"
                      value={ghName}
                      onChange={(e) => setGhName(e.target.value)}
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-purple-500"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                      Public GitHub Repository URL
                    </label>
                    <input
                      type="url"
                      placeholder="https://github.com/owner/repository"
                      value={ghUrl}
                      onChange={(e) => setGhUrl(e.target.value)}
                      className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-purple-500"
                    />
                  </div>

                  <button
                    type="submit"
                    className="flex items-center space-x-2 bg-purple-600 hover:bg-purple-500 text-white font-semibold text-sm px-5 py-2.5 rounded-lg transition-colors shadow-lg"
                  >
                    <Github className="w-4 h-4" />
                    <span>Clone & Scan Repository</span>
                  </button>
                </form>
              )}
            </>
          )}
        </div>
      </div>

      {/* Existing Projects Table */}
      <div className="bg-[#111827] border border-slate-800 rounded-xl p-6 shadow-xl">
        <h3 className="text-sm font-semibold text-slate-200 uppercase tracking-wider mb-4">Ingested Projects Catalog</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 uppercase font-semibold">
                <th className="py-3 px-3">Project Name</th>
                <th className="py-3 px-3">Source Type</th>
                <th className="py-3 px-3">Created At</th>
                <th className="py-3 px-3">Status</th>
                <th className="py-3 px-3">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {projects.map((proj) => (
                <tr key={proj.id} className="hover:bg-slate-800/50 transition-colors">
                  <td className="py-3.5 px-3 font-semibold text-slate-200">{proj.name}</td>
                  <td className="py-3.5 px-3 uppercase text-purple-400 font-mono">{proj.source_type}</td>
                  <td className="py-3.5 px-3 text-slate-400">{new Date(proj.created_at).toLocaleDateString()}</td>
                  <td className="py-3.5 px-3">
                    <span className="px-2 py-0.5 rounded text-[10px] uppercase font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                      {proj.status}
                    </span>
                  </td>
                  <td className="py-3.5 px-3">
                    <button
                      onClick={() => {
                        setCurrentProject(proj);
                        navigate(`/projects/${proj.id}`);
                      }}
                      className="flex items-center space-x-1.5 text-xs text-purple-400 hover:text-purple-300 font-medium"
                    >
                      <span>Open Workspace</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Projects;
