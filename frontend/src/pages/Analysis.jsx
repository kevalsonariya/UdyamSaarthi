import React, { useState } from 'react';
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
} from 'lucide-react';
import {
  Button,
  Card,
  Badge,
  SectionHeader,
  StatCard,
} from '../components/common';
import { useBizSahayak } from '../hooks/useBizSahayak';
import { formatCurrency } from '../utils/formatters';

export const Analysis = () => {
  const navigate = useNavigate();
  const { inputData } = useBizSahayak();

  const [activeTab, setActiveTab] = useState('overview');

  // Location and business context
  const location = inputData.location || 'Anand, Gujarat';
  const category = inputData.business_category || 'Textile & Clothing';
  const capital = inputData.available_capital || 100000;

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      {/* Header */}
      <SectionHeader
        title={`Hyper-Local Advisory: ${category}`}
        subtitle={`Feasibility, market reach, SWOT, and competitive dynamics evaluated for ${location}.`}
        icon={Compass}
        badge={
          <Badge variant="primary" size="md">
            Step 2 of 4
          </Badge>
        }
        action={
          <Button
            variant="primary"
            size="md"
            onClick={() => navigate('/financial')}
            icon={ArrowRight}
          >
            Proceed to Financial Plan
          </Button>
        }
      />

      {/* Prototype Notice */}
      <div className="bg-amber-50/70 border border-amber-200 rounded-xl px-4 py-2.5 flex items-center gap-2 text-xs text-amber-900">
        <Info className="w-4 h-4 text-amber-700 shrink-0" />
        <span>
          <strong>Prototype Data Notice:</strong> Market reach, competitor density, and pricing benchmarks are simulated for demonstration purposes.
        </span>
      </div>

      {/* Top Level Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          label="Feasibility Score"
          value="82 / 100"
          subtext="High feasibility in Anand cluster"
          variant="primary"
          icon={TrendingUp}
        />
        <StatCard
          label="Market Catchment"
          value="18,500+"
          subtext="Estimated 12 km rural-peri-urban radius"
          variant="secondary"
          icon={Users}
        />
        <StatCard
          label="Local Competition"
          value="Moderate"
          subtext="4 established apparel micro-units"
          variant="info"
          icon={Target}
        />
        <StatCard
          label="Risk Assessment"
          value="Low to Medium"
          subtext="Working capital cycle & seasonal peaks"
          variant="default"
          icon={AlertTriangle}
        />
      </div>

      {/* Section 1: Market Reach & Catchment */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card title="Market Reach & Demographics" subtitle={`Spatial catchment around ${location}`}>
          <div className="space-y-4">
            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
              <div className="flex justify-between items-center text-xs font-semibold text-slate-500 mb-1">
                <span>Primary Catchment Radius</span>
                <span className="text-emerald-800 font-bold">0 - 7 km</span>
              </div>
              <p className="text-xs text-slate-700 leading-relaxed">
                Dense village clusters, weekly haats (bazaars), and local institutions generating regular household apparel demand.
              </p>
            </div>

            <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
              <div className="flex justify-between items-center text-xs font-semibold text-slate-500 mb-1">
                <span>Secondary Catchment Radius</span>
                <span className="text-amber-700 font-bold">7 - 18 km</span>
              </div>
              <p className="text-xs text-slate-700 leading-relaxed">
                Neighboring talukas and highway connectivity providing institutional orders (school uniforms, festival bulk wear).
              </p>
            </div>

            <div className="p-3.5 bg-emerald-50/60 rounded-xl border border-emerald-100 flex items-center justify-between text-xs">
              <span className="font-semibold text-emerald-900">Estimated Target Customer Base:</span>
              <span className="font-bold text-emerald-800 text-sm">~4,200 households</span>
            </div>
          </div>
        </Card>

        {/* Section 2: Opportunity Analysis */}
        <Card title="Opportunity Analysis" subtitle="Key drivers favoring this micro-enterprise">
          <div className="space-y-3">
            {[
              {
                title: 'Festive & Wedding Season Demand',
                desc: 'High seasonal surge in demand for ethnic readymade garments with 30-40% margin potential.',
              },
              {
                title: 'Proximity to Textile Supply Hubs',
                desc: 'Access to Ahmedabad and Surat fabric wholesale markets reduces procurement lead times.',
              },
              {
                title: 'Rising Demand for Custom Tailoring',
                desc: 'Rural consumers prefer durable, locally tailored everyday wear over high-priced metro brands.',
              },
            ].map((item, idx) => (
              <div key={idx} className="flex items-start gap-3 p-3 rounded-xl bg-slate-50 border border-slate-100">
                <CheckCircle2 className="w-4 h-4 text-emerald-700 shrink-0 mt-0.5" />
                <div>
                  <h4 className="text-xs font-bold text-slate-800">{item.title}</h4>
                  <p className="text-xs text-slate-500 mt-0.5 leading-relaxed">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* Section 3: SWOT Matrix */}
      <Card title="SWOT Analysis" subtitle="Detailed situational matrix for rural operations">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Strengths */}
          <div className="p-4 rounded-xl bg-emerald-50/60 border border-emerald-200">
            <div className="flex items-center gap-2 mb-2">
              <Badge variant="success" size="sm">Strengths</Badge>
            </div>
            <ul className="text-xs text-slate-700 space-y-1.5 list-disc list-inside">
              <li>Low overhead cost relative to urban retail counterparts.</li>
              <li>Strong direct relationships with local community and customers.</li>
              <li>Flexibility to offer personalized alterations and fast turnaround.</li>
            </ul>
          </div>

          {/* Weaknesses */}
          <div className="p-4 rounded-xl bg-amber-50/60 border border-amber-200">
            <div className="flex items-center gap-2 mb-2">
              <Badge variant="secondary" size="sm">Weaknesses</Badge>
            </div>
            <ul className="text-xs text-slate-700 space-y-1.5 list-disc list-inside">
              <li>Limited initial working capital for bulk fabric stocking.</li>
              <li>Dependence on manual machinery in early phases.</li>
              <li>Lack of structured digital bookkeeping habits.</li>
            </ul>
          </div>

          {/* Opportunities */}
          <div className="p-4 rounded-xl bg-sky-50/60 border border-sky-200">
            <div className="flex items-center gap-2 mb-2">
              <Badge variant="info" size="sm">Opportunities</Badge>
            </div>
            <ul className="text-xs text-slate-700 space-y-1.5 list-disc list-inside">
              <li>Partnerships with local schools and village cooperatives for uniforms.</li>
              <li>Utilizing government subsidized credit schemes with moratorium benefits.</li>
              <li>WhatsApp-based cataloging for nearby village customers.</li>
            </ul>
          </div>

          {/* Threats */}
          <div className="p-4 rounded-xl bg-red-50/60 border border-red-200">
            <div className="flex items-center gap-2 mb-2">
              <Badge variant="danger" size="sm">Threats & Risks</Badge>
            </div>
            <ul className="text-xs text-slate-700 space-y-1.5 list-disc list-inside">
              <li>Fluctuations in cotton raw material and fabric wholesale prices.</li>
              <li>Cheap synthetic garment imports in weekly markets.</li>
              <li>Extended credit requests from local customers during harvest gaps.</li>
            </ul>
          </div>
        </div>
      </Card>

      {/* Section 4: Competitor Mapping & Pricing Guidance */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Competitor Mapping */}
        <Card title="Competitor Mapping" subtitle="Identified competitors within 10 km radius">
          <div className="space-y-3">
            {[
              {
                name: 'Kisan Readymade Stores',
                type: 'Traditional Retailer',
                strength: 'Established location',
                pricePoint: '₹350 - ₹900',
              },
              {
                name: 'Anand Tailoring Center',
                type: 'Job-work Tailor',
                strength: 'Skilled stitching',
                pricePoint: '₹150 - ₹400',
              },
              {
                name: 'Weekly Haat Vendors',
                type: 'Informal Mobile Stalls',
                strength: 'Low price points',
                pricePoint: '₹120 - ₹300',
              },
            ].map((comp, idx) => (
              <div key={idx} className="p-3 bg-slate-50 rounded-xl border border-slate-200 flex items-center justify-between">
                <div>
                  <h4 className="text-xs font-bold text-slate-800">{comp.name}</h4>
                  <span className="text-[11px] text-slate-500">{comp.type} • {comp.strength}</span>
                </div>
                <div className="text-right">
                  <span className="text-xs font-semibold text-emerald-800">{comp.pricePoint}</span>
                </div>
              </div>
            ))}
          </div>
        </Card>

        {/* Pricing Guidance */}
        <Card title="Pricing & Margin Guidance" subtitle="Recommended pricing for sustainable unit economics">
          <div className="space-y-3 text-xs">
            <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
              <span className="font-semibold text-slate-700">Cotton Everyday Shirts / Kurta</span>
              <span className="font-bold text-emerald-800">MRP ₹450 (Cost: ₹280 | Margin: 38%)</span>
            </div>
            <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
              <span className="font-semibold text-slate-700">School Uniform Set (Stitched)</span>
              <span className="font-bold text-emerald-800">MRP ₹650 (Cost: ₹420 | Margin: 35%)</span>
            </div>
            <div className="flex justify-between items-center p-2.5 bg-slate-50 rounded-xl border border-slate-200">
              <span className="font-semibold text-slate-700">Custom Alteration & Tailoring</span>
              <span className="font-bold text-emerald-800">Fee ₹180 (Cost: ₹50 | Margin: 72%)</span>
            </div>

            <div className="p-3 bg-amber-50 rounded-xl border border-amber-200 text-amber-900 mt-2">
              <span className="font-bold">Pricing Recommendation: </span>
              Position between cheap weekly haat vendors and urban town showrooms to balance volume with healthy cash margins.
            </div>
          </div>
        </Card>
      </div>

      {/* Navigation Footer */}
      <div className="flex items-center justify-between pt-4 border-t border-slate-200">
        <Button variant="ghost" onClick={() => navigate('/business-input')}>
          ← Back to Business Input
        </Button>
        <Button
          variant="primary"
          size="lg"
          onClick={() => navigate('/financial')}
          icon={ArrowRight}
        >
          Next: Financial Structuring & Scheme Selection
        </Button>
      </div>
    </div>
  );
};

export default Analysis;
