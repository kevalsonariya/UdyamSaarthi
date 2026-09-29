import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Compass, FileText, PieChart, Home, PlusCircle } from 'lucide-react';
import { useTranslation, LanguageSelector } from '../context/LanguageContext';

export const Navbar = () => {
  const location = useLocation();
  const { t } = useTranslation();

  const navLinks = [
    { to: '/home', label: t('nav.home'), icon: Home },
    { to: '/business-input', label: t('nav.newBusiness'), icon: PlusCircle },
    { to: '/analysis', label: t('nav.feasibility'), icon: Compass },
    { to: '/financial', label: t('nav.financial'), icon: PieChart },
    { to: '/report', label: t('nav.report'), icon: FileText },
  ];

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200">
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-16 sm:h-20">
          {/* Logo & Tagline */}
          <Link to="/home" className="flex items-center gap-2.5 sm:gap-3 group text-decoration-none shrink-0">
            <div className="w-10 h-10 sm:w-11 sm:h-11 rounded-2xl bg-emerald-800 text-white flex items-center justify-center font-black text-lg sm:text-xl shadow-md group-hover:bg-emerald-900 transition-colors">
              US
            </div>
            <div>
              <div className="flex items-center gap-1.5 sm:gap-2">
                <span className="text-lg sm:text-2xl font-extrabold text-emerald-950 tracking-tight">
                  Udyam<span className="text-amber-600">Saarthi</span>
                </span>
                <span className="text-[10px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200">
                  SIH26091
                </span>
              </div>
              <p className="text-[11px] text-slate-500 font-medium hidden sm:block">
                {t('nav.tagline')}
              </p>
            </div>
          </Link>

          {/* Navigation Links and Language Selector */}
          <div className="flex items-center gap-2 sm:gap-3">
            <nav className="flex items-center gap-1 sm:gap-1.5">
              {navLinks.map((link) => {
                const Icon = link.icon;
                const isActive = location.pathname === link.to;

                return (
                  <Link
                    key={link.to}
                    to={link.to}
                    className={`inline-flex items-center gap-1.5 px-2.5 sm:px-3 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all ${
                      isActive
                        ? 'bg-emerald-800 text-white shadow-xs'
                        : 'text-slate-600 hover:text-emerald-900 hover:bg-emerald-50/60'
                    }`}
                  >
                    <Icon className="w-4 h-4 shrink-0" />
                    <span className="hidden lg:inline">{link.label}</span>
                  </Link>
                );
              })}
            </nav>

            {/* Language Selector */}
            <LanguageSelector />
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
