import React from 'react';

export const Card = ({
  children,
  className = '',
  title,
  subtitle,
  action,
  headerBorder = false,
  badge,
  onClick,
}) => {
  return (
    <div
      onClick={onClick}
      className={`bg-white rounded-2xl border border-slate-100 card-shadow overflow-hidden transition-all duration-200 ${
        onClick ? 'cursor-pointer hover:border-emerald-200 hover:shadow-md' : ''
      } ${className}`}
    >
      {(title || subtitle || action || badge) && (
        <div
          className={`px-5 py-4 flex items-center justify-between gap-4 ${
            headerBorder ? 'border-b border-slate-100' : ''
          }`}
        >
          <div>
            <div className="flex items-center gap-2">
              {title && (
                <h3 className="text-base font-bold text-slate-800 tracking-tight">
                  {title}
                </h3>
              )}
              {badge}
            </div>
            {subtitle && (
              <p className="text-xs text-slate-500 mt-0.5">{subtitle}</p>
            )}
          </div>
          {action && <div className="shrink-0">{action}</div>}
        </div>
      )}
      <div className="p-5">{children}</div>
    </div>
  );
};

export default Card;
