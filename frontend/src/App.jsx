import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ProjectProvider, useProject } from './context/ProjectContext';
import Sidebar from './components/Sidebar';
import Topbar from './components/Topbar';

import Dashboard from './pages/Dashboard';
import Projects from './pages/Projects';
import ProjectOverview from './pages/ProjectOverview';
import AssetsPage from './pages/AssetsPage';
import AssetDetailsPage from './pages/AssetDetailsPage';
import RecommendationsPage from './pages/RecommendationsPage';
import RoadmapPage from './pages/RoadmapPage';
import DependencyGraphPage from './pages/DependencyGraphPage';
import { api } from './api/client';

const MainLayout = () => {
  const { currentProject, fetchProjects } = useProject();
  const [scanning, setScanning] = useState(false);

  const handleGlobalScan = async () => {
    if (!currentProject) return;
    setScanning(true);
    try {
      await api.startScan(currentProject.id);
      await fetchProjects();
      window.location.reload();
    } catch (err) {
      alert(`Scan execution error: ${err.response?.data?.detail || err.message}`);
    } finally {
      setScanning(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-[#0B0F19]">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Topbar onTriggerScan={handleGlobalScan} scanning={scanning} />
        <main className="flex-1 overflow-y-auto">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/projects" element={<Projects />} />
            <Route path="/projects/:id" element={<ProjectOverview />} />
            <Route path="/projects/:id/assets" element={<AssetsPage />} />
            <Route path="/projects/:id/assets/:assetId" element={<AssetDetailsPage />} />
            <Route path="/projects/:id/recommendations" element={<RecommendationsPage />} />
            <Route path="/projects/:id/roadmap" element={<RoadmapPage />} />
            <Route path="/projects/:id/graph" element={<DependencyGraphPage />} />
          </Routes>
        </main>
      </div>
    </div>
  );
};

export function App() {
  return (
    <Router>
      <ProjectProvider>
        <MainLayout />
      </ProjectProvider>
    </Router>
  );
}

export default App;
