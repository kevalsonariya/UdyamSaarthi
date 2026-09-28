import React from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import Navbar from './Navbar';
import Footer from './Footer';
import ProgressIndicator from '../components/common/ProgressIndicator';

export const MainLayout = () => {
  const location = useLocation();

  // Show progress indicator only on the core multi-step advisory flow
  const workflowRoutes = ['/business-input', '/analysis', '/financial', '/report'];
  const showProgress = workflowRoutes.includes(location.pathname);

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-800">
      <Navbar />
      {showProgress && <ProgressIndicator />}
      <main className="flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 py-6 sm:py-8">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
};

export default MainLayout;
