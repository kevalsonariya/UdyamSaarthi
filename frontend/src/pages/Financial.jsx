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
import { useTranslation } from '../context/LanguageContext';

export const Financial = () => {
  const navigate = useNavigate();
  const { inputData, analysisData, financialData, setFinancialData } = useBizSahayak();
  const { t, getCategoryLabel } = useTranslation();

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
      setError(t('financial.errorTitle'));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // If not already fetched or parameters changed, retrieve from backend service
    const matchesCurrent = Boolean(
      financialData &&
      financialData.financial?.available_capital === capital &&
      (!financialData.input || (financialData.input.business_category === category && financialData.input.location === location))
    );
    if (!matchesCurrent) {
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
          title={t('financial.errorTitle')}
          message={error || t('common.errorMessage')}
          retryLabel={t('financial.retryBtn')}
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
        title={t('financial.headerTitle')}
        subtitle={t('financial.headerSubtitle', {
          category: getCategoryLabel(category),
          location,
        })}
        icon={PieChartIcon}
        badge={
          <Badge variant="primary" size="md">
            {t('financial.stepBadge')}
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
            {t('financial.viewReportBtn')}
          </Button>
        }
      />

      {/* Mandatory Financial Disclaimer Notice */}
      <div className="bg-amber-50/90 border border-amber-200/90 rounded-2xl p-4 flex items-start gap-3 shadow-2xs">
        <Info className="w-5 h-5 text-amber-700 shrink-0 mt-0.5" />
        <div className="text-xs text-amber-950 leading-relaxed">
          <strong className="font-bold">{t('financial.disclaimerNotice')}</strong>
          {financial.financial_disclaimer || t('financial.disclaimerText')}
        </div>
      </div>

      {/* 1. FINANCIAL STRUCTURING */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
            <Banknote className="w-4 h-4 text-emerald-700" />
            {t('financial.structuringTitle')}
          </h3>
          <Badge variant="neutral" size="sm">{t('financial.deterministicBadge')}</Badge>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard
            label={t('financial.availableCapital')}
            value={formatCurrency(financial.available_capital)}
            subtext={t('financial.promoterEquitySub')}
            variant="secondary"
            icon={Banknote}
          />
          <StatCard
            label={t('financial.projectCost')}
            value={formatCurrency(financial.project_cost)}
            subtext={t('financial.projectCostSub')}
            variant="primary"
            icon={PieChartIcon}
          />
          <StatCard
            label={t('financial.maxLoan')}
            value={formatCurrency(scheme.eligible_funding)}
            subtext={t('financial.maxLoanSub')}
            variant="info"
            icon={ShieldCheck}
          />
          <StatCard
            label={t('financial.selectedScheme')}
            value={scheme.scheme_name}
            subtext={scheme.scheme_code || 'Government Priority Credit'}
            variant="warning"
            icon={Layers}
          />
        </div>
      </div>

      {/* 2. LOAN TERMS */}
      <Card
        title={t('financial.loanTermsTitle')}
        subtitle={t('financial.loanTermsSubtitle', { scheme: scheme.scheme_name })}
        badge={<Badge variant="primary" size="md">{scheme.scheme_name}</Badge>}
      >
        <div className="space-y-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="p-4 bg-emerald-50/70 border border-emerald-200 rounded-xl space-y-1">
              <span className="text-xs font-semibold text-emerald-800 uppercase block">
                {t('financial.interestRate')}
              </span>
              <span className="text-2xl font-extrabold text-emerald-950">
                {formatPercentage(scheme.interest_rate_percent)}
              </span>
              <span className="text-[11px] text-emerald-700 block">
                {t('financial.fixedAnnual')}
              </span>
            </div>

            <div className="p-4 bg-amber-50/70 border border-amber-200 rounded-xl space-y-1">
              <span className="text-xs font-semibold text-amber-800 uppercase block">
                {t('financial.loanTenure')}
              </span>
              <span className="text-2xl font-extrabold text-amber-950">
                {scheme.tenure_years} {t('financial.years')}
              </span>
              <span className="text-[11px] text-amber-700 block">
                {t('financial.totalMonths', { months: scheme.tenure_months })}
              </span>
            </div>

            <div className="p-4 bg-sky-50/70 border border-sky-200 rounded-xl space-y-1">
              <span className="text-xs font-semibold text-sky-800 uppercase block">
                {t('financial.moratoriumPeriod')}
              </span>
              <span className="text-2xl font-extrabold text-sky-950">
                {scheme.moratorium_months} {t('financial.months')}
              </span>
              <span className="text-[11px] text-sky-700 block">
                {t('financial.graceOnPrincipal')}
              </span>
            </div>

            <div className="p-4 bg-purple-50/70 border border-purple-200 rounded-xl space-y-1">
              <span className="text-xs font-semibold text-purple-800 uppercase block">
                {t('financial.repaymentFreq')}
              </span>
              <span className="text-xl font-extrabold text-purple-950">
                {t('financial.monthlyFreq')}
              </span>
              <span className="text-[11px] text-purple-700 block">
                {t('financial.quarterlyRollup')}
              </span>
            </div>
          </div>

          {/* Scheme Criteria & Benefits */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-2">
              <span className="font-bold text-slate-800 block text-xs uppercase tracking-wider">
                {t('financial.eligibilityTitle')}
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
                {t('financial.keyBenefitsTitle')}
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
          title={t('financial.emiSummaryTitle')}
          subtitle={t('financial.emiSummarySubtitle')}
        >
          <div className="space-y-3.5 text-xs text-slate-700">
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-600">{t('financial.sanctionedPrincipal')}</span>
              <span className="font-bold text-slate-900">
                {formatCurrency(emi.principal_amount)}
              </span>
            </div>
            <div className="flex justify-between items-center p-3 bg-emerald-50/70 border border-emerald-200 rounded-xl">
              <div>
                <span className="font-bold text-emerald-950 block">{t('financial.monthlyEmi')}</span>
                <span className="text-[11px] text-emerald-700">
                  {t('financial.emiApplicableFor', { months: emi.post_moratorium_tenure_months })}
                </span>
              </div>
              <span className="text-base font-extrabold text-emerald-900">
                {formatCurrency(emi.monthly_emi)}
              </span>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-600">{t('financial.totalInterest')}</span>
              <span className="font-bold text-amber-800">
                {formatCurrency(emi.total_interest_payable)}
              </span>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-600">{t('financial.totalRepayment')}</span>
              <span className="font-bold text-slate-900">
                {formatCurrency(emi.total_repayment_amount)}
              </span>
            </div>
          </div>
        </Card>

        {/* Moratorium Handling Card */}
        <Card
          title={t('financial.moratoriumTitle')}
          subtitle={t('financial.moratoriumSubtitle')}
        >
          <div className="space-y-3.5 text-xs text-slate-700">
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-600">{t('financial.moratoriumDuration')}</span>
              <span className="font-bold text-slate-900">
                {emi.moratorium_months} {t('financial.months')}
              </span>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-600">{t('financial.principalInMoratorium')}</span>
              <span className="font-bold text-emerald-800">{t('financial.zeroPrincipal')}</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-amber-50/70 border border-amber-200 rounded-xl">
              <span className="text-slate-700">{t('financial.simpleInterest')}</span>
              <span className="font-bold text-amber-900">
                {formatCurrency(emi.moratorium_monthly_interest)}
              </span>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-600">{t('financial.firstEmiStarts')}</span>
              <span className="font-bold text-slate-900">
                {t('financial.monthNum', { month: emi.moratorium_months + 1 })}
              </span>
            </div>
            <p className="text-slate-500 pt-1 leading-relaxed text-[11px]">
              {t('financial.moratoriumExpl', {
                months: emi.moratorium_months,
                startMonth: emi.moratorium_months + 1,
              })}
            </p>
          </div>
        </Card>
      </div>

      {/* 4. REPAYMENT SCHEDULE WITH MONTHLY & QUARTERLY VIEWS */}
      <Card
        title={t('financial.repaymentTitle')}
        subtitle={
          repaymentView === 'monthly'
            ? t('financial.repaymentMonthlySub', { count: scheduleArray.length })
            : t('financial.repaymentQuarterlySub', { count: quarterlyScheduleArray.length })
        }
        badge={
          <Badge variant="neutral" size="sm">
            {t('financial.scheduleBadge')}
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
                {t('financial.monthlyViewBtn')}
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
                {t('financial.quarterlyViewBtn')}
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
                ? t('financial.showFirstBtn', { count: initialDisplayCount })
                : t('financial.viewAllBtn', { count: activeSchedule.length })}
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
                      <th className="py-2.5 px-3">{t('financial.tableMonth')}</th>
                      <th className="py-2.5 px-3">{t('financial.tableType')}</th>
                      <th className="py-2.5 px-3 text-right">{t('financial.tableOpening')}</th>
                      <th className="py-2.5 px-3 text-right">{t('financial.tableEmiPayment')}</th>
                      <th className="py-2.5 px-3 text-right">{t('financial.tablePrincipal')}</th>
                      <th className="py-2.5 px-3 text-right">{t('financial.tableInterest')}</th>
                      <th className="py-2.5 px-3 text-right">{t('financial.tableRemaining')}</th>
                    </>
                  ) : (
                    <>
                      <th className="py-2.5 px-3">{t('financial.tableQuarter')}</th>
                      <th className="py-2.5 px-3">{t('financial.tablePhase')}</th>
                      <th className="py-2.5 px-3 text-right">{t('financial.tableOpening')}</th>
                      <th className="py-2.5 px-3 text-right">{t('financial.tableTotalPayment')}</th>
                      <th className="py-2.5 px-3 text-right">{t('financial.tablePrincipalPaid')}</th>
                      <th className="py-2.5 px-3 text-right">{t('financial.tableInterestPaid')}</th>
                      <th className="py-2.5 px-3 text-right">{t('financial.tableRemaining')}</th>
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
                          {t('financial.monthNum', { month: row.month })}
                        </td>
                        <td className="py-2.5 px-3">
                          {row.is_moratorium ? (
                            <Badge variant="warning" size="sm">
                              {t('financial.moratoriumTag')}
                            </Badge>
                          ) : (
                            <Badge variant="primary" size="sm">
                              {t('financial.regularEmiTag')}
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
                          {t('financial.tableQuarter')} {row.quarter} (Yr {row.year})
                        </td>
                        <td className="py-2.5 px-3">
                          {row.is_moratorium ? (
                            <Badge variant="warning" size="sm">
                              {t('financial.moratoriumQuarterTag')}
                            </Badge>
                          ) : (
                            <Badge variant="primary" size="sm">
                              {t('financial.amortizedPaymentTag')}
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
                {t('financial.displayRemaining', {
                  count: activeSchedule.length - initialDisplayCount,
                  unit: repaymentView === 'monthly' ? t('financial.monthsUnit') : t('financial.quartersUnit'),
                })}
              </button>
            </div>
          )}
        </div>
      </Card>

      {/* 5. WORKING CAPITAL PLANNING SECTION */}
      <Card
        title={t('financial.workingCapitalTitle')}
        subtitle={t('financial.workingCapitalSubtitle')}
        badge={
          <Badge variant="neutral" size="sm">
            {t('financial.demoEstimateBadge')}
          </Badge>
        }
      >
        <div className="space-y-6">
          {/* Planning estimate notice */}
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl flex items-start gap-2.5 text-xs text-slate-600">
            <Info className="w-4 h-4 text-slate-500 shrink-0 mt-0.5" />
            <span>
              <strong>{t('financial.planningNoticeTitle')}</strong>
              {t('financial.planningNoticeText')}
            </span>
          </div>

          {/* Working Capital Highlights */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="p-4 bg-emerald-50/70 border border-emerald-200 rounded-xl space-y-1">
              <span className="text-xs font-semibold text-emerald-800 uppercase block">
                {t('financial.monthlyOperatingCost')}
              </span>
              <span className="text-2xl font-extrabold text-emerald-950">
                {formatCurrency(monthlyOpex)}
              </span>
              <span className="text-[11px] text-emerald-700 block">
                {t('financial.monthlyOpexSub')}
              </span>
            </div>

            <div className="p-4 bg-amber-50/70 border border-amber-200 rounded-xl space-y-1">
              <span className="text-xs font-semibold text-amber-800 uppercase block">
                {t('financial.recommendedReserve')}
              </span>
              <span className="text-2xl font-extrabold text-amber-950">
                {formatCurrency(recommendedReserve)}
              </span>
              <span className="text-[11px] text-amber-700 block">
                {t('financial.reserveSub')}
              </span>
            </div>

            <div className="p-4 bg-sky-50/70 border border-sky-200 rounded-xl space-y-1">
              <span className="text-xs font-semibold text-sky-800 uppercase block">
                {t('financial.totalWorkingCapital')}
              </span>
              <span className="text-2xl font-extrabold text-sky-950">
                {formatCurrency(totalWorkingCapital)}
              </span>
              <span className="text-[11px] text-sky-700 block">
                {t('financial.workingCapitalSub')}
              </span>
            </div>
          </div>

          {/* Itemized OPEX Breakdown */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-2.5 text-xs">
              <h4 className="font-bold text-slate-800 uppercase tracking-wider text-[11px] flex items-center gap-1.5">
                <Boxes className="w-3.5 h-3.5 text-emerald-700" />
                {t('financial.itemizedOpexTitle')}
              </h4>
              <div className="space-y-2">
                <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                  <span className="text-slate-600 flex items-center gap-2">
                    <Boxes className="w-3.5 h-3.5 text-slate-400" />
                    {t('financial.inventory')}
                  </span>
                  <span className="font-bold text-slate-900">{formatCurrency(inventoryReq)}</span>
                </div>
                <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                  <span className="text-slate-600 flex items-center gap-2">
                    <Users className="w-3.5 h-3.5 text-slate-400" />
                    {t('financial.labour')}
                  </span>
                  <span className="font-bold text-slate-900">{formatCurrency(labourCost)}</span>
                </div>
                <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                  <span className="text-slate-600 flex items-center gap-2">
                    <Building className="w-3.5 h-3.5 text-slate-400" />
                    {t('financial.rent')}
                  </span>
                  <span className="font-bold text-slate-900">{formatCurrency(rentCost)}</span>
                </div>
                <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                  <span className="text-slate-600 flex items-center gap-2">
                    <Zap className="w-3.5 h-3.5 text-slate-400" />
                    {t('financial.utilities')}
                  </span>
                  <span className="font-bold text-slate-900">{formatCurrency(utilitiesCost)}</span>
                </div>
                <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                  <span className="text-slate-600 flex items-center gap-2">
                    <Truck className="w-3.5 h-3.5 text-slate-400" />
                    {t('financial.transportation')}
                  </span>
                  <span className="font-bold text-slate-900">{formatCurrency(transportCost)}</span>
                </div>
                <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                  <span className="text-slate-600 flex items-center gap-2">
                    <Megaphone className="w-3.5 h-3.5 text-slate-400" />
                    {t('financial.marketing')}
                  </span>
                  <span className="font-bold text-slate-900">{formatCurrency(marketingCost)}</span>
                </div>
                <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                  <span className="text-slate-600 flex items-center gap-2">
                    <Briefcase className="w-3.5 h-3.5 text-slate-400" />
                    {t('financial.other')}
                  </span>
                  <span className="font-bold text-slate-900">{formatCurrency(otherCost)}</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-emerald-50/70 border border-emerald-200 rounded-xl font-bold">
                  <span className="text-emerald-950">{t('financial.totalMonthlyCost')}</span>
                  <span className="text-emerald-900 text-sm">{formatCurrency(monthlyOpex)}</span>
                </div>
              </div>
            </div>

            {/* Operational Cashflow & Viability */}
            <div className="space-y-2.5 text-xs">
              <h4 className="font-bold text-slate-800 uppercase tracking-wider text-[11px] flex items-center gap-1.5">
                <TrendingUp className="w-3.5 h-3.5 text-amber-700" />
                {t('financial.viabilityTitle')}
              </h4>
              <div className="space-y-2">
                <div className="p-3 bg-amber-50/70 border border-amber-200 rounded-xl space-y-1">
                  <span className="text-slate-600 block">{t('financial.recommendedReserveCard')}</span>
                  <span className="text-lg font-extrabold text-amber-900 block">
                    {formatCurrency(recommendedReserve)}
                  </span>
                  <p className="text-[11px] text-amber-800">
                    {t('financial.reserveExplanation')}
                  </p>
                </div>

                <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                  <span className="text-slate-600">{t('financial.breakEvenRevenue')}</span>
                  <span className="font-bold text-slate-900">
                    {formatCurrency(working_capital.break_even_monthly_revenue)}
                  </span>
                </div>

                <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
                  <span className="text-slate-600">{t('financial.projectedRevenue')}</span>
                  <span className="font-bold text-emerald-800">
                    {formatCurrency(working_capital.projected_monthly_revenue)}
                  </span>
                </div>

                <div className="flex justify-between items-center p-2.5 bg-emerald-50/70 border border-emerald-200 rounded-xl">
                  <span className="font-bold text-emerald-950">{t('financial.projectedProfit')}</span>
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
      {analysisData?.ai_explanation &&
       (!analysisData.input || (analysisData.input.business_category === category && Number(analysisData.input.available_capital) === capital)) && (
        <Card
          title={t('financial.aiAdvisoryFinTitle')}
          subtitle={t('financial.aiAdvisoryFinSubtitle')}
          badge={
            <Badge variant="primary" size="sm">
              {t('financial.aiAdvisoryFinBadge')}
            </Badge>
          }
          className="border-emerald-200 bg-emerald-50/20"
        >
          <div className="space-y-3.5 text-xs text-slate-700">
            <div className="p-3.5 bg-white rounded-xl border border-slate-200 space-y-1">
              <span className="font-bold text-slate-900 block">{t('financial.equityStructureTitle')}</span>
              <p className="leading-relaxed text-slate-600">
                {analysisData.ai_explanation.financial_explanation}
              </p>
            </div>
            <div className="p-3.5 bg-white rounded-xl border border-slate-200 space-y-1">
              <span className="font-bold text-slate-900 block">{t('financial.moratoriumImpactTitle')}</span>
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
          <strong>{t('financial.footerDisclaimerTitle')}</strong>
          {t('financial.footerDisclaimerText')}
        </p>
      </div>

      {/* Bottom Navigation */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-slate-200">
        <Button
          variant="outline"
          onClick={() => navigate('/analysis')}
          icon={RotateCcw}
        >
          {t('financial.backToAnalysisBtn')}
        </Button>
        <Button
          variant="primary"
          size="lg"
          onClick={() => navigate('/report')}
          icon={ArrowRight}
          className="w-full sm:w-auto font-bold shadow-md"
        >
          {t('financial.viewFinalReportBtn')}
        </Button>
      </div>
    </div>
  );
};

export default Financial;
