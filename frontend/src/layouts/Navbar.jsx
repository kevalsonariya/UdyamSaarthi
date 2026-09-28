import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Compass, FileText, PieChart, Home, PlusCircle } from 'lucide-react';

export const Navbar = () => {
  const location = useLocation();

  const navLinks = [
    { to: '/home', label: 'Home', icon: Home },
    { to: '/business-input', label: 'New Business', icon: PlusCircle },
    { to: '/analysis', label: 'Feasibility & Market', icon: Compass },
    { to: '/financial', label: 'Financial Plan', icon: PieChart },
    { to: '/report', label: 'Summary Report', icon: FileText },
  ];

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200">
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-16 sm:h-20">
          {/* Logo & Tagline */}
          <Link to="/home" className="flex items-center gap-3 group text-decoration-none">
            <div className="w-10 h-10 sm:w-11 sm:h-11 rounded-2xl bg-emerald-800 text-white flex items-center justify-center font-black text-xl shadow-md group-hover:bg-emerald-900 transition-colors">
              BS
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xl sm:text-2xl font-extrabold text-emerald-950 tracking-tight">
                  Biz<span className="text-amber-600">Sahayak</span>
                </span>
                <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200">
                  SIH 2026
                </span>
              </div>
              <p className="text-[11px] text-slate-500 font-medium hidden sm:block">
                From Business Idea → Business Insight → Financial Plan
              </p>
            </div>
          </Link>

          {/* Navigation Links */}
          <nav className="flex items-center gap-1 sm:gap-2">
            {navLinks.map((link) => {
              const Icon = link.icon;
              const isActive = location.pathname === link.to;

              return (
                <Link
                  key={link.to}
                  to={link.to}
                  className={`inline-flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all ${
                    isActive
                      ? 'bg-emerald-800 text-white shadow-xs'
                      : 'text-slate-600 hover:text-emerald-900 hover:bg-emerald-50/60'
                  }`}
                >
                  <Icon className="w-4 h-4 shrink-0" />
                  <span className="hidden md:inline">{link.label}</span>
                </Link>
              );
            })}
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
