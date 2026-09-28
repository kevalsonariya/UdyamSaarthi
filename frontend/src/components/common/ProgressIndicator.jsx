import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Check } from 'lucide-react';

const STEPS = [
  { path: '/business-input', label: '1. Business Input', short: 'Input' },
  { path: '/analysis', label: '2. Feasibility & Market', short: 'Analysis' },
  { path: '/financial', label: '3. Financial & Scheme', short: 'Financial' },
  { path: '/report', label: '4. Final Business Plan', short: 'Report' },
];

export const ProgressIndicator = ({ currentStepIndex }) => {
  const location = useLocation();

  // Determine active step index if not explicitly provided
  const activeIndex =
    currentStepIndex !== undefined
      ? currentStepIndex
      : STEPS.findIndex((s) => s.path === location.pathname);

  return (
    <div className="w-full bg-white border-b border-slate-200 py-3.5 px-4 shadow-2xs">
      <div className="max-w-5xl mx-auto">
        <div className="flex items-center justify-between relative">
          {/* Progress bar background line */}
          <div className="absolute top-1/2 left-0 right-0 h-0.5 bg-slate-200 -translate-y-1/2 z-0 hidden sm:block" />

          {/* Active progress bar line */}
          <div
            className="absolute top-1/2 left-0 h-0.5 bg-emerald-700 -translate-y-1/2 z-0 hidden sm:block transition-all duration-300"
            style={{
              width: `${(Math.max(0, activeIndex) / (STEPS.length - 1)) * 100}%`,
            }}
          />

          {STEPS.map((step, idx) => {
            const isCompleted = idx < activeIndex;
            const isCurrent = idx === activeIndex;

            return (
              <Link
                key={step.path}
                to={step.path}
                className="relative z-10 flex flex-col sm:flex-row items-center gap-2 group text-decoration-none focus:outline-none"
              >
                <div
                  className={`w-7 h-7 sm:w-8 sm:h-8 rounded-full flex items-center justify-center text-xs font-bold transition-all duration-200 ${
                    isCompleted
                      ? 'bg-emerald-700 text-white shadow-xs'
                      : isCurrent
                      ? 'bg-amber-500 text-white ring-4 ring-amber-100 shadow-sm'
                      : 'bg-slate-100 text-slate-500 border border-slate-300 group-hover:bg-slate-200'
                  }`}
                >
                  {isCompleted ? <Check className="w-4 h-4 stroke-[3]" /> : idx + 1}
                </div>
                <span
                  className={`text-xs sm:text-sm font-semibold transition-colors hidden md:inline ${
                    isCurrent
                      ? 'text-amber-800 font-bold'
                      : isCompleted
                      ? 'text-emerald-900'
                      : 'text-slate-500 group-hover:text-slate-700'
                  }`}
                >
                  {step.label}
                </span>
                <span
                  className={`text-[11px] font-semibold transition-colors sm:hidden ${
                    isCurrent
                      ? 'text-amber-700 font-bold'
                      : isCompleted
                      ? 'text-emerald-800'
                      : 'text-slate-400'
                  }`}
                >
                  {step.short}
                </span>
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default ProgressIndicator;
