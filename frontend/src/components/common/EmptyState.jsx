import React from 'react';
import { FolderOpen } from 'lucide-react';
import Button from './Button';

export const EmptyState = ({
  icon: Icon = FolderOpen,
  title = 'No business data available yet',
  description = 'Enter your location, margin capital, and business category to generate a customized feasibility and financial plan.',
  actionLabel = 'Start Business Input',
  onAction,
  className = '',
}) => {
  return (
    <div
      className={`bg-white rounded-2xl border border-dashed border-slate-300 p-8 sm:p-12 text-center max-w-lg mx-auto ${className}`}
    >
      <div className="w-14 h-14 rounded-2xl bg-slate-50 text-slate-400 flex items-center justify-center mx-auto mb-4 border border-slate-200">
        <Icon className="w-7 h-7" />
      </div>
      <h3 className="text-base sm:text-lg font-bold text-slate-800 tracking-tight mb-2">
        {title}
      </h3>
      <p className="text-sm text-slate-500 leading-relaxed mb-6 max-w-sm mx-auto">
        {description}
      </p>
      {onAction && (
        <Button variant="primary" size="md" onClick={onAction}>
          {actionLabel}
        </Button>
      )}
    </div>
  );
};

export default EmptyState;
