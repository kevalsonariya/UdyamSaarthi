import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Banknote,
  PieChart as PieChartIcon,
  Calendar,
  Clock,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
  AlertCircle,
  FileText,
  Info,
} from 'lucide-react';
import {
  Button,
  Card,
  Badge,
  SectionHeader,
  StatCard,
} from '../components/common';
import { useBizSahayak } from '../hooks/useBizSahayak';
import { formatCurrency, formatPercentage } from '../utils/formatters';
import { FINANCIAL_DISCLAIMER } from '../data/defaultData';

export const Financial = () => {
  const navigate = useNavigate();
  const { inputData } = useBizSahayak();

  const capital = Number(inputData.available_capital) || 100000;
  const location = inputData.location || 'Anand, Gujarat';
  const category = inputData.business_category || 'Textile & Clothing';

  // Deterministic Formulas:
  // Project Cost = Available Margin / 10%
  const projectCost = capital / 0.1;

  // Maximum Loan = 90% of Project Cost
  const rawMaxLoan = projectCost * 0.9;

  // Scheme Routing Rule:
  // If Project Cost <= 1.40 Lakh: Micro Finance Scheme (6.5%, 3y, 3mo moratorium, max ₹1.25L)
  // If 1.40 Lakh < Project Cost <= 50 Lakh: Term Loan Scheme (8%, 7y, 6mo moratorium, max ₹45L)
  const isMicroFinance = projectCost <= 140000;
  const schemeName = isMicroFinance ? 'Micro Finance Scheme' : 'Term Loan Scheme';
  const interestRate = isMicroFinance ? 6.5 : 8.0;
  const tenureYears = isMicroFinance ? 3 : 7;
  const moratoriumMonths = isMicroFinance ? 3 : 6;
  const maxAgencyFunding = isMicroFinance ? 125000 : 4500000;

  // Actual sanctioned loan amount capped by scheme max funding
  const sanctionedLoan = Math.min(rawMaxLoan, maxAgencyFunding);

  // EMI Calculation:
  // Tenure after moratorium in months
  const totalMonths = tenureYears * 12;
  const repaymentMonths = totalMonths - moratoriumMonths;
  const monthlyRate = interestRate / 12 / 100;
  const emi =
    (sanctionedLoan * monthlyRate * Math.pow(1 + monthlyRate, repaymentMonths)) /
    (Math.pow(1 + monthlyRate, repaymentMonths) - 1);

  // Working Capital Planning (Deterministic estimation)
  const machineryFixedAssets = projectCost * 0.6;
  const initialInventory = projectCost * 0.25;
  const operatingCashReserve = projectCost * 0.15;

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      {/* Header */}
      <SectionHeader
        title="Financial Structuring & Scheme Selection"
        subtitle={`Deterministic financial model and credit appraisal breakdown for ${category} in ${location}.`}
        icon={PieChartIcon}
        badge={
          <Badge variant="primary" size="md">
            Step 3 of 4
          </Badge>
        }
        action={
          <Button
            variant="primary"
            size="md"
            onClick={() => navigate('/report')}
            icon={ArrowRight}
          >
            Generate Final Business Plan
          </Button>
        }
      />

      {/* Mandatory Disclaimer */}
      <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4 flex items-start gap-3">
        <Info className="w-5 h-5 text-amber-700 shrink-0 mt-0.5" />
        <div className="text-xs text-amber-900 leading-relaxed">
          <strong className="font-bold">Official Disclaimer: </strong>
          {FINANCIAL_DISCLAIMER}
        </div>
      </div>

      {/* Key Numbers (Stat Cards) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          label="Your Margin Capital"
          value={formatCurrency(capital)}
          subtext="10% Promoter Contribution"
          variant="secondary"
          icon={Banknote}
        />
        <StatCard
          label="Total Project Cost"
          value={formatCurrency(projectCost)}
          subtext="Calculated as Capital / 10%"
          variant="primary"
          icon={PieChartIcon}
        />
        <StatCard
          label="Maximum Loan Amount"
          value={formatCurrency(sanctionedLoan)}
          subtext="90% of Project Cost"
          variant="info"
          icon={ShieldCheck}
        />
        <StatCard
          label="Estimated Monthly EMI"
          value={formatCurrency(Math.round(emi))}
          subtext={`For ${repaymentMonths} months after moratorium`}
          variant="primary"
          icon={Calendar}
        />
      </div>

      {/* Scheme Router Card */}
      <Card
        title="Automatic Scheme Recommendation"
        subtitle="Deterministically routed based on Project Cost criteria"
        badge={
          <Badge variant={isMicroFinance ? 'info' : 'primary'} size="md">
            {schemeName}
          </Badge>
        }
      >
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-4 bg-emerald-50/70 border border-emerald-200 rounded-xl space-y-2">
            <span className="text-xs font-semibold text-emerald-800 uppercase block">
              Interest Rate
            </span>
            <span className="text-3xl font-extrabold text-emerald-950">
              {formatPercentage(interestRate)}
            </span>
            <span className="text-xs text-emerald-700 block">
              Fixed subsidized annual interest
            </span>
          </div>

          <div className="p-4 bg-amber-50/70 border border-amber-200 rounded-xl space-y-2">
            <span className="text-xs font-semibold text-amber-800 uppercase block">
              Loan Tenure
            </span>
            <span className="text-3xl font-extrabold text-amber-950">
              {tenureYears} Years
            </span>
            <span className="text-xs text-amber-700 block">
              {totalMonths} total loan months
            </span>
          </div>

          <div className="p-4 bg-sky-50/70 border border-sky-200 rounded-xl space-y-2">
            <span className="text-xs font-semibold text-sky-800 uppercase block">
              Moratorium Period
            </span>
            <span className="text-3xl font-extrabold text-sky-950">
              {moratoriumMonths} Months
            </span>
            <span className="text-xs text-sky-700 block">
              Grace period before principal repayment starts
            </span>
          </div>
        </div>

        {/* Boundary Condition Rule Explanation */}
        <div className="mt-5 p-4 bg-slate-50 border border-slate-200 rounded-xl text-xs space-y-2">
          <div className="font-bold text-slate-800 flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4 text-emerald-700" />
            Scheme Routing Rule Applied:
          </div>
          <p className="text-slate-600">
            {isMicroFinance
              ? `Project Cost of ${formatCurrency(
                  projectCost
                )} is ≤ ₹1.40 Lakh → Routed to Micro Finance Scheme (Max Agency Funding: ₹1.25 Lakh, Tenure: 3 Years, Moratorium: 3 Months).`
              : `Project Cost of ${formatCurrency(
                  projectCost
                )} is > ₹1.40 Lakh and ≤ ₹50 Lakh → Routed to Term Loan Scheme (Max Agency Funding: ₹45 Lakh, Tenure: 7 Years, Moratorium: 6 Months).`}
          </p>
        </div>
      </Card>

      {/* Moratorium & Repayment Schedule */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card
          title="Moratorium Details (Grace Period)"
          subtitle="Support during initial enterprise setup"
        >
          <div className="space-y-3.5 text-xs text-slate-700">
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="font-semibold">Moratorium Duration:</span>
              <span className="font-bold text-slate-900">{moratoriumMonths} Months</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="font-semibold">Principal Repayment in Moratorium:</span>
              <span className="font-bold text-emerald-800">₹0 (Deferred)</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="font-semibold">Start of Regular Monthly EMI:</span>
              <span className="font-bold text-slate-900">Month {moratoriumMonths + 1}</span>
            </div>
            <p className="text-slate-500 pt-1 leading-relaxed">
              The moratorium allows micro-entrepreneurs to purchase equipment, set up operations, and achieve initial positive cashflow before principal repayment begins.
            </p>
          </div>
        </Card>

        {/* Working Capital Breakdown */}
        <Card
          title="Working Capital & Project Allocation"
          subtitle="Recommended utilization of the total project size"
        >
          <div className="space-y-3 text-xs">
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 flex justify-between items-center">
              <div>
                <span className="font-bold text-slate-800 block">Machinery & Fixed Assets (60%)</span>
                <span className="text-slate-500 text-[11px]">Sewing units, cutting tables, shop fittings</span>
              </div>
              <span className="font-bold text-slate-900">{formatCurrency(machineryFixedAssets)}</span>
            </div>

            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 flex justify-between items-center">
              <div>
                <span className="font-bold text-slate-800 block">Initial Fabric & Raw Materials (25%)</span>
                <span className="text-slate-500 text-[11px]">Wholesale procurement buffer</span>
              </div>
              <span className="font-bold text-slate-900">{formatCurrency(initialInventory)}</span>
            </div>

            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 flex justify-between items-center">
              <div>
                <span className="font-bold text-slate-800 block">Operating Cash Reserve (15%)</span>
                <span className="text-slate-500 text-[11px]">Utilities, rent advance, working capital buffer</span>
              </div>
              <span className="font-bold text-slate-900">{formatCurrency(operatingCashReserve)}</span>
            </div>
          </div>
        </Card>
      </div>

      {/* Navigation Footer */}
      <div className="flex items-center justify-between pt-4 border-t border-slate-200">
        <Button variant="ghost" onClick={() => navigate('/analysis')}>
          ← Back to Advisory Analysis
        </Button>
        <Button
          variant="primary"
          size="lg"
          onClick={() => navigate('/report')}
          icon={ArrowRight}
        >
          View Final Business Plan & Download PDF
        </Button>
      </div>
    </div>
  );
};

export default Financial;
