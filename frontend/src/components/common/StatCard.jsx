import React from 'react';

export const StatCard = ({
  label,
  value,
  subtext,
  icon: Icon,
  variant = 'default',
  trend,
  className = '',
}) => {
  const borderStyles = {
    default: 'border-slate-200',
    primary: 'border-l-4 border-l-emerald-700 border-slate-200',
    secondary: 'border-l-4 border-l-amber-500 border-slate-200',
    info: 'border-l-4 border-l-sky-500 border-slate-200',
  };

  const iconBg = {
    default: 'bg-slate-100 text-slate-700',
    primary: 'bg-emerald-50 text-emerald-800',
    secondary: 'bg-amber-50 text-amber-700',
    info: 'bg-sky-50 text-sky-700',
  };

  return (
    <div
      className={`bg-white rounded-2xl border p-5 card-shadow ${
        borderStyles[variant] || borderStyles.default
      } ${className}`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="space-y-1">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
            {label}
          </p>
          <p className="text-2xl font-extrabold text-slate-900 tracking-tight">
            {value}
          </p>
        </div>
        {Icon && (
          <div
            className={`p-2.5 rounded-xl shrink-0 ${
              iconBg[variant] || iconBg.default
            }`}
          >
            <Icon className="w-5 h-5" />
          </div>
        )}
      </div>
      {(subtext || trend) && (
        <div className="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
          {subtext && <span>{subtext}</span>}
          {trend && <span className="font-semibold text-emerald-700">{trend}</span>}
        </div>
      )}
    </div>
  );
};

export default StatCard;
