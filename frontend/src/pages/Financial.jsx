import React, { useState, useEffect } from 'react';
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
  TrendingDown,
  RotateCcw,
  Layers,
  HelpCircle,
  ChevronDown,
  ChevronUp,
} from 'lucide-react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import {
  Button,
  Card,
  Badge,
  SectionHeader,
  StatCard,
  FinancialSkeleton,
  ErrorState,
} from '../components/common';
import { useBizSahayak } from '../hooks/useBizSahayak';
import { formatCurrency, formatPercentage } from '../utils/formatters';
import { bizApi } from '../services/api';

export const Financial = () => {
  const navigate = useNavigate();
  const { inputData, analysisData, financialData, setFinancialData } = useBizSahayak();

  const [loading, setLoading] = useState(!financialData);
  const [error, setError] = useState(null);
  const [showFullSchedule, setShowFullSchedule] = useState(false);

  const location = inputData.location || 'Anand, Gujarat';
  const category = inputData.business_category || 'Textile & Clothing';
  const capital = Number(inputData.available_capital) || 100000;

  // Fetch financial plan from backend service
  const fetchFinancialPlan = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await bizApi.getFinancialPlan({
        location,
        business_category: category,
        available_capital: capital,
      });
      setFinancialData(data);
    } catch (err) {
      console.error('Failed to load financial plan:', err);
      setError('Unable to load deterministic financial calculation. Please retry.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // If not already fetched or capital changed, retrieve from backend service
    if (!financialData || financialData.financial?.available_capital !== capital) {
      fetchFinancialPlan();
    }
  }, [capital, category, location]);

  if (loading) {
    return <FinancialSkeleton />;
  }

  if (error || !financialData) {
    return (
      <div className="py-12">
        <ErrorState
          title="Financial Plan Could Not Be Loaded"
          message={error || 'Failed to retrieve deterministic financial structuring values.'}
          retryLabel="Retry Financial Engine"
          onRetry={fetchFinancialPlan}
        />
      </div>
    );
  }

  // Destructure verified values directly from backend service
  const { financial, scheme, emi, repayment, working_capital } = financialData;

  // Extract actual schedule array safely whether repayment is an array or { schedule: [...] }
  const scheduleArray = Array.isArray(repayment)
    ? repayment
    : Array.isArray(repayment?.schedule)
    ? repayment.schedule
    : Array.isArray(repayment?.data?.schedule)
    ? repayment.data.schedule
    : [];

  // Repayment chart data (sample every 3-6 months for clean visualization)
  const chartData = scheduleArray
    .filter((_, idx) => idx % (scheduleArray.length > 40 ? 3 : 1) === 0 || idx === scheduleArray.length - 1)
    .map((item) => ({
      name: `M${item.month}`,
      balance: Math.round(item.closing_balance),
      principal: Math.round(item.principal_component),
      interest: Math.round(item.interest_component),
    }));

  const visibleSchedule = showFullSchedule
    ? scheduleArray
    : scheduleArray.slice(0, 12);

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      {/* Header */}
      <SectionHeader
        title="Financial Structuring & Loan Sizing"
        subtitle={`Deterministic financial model, government scheme routing, and debt appraisal for ${category} in ${location}.`}
        icon={PieChartIcon}
        badge={
          <Badge variant="primary" size="md">
            Step 3 of 4 • Financials
          </Badge>
        }
        action={
          <Button
            variant="primary"
            size="md"
            onClick={() => navigate('/report')}
            icon={ArrowRight}
            className="shadow-sm font-semibold"
          >
            View Final Business Plan
          </Button>
        }
      />

      {/* Mandatory Financial Disclaimer */}
      <div className="bg-amber-50/90 border border-amber-200/90 rounded-2xl p-4 flex items-start gap-3 shadow-2xs">
        <Info className="w-5 h-5 text-amber-700 shrink-0 mt-0.5" />
        <div className="text-xs text-amber-950 leading-relaxed">
          <strong className="font-bold">Official Disclaimer: </strong>
          {financial.financial_disclaimer ||
            'Indicative calculation for planning purposes. Verify applicable scheme terms before making financial decisions.'}
        </div>
      </div>

      {/* 1. Financial Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          label="Available Capital"
          value={formatCurrency(financial.available_capital)}
          subtext="10% Promoter Contribution"
          variant="secondary"
          icon={Banknote}
        />
        <StatCard
          label="Project Cost"
          value={formatCurrency(financial.project_cost)}
          subtext="Calculated as Capital / 10%"
          variant="primary"
          icon={PieChartIcon}
        />
        <StatCard
          label="Maximum Loan Amount"
          value={formatCurrency(scheme.eligible_funding)}
          subtext="90% Debt Component"
          variant="info"
          icon={ShieldCheck}
        />
        <StatCard
          label="Monthly EMI"
          value={formatCurrency(emi.monthly_emi)}
          subtext={`For ${emi.post_moratorium_tenure_months} months`}
          variant="primary"
          icon={Calendar}
        />
      </div>

      {/* 2. Recommended Scheme Card */}
      <Card
        title="Recommended Scheme"
        subtitle="Deterministically routed by project cost boundary thresholds"
        badge={<Badge variant="primary" size="md">{scheme.scheme_name}</Badge>}
      >
        <div className="space-y-6">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="p-4 bg-emerald-50/70 border border-emerald-200 rounded-xl space-y-1">
              <span className="text-xs font-semibold text-emerald-800 uppercase block">
                Interest Rate
              </span>
              <span className="text-3xl font-extrabold text-emerald-950">
                {formatPercentage(scheme.interest_rate_percent)}
              </span>
              <span className="text-xs text-emerald-700 block">
                Subsidized fixed annual interest
              </span>
            </div>

            <div className="p-4 bg-amber-50/70 border border-amber-200 rounded-xl space-y-1">
              <span className="text-xs font-semibold text-amber-800 uppercase block">
                Repayment Period (Tenure)
              </span>
              <span className="text-3xl font-extrabold text-amber-950">
                {scheme.tenure_years} Years
              </span>
              <span className="text-xs text-amber-700 block">
                {scheme.tenure_months} total sanctioned months
              </span>
            </div>

            <div className="p-4 bg-sky-50/70 border border-sky-200 rounded-xl space-y-1">
              <span className="text-xs font-semibold text-sky-800 uppercase block">
                Moratorium Period
              </span>
              <span className="text-3xl font-extrabold text-sky-950">
                {scheme.moratorium_months} Months
              </span>
              <span className="text-xs text-sky-700 block">
                Gestation grace prior to principal repayment
              </span>
            </div>
          </div>

          {/* Scheme Criteria & Benefits */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-2">
              <span className="font-bold text-slate-800 block text-xs uppercase tracking-wider">
                Eligibility & Compliance
              </span>
              <ul className="space-y-1.5 text-slate-600">
                {scheme.eligibility_criteria?.map((item, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-700 shrink-0 mt-0.5" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-2">
              <span className="font-bold text-slate-800 block text-xs uppercase tracking-wider">
                Key Scheme Benefits
              </span>
              <ul className="space-y-1.5 text-slate-600">
                {scheme.key_benefits?.map((item, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-amber-700 shrink-0 mt-0.5" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </Card>

      {/* Phase B4: AI Financial Plan Explained */}
      {analysisData?.ai_explanation && (
        <Card
          title="AI Advisory: Financial Structuring & Scheme Explained"
          subtitle="Clear breakdown of how your debt is structured and why the moratorium benefits you"
          badge={
            <Badge variant="primary" size="sm">
              AI Advisory Explanation
            </Badge>
          }
          className="border-emerald-200 bg-emerald-50/20"
        >
          <div className="space-y-3.5 text-xs text-slate-700">
            <div className="p-3.5 bg-white rounded-xl border border-slate-200 space-y-1">
              <span className="font-bold text-slate-900 block">Capital & Equity Structure:</span>
              <p className="leading-relaxed text-slate-600">{analysisData.ai_explanation.financial_explanation}</p>
            </div>
            <div className="p-3.5 bg-white rounded-xl border border-slate-200 space-y-1">
              <span className="font-bold text-slate-900 block">Moratorium Grace Period Impact:</span>
              <p className="leading-relaxed text-slate-600">{analysisData.ai_explanation.scheme_explanation}</p>
            </div>
          </div>
        </Card>
      )}

      {/* 3. EMI & Moratorium Breakdown Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* EMI Card */}
        <Card title="Monthly EMI Breakdown" subtitle="Post-moratorium amortized monthly installment">
          <div className="space-y-3.5 text-xs text-slate-700">
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-600">Sanctioned Loan Principal:</span>
              <span className="font-bold text-slate-900">{formatCurrency(emi.principal_amount)}</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-600">Post-Moratorium EMI Months:</span>
              <span className="font-bold text-slate-900">{emi.post_moratorium_tenure_months} Months</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-emerald-50/70 border border-emerald-200 rounded-xl">
              <span className="font-bold text-emerald-950">Regular Monthly EMI:</span>
              <span className="text-base font-extrabold text-emerald-900">
                {formatCurrency(emi.monthly_emi)}
              </span>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-600">Total Interest Payable:</span>
              <span className="font-bold text-amber-800">{formatCurrency(emi.total_interest_payable)}</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-600">Total Repayment Amount:</span>
              <span className="font-bold text-slate-900">{formatCurrency(emi.total_repayment_amount)}</span>
            </div>
          </div>
        </Card>

        {/* Moratorium Card */}
        <Card title="Moratorium Period (Grace Period)" subtitle="Cashflow protection during initial setup">
          <div className="space-y-3.5 text-xs text-slate-700">
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-600">Moratorium Period:</span>
              <span className="font-bold text-slate-900">{emi.moratorium_months} Months</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-600">Principal Repayment in Moratorium:</span>
              <span className="font-bold text-emerald-800">₹0 (Zero Principal)</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-amber-50/70 border border-amber-200 rounded-xl">
              <span className="text-slate-700">Moratorium Simple Monthly Interest:</span>
              <span className="font-bold text-amber-900">{formatCurrency(emi.moratorium_monthly_interest)}</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-600">First Regular EMI Starts:</span>
              <span className="font-bold text-slate-900">Month {emi.moratorium_months + 1}</span>
            </div>
            <p className="text-slate-500 pt-1 leading-relaxed text-[11px]">
              During the {emi.moratorium_months}-month grace period, only simple interest is serviced. No principal is due, enabling positive cashflow accumulation before full amortization.
            </p>
          </div>
        </Card>
      </div>

      {/* 4. Repayment Schedule Amortization Chart */}
      <Card
        title="Amortization Trajectory (Loan Balance Over Time)"
        subtitle="Gradual reduction of outstanding loan balance across the repayment period"
      >
        <div className="h-56 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData} margin={{ top: 10, right: 10, left: 10, bottom: 0 }}>
              <defs>
                <linearGradient id="colorBalance" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#15803d" stopOpacity={0.4} />
                  <stop offset="95%" stopColor="#15803d" stopOpacity={0.0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#64748b' }} />
              <YAxis
                tickFormatter={(val) => `₹${(val / 100000).toFixed(1)}L`}
                tick={{ fontSize: 11, fill: '#64748b' }}
              />
              <Tooltip
                formatter={(val) => [formatCurrency(val), 'Outstanding Loan Balance']}
                contentStyle={{ borderRadius: '12px', fontSize: '12px' }}
              />
              <Area
                type="monotone"
                dataKey="balance"
                stroke="#15803d"
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorBalance)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </Card>

      {/* 5. Repayment Schedule Table */}
      <Card
        title="Repayment Schedule"
        subtitle={`Month-by-month amortization schedule (${repayment?.length || 0} total months)`}
        action={
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowFullSchedule(!showFullSchedule)}
            icon={showFullSchedule ? ChevronUp : ChevronDown}
          >
            {showFullSchedule ? 'Show Less (First 12 Months)' : `View All (${repayment?.length || 0} Months)`}
          </Button>
        }
      >
        {/* Responsive Table Container with Horizontal Scrolling */}
        <div className="overflow-x-auto -mx-5 px-5">
          <table className="w-full text-left text-xs whitespace-nowrap">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500 uppercase tracking-wider font-semibold">
                <th className="py-2.5 px-3">Month</th>
                <th className="py-2.5 px-3">Type</th>
                <th className="py-2.5 px-3 text-right">Opening Balance</th>
                <th className="py-2.5 px-3 text-right">Installment</th>
                <th className="py-2.5 px-3 text-right">Principal</th>
                <th className="py-2.5 px-3 text-right">Interest</th>
                <th className="py-2.5 px-3 text-right">Closing Balance</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {visibleSchedule.map((row) => (
                <tr
                  key={row.month}
                  className={`hover:bg-slate-50 transition-colors ${
                    row.is_moratorium ? 'bg-amber-50/40 text-amber-950 font-medium' : ''
                  }`}
                >
                  <td className="py-2.5 px-3 font-semibold text-slate-800">
                    Month {row.month}
                  </td>
                  <td className="py-2.5 px-3">
                    {row.is_moratorium ? (
                      <Badge variant="warning" size="sm">
                        Moratorium
                      </Badge>
                    ) : (
                      <Badge variant="primary" size="sm">
                        Regular EMI
                      </Badge>
                    )}
                  </td>
                  <td className="py-2.5 px-3 text-right text-slate-600">
                    {formatCurrency(row.opening_balance)}
                  </td>
                  <td className="py-2.5 px-3 text-right font-bold text-slate-900">
                    {formatCurrency(row.installment_amount)}
                  </td>
                  <td className="py-2.5 px-3 text-right text-emerald-800 font-medium">
                    {formatCurrency(row.principal_component)}
                  </td>
                  <td className="py-2.5 px-3 text-right text-amber-800">
                    {formatCurrency(row.interest_component)}
                  </td>
                  <td className="py-2.5 px-3 text-right font-semibold text-slate-800">
                    {formatCurrency(row.closing_balance)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {!showFullSchedule && (repayment?.length || 0) > 12 && (
          <div className="pt-4 text-center border-t border-slate-100 mt-2">
            <button
              type="button"
              onClick={() => setShowFullSchedule(true)}
              className="text-xs font-semibold text-emerald-800 hover:text-emerald-950 cursor-pointer"
            >
              + Display remaining {(repayment?.length || 0) - 12} installment months
            </button>
          </div>
        )}
      </Card>

      {/* 6. Working Capital Planning Section */}
      <Card
        title="Working Capital & Operational Expenses"
        subtitle="Monthly operational expenditure breakdown and liquidity buffer"
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-3 text-xs">
            <h4 className="font-bold text-slate-800 uppercase tracking-wider text-[11px]">
              Monthly Operating Expenses (OPEX):
            </h4>
            <div className="space-y-2">
              <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                <span className="text-slate-600">Raw Material Inputs:</span>
                <span className="font-bold text-slate-900">
                  {formatCurrency(working_capital.monthly_raw_materials)}
                </span>
              </div>
              <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                <span className="text-slate-600">Labor & Helper Wages:</span>
                <span className="font-bold text-slate-900">
                  {formatCurrency(working_capital.monthly_labor_wages)}
                </span>
              </div>
              <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                <span className="text-slate-600">Rent & Electric Utilities:</span>
                <span className="font-bold text-slate-900">
                  {formatCurrency(working_capital.monthly_rent_utilities)}
                </span>
              </div>
              <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                <span className="text-slate-600">Logistics & Packaging:</span>
                <span className="font-bold text-slate-900">
                  {formatCurrency(working_capital.monthly_logistics_packaging)}
                </span>
              </div>
              <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                <span className="text-slate-600">Contingency Maintenance:</span>
                <span className="font-bold text-slate-900">
                  {formatCurrency(working_capital.monthly_contingency_buffer)}
                </span>
              </div>
              <div className="flex justify-between items-center p-3 bg-emerald-50/70 border border-emerald-200 rounded-xl font-bold">
                <span className="text-emerald-950">Total Monthly Operating Expense:</span>
                <span className="text-emerald-900 text-sm">
                  {formatCurrency(working_capital.total_monthly_operating_expense)}
                </span>
              </div>
            </div>
          </div>

          <div className="space-y-3 text-xs">
            <h4 className="font-bold text-slate-800 uppercase tracking-wider text-[11px]">
              Cashflow Viability & Reserves:
            </h4>
            <div className="space-y-2">
              <div className="p-3 bg-amber-50/70 border border-amber-200 rounded-xl space-y-1">
                <span className="text-slate-600 block">Recommended 3-Month Reserve:</span>
                <span className="text-lg font-extrabold text-amber-900 block">
                  {formatCurrency(working_capital.recommended_3_months_reserve)}
                </span>
                <p className="text-[11px] text-amber-800">
                  Buffer capital to absorb seasonal agricultural harvest payment gaps.
                </p>
              </div>

              <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                <span className="text-slate-600">Break-Even Monthly Revenue:</span>
                <span className="font-bold text-slate-900">
                  {formatCurrency(working_capital.break_even_monthly_revenue)}
                </span>
              </div>

              <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                <span className="text-slate-600">Projected Monthly Revenue:</span>
                <span className="font-bold text-emerald-800">
                  {formatCurrency(working_capital.projected_monthly_revenue)}
                </span>
              </div>

              <div className="flex justify-between items-center p-2.5 bg-emerald-50/70 border border-emerald-200 rounded-xl">
                <span className="font-bold text-emerald-950">Projected Net Monthly Profit:</span>
                <span className="font-extrabold text-emerald-900 text-sm">
                  {formatCurrency(working_capital.projected_monthly_net_profit)}
                </span>
              </div>
            </div>
          </div>
        </div>
      </Card>

      {/* Bottom Navigation */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-slate-200">
        <Button
          variant="outline"
          onClick={() => navigate('/analysis')}
          icon={RotateCcw}
        >
          ← Back to Advisory Analysis
        </Button>
        <Button
          variant="primary"
          size="lg"
          onClick={() => navigate('/report')}
          icon={ArrowRight}
          className="w-full sm:w-auto font-bold shadow-md"
        >
          View Final Business Plan & Download Dossier
        </Button>
      </div>
    </div>
  );
};

export default Financial;
