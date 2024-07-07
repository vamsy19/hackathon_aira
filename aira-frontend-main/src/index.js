import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import LoginPage from './pages/loginPage';
import WorkspacePage from './pages/workspacePage';
import CreateOrganizationPage from './pages/createOrganizationPage';
import CreateProjectPage from './pages/createProjectPage';
import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/workspace" element={<WorkspacePage />} />
        <Route path="/create-organization" element={<CreateOrganizationPage />} />
        <Route path="/create-project" element={<CreateProjectPage />} />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  </React.StrictMode>
);