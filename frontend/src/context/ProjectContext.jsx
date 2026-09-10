import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../api/client';

const ProjectContext = createContext();

export const ProjectProvider = ({ children }) => {
  const [projects, setProjects] = useState([]);
  const [currentProject, setCurrentProject] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchProjects = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.getProjects();
      setProjects(response.data);
      if (response.data.length > 0 && !currentProject) {
        setCurrentProject(response.data[0]);
      }
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to fetch projects');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const selectProject = (project) => {
    setCurrentProject(project);
  };

  return (
    <ProjectContext.Provider value={{
      projects,
      currentProject,
      setCurrentProject: selectProject,
      fetchProjects,
      loading,
      error
    }}>
      {children}
    </ProjectContext.Provider>
  );
};

export const useProject = () => useContext(ProjectContext);
