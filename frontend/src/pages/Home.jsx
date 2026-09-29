import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Compass,
  TrendingUp,
  Calculator,
  ShieldCheck,
  Calendar,
  FileCheck2,
  ArrowRight,
  Sparkles,
  CheckCircle2,
  MapPin,
  Store,
  Banknote,
} from 'lucide-react';
import { Button, Card, Badge } from '../components/common';
import { DEFAULT_DEMO_SCENARIO } from '../data/defaultData';
import { formatCurrency } from '../utils/formatters';
import { useBizSahayak } from '../hooks/useBizSahayak';
import { useTranslation } from '../context/LanguageContext';

export const Home = () => {
  const navigate = useNavigate();
  const { setInputData } = useBizSahayak();
  const { t, getCategoryLabel } = useTranslation();

  const handleStartAnalysis = () => {
    navigate('/business-input');
  };

  const handleLaunchDemo = () => {
    setInputData({
      location: DEFAULT_DEMO_SCENARIO.location,
      business_category: DEFAULT_DEMO_SCENARIO.business_category,
      available_capital: DEFAULT_DEMO_SCENARIO.available_capital,
    });
    navigate('/business-input');
  };

  const features = [
    {
      title: t('home.feat1Title'),
      description: t('home.feat1Desc'),
      icon: Compass,
      color: 'bg-emerald-50 text-emerald-800 border-emerald-200',
    },
    {
      title: t('home.feat2Title'),
      description: t('home.feat2Desc'),
      icon: Calculator,
      color: 'bg-sky-50 text-sky-800 border-sky-200',
    },
    {
      title: t('home.feat3Title'),
      description: t('home.feat3Desc'),
      icon: Calendar,
      color: 'bg-teal-50 text-teal-800 border-teal-200',
    },
    {
      title: t('home.feat4Title'),
      description: t('home.feat4Desc'),
      icon: FileCheck2,
      color: 'bg-rose-50 text-rose-800 border-rose-200',
    },
  ];

  return (
    <div className="space-y-12 sm:space-y-16">
      {/* Hero Section */}
      <section className="text-center max-w-3xl mx-auto pt-4 sm:pt-10 space-y-6">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-emerald-100/90 border border-emerald-200 text-emerald-950 text-xs font-bold shadow-2xs">
          <Sparkles className="w-3.5 h-3.5 text-emerald-700" />
          <span>{t('home.heroBadge')}</span>
        </div>

        <div className="space-y-3">
          <h1 className="text-4xl sm:text-6xl font-black text-slate-900 tracking-tight leading-tight">
            Udyam<span className="text-amber-600">Saarthi</span>
          </h1>
          <p className="text-lg sm:text-2xl font-bold text-emerald-900 tracking-tight">
            "{t('nav.tagline')}"
          </p>
        </div>

        <p className="text-sm sm:text-base text-slate-600 leading-relaxed max-w-2xl mx-auto">
          {t('home.heroSubtitle')}
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
          <Button
            variant="primary"
            size="lg"
            onClick={handleStartAnalysis}
            icon={ArrowRight}
            className="w-full sm:w-auto text-base px-8 py-3.5 shadow-md hover:shadow-lg font-bold"
          >
            {t('home.startPlanningBtn')}
          </Button>

          <Button
            variant="outline"
            size="lg"
            onClick={handleLaunchDemo}
            className="w-full sm:w-auto font-semibold"
          >
            {t('input.loadDemoBtn')}
          </Button>
        </div>
      </section>

      {/* Featured Scenario Benchmark Card */}
      <section className="max-w-4xl mx-auto">
        <Card
          className="border-emerald-200 bg-gradient-to-br from-emerald-50/70 via-white to-amber-50/40"
          title="SIH26091 Benchmark Evaluation Scenario"
          badge={
            <Badge variant="primary" size="sm">
              {t('nav.sihBadge')}
            </Badge>
          }
        >
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-1">
            <div className="bg-white p-4 rounded-xl border border-slate-200 flex items-center gap-3">
              <div className="p-2 rounded-lg bg-emerald-100 text-emerald-800">
                <MapPin className="w-5 h-5" />
              </div>
              <div>
                <span className="text-xs text-slate-500 font-semibold block uppercase">
                  {t('analysis.locationTag')}
                </span>
                <span className="text-sm sm:text-base font-bold text-slate-800">
                  {DEFAULT_DEMO_SCENARIO.location}
                </span>
              </div>
            </div>

            <div className="bg-white p-4 rounded-xl border border-slate-200 flex items-center gap-3">
              <div className="p-2 rounded-lg bg-amber-100 text-amber-800">
                <Store className="w-5 h-5" />
              </div>
              <div>
                <span className="text-xs text-slate-500 font-semibold block uppercase">
                  {t('analysis.categoryTag')}
                </span>
                <span className="text-sm sm:text-base font-bold text-slate-800">
                  {getCategoryLabel(DEFAULT_DEMO_SCENARIO.business_category)}
                </span>
              </div>
            </div>

            <div className="bg-white p-4 rounded-xl border border-slate-200 flex items-center gap-3">
              <div className="p-2 rounded-lg bg-emerald-100 text-emerald-800">
                <Banknote className="w-5 h-5" />
              </div>
              <div>
                <span className="text-xs text-slate-500 font-semibold block uppercase">
                  {t('analysis.capitalTag')}
                </span>
                <span className="text-sm sm:text-base font-bold text-emerald-800">
                  {formatCurrency(DEFAULT_DEMO_SCENARIO.available_capital)}
                </span>
              </div>
            </div>
          </div>

          <div className="mt-4 pt-4 border-t border-slate-200/80 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs text-slate-600">
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-700 shrink-0" />
              <span>
                {t('financial.deterministicBadge')}: <strong className="text-slate-800">₹10 Lakh Project Cost</strong>{' '}
                → <strong className="text-emerald-900">{DEFAULT_DEMO_SCENARIO.scheme_name}</strong>
              </span>
            </span>
            <Button
              variant="subtle"
              size="sm"
              onClick={handleLaunchDemo}
              icon={ArrowRight}
            >
              {t('input.loadDemoBtn')}
            </Button>
          </div>
        </Card>
      </section>

      {/* Feature Section */}
      <section className="max-w-5xl mx-auto space-y-6">
        <div className="text-center space-y-2">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            {t('home.featuresTitle')}
          </h2>
          <p className="text-sm sm:text-base text-slate-500 max-w-xl mx-auto">
            {t('home.featuresSubtitle')}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          {features.map((feat, idx) => {
            const Icon = feat.icon;
            return (
              <Card key={idx} className="hover:border-emerald-300 card-hover flex flex-col justify-between">
                <div className="space-y-3">
                  <div
                    className={`w-12 h-12 rounded-2xl border flex items-center justify-center ${feat.color}`}
                  >
                    <Icon className="w-6 h-6" />
                  </div>
                  <h3 className="text-base font-bold text-slate-900">
                    {feat.title}
                  </h3>
                  <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                    {feat.description}
                  </p>
                </div>
              </Card>
            );
          })}
        </div>
      </section>

      {/* Bottom CTA Banner */}
      <section className="max-w-4xl mx-auto bg-emerald-900 text-white rounded-3xl p-8 sm:p-10 shadow-xl relative overflow-hidden">
        <div className="relative z-10 space-y-4 text-center sm:text-left sm:flex sm:items-center sm:justify-between sm:space-y-0 gap-6">
          <div className="space-y-2 max-w-lg">
            <h3 className="text-2xl sm:text-3xl font-bold tracking-tight">
              {t('home.ctaTitle')}
            </h3>
            <p className="text-emerald-100 text-sm leading-relaxed">
              {t('home.ctaSubtitle')}
            </p>
          </div>
          <Button
            variant="secondary"
            size="lg"
            onClick={handleStartAnalysis}
            icon={ArrowRight}
            className="w-full sm:w-auto shrink-0 shadow-lg text-amber-950 font-bold"
          >
            {t('home.ctaBtn')}
          </Button>
        </div>
      </section>
    </div>
  );
};

export default Home;
