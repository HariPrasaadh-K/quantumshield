import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const client = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Health
  getHealth: () => client.get('/health'),

  // Projects
  getProjects: () => client.get('/projects'),
  getProject: (id) => client.get(`/projects/${id}`),
  uploadProjectZip: (formData) => client.post('/projects/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  createGithubProject: (data) => client.post('/projects/github', data),
  createDemoProject: () => client.post('/projects/demo'),

  // Scans
  startScan: (projectId) => client.post(`/projects/${projectId}/scan`),
  getProjectScans: (projectId) => client.get(`/projects/${projectId}/scans`),

  // Assets
  getAssets: (projectId, params) => client.get(`/projects/${projectId}/assets`, { params }),
  getAssetDetail: (projectId, assetId) => client.get(`/projects/${projectId}/assets/${assetId}`),
  updateAssetContext: (projectId, assetId, updates) => client.patch(`/projects/${projectId}/assets/${assetId}`, updates),
  getRiskSummary: (projectId) => client.get(`/projects/${projectId}/risk-summary`),
  getRecommendations: (projectId) => client.get(`/projects/${projectId}/recommendations`),

  // Roadmap & Graph
  generateRoadmap: (projectId, params) => client.post(`/projects/${projectId}/roadmap`, params),
  getRoadmap: (projectId) => client.get(`/projects/${projectId}/roadmap`),
  getDependencyGraph: (projectId) => client.get(`/projects/${projectId}/dependency-graph`),

  // Export URLs
  getCbomJsonUrl: (projectId) => `${API_BASE_URL}/api/projects/${projectId}/export/json`,
  getPdfReportUrl: (projectId) => `${API_BASE_URL}/api/projects/${projectId}/export/pdf`,
};

export default client;
