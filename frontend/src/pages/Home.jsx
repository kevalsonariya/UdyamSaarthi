import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Compass,
  TrendingUp,
  ShieldCheck,
  CheckCircle2,
  ArrowRight,
  Sparkles,
  Calculator,
  FileCheck2,
  Building2,
} from 'lucide-react';
import { Button, Card, Badge } from '../components/common';
import { DEFAULT_DEMO_SCENARIO, FINANCIAL_DISCLAIMER } from '../data/defaultData';
import { formatCurrency } from '../utils/formatters';
import { useBizSahayak } from '../hooks/useBizSahayak';

export const Home = () => {
  const navigate = useNavigate();
  const { setInputData } = useBizSahayak();

  const handleLaunchDemo = () => {
    setInputData({
      location: DEFAULT_DEMO_SCENARIO.location,
      business_category: DEFAULT_DEMO_SCENARIO.business_category,
      available_capital: DEFAULT_DEMO_SCENARIO.available_capital,
    });
    navigate('/business-input');
  };

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="text-center max-w-3xl mx-auto pt-4 sm:pt-8 space-y-6">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-100/80 border border-emerald-200 text-emerald-900 text-xs font-bold">
          <Sparkles className="w-3.5 h-3.5 text-emerald-700" />
          <span>SIH26091 — Rural Micro-Entrepreneur Empowerment</span>
        </div>

        <h1 className="text-3xl sm:text-5xl font-black text-slate-900 tracking-tight leading-tight">
          From Business Idea <span className="text-emerald-800">→</span> Business Insight{' '}
          <span className="text-emerald-800">→</span>{' '}
          <span className="text-amber-600">Financial Plan</span>
        </h1>

        <p className="text-base sm:text-lg text-slate-600 leading-relaxed">
          BizSahayak bridges the gap for rural micro-entrepreneurs by turning localized
          market intuition into bank-ready financial structuring, automatic scheme routing,
          and transparent repayment schedules.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
          <Button
            variant="primary"
            size="lg"
            onClick={() => navigate('/business-input')}
            icon={ArrowRight}
            className="w-full sm:w-auto"
          >
            Start Business Advisory
          </Button>

          <Button
            variant="outline"
            size="lg"
            onClick={handleLaunchDemo}
            className="w-full sm:w-auto"
          >
            Load Anand, Gujarat Demo
          </Button>
        </div>
      </section>

      {/* Default Demo Scenario Callout */}
      <section className="max-w-4xl mx-auto">
        <Card
          className="border-emerald-200 bg-gradient-to-br from-emerald-50/70 via-white to-amber-50/40"
          title="Featured Benchmark Scenario"
          badge={
            <Badge variant="primary" size="sm">
              Default SIH Demo
            </Badge>
          }
        >
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-1">
            <div className="bg-white p-4 rounded-xl border border-slate-200">
              <span className="text-xs text-slate-500 font-semibold block uppercase">
                Location
              </span>
              <span className="text-base font-bold text-slate-800">
                {DEFAULT_DEMO_SCENARIO.location}
              </span>
            </div>
            <div className="bg-white p-4 rounded-xl border border-slate-200">
              <span className="text-xs text-slate-500 font-semibold block uppercase">
                Category
              </span>
              <span className="text-base font-bold text-slate-800">
                {DEFAULT_DEMO_SCENARIO.business_category}
              </span>
            </div>
            <div className="bg-white p-4 rounded-xl border border-slate-200">
              <span className="text-xs text-slate-500 font-semibold block uppercase">
                Margin Capital
              </span>
              <span className="text-base font-bold text-emerald-800">
                {formatCurrency(DEFAULT_DEMO_SCENARIO.available_capital)}
              </span>
            </div>
          </div>

          <div className="mt-4 pt-4 border-t border-slate-200/80 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs text-slate-600">
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-700" />
              Routes deterministically to{' '}
              <strong className="text-slate-800">
                {DEFAULT_DEMO_SCENARIO.scheme_name} (₹10 Lakh Project)
              </strong>
            </span>
            <Button
              variant="subtle"
              size="sm"
              onClick={handleLaunchDemo}
              icon={ArrowRight}
            >
              Analyze This Scenario
            </Button>
          </div>
        </Card>
      </section>

      {/* 3 Pillars of BizSahayak */}
      <section className="max-w-5xl mx-auto">
        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">
            How BizSahayak Works for You
          </h2>
          <p className="text-sm text-slate-500 mt-1">
            Deterministic financial models combined with transparent local insights
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="hover:border-emerald-300">
            <div className="w-12 h-12 rounded-xl bg-emerald-100 text-emerald-800 flex items-center justify-center mb-4">
              <Compass className="w-6 h-6" />
            </div>
            <h3 className="text-base font-bold text-slate-900 mb-2">
              1. Hyper-Local Market Insights
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Understand customer reach radius, competition clusters, opportunity
              matrices, and recommended product pricing tailored to your geography.
            </p>
          </Card>

          <Card className="hover:border-amber-300">
            <div className="w-12 h-12 rounded-xl bg-amber-100 text-amber-800 flex items-center justify-center mb-4">
              <Calculator className="w-6 h-6" />
            </div>
            <h3 className="text-base font-bold text-slate-900 mb-2">
              2. Deterministic Financial Engine
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Calculates 10% margin project sizing, 90% loan eligibility, Micro Finance vs
              Term Loan routing, exact monthly EMIs, and moratorium periods.
            </p>
          </Card>

          <Card className="hover:border-emerald-300">
            <div className="w-12 h-12 rounded-xl bg-sky-100 text-sky-800 flex items-center justify-center mb-4">
              <FileCheck2 className="w-6 h-6" />
            </div>
            <h3 className="text-base font-bold text-slate-900 mb-2">
              3. Bank-Ready Business Plan
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Generates a transparent, plain-language business summary with complete
              amortization schedules and working capital requirements for credit appraisal.
            </p>
          </Card>
        </div>
      </section>
    </div>
  );
};

export default Home;
