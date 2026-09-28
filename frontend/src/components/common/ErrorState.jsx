import React from 'react';
import { AlertTriangle } from 'lucide-react';
import Button from './Button';

export const ErrorState = ({
  title = 'Something went wrong',
  message = 'We could not complete the operation. Please check your network connection or try again.',
  retryLabel = 'Try Again',
  onRetry,
  className = '',
}) => {
  return (
    <div
      className={`bg-white rounded-2xl border border-red-200 card-shadow p-8 sm:p-10 text-center max-w-lg mx-auto ${className}`}
    >
      <div className="w-14 h-14 rounded-2xl bg-red-50 text-red-600 flex items-center justify-center mx-auto mb-4 border border-red-100">
        <AlertTriangle className="w-7 h-7" />
      </div>
      <h3 className="text-base sm:text-lg font-bold text-slate-800 tracking-tight mb-2">
        {title}
      </h3>
      <p className="text-sm text-slate-500 leading-relaxed mb-6 max-w-sm mx-auto">
        {message}
      </p>
      {onRetry && (
        <Button variant="primary" size="md" onClick={onRetry}>
          {retryLabel}
        </Button>
      )}
    </div>
  );
};

export default ErrorState;
