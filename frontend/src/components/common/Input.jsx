import React from 'react';

export const Input = ({
  label,
  helper,
  error,
  icon: Icon,
  prefix,
  suffix,
  className = '',
  id,
  type = 'text',
  ...props
}) => {
  const inputId = id || (label ? label.toLowerCase().replace(/\s+/g, '-') : undefined);

  return (
    <div className="w-full">
      {label && (
        <label
          htmlFor={inputId}
          className="block text-sm font-semibold text-slate-700 mb-1.5"
        >
          {label}
        </label>
      )}
      <div className="relative rounded-xl shadow-xs">
        {Icon && (
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
            <Icon className="h-4 w-4" />
          </div>
        )}
        {prefix && !Icon && (
          <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500 font-medium text-sm">
            {prefix}
          </div>
        )}
        <input
          id={inputId}
          type={type}
          className={`block w-full rounded-xl border ${
            error
              ? 'border-red-400 focus:border-red-500 focus:ring-red-200'
              : 'border-slate-300 hover:border-slate-400 focus:border-emerald-600 focus:ring-emerald-100'
          } bg-white px-3.5 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-3 transition-colors ${
            Icon || prefix ? 'pl-9' : ''
          } ${suffix ? 'pr-12' : ''} ${className}`}
          {...props}
        />
        {suffix && (
          <div className="absolute inset-y-0 right-0 pr-3.5 flex items-center pointer-events-none text-slate-500 text-xs font-medium">
            {suffix}
          </div>
        )}
      </div>
      {error && <p className="mt-1.5 text-xs text-red-600 font-medium">{error}</p>}
      {helper && !error && (
        <p className="mt-1.5 text-xs text-slate-500">{helper}</p>
      )}
    </div>
  );
};

export default Input;
