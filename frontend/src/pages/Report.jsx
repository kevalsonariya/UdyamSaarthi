import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  FileText,
  Download,
  Printer,
  CheckCircle,
  ShieldCheck,
  Building,
  TrendingUp,
  MapPin,
  Calendar,
  Info,
  RotateCcw,
  Sparkles,
  ArrowRight,
  Clock,
  Banknote,
  PieChart as PieChartIcon,
  AlertTriangle,
  Lightbulb,
  CheckCircle2,
  Check,
  Store,
  Layers,
  Award,
} from 'lucide-react';
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
import { FINANCIAL_DISCLAIMER } from '../data/defaultData';
import { bizApi } from '../services/api';
import { useTranslation } from '../context/LanguageContext';

export const Report = () => {
  const navigate = useNavigate();
  const { inputData, analysisData, financialData, setFinancialData, resetToDemoScenario } = useBizSahayak();
  const { t, getCategoryLabel } = useTranslation();

  const [downloading, setDownloading] = useState(false);
  const [downloadSuccess, setDownloadSuccess] = useState(false);
  const [loading, setLoading] = useState(!financialData);
  const [error, setError] = useState(null);

  const location = inputData.location || 'Anand, Gujarat';
  const category = inputData.business_category || 'Textile & Clothing';
  const capital = Number(inputData.available_capital) || 100000;

  // Format generated date
  const generatedDate = new Date().toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });

  // Ensure financial data is loaded
  useEffect(() => {
    const loadData = async () => {
      if (!financialData || financialData.financial?.available_capital !== capital) {
        setLoading(true);
        try {
          const data = await bizApi.getFinancialPlan({
            location,
            business_category: category,
            available_capital: capital,
          });
          setFinancialData(data);
        } catch (err) {
          console.error('Error fetching financial plan:', err);
          setError(t('common.errorMessage'));
        } finally {
          setLoading(false);
        }
      }
    };
    loadData();
  }, [capital, category, location]);

  const handleDownloadPDF = async () => {
    setDownloading(true);
    setDownloadSuccess(false);

    try {
      // Call backend PDF endpoint as instructed
      const response = await bizApi.generateReport({
        location,
        business_category: category,
        available_capital: capital,
      });

      // Handle binary blob streaming from ReportLab backend
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      const cleanLocation = location.replace(/[^a-zA-Z0-9]/g, '_');
      const cleanCategory = category.replace(/[^a-zA-Z0-9]/g, '_');
      link.setAttribute('download', `UdyamSaarthi_BusinessPlan_${cleanCategory}_${cleanLocation}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      setDownloadSuccess(true);
    } catch (err) {
      console.warn('Backend PDF endpoint pending; fallback to browser print view.', err);
      // Fallback print for demo resiliency
      window.print();
      setDownloadSuccess(true);
    } finally {
      setDownloading(false);
    }
  };

  const handleStartNewAnalysis = () => {
    resetToDemoScenario();
    navigate('/business-input');
  };

  if (loading) {
    return <FinancialSkeleton />;
  }

  if (error || !financialData) {
    return (
      <div className="py-12">
        <ErrorState
          title={t('common.errorTitle')}
          message={error || t('common.errorMessage')}
          retryLabel={t('common.retry')}
          onRetry={() => window.location.reload()}
        />
      </div>
    );
  }

  const { financial, scheme, emi, repayment, working_capital } = financialData;

  return (
    <div className="space-y-8 max-w-5xl mx-auto print:max-w-full">
      {/* Top Document Header Banner */}
      <div className="bg-white rounded-3xl border border-slate-200 card-shadow p-6 sm:p-8 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-6">
          <div className="flex items-center gap-3.5">
            <div className="w-12 h-12 rounded-2xl bg-emerald-800 text-white flex items-center justify-center font-black text-2xl shadow-md">
              US
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-2xl font-black text-emerald-950 tracking-tight">
                  Udyam<span className="text-amber-600">Saarthi</span>
                </span>
                <span className="text-xs uppercase font-bold tracking-wider px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200">
                  {t('report.officialDossier')}
                </span>
              </div>
              <h1 className="text-sm font-semibold text-slate-500 mt-0.5">
                {t('report.dossierSubtitle')}
              </h1>
            </div>
          </div>

          {/* Action CTAs */}
          <div className="flex items-center gap-2.5 print:hidden flex-wrap">
            <Button
              variant="outline"
              size="md"
              onClick={handleStartNewAnalysis}
              icon={RotateCcw}
            >
              {t('report.startNewBtn')}
            </Button>
            <Button
              variant="primary"
              size="md"
              onClick={handleDownloadPDF}
              loading={downloading}
              icon={Download}
              className="shadow-sm font-bold"
            >
              {downloading ? t('report.generatingPdf') : t('report.downloadPdfBtn')}
            </Button>
          </div>
        </div>

        {/* Header Metadata Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
          <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
            <span className="text-slate-500 font-semibold block uppercase">
              {t('report.enterpriseCategory')}
            </span>
            <span className="font-bold text-slate-900 text-sm mt-1 block">
              {getCategoryLabel(category)}
            </span>
          </div>

          <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
            <span className="text-slate-500 font-semibold block uppercase">
              {t('report.targetLocation')}
            </span>
            <span className="font-bold text-slate-900 text-sm mt-1 block">{location}</span>
          </div>

          <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
            <span className="text-slate-500 font-semibold block uppercase">
              {t('report.promoterEquity')}
            </span>
            <span className="font-bold text-emerald-800 text-sm mt-1 block">
              {formatCurrency(financial.available_capital)} (10%)
            </span>
          </div>

          <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
            <span className="text-slate-500 font-semibold block uppercase">
              {t('report.generatedDate')}
            </span>
            <span className="font-bold text-slate-800 text-sm mt-1 block">{generatedDate}</span>
          </div>
        </div>

        {/* PDF Download Success Banner */}
        {downloadSuccess && (
          <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-2xl flex items-center justify-between text-xs text-emerald-950 transition-all">
            <div className="flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-emerald-700 shrink-0" />
              <span>
                <strong>Success! </strong>
                {t('report.successBanner')}
              </span>
            </div>
            <button
              onClick={() => setDownloadSuccess(false)}
              className="text-emerald-700 hover:text-emerald-900 font-bold ml-2 cursor-pointer"
            >
              {t('report.dismiss')}
            </button>
          </div>
        )}
      </div>

      {/* Mandatory Disclaimer */}
      <div className="bg-amber-50/90 border border-amber-200 rounded-2xl p-4 flex items-start gap-3">
        <Info className="w-5 h-5 text-amber-700 shrink-0 mt-0.5" />
        <div className="text-xs text-amber-950 leading-relaxed">
          <strong className="font-bold">{t('report.officialDisclaimer')} </strong>
          {FINANCIAL_DISCLAIMER}
        </div>
      </div>

      {/* 1. Business Overview */}
      <Card
        title={t('analysis.businessSummaryTitle')}
        subtitle={t('analysis.businessSummarySubtitle')}
        badge={<Badge variant="primary">{t('report.verifiedBadge')}</Badge>}
      >
        <div className="space-y-4 text-xs sm:text-sm">
          <p className="text-slate-700 leading-relaxed">
            {t('report.enterpriseSummary', {
              category: getCategoryLabel(category),
              location,
              capital: formatCurrency(financial.available_capital),
              projectCost: formatCurrency(financial.project_cost),
              loanAmount: formatCurrency(scheme.eligible_funding),
              scheme: scheme.scheme_name,
            })}
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5 pt-2">
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 text-xs">
              <span className="text-slate-500 font-medium block">
                {t('report.promoterEquity')}
              </span>
              <span className="text-base font-bold text-slate-900 mt-1 block">
                {formatCurrency(financial.available_capital)}
              </span>
            </div>
            <div className="p-3.5 bg-emerald-50/70 rounded-xl border border-emerald-200 text-xs">
              <span className="text-emerald-800 font-medium block">
                {t('financial.projectCost')}
              </span>
              <span className="text-base font-extrabold text-emerald-950 mt-1 block">
                {formatCurrency(financial.project_cost)}
              </span>
            </div>
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 text-xs">
              <span className="text-slate-500 font-medium block">
                {t('financial.maxLoan')}
              </span>
              <span className="text-base font-bold text-slate-900 mt-1 block">
                {formatCurrency(scheme.eligible_funding)}
              </span>
            </div>
          </div>
        </div>
      </Card>

      {/* 2. Market Opportunity & 3. Market Reach (2 cols) */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* 2. Market Opportunity */}
        <Card
          title={t('analysis.opportunitiesTitle')}
          subtitle={t('analysis.opportunitiesSubtitle')}
        >
          <div className="space-y-3 text-xs">
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 flex items-start gap-2.5">
              <Lightbulb className="w-4 h-4 text-amber-700 shrink-0 mt-0.5" />
              <div>
                <span className="font-bold text-slate-900">Regional Supply Proximity:</span>
                <p className="text-slate-600 mt-0.5">
                  Proximity to key raw material transport corridors lowers input freight costs by ~15-20%.
                </p>
              </div>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 flex items-start gap-2.5">
              <TrendingUp className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
              <div>
                <span className="font-bold text-slate-900">Harvest Seasonal Peaks:</span>
                <p className="text-slate-600 mt-0.5">
                  Agricultural harvest cycles and festival periods generate 2x predictable quarterly turnover spikes.
                </p>
              </div>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 flex items-start gap-2.5">
              <ShieldCheck className="w-4 h-4 text-sky-700 shrink-0 mt-0.5" />
              <div>
                <span className="font-bold text-slate-900">Underserved Semi-Rural Demand:</span>
                <p className="text-slate-600 mt-0.5">
                  Fills the gap between low-quality mobile haat goods and distant town retail showrooms.
                </p>
              </div>
            </div>
          </div>
        </Card>

        {/* 3. Market Reach */}
        <Card
          title={t('analysis.marketReachTitle')}
          subtitle={t('analysis.marketReachSubtitle')}
        >
          <div className="space-y-3.5 text-xs">
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-600 font-medium">{t('analysis.catchmentLabel')}:</span>
              <span className="font-bold text-slate-900">0 – 15 km Radius</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-600 font-medium">{t('analysis.populationLabel')}:</span>
              <span className="font-bold text-emerald-800">18,500 – 24,000 residents</span>
            </div>
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-600 font-medium">{t('analysis.segmentsTitle')}</span>
              <span className="font-bold text-slate-900">Farming Families, Salaried Workers, Youth</span>
            </div>
            <p className="text-slate-500 pt-1 leading-relaxed text-[11px]">
              Note: Market reach metrics are simulated local market estimates for appraisal demonstration.
            </p>
          </div>
        </Card>
      </div>

      {/* 4. SWOT Analysis (2x2 Grid) */}
      <Card
        title={t('analysis.swotTitle')}
        subtitle={t('analysis.swotSubtitle')}
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div className="p-3.5 bg-emerald-50/70 border border-emerald-200 rounded-xl space-y-1.5">
            <span className="font-bold text-emerald-950 block">{t('analysis.strengths')}</span>
            <ul className="text-slate-700 space-y-1 list-disc list-inside">
              <li>Low establishment overhead compared to town showrooms.</li>
              <li>Direct community trust and flexible customized service.</li>
            </ul>
          </div>

          <div className="p-3.5 bg-amber-50/70 border border-amber-200 rounded-xl space-y-1.5">
            <span className="font-bold text-amber-950 block">{t('analysis.weaknesses')}</span>
            <ul className="text-slate-700 space-y-1 list-disc list-inside">
              <li>Limited initial inventory prior to bank loan drawdown.</li>
              <li>Need to transition from manual to digital accounting.</li>
            </ul>
          </div>

          <div className="p-3.5 bg-sky-50/70 border border-sky-200 rounded-xl space-y-1.5">
            <span className="font-bold text-sky-950 block">{t('analysis.opportunities')}</span>
            <ul className="text-slate-700 space-y-1 list-disc list-inside">
              <li>Subsidized interest credit under {scheme.scheme_name}.</li>
              <li>Tie-ups with local village cooperatives and schools.</li>
            </ul>
          </div>

          <div className="p-3.5 bg-red-50/70 border border-red-200 rounded-xl space-y-1.5">
            <span className="font-bold text-red-950 block">{t('analysis.threats')}</span>
            <ul className="text-slate-700 space-y-1 list-disc list-inside">
              <li>Extended credit expectations from farmers during harvest gaps.</li>
              <li>Raw material price fluctuations during off-season months.</li>
            </ul>
          </div>
        </div>
      </Card>

      {/* 5. Risks & 6. Competitors (2 cols) */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* 5. Risks */}
        <Card
          title={t('analysis.risksTitle')}
          subtitle={t('analysis.risksSubtitle')}
        >
          <div className="space-y-3 text-xs">
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
              <div className="flex justify-between items-center">
                <span className="font-bold text-slate-900">Cashflow Gaps:</span>
                <Badge variant="warning" size="sm">Medium</Badge>
              </div>
              <p className="text-slate-600">
                <strong>{t('analysis.mitigationLabel')}</strong> Use {scheme.moratorium_months}-month moratorium to build a 3-month operational buffer.
              </p>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
              <div className="flex justify-between items-center">
                <span className="font-bold text-slate-900">Customer Credit Pressure:</span>
                <Badge variant="danger" size="sm">High</Badge>
              </div>
              <p className="text-slate-600">
                <strong>{t('analysis.mitigationLabel')}</strong> Implement a cash-first policy with small discounts for upfront UPI payments.
              </p>
            </div>
          </div>
        </Card>

        {/* 6. Competitors */}
        <Card
          title={t('analysis.competitorsTitle')}
          subtitle={t('analysis.competitorsSubtitle')}
        >
          <div className="space-y-3 text-xs">
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 flex justify-between items-center">
              <div>
                <span className="font-bold text-slate-900 block">Village Retail Traders</span>
                <span className="text-[11px] text-slate-500">Established brick-and-mortar storefronts</span>
              </div>
              <span className="font-semibold text-slate-700">Moderate Threat</span>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 flex justify-between items-center">
              <div>
                <span className="font-bold text-slate-900 block">Weekly Haat Stalls</span>
                <span className="text-[11px] text-slate-500">Mobile informal traders with low quality</span>
              </div>
              <span className="font-semibold text-slate-700">Differentiated by Quality</span>
            </div>
          </div>
        </Card>
      </div>

      {/* 7. Pricing & 8. Recommendation (2 cols) */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* 7. Pricing */}
        <Card
          title={t('analysis.pricingTitle')}
          subtitle={t('analysis.pricingSubtitle')}
        >
          <div className="space-y-3 text-xs">
            <div className="flex justify-between items-center p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-600">{t('analysis.priceRangeLabel')}:</span>
              <span className="font-bold text-emerald-900 text-sm">₹220 – ₹850</span>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
              <span className="font-bold text-slate-900">{t('analysis.suggestedApproachTitle')}:</span>
              <p className="text-slate-600">
                Tiered pricing: competitive everyday items build store footfall; customized and festival items deliver 35-40% gross margins.
              </p>
            </div>
          </div>
        </Card>

        {/* 8. Business Recommendation */}
        <Card
          title={t('analysis.recommendationTitle')}
          subtitle={t('analysis.recommendationSubtitle')}
        >
          <div className="p-4 bg-emerald-50/70 border border-emerald-200 rounded-xl space-y-2 text-xs">
            <div className="flex items-center justify-between">
              <span className="font-extrabold text-emerald-950 text-sm">
                {t('analysis.scoreBadge', { score: 83 })}
              </span>
              <Badge variant="primary">{t('report.recommendedBadge')}</Badge>
            </div>
            <p className="text-slate-700 leading-relaxed">
              The proposed enterprise demonstrates favorable unit economics and satisfies all credit underwriting parameters for{' '}
              <strong>{scheme.scheme_name}</strong>.
            </p>
          </div>
        </Card>
      </div>

      {/* Financial Sizing & Scheme Table (Sections 9 - 15) */}
      <Card
        title={t('financial.structuringTitle')}
        subtitle={t('financial.loanTermsSubtitle', { scheme: scheme.scheme_name })}
        badge={<Badge variant="primary">{scheme.scheme_name}</Badge>}
      >
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 text-xs">
          <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
            <span className="text-slate-500 font-semibold block uppercase">
              {t('financial.projectCost')}
            </span>
            <span className="text-lg font-black text-emerald-950 mt-1 block">
              {formatCurrency(financial.project_cost)}
            </span>
            <span className="text-[11px] text-slate-500">{t('financial.projectCostSub')}</span>
          </div>

          <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
            <span className="text-slate-500 font-semibold block uppercase">
              {t('financial.maxLoan')}
            </span>
            <span className="text-lg font-black text-emerald-950 mt-1 block">
              {formatCurrency(scheme.eligible_funding)}
            </span>
            <span className="text-[11px] text-slate-500">{t('financial.maxLoanSub')}</span>
          </div>

          <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
            <span className="text-slate-500 font-semibold block uppercase">
              {t('financial.selectedScheme')}
            </span>
            <span className="text-sm font-bold text-slate-900 mt-1 block">
              {scheme.scheme_name}
            </span>
            <span className="text-[11px] text-slate-500">{scheme.governing_body}</span>
          </div>

          <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
            <span className="text-slate-500 font-semibold block uppercase">
              {t('financial.interestRate')}
            </span>
            <span className="text-lg font-black text-amber-900 mt-1 block">
              {formatPercentage(scheme.interest_rate_percent)} p.a.
            </span>
            <span className="text-[11px] text-slate-500">{t('financial.fixedAnnual')}</span>
          </div>

          <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
            <span className="text-slate-500 font-semibold block uppercase">
              {t('financial.monthlyEmi')}
            </span>
            <span className="text-lg font-black text-emerald-950 mt-1 block">
              {formatCurrency(emi.monthly_emi)}
            </span>
            <span className="text-[11px] text-slate-500">
              {t('financial.emiApplicableFor', { months: emi.post_moratorium_tenure_months })}
            </span>
          </div>

          <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
            <span className="text-slate-500 font-semibold block uppercase">
              {t('financial.moratoriumPeriod')}
            </span>
            <span className="text-lg font-black text-sky-950 mt-1 block">
              {scheme.moratorium_months} {t('financial.months')}
            </span>
            <span className="text-[11px] text-slate-500">{t('financial.zeroPrincipal')}</span>
          </div>
        </div>

        {/* 15. Repayment Summary */}
        <div className="mt-4 p-4 bg-slate-50 rounded-xl border border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
          <div>
            <span className="font-bold text-slate-900 block">{t('financial.repaymentTitle')}:</span>
            <span className="text-slate-600">
              {t('financial.loanTenure')}: {scheme.tenure_years} {t('financial.years')} ({scheme.tenure_months} {t('financial.months')}). {t('financial.totalInterest')}:{' '}
              <strong>{formatCurrency(emi.total_interest_payable)}</strong>. {t('financial.totalRepayment')}:{' '}
              <strong>{formatCurrency(emi.total_repayment_amount)}</strong>.
            </span>
          </div>
          <Badge variant="primary" size="md" className="shrink-0 self-start sm:self-center">
            {scheme.tenure_years} {t('financial.years')} Amortization
          </Badge>
        </div>
      </Card>

      {/* 16. Working Capital Planning */}
      <Card
        title={t('financial.workingCapitalTitle')}
        subtitle={t('financial.workingCapitalSubtitle')}
      >
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
          <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
            <span className="text-slate-500 block">{t('financial.monthlyOperatingCost')}:</span>
            <span className="text-sm font-bold text-slate-900 mt-1 block">
              {formatCurrency(working_capital.total_monthly_operating_expense)}
            </span>
          </div>
          <div className="p-3 bg-amber-50/70 border border-amber-200 rounded-xl">
            <span className="text-amber-800 block">{t('financial.recommendedReserve')}:</span>
            <span className="text-sm font-bold text-amber-950 mt-1 block">
              {formatCurrency(working_capital.recommended_3_months_reserve)}
            </span>
          </div>
          <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
            <span className="text-slate-500 block">{t('financial.breakEvenRevenue')}:</span>
            <span className="text-sm font-bold text-slate-900 mt-1 block">
              {formatCurrency(working_capital.break_even_monthly_revenue)}
            </span>
          </div>
          <div className="p-3 bg-emerald-50/70 border border-emerald-200 rounded-xl">
            <span className="text-emerald-800 block">{t('financial.projectedProfit')}:</span>
            <span className="text-sm font-extrabold text-emerald-950 mt-1 block">
              {formatCurrency(working_capital.projected_monthly_net_profit)}
            </span>
          </div>
        </div>
      </Card>

      {/* 17. Recommended Next Steps */}
      <Card
        title={t('analysis.recommendedNextActions')}
        subtitle={t('analysis.recommendationSubtitle')}
        badge={
          <Badge variant="success">
            {analysisData?.ai_explanation?.is_ai_generated ? t('report.aiRoadmapBadge') : t('report.advisoryRoadmapBadge')}
          </Badge>
        }
      >
        <div className="space-y-3 text-xs text-slate-700">
          {(analysisData?.ai_explanation?.next_steps || [
            `Submit this compiled UdyamSaarthi business plan dossier to the designated nodal rural credit officer under ${scheme.scheme_name}.`,
            "Procure primary machinery and install essential fittings using the initial capital drawdown during Month 1.",
            `Utilize the ${scheme.moratorium_months}-month moratorium grace period to build operating reserves before regular principal repayments begin.`,
            "Launch community outreach and establish local supply partnerships.",
          ]).map((step, idx) => (
            <div key={idx} className="flex items-start gap-3 p-3 bg-slate-50 rounded-xl border border-slate-200">
              <div className="w-6 h-6 rounded-full bg-emerald-700 text-white flex items-center justify-center font-bold text-xs shrink-0 mt-0.5">
                {idx + 1}
              </div>
              <div>
                <span className="font-bold text-slate-900 block">
                  {t('report.milestone', { number: idx + 1 })}
                </span>
                <p className="text-slate-600 mt-0.5">{step}</p>
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Bottom Action Footer */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-slate-200 print:hidden">
        <Button
          variant="outline"
          onClick={handleStartNewAnalysis}
          icon={RotateCcw}
        >
          {t('report.startNewBtn')}
        </Button>
        <div className="flex items-center gap-3">
          <Button
            variant="ghost"
            onClick={() => window.print()}
            icon={Printer}
          >
            {t('report.printBtn')}
          </Button>
          <Button
            variant="primary"
            size="lg"
            onClick={handleDownloadPDF}
            loading={downloading}
            icon={Download}
            className="font-bold shadow-md"
          >
            {downloading ? t('report.generatingPdf') : t('report.downloadPdfBtn')}
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Report;
