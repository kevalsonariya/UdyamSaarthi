import React from 'react';

export const Skeleton = ({ className = '', rounded = 'rounded-xl' }) => {
  return (
    <div
      className={`bg-slate-200 animate-pulse ${rounded} ${className}`}
    />
  );
};

export const AnalysisSkeleton = () => {
  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      {/* Header Skeleton */}
      <div className="flex justify-between items-center">
        <div className="space-y-2">
          <Skeleton className="h-8 w-64" />
          <Skeleton className="h-4 w-96" />
        </div>
        <Skeleton className="h-10 w-40" />
      </div>

      {/* Summary Skeleton */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <Skeleton className="h-24 w-full" />
        <Skeleton className="h-24 w-full" />
        <Skeleton className="h-24 w-full" />
      </div>

      {/* 2 Col Skeletons */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Skeleton className="h-64 w-full" />
        <Skeleton className="h-64 w-full" />
      </div>

      {/* SWOT Skeleton */}
      <Skeleton className="h-72 w-full" />

      {/* Competitors & Pricing Skeleton */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Skeleton className="h-64 w-full" />
        <Skeleton className="h-64 w-full" />
      </div>

      {/* Recommendation Skeleton */}
      <Skeleton className="h-44 w-full" />
    </div>
  );
};

export const FinancialSkeleton = () => {
  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      {/* Header Skeleton */}
      <div className="flex justify-between items-center">
        <div className="space-y-2">
          <Skeleton className="h-8 w-64" />
          <Skeleton className="h-4 w-96" />
        </div>
        <Skeleton className="h-10 w-40" />
      </div>

      {/* Disclaimer Banner Skeleton */}
      <Skeleton className="h-16 w-full rounded-2xl" />

      {/* Stat Cards Skeleton */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Skeleton className="h-28 w-full rounded-2xl" />
        <Skeleton className="h-28 w-full rounded-2xl" />
        <Skeleton className="h-28 w-full rounded-2xl" />
        <Skeleton className="h-28 w-full rounded-2xl" />
      </div>

      {/* Scheme Card Skeleton */}
      <Skeleton className="h-64 w-full rounded-2xl" />

      {/* EMI & Moratorium Grid Skeleton */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Skeleton className="h-56 w-full rounded-2xl" />
        <Skeleton className="h-56 w-full rounded-2xl" />
      </div>

      {/* Working Capital Skeleton */}
      <Skeleton className="h-64 w-full rounded-2xl" />

      {/* Table Skeleton */}
      <Skeleton className="h-96 w-full rounded-2xl" />
    </div>
  );
};

export default Skeleton;
