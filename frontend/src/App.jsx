import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { BizSahayakProvider } from './hooks/useBizSahayak';
import { LanguageProvider } from './context/LanguageContext';
import { ErrorBoundary } from './components/common/ErrorBoundary';
import MainLayout from './layouts/MainLayout';
import Home from './pages/Home';
import BusinessInput from './pages/BusinessInput';
import Analysis from './pages/Analysis';
import Financial from './pages/Financial';
import Report from './pages/Report';

function App() {
  return (
    <ErrorBoundary>
      <LanguageProvider>
        <BizSahayakProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<MainLayout />}>
              <Route index element={<Navigate to="/home" replace />} />
              <Route path="home" element={<Home />} />
              <Route path="business-input" element={<BusinessInput />} />
              <Route path="analysis" element={<Analysis />} />
              <Route path="financial" element={<Financial />} />
              <Route path="report" element={<Report />} />
              <Route path="*" element={<Navigate to="/home" replace />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </BizSahayakProvider>
    </LanguageProvider>
  </ErrorBoundary>
  );
}

export default App;
