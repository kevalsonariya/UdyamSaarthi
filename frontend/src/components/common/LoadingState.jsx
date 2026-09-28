import React from 'react';
import { Sparkles } from 'lucide-react';

export const LoadingState = ({
  title = 'Analyzing your business opportunity...',
  subtitle = 'Evaluating local market demand, competition density, and financial structuring rules.',
  className = '',
}) => {
  return (
    <div
      className={`bg-white rounded-2xl border border-slate-200 card-shadow p-8 sm:p-12 text-center max-w-lg mx-auto ${className}`}
    >
      <div className="relative inline-flex items-center justify-center mb-6">
        <div className="w-16 h-16 rounded-2xl bg-emerald-50 text-emerald-800 flex items-center justify-center animate-pulse">
          <Sparkles className="w-8 h-8 text-emerald-700 animate-spin" style={{ animationDuration: '4s' }} />
        </div>
        <div className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-amber-500 animate-ping" />
      </div>

      <h3 className="text-lg sm:text-xl font-bold text-slate-900 tracking-tight mb-2">
        {title}
      </h3>
      <p className="text-sm text-slate-500 leading-relaxed max-w-md mx-auto">
        {subtitle}
      </p>

      <div className="mt-6 flex items-center justify-center gap-2">
        <span className="w-2 h-2 rounded-full bg-emerald-700 animate-bounce" style={{ animationDelay: '0ms' }}></span>
        <span className="w-2 h-2 rounded-full bg-emerald-700 animate-bounce" style={{ animationDelay: '150ms' }}></span>
        <span className="w-2 h-2 rounded-full bg-emerald-700 animate-bounce" style={{ animationDelay: '300ms' }}></span>
      </div>
    </div>
  );
};

export default LoadingState;
