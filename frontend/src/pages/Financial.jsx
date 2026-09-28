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
  Percent,
  TrendingUp,
  Boxes,
  Truck,
  Users,
  Building,
  Zap,
  Megaphone,
  Briefcase,
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
  const [repaymentView, setRepaymentView] = useState('monthly'); // 'monthly' | 'quarterly'
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

  // Extract actual monthly schedule array safely whether repayment is an array or { schedule: [...] }
  const scheduleArray = Array.isArray(repayment)
    ? repayment
    : Array.isArray(repayment?.schedule)
    ? repayment.schedule
    : Array.isArray(repayment?.data?.schedule)
    ? repayment.data.schedule
    : [];

  // Pure deterministic quarterly roll-up derivation (matches backend financial_engine)
  const deriveQuarterlySchedule = (monthlyList) => {
    if (!Array.isArray(monthlyList) || monthlyList.length === 0) return [];
    const quarters = [];
    const chunkSize = 3;
    for (let i = 0; i < monthlyList.length; i += chunkSize) {
      const chunk = monthlyList.slice(i, i + chunkSize);
      const qNum = Math.floor(i / chunkSize) + 1;
      const yNum = Math.floor((qNum - 1) / 4) + 1;
      const pPaid = chunk.reduce(
        (sum, m) => sum + (Number(m.principal_component ?? m.principal ?? 0)),
        0
      );
      const iPaid = chunk.reduce(
        (sum, m) => sum + (Number(m.interest_component ?? m.interest ?? 0)),
        0
      );
      const totPay = chunk.reduce(
        (sum, m) => sum + (Number(m.installment_amount ?? m.emi ?? 0)),
        0
      );
      const openBal = chunk[0]?.opening_balance ?? 0;
      const remBal = chunk[chunk.length - 1]?.closing_balance ?? 0;
      const isMorat = chunk.every((m) => m.is_moratorium);

      quarters.push({
        quarter: qNum,
        year: yNum,
        is_moratorium: isMorat,
        opening_balance: Math.round(openBal * 100) / 100,
        principal_paid: Math.round(pPaid * 100) / 100,
        interest_paid: Math.round(iPaid * 100) / 100,
        total_payment: Math.round(totPay * 100) / 100,
        remaining_balance: Math.round(remBal * 100) / 100,
      });
    }
    return quarters;
  };

  const quarterlyScheduleArray = Array.isArray(financialData?.quarterly_repayment)
    ? financialData.quarterly_repayment
    : Array.isArray(repayment?.quarterly_schedule)
    ? repayment.quarterly_schedule
    : Array.isArray(repayment?.data?.quarterly_schedule)
    ? repayment.data.quarterly_schedule
    : deriveQuarterlySchedule(scheduleArray);

  // Active view dataset
  const activeSchedule = repaymentView === 'monthly' ? scheduleArray : quarterlyScheduleArray;
  const initialDisplayCount = repaymentView === 'monthly' ? 12 : 8;
  const visibleSchedule = showFullSchedule
    ? activeSchedule
    : activeSchedule.slice(0, initialDisplayCount);

  // Repayment chart data (sample appropriately for clean visualization)
  const chartData = activeSchedule
    .filter((_, idx, arr) => idx % (arr.length > 24 ? 3 : 1) === 0 || idx === arr.length - 1)
    .map((item) => ({
      name: repaymentView === 'monthly' ? `M${item.month}` : `Q${item.quarter}`,
      balance: Math.round(item.closing_balance ?? item.remaining_balance ?? 0),
      principal: Math.round(item.principal_component ?? item.principal_paid ?? 0),
      interest: Math.round(item.interest_component ?? item.interest_paid ?? 0),
    }));

  // Normalized Working Capital fields (with deterministic backend ratios)
  const monthlyOpex =
    working_capital?.monthly_operating_cost ??
    working_capital?.total_monthly_operating_expense ??
    financial.project_cost * 0.095;
  const inventoryReq =
    working_capital?.inventory ??
    working_capital?.monthly_raw_materials ??
    financial.project_cost * 0.045;
  const labourCost =
    working_capital?.labour ??
    working_capital?.monthly_labor_wages ??
    financial.project_cost * 0.025;
  const rentCost =
    working_capital?.rent ??
    (working_capital?.monthly_rent_utilities
      ? working_capital.monthly_rent_utilities * (2 / 3)
      : financial.project_cost * 0.008);
  const utilitiesCost =
    working_capital?.utilities ??
    (working_capital?.monthly_rent_utilities
      ? working_capital.monthly_rent_utilities * (1 / 3)
      : financial.project_cost * 0.004);
  const transportCost =
    working_capital?.transportation ??
    working_capital?.monthly_logistics_packaging ??
    financial.project_cost * 0.008;
  const marketingCost =
    working_capital?.marketing ?? financial.project_cost * 0.003;
  const otherCost =
    working_capital?.other ?? financial.project_cost * 0.002;
  const recommendedReserve =
    working_capital?.recommended_reserve ??
    working_capital?.recommended_3_months_reserve ??
    monthlyOpex * 3;
  const totalWorkingCapital =
    working_capital?.total_working_capital ?? recommendedReserve;

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

      {/* Mandatory Financial Disclaimer Notice */}
      <div className="bg-amber-50/90 border border-amber-200/90 rounded-2xl p-4 flex items-start gap-3 shadow-2xs">
        <Info className="w-5 h-5 text-amber-700 shrink-0 mt-0.5" />
        <div className="text-xs text-amber-950 leading-relaxed">
          <strong className="font-bold">Indicative repayment calculation: </strong>
          {financial.financial_disclaimer ||
            'Verify applicable scheme terms before making financial decisions.'}
        </div>
      </div>

      {/* 1. FINANCIAL STRUCTURING */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
            <Banknote className="w-4 h-4 text-emerald-700" />
            Financial Structuring
          </h3>
          <Badge variant="neutral" size="sm">Deterministic Formula</Badge>
        </div>
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
            subtext="Calculated as Margin / 10%"
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
            label="Selected Scheme"
            value={scheme.scheme_name}
            subtext={scheme.scheme_code || 'Government Priority Credit'}
            variant="warning"
            icon={Layers}
          />
        </div>
      </div>

      {/* 2. LOAN TERMS */}
      <Card
        title="Loan Terms & Scheme Specifications"
        subtitle={`Official debt terms deterministically routed under ${scheme.scheme_name}`}
        badge={<Badge variant="primary" size="md">{scheme.scheme_name}</Badge>}
      >
        <div className="space-y-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="p-4 bg-emerald-50/70 border border-emerald-200 rounded-xl space-y-1">
              <span className="text-xs font-semibold text-emerald-800 uppercase block">
                Interest Rate
              </span>
              <span className="text-2xl font-extrabold text-emerald-950">
                {formatPercentage(scheme.interest_rate_percent)}
              </span>
              <span className="text-[11px] text-emerald-700 block">
                Fixed annual rate
              </span>
            </div>

            <div className="p-4 bg-amber-50/70 border border-amber-200 rounded-xl space-y-1">
              <span className="text-xs font-semibold text-amber-800 uppercase block">
                Loan Tenure
              </span>
              <span className="text-2xl font-extrabold text-amber-950">
                {scheme.tenure_years} Years
              </span>
              <span className="text-[11px] text-amber-700 block">
                {scheme.tenure_months} total months
              </span>
            </div>

            <div className="p-4 bg-sky-50/70 border border-sky-200 rounded-xl space-y-1">
              <span className="text-xs font-semibold text-sky-800 uppercase block">
                Moratorium Period
              </span>
              <span className="text-2xl font-extrabold text-sky-950">
                {scheme.moratorium_months} Months
              </span>
              <span className="text-[11px] text-sky-700 block">
                Grace on principal
              </span>
            </div>

            <div className="p-4 bg-purple-50/70 border border-purple-200 rounded-xl space-y-1">
              <span className="text-xs font-semibold text-purple-800 uppercase block">
                Repayment Frequency
              </span>
              <span className="text-xl font-extrabold text-purple-950">
                Monthly
              </span>
              <span className="text-[11px] text-purple-700 block">
                Quarterly roll-up enabled
              </span>
            </div>
          </div>

          {/* Scheme Criteria & Benefits */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-2">
              <span className="font-bold text-slate-800 block text-xs uppercase tracking-wider">
                Eligibility & Scheme Guidelines
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
                Key Scheme Benefits & Guarantee
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

      {/* 3. EMI SUMMARY & MORATORIUM HANDLING */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* EMI Summary Card */}
        <Card
          title="EMI Summary"
          subtitle="Post-moratorium amortized monthly installment calculation"
        >
          <div className="space-y-3.5 text-xs text-slate-700">
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-600">Sanctioned Loan Principal:</span>
              <span className="font-bold text-slate-900">
                {formatCurrency(emi.principal_amount)}
              </span>
            </div>
            <div className="flex justify-between items-center p-3 bg-emerald-50/70 border border-emerald-200 rounded-xl">
              <div>
                <span className="font-bold text-emerald-950 block">Monthly EMI:</span>
                <span className="text-[11px] text-emerald-700">
                  Applicable for {emi.post_moratorium_tenure_months} months post-moratorium
                </span>
              </div>
              <span className="text-base font-extrabold text-emerald-900">
                {formatCurrency(emi.monthly_emi)}
              </span>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-600">Total Interest Payable:</span>
              <span className="font-bold text-amber-800">
                {formatCurrency(emi.total_interest_payable)}
              </span>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-600">Total Repayment Amount:</span>
              <span className="font-bold text-slate-900">
                {formatCurrency(emi.total_repayment_amount)}
              </span>
            </div>
          </div>
        </Card>

        {/* Moratorium Handling Card */}
        <Card
          title="Moratorium Grace Period"
          subtitle="Statutory gestation protection during business setup"
        >
          <div className="space-y-3.5 text-xs text-slate-700">
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-600">Moratorium Duration:</span>
              <span className="font-bold text-slate-900">{emi.moratorium_months} Months</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-600">Principal Due in Moratorium:</span>
              <span className="font-bold text-emerald-800">₹0 (Zero Principal)</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-amber-50/70 border border-amber-200 rounded-xl">
              <span className="text-slate-700">Simple Monthly Interest:</span>
              <span className="font-bold text-amber-900">
                {formatCurrency(emi.moratorium_monthly_interest)}
              </span>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-600">First Full EMI Starts:</span>
              <span className="font-bold text-slate-900">Month {emi.moratorium_months + 1}</span>
            </div>
            <p className="text-slate-500 pt-1 leading-relaxed text-[11px]">
              During the {emi.moratorium_months}-month grace period, only simple interest is serviced.
              Principal amortization begins at Month {emi.moratorium_months + 1}, giving the enterprise
              time to ramp up sales and establish positive operating cashflow.
            </p>
          </div>
        </Card>
      </div>

      {/* 4. REPAYMENT SCHEDULE WITH MONTHLY & QUARTERLY VIEWS */}
      <Card
        title="Repayment Schedule"
        subtitle={
          repaymentView === 'monthly'
            ? `Deterministic month-by-month amortization schedule (${scheduleArray.length} total months)`
            : `Deterministic quarterly roll-up presentation (${quarterlyScheduleArray.length} total quarters)`
        }
        badge={
          <Badge variant="neutral" size="sm">
            Indicative Repayment Schedule
          </Badge>
        }
        action={
          <div className="flex items-center gap-2">
            {/* View Selector Toggle */}
            <div className="flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200 text-xs">
              <button
                type="button"
                onClick={() => {
                  setShowFullSchedule(false);
                  setRepaymentView('monthly');
                }}
                className={`px-3 py-1 font-bold rounded-lg transition-all cursor-pointer ${
                  repaymentView === 'monthly'
                    ? 'bg-white text-emerald-900 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                Monthly View
              </button>
              <button
                type="button"
                onClick={() => {
                  setShowFullSchedule(false);
                  setRepaymentView('quarterly');
                }}
                className={`px-3 py-1 font-bold rounded-lg transition-all cursor-pointer ${
                  repaymentView === 'quarterly'
                    ? 'bg-white text-emerald-900 shadow-xs'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                Quarterly View
              </button>
            </div>

            {/* Expand / Collapse Button */}
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowFullSchedule(!showFullSchedule)}
              icon={showFullSchedule ? ChevronUp : ChevronDown}
            >
              {showFullSchedule
                ? `Show First ${initialDisplayCount}`
                : `View All (${activeSchedule.length})`}
            </Button>
          </div>
        }
      >
        <div className="space-y-5">
          {/* Amortization Chart */}
          <div className="h-52 w-full pt-1">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData} margin={{ top: 10, right: 10, left: 10, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorBalance" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#15803d" stopOpacity={0.35} />
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
                  formatter={(val) => [formatCurrency(val), 'Outstanding Balance']}
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

          {/* Repayment Schedule Table */}
          <div className="overflow-x-auto -mx-5 px-5">
            <table className="w-full text-left text-xs whitespace-nowrap">
              <thead>
                <tr className="border-b border-slate-200 text-slate-500 uppercase tracking-wider font-semibold">
                  {repaymentView === 'monthly' ? (
                    <>
                      <th className="py-2.5 px-3">Month</th>
                      <th className="py-2.5 px-3">Type</th>
                      <th className="py-2.5 px-3 text-right">Opening Balance</th>
                      <th className="py-2.5 px-3 text-right">EMI / Payment</th>
                      <th className="py-2.5 px-3 text-right">Principal</th>
                      <th className="py-2.5 px-3 text-right">Interest</th>
                      <th className="py-2.5 px-3 text-right">Remaining Balance</th>
                    </>
                  ) : (
                    <>
                      <th className="py-2.5 px-3">Quarter</th>
                      <th className="py-2.5 px-3">Phase</th>
                      <th className="py-2.5 px-3 text-right">Opening Balance</th>
                      <th className="py-2.5 px-3 text-right">Total Payment (Quarter)</th>
                      <th className="py-2.5 px-3 text-right">Principal Paid</th>
                      <th className="py-2.5 px-3 text-right">Interest Paid</th>
                      <th className="py-2.5 px-3 text-right">Remaining Balance</th>
                    </>
                  )}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {repaymentView === 'monthly'
                  ? visibleSchedule.map((row) => (
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
                          {formatCurrency(row.installment_amount ?? row.emi)}
                        </td>
                        <td className="py-2.5 px-3 text-right text-emerald-800 font-medium">
                          {formatCurrency(row.principal_component ?? row.principal)}
                        </td>
                        <td className="py-2.5 px-3 text-right text-amber-800">
                          {formatCurrency(row.interest_component ?? row.interest)}
                        </td>
                        <td className="py-2.5 px-3 text-right font-semibold text-slate-800">
                          {formatCurrency(row.closing_balance)}
                        </td>
                      </tr>
                    ))
                  : visibleSchedule.map((row) => (
                      <tr
                        key={row.quarter}
                        className={`hover:bg-slate-50 transition-colors ${
                          row.is_moratorium ? 'bg-amber-50/40 text-amber-950 font-medium' : ''
                        }`}
                      >
                        <td className="py-2.5 px-3 font-semibold text-slate-800">
                          Quarter {row.quarter} (Yr {row.year})
                        </td>
                        <td className="py-2.5 px-3">
                          {row.is_moratorium ? (
                            <Badge variant="warning" size="sm">
                              Moratorium Quarter
                            </Badge>
                          ) : (
                            <Badge variant="primary" size="sm">
                              Amortized Payment
                            </Badge>
                          )}
                        </td>
                        <td className="py-2.5 px-3 text-right text-slate-600">
                          {formatCurrency(row.opening_balance)}
                        </td>
                        <td className="py-2.5 px-3 text-right font-bold text-slate-900">
                          {formatCurrency(row.total_payment ?? row.installment_amount)}
                        </td>
                        <td className="py-2.5 px-3 text-right text-emerald-800 font-medium">
                          {formatCurrency(row.principal_paid ?? row.principal_component)}
                        </td>
                        <td className="py-2.5 px-3 text-right text-amber-800">
                          {formatCurrency(row.interest_paid ?? row.interest_component)}
                        </td>
                        <td className="py-2.5 px-3 text-right font-semibold text-slate-800">
                          {formatCurrency(row.remaining_balance ?? row.closing_balance)}
                        </td>
                      </tr>
                    ))}
              </tbody>
            </table>
          </div>

          {!showFullSchedule && activeSchedule.length > initialDisplayCount && (
            <div className="pt-3 text-center border-t border-slate-100 mt-2">
              <button
                type="button"
                onClick={() => setShowFullSchedule(true)}
                className="text-xs font-semibold text-emerald-800 hover:text-emerald-950 cursor-pointer"
              >
                + Display all remaining {activeSchedule.length - initialDisplayCount}{' '}
                {repaymentView === 'monthly' ? 'installment months' : 'quarters'}
              </button>
            </div>
          )}
        </div>
      </Card>

      {/* 5. WORKING CAPITAL PLANNING SECTION */}
      <Card
        title="Working Capital & Operational Expense Breakdown"
        subtitle="Itemized operational cost requirements and recommended liquidity buffer"
        badge={
          <Badge variant="neutral" size="sm">
            Demo/Indicative Estimate
          </Badge>
        }
      >
        <div className="space-y-6">
          {/* Planning estimate notice */}
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl flex items-start gap-2.5 text-xs text-slate-600">
            <Info className="w-4 h-4 text-slate-500 shrink-0 mt-0.5" />
            <span>
              <strong>Planning Notice: </strong>
              The working-capital calculation is presented as an indicative operational estimate for cashflow planning, not a guaranteed funding sanction. Ratios are aligned to standard priority-sector enterprise benchmarks.
            </span>
          </div>

          {/* Working Capital Highlights */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="p-4 bg-emerald-50/70 border border-emerald-200 rounded-xl space-y-1">
              <span className="text-xs font-semibold text-emerald-800 uppercase block">
                Estimated Monthly Operating Cost
              </span>
              <span className="text-2xl font-extrabold text-emerald-950">
                {formatCurrency(monthlyOpex)}
              </span>
              <span className="text-[11px] text-emerald-700 block">
                9.5% of total project cost
              </span>
            </div>

            <div className="p-4 bg-amber-50/70 border border-amber-200 rounded-xl space-y-1">
              <span className="text-xs font-semibold text-amber-800 uppercase block">
                Recommended 3-Month Reserve
              </span>
              <span className="text-2xl font-extrabold text-amber-950">
                {formatCurrency(recommendedReserve)}
              </span>
              <span className="text-[11px] text-amber-700 block">
                Liquidity buffer for harvest cycles
              </span>
            </div>

            <div className="p-4 bg-sky-50/70 border border-sky-200 rounded-xl space-y-1">
              <span className="text-xs font-semibold text-sky-800 uppercase block">
                Total Working Capital Requirement
              </span>
              <span className="text-2xl font-extrabold text-sky-950">
                {formatCurrency(totalWorkingCapital)}
              </span>
              <span className="text-[11px] text-sky-700 block">
                Initial operational liquidity
              </span>
            </div>
          </div>

          {/* Itemized OPEX Breakdown */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2.5 text-xs">
              <h4 className="font-bold text-slate-800 uppercase tracking-wider text-[11px] flex items-center gap-1.5">
                <Boxes className="w-3.5 h-3.5 text-emerald-700" />
                Itemized Operating Expenses (Monthly OPEX):
              </h4>
              <div className="space-y-2">
                <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                  <span className="text-slate-600 flex items-center gap-2">
                    <Boxes className="w-3.5 h-3.5 text-slate-400" />
                    Inventory Requirement:
                  </span>
                  <span className="font-bold text-slate-900">{formatCurrency(inventoryReq)}</span>
                </div>
                <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                  <span className="text-slate-600 flex items-center gap-2">
                    <Users className="w-3.5 h-3.5 text-slate-400" />
                    Labour / Personnel:
                  </span>
                  <span className="font-bold text-slate-900">{formatCurrency(labourCost)}</span>
                </div>
                <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                  <span className="text-slate-600 flex items-center gap-2">
                    <Building className="w-3.5 h-3.5 text-slate-400" />
                    Rent:
                  </span>
                  <span className="font-bold text-slate-900">{formatCurrency(rentCost)}</span>
                </div>
                <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                  <span className="text-slate-600 flex items-center gap-2">
                    <Zap className="w-3.5 h-3.5 text-slate-400" />
                    Utilities:
                  </span>
                  <span className="font-bold text-slate-900">{formatCurrency(utilitiesCost)}</span>
                </div>
                <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                  <span className="text-slate-600 flex items-center gap-2">
                    <Truck className="w-3.5 h-3.5 text-slate-400" />
                    Transportation / Logistics:
                  </span>
                  <span className="font-bold text-slate-900">{formatCurrency(transportCost)}</span>
                </div>
                <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                  <span className="text-slate-600 flex items-center gap-2">
                    <Megaphone className="w-3.5 h-3.5 text-slate-400" />
                    Marketing:
                  </span>
                  <span className="font-bold text-slate-900">{formatCurrency(marketingCost)}</span>
                </div>
                <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                  <span className="text-slate-600 flex items-center gap-2">
                    <Briefcase className="w-3.5 h-3.5 text-slate-400" />
                    Other Operating Expenses:
                  </span>
                  <span className="font-bold text-slate-900">{formatCurrency(otherCost)}</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-emerald-50/70 border border-emerald-200 rounded-xl font-bold">
                  <span className="text-emerald-950">Total Monthly Operating Cost:</span>
                  <span className="text-emerald-900 text-sm">{formatCurrency(monthlyOpex)}</span>
                </div>
              </div>
            </div>

            {/* Operational Cashflow & Viability */}
            <div className="space-y-2.5 text-xs">
              <h4 className="font-bold text-slate-800 uppercase tracking-wider text-[11px] flex items-center gap-1.5">
                <TrendingUp className="w-3.5 h-3.5 text-amber-700" />
                Cashflow Viability & Revenue Benchmarks:
              </h4>
              <div className="space-y-2">
                <div className="p-3 bg-amber-50/70 border border-amber-200 rounded-xl space-y-1">
                  <span className="text-slate-600 block">Recommended Working Capital Reserve:</span>
                  <span className="text-lg font-extrabold text-amber-900 block">
                    {formatCurrency(recommendedReserve)}
                  </span>
                  <p className="text-[11px] text-amber-800">
                    Provides a 3-month operational buffer to absorb seasonal rural harvest credit cycles.
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
        </div>
      </Card>

      {/* 6. AI FINANCIAL EXPLANATION (Preserved from Phase B4) */}
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
              <p className="leading-relaxed text-slate-600">
                {analysisData.ai_explanation.financial_explanation}
              </p>
            </div>
            <div className="p-3.5 bg-white rounded-xl border border-slate-200 space-y-1">
              <span className="font-bold text-slate-900 block">Moratorium Grace Period Impact:</span>
              <p className="leading-relaxed text-slate-600">
                {analysisData.ai_explanation.scheme_explanation}
              </p>
            </div>
          </div>
        </Card>
      )}

      {/* 7. DISCLAIMER FOOTER */}
      <div className="bg-slate-50 border border-slate-200 rounded-2xl p-4 text-xs text-slate-500 leading-relaxed text-center">
        <p>
          <strong>Statutory Disclaimer: </strong>
          Indicative calculation for planning purposes. Verify applicable scheme terms before making financial decisions.
          All figures are computed deterministically under established micro-credit norms.
        </p>
      </div>

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
