import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Compass,
  ArrowRight,
  TrendingUp,
  AlertTriangle,
  Users,
  Target,
  CheckCircle2,
  Tag,
  Lightbulb,
  Building,
  Sparkles,
  Info,
  MapPin,
  Store,
  Banknote,
  ShieldAlert,
  ArrowUpRight,
  RotateCcw,
} from 'lucide-react';
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
} from 'recharts';
import {
  Button,
  Card,
  Badge,
  SectionHeader,
  StatCard,
  AnalysisSkeleton,
  ErrorState,
} from '../components/common';
import { useBizSahayak } from '../hooks/useBizSahayak';
import { formatCurrency } from '../utils/formatters';
import { bizApi } from '../services/api';
import { useTranslation } from '../context/LanguageContext';

const SEGMENT_COLORS = ['#15803d', '#d97706', '#0284c7'];

export const Analysis = () => {
  const navigate = useNavigate();
  const { inputData, analysisData, setAnalysisData } = useBizSahayak();
  const { t, getCategoryLabel } = useTranslation();

  const [loading, setLoading] = useState(!analysisData);
  const [error, setError] = useState(null);

  const location = inputData.location || 'Anand, Gujarat';
  const category = inputData.business_category || 'Textile & Clothing';
  const capital = Number(inputData.available_capital) || 100000;

  const fetchAnalysis = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await bizApi.analyzeBusiness({
        location,
        business_category: category,
        available_capital: capital,
      });
      setAnalysisData(data);
    } catch (err) {
      console.error('Failed to load analysis:', err);
      setError(t('analysis.errorMessage'));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // If not already in cache or if input changed, fetch
    if (!analysisData) {
      fetchAnalysis();
    }
  }, [location, category, capital]);

  if (loading) {
    return <AnalysisSkeleton />;
  }

  if (error || !analysisData) {
    return (
      <div className="py-12">
        <ErrorState
          title={t('analysis.errorTitle')}
          message={error || t('analysis.errorMessage')}
          retryLabel={t('analysis.retryBtn')}
          onRetry={fetchAnalysis}
        />
      </div>
    );
  }

  const {
    is_verified,
    business_summary,
    market_reach,
    opportunities,
    swot,
    risks,
    competitors,
    pricing,
    recommendation,
  } = analysisData;

  const severityBadge = (severity) => {
    const sev = (severity || '').toLowerCase();
    if (sev === 'high') return <Badge variant="danger">{severity}</Badge>;
    if (sev === 'medium') return <Badge variant="warning">{severity}</Badge>;
    return <Badge variant="info">{severity}</Badge>;
  };

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      {/* Header */}
      <SectionHeader
        title={t('analysis.headerTitle', { category: getCategoryLabel(category) })}
        subtitle={t('analysis.headerSubtitle', { location })}
        icon={Compass}
        badge={
          <Badge variant="primary" size="md">
            {t('analysis.stepBadge')}
          </Badge>
        }
        action={
          <Button
            variant="primary"
            size="md"
            onClick={() => navigate('/financial')}
            icon={ArrowRight}
            className="shadow-sm font-semibold"
          >
            {t('analysis.proceedBtn')}
          </Button>
        }
      />

      {/* Prototype Data Notice (Mandatory Rule) */}
      <div className="bg-amber-50/80 border border-amber-200/90 rounded-2xl p-4 flex items-start gap-3">
        <Info className="w-5 h-5 text-amber-700 shrink-0 mt-0.5" />
        <div className="text-xs text-amber-950 leading-relaxed">
          <strong className="font-bold">{t('analysis.simulatedNoticeTitle')}</strong>
          <span>{t('analysis.simulatedNoticeText')}</span>
        </div>
      </div>

      {/* 1. Business Summary Card */}
      <Card
        title={t('analysis.businessSummaryTitle')}
        subtitle={t('analysis.businessSummarySubtitle')}
        badge={<Badge variant="default">{t('analysis.profileBadge')}</Badge>}
      >
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 flex items-center gap-3">
            <div className="p-2.5 rounded-lg bg-emerald-100 text-emerald-800 shrink-0">
              <MapPin className="w-4 h-4" />
            </div>
            <div>
              <span className="text-xs text-slate-500 font-semibold block uppercase">
                {t('analysis.locationTag')}
              </span>
              <span className="text-sm font-bold text-slate-900">{location}</span>
            </div>
          </div>

          <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 flex items-center gap-3">
            <div className="p-2.5 rounded-lg bg-amber-100 text-amber-800 shrink-0">
              <Store className="w-4 h-4" />
            </div>
            <div>
              <span className="text-xs text-slate-500 font-semibold block uppercase">
                {t('analysis.categoryTag')}
              </span>
              <span className="text-sm font-bold text-slate-900">{getCategoryLabel(category)}</span>
            </div>
          </div>

          <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 flex items-center gap-3">
            <div className="p-2.5 rounded-lg bg-emerald-100 text-emerald-800 shrink-0">
              <Banknote className="w-4 h-4" />
            </div>
            <div>
              <span className="text-xs text-slate-500 font-semibold block uppercase">
                {t('analysis.capitalTag')}
              </span>
              <span className="text-sm font-bold text-emerald-800">{formatCurrency(capital)}</span>
            </div>
          </div>
        </div>
      </Card>

      {/* Phase B4: AI-Assisted Advisory Explanation */}
      {analysisData?.ai_explanation && (
        <Card
          title={t('analysis.aiAdvisoryTitle')}
          subtitle={t('analysis.aiAdvisorySubtitle')}
          badge={
            <Badge variant="primary" size="sm">
              {t('analysis.aiBadge')}
            </Badge>
          }
          className="border-emerald-200 bg-emerald-50/30"
        >
          <div className="space-y-3.5 text-xs text-slate-700">
            <div className="p-3.5 bg-white rounded-xl border border-emerald-200 space-y-1">
              <span className="font-bold text-emerald-950 block">Executive Summary:</span>
              <p className="leading-relaxed text-slate-700">{analysisData.ai_explanation.summary}</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div className="p-3 bg-white rounded-xl border border-slate-200 space-y-1">
                <span className="font-bold text-slate-900 block">Local Market Insight:</span>
                <p className="leading-relaxed text-slate-600">{analysisData.ai_explanation.market_insight}</p>
              </div>
              <div className="p-3 bg-white rounded-xl border border-slate-200 space-y-1">
                <span className="font-bold text-slate-900 block">Why This Opportunity Matters:</span>
                <p className="leading-relaxed text-slate-600">{analysisData.ai_explanation.opportunity_explanation}</p>
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* 2. Market Reach Card (with Demographics & Simple Chart) */}
      <Card
        title={t('analysis.marketReachTitle')}
        subtitle={t('analysis.marketReachSubtitle')}
      >
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-center">
          {/* Territory & Channels (2 cols) */}
          <div className="lg:col-span-2 space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
              <div className="p-3.5 bg-emerald-50/70 border border-emerald-200 rounded-xl">
                <span className="text-[11px] font-bold text-emerald-800 uppercase block mb-1">
                  {t('analysis.consumerReachLabel')}
                </span>
                <span className="text-xl font-extrabold text-emerald-950">
                  {market_reach?.estimated_consumer_reach}
                </span>
                <p className="text-[11px] text-emerald-700 mt-1">
                  Total accessible rural population within reachable travel time.
                </p>
              </div>

              <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl">
                <span className="text-[11px] font-bold text-slate-600 uppercase block mb-1">
                  {t('analysis.operationalAreaLabel')}
                </span>
                <span className="text-sm font-bold text-slate-900 block">
                  {market_reach?.local_area}
                </span>
                <p className="text-[11px] text-slate-500 mt-1">
                  Primary village settlements & weekly haat connections.
                </p>
              </div>
            </div>

            {/* Distribution Channels */}
            <div>
              <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2.5">
                {t('analysis.distributionChannelsTitle')}
              </h4>
              <div className="space-y-2">
                {market_reach?.distribution_channels?.map((chan, idx) => (
                  <div
                    key={idx}
                    className="p-3 bg-white border border-slate-200 rounded-xl flex flex-col sm:flex-row sm:items-center justify-between gap-2 shadow-2xs text-xs"
                  >
                    <div>
                      <span className="font-bold text-slate-800">{chan.name}</span>
                      <p className="text-slate-500 text-[11px] mt-0.5">{chan.description}</p>
                    </div>
                    <Badge variant="primary" size="sm" className="self-start sm:self-center shrink-0">
                      {chan.suitability}
                    </Badge>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Customer Segments Chart (1 col) */}
          <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl flex flex-col items-center">
            <span className="text-xs font-bold text-slate-700 mb-2">
              {t('analysis.customerSegmentMixTitle')}
            </span>
            <div className="w-full h-44">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={market_reach?.customer_segments || []}
                    dataKey="percentage"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    innerRadius={36}
                    outerRadius={60}
                    paddingAngle={3}
                  >
                    {(market_reach?.customer_segments || []).map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={SEGMENT_COLORS[index % SEGMENT_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    formatter={(val, name) => [`${val}%`, name]}
                    contentStyle={{ borderRadius: '12px', fontSize: '12px' }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div className="w-full space-y-1.5 mt-2">
              {market_reach?.customer_segments?.map((seg, idx) => (
                <div key={idx} className="flex justify-between items-center text-[11px]">
                  <span className="flex items-center gap-1.5 text-slate-600">
                    <span
                      className="w-2.5 h-2.5 rounded-full"
                      style={{ backgroundColor: SEGMENT_COLORS[idx % SEGMENT_COLORS.length] }}
                    />
                    {seg.name}
                  </span>
                  <span className="font-bold text-slate-800">{seg.percentage}%</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </Card>

      {/* 3. Opportunity Analysis */}
      <Card
        title={t('analysis.opportunitiesTitle')}
        subtitle={t('analysis.opportunitiesSubtitle')}
      >
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {opportunities?.map((opp, idx) => (
            <div
              key={idx}
              className="p-4 bg-slate-50 border border-slate-200 rounded-xl flex flex-col justify-between space-y-3"
            >
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="p-2 rounded-lg bg-emerald-100 text-emerald-800">
                    <Lightbulb className="w-4 h-4" />
                  </div>
                  <Badge variant="primary" size="sm">
                    {opp.impact}
                  </Badge>
                </div>
                <h4 className="text-xs font-bold text-slate-900 leading-snug">{opp.title}</h4>
                <p className="text-xs text-slate-600 leading-relaxed">{opp.description}</p>
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* 4. SWOT Analysis (2x2 Responsive Layout) */}
      <Card
        title={t('analysis.swotTitle')}
        subtitle={t('analysis.swotSubtitle')}
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Strengths */}
          <div className="p-4 rounded-xl bg-emerald-50/70 border border-emerald-200 space-y-2.5">
            <div className="flex items-center justify-between">
              <Badge variant="success" size="md">
                {t('analysis.strengthsInternal')}
              </Badge>
            </div>
            <ul className="text-xs text-slate-700 space-y-2">
              {swot?.strengths?.map((item, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="text-emerald-700 font-bold shrink-0">✓</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Weaknesses */}
          <div className="p-4 rounded-xl bg-amber-50/70 border border-amber-200 space-y-2.5">
            <div className="flex items-center justify-between">
              <Badge variant="secondary" size="md">
                {t('analysis.weaknessesInternal')}
              </Badge>
            </div>
            <ul className="text-xs text-slate-700 space-y-2">
              {swot?.weaknesses?.map((item, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="text-amber-700 font-bold shrink-0">!</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Opportunities */}
          <div className="p-4 rounded-xl bg-sky-50/70 border border-sky-200 space-y-2.5">
            <div className="flex items-center justify-between">
              <Badge variant="info" size="md">
                {t('analysis.opportunitiesExternal')}
              </Badge>
            </div>
            <ul className="text-xs text-slate-700 space-y-2">
              {swot?.opportunities?.map((item, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="text-sky-700 font-bold shrink-0">★</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Threats */}
          <div className="p-4 rounded-xl bg-red-50/70 border border-red-200 space-y-2.5">
            <div className="flex items-center justify-between">
              <Badge variant="danger" size="md">
                {t('analysis.threatsExternal')}
              </Badge>
            </div>
            <ul className="text-xs text-slate-700 space-y-2">
              {swot?.threats?.map((item, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="text-red-700 font-bold shrink-0">✕</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </Card>

      {/* 5. Risks / Threats with Mitigations */}
      <Card
        title={t('analysis.risksTitle')}
        subtitle={t('analysis.risksSubtitle')}
      >
        <div className="space-y-3.5">
          {risks?.map((risk, idx) => (
            <div
              key={idx}
              className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-2 text-xs"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1.5">
                <span className="font-bold text-slate-900 text-sm">{risk.title}</span>
                <div className="flex items-center gap-2">
                  <span className="text-slate-500 font-medium">{t('analysis.severityLabel')}</span>
                  {severityBadge(risk.severity)}
                </div>
              </div>
              <p className="text-slate-600 leading-relaxed">{risk.description}</p>
              <div className="pt-2 border-t border-slate-200/80 flex items-start gap-2 text-emerald-950 font-medium bg-emerald-50/60 p-2.5 rounded-lg">
                <CheckCircle2 className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
                <span>
                  <strong>{t('analysis.mitigationLabel')} </strong> {risk.mitigation}
                </span>
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* 6. Competitor Mapping & 7. Pricing (2 cols) */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
        {/* 6. Competitor Mapping Table/Cards */}
        <Card
          title={t('analysis.competitorsTitle')}
          subtitle={t('analysis.competitorsSubtitle')}
        >
          <div className="space-y-3 text-xs">
            {competitors?.map((comp, idx) => (
              <div
                key={idx}
                className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5"
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-900 text-sm">{comp.name}</span>
                  <Badge variant="default" size="sm">
                    {comp.pricing_tier}
                  </Badge>
                </div>
                <div className="text-slate-500">
                  <span>{comp.type}</span> • <span>{comp.presence}</span>
                </div>
                <div className="pt-1 text-[11px] text-amber-900 font-medium">
                  <strong>{t('analysis.unmetGapLabel')} </strong> {comp.weakness}
                </div>
              </div>
            ))}
          </div>
        </Card>

        {/* 7. Product Market Value / Pricing Guidance */}
        <Card
          title={t('analysis.pricingTitle')}
          subtitle={t('analysis.pricingSubtitle')}
        >
          <div className="space-y-4 text-xs">
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
              <span className="text-slate-500 font-semibold block uppercase text-[11px] mb-1">
                {t('analysis.priceRangeLabel')}
              </span>
              <span className="text-2xl font-extrabold text-emerald-900 block">
                {pricing?.estimated_price_range}
              </span>
              <p className="text-slate-500 text-[11px] mt-1">
                Competitive band accommodating local household budgets.
              </p>
            </div>

            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
              <span className="font-bold text-slate-800 block text-xs">
                {t('analysis.purchasingPowerTitle')}
              </span>
              <p className="text-slate-600 leading-relaxed">{pricing?.purchasing_power_context}</p>
            </div>

            <div className="p-3.5 bg-amber-50/70 border border-amber-200 rounded-xl space-y-1 text-amber-950">
              <span className="font-bold text-xs block">
                {t('analysis.suggestedApproachTitle')}
              </span>
              <p className="text-slate-700 leading-relaxed text-[11px]">{pricing?.suggested_approach}</p>
            </div>
          </div>
        </Card>
      </div>

      {/* 8. Prominent Final Business Recommendation Card */}
      <Card
        className="border-emerald-300 bg-gradient-to-br from-emerald-50/90 via-white to-emerald-50/40 p-6 sm:p-8"
        title={t('analysis.recommendationTitle')}
        subtitle={t('analysis.recommendationSubtitle')}
        badge={
          <Badge variant="primary" size="md">
            {t('analysis.scoreBadge', { score: recommendation?.score || 83 })}
          </Badge>
        }
      >
        <div className="space-y-4 text-xs sm:text-sm">
          <div className="space-y-1.5">
            <h3 className="text-lg sm:text-xl font-black text-emerald-950">
              {recommendation?.headline}
            </h3>
            <p className="text-slate-700 leading-relaxed text-xs sm:text-sm">
              {recommendation?.summary}
            </p>
          </div>

          <div className="pt-3 border-t border-emerald-200/80 space-y-2">
            <span className="text-xs font-bold text-slate-800 uppercase tracking-wider block">
              {t('analysis.recommendedNextActions')}
            </span>
            <ul className="space-y-1.5 text-xs text-slate-700">
              {recommendation?.key_actions?.map((act, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
                  <span>{act}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </Card>

      {/* Bottom Navigation */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-slate-200">
        <Button
          variant="outline"
          onClick={() => navigate('/business-input')}
          icon={RotateCcw}
        >
          {t('analysis.modifyInputBtn')}
        </Button>
        <Button
          variant="primary"
          size="lg"
          onClick={() => navigate('/financial')}
          icon={ArrowRight}
          className="w-full sm:w-auto font-bold shadow-md"
        >
          {t('analysis.proceedToFinancialBtn')}
        </Button>
      </div>
    </div>
  );
};

export default Analysis;
