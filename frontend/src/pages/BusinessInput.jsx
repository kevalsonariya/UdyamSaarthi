import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  MapPin,
  Banknote,
  Store,
  ArrowRight,
  Info,
  CheckCircle,
  Sparkles,
  RotateCcw,
} from 'lucide-react';
import {
  Button,
  Card,
  Input,
  Select,
  SectionHeader,
  Badge,
  StatCard,
} from '../components/common';
import {
  BUSINESS_CATEGORIES,
  POPULAR_LOCATIONS,
  DEFAULT_DEMO_SCENARIO,
} from '../data/defaultData';
import { formatCurrency, formatLakhs } from '../utils/formatters';
import { useBizSahayak } from '../hooks/useBizSahayak';

export const BusinessInput = () => {
  const navigate = useNavigate();
  const { inputData, setInputData, resetToDemoScenario } = useBizSahayak();

  const [location, setLocation] = useState(inputData.location || '');
  const [category, setCategory] = useState(inputData.business_category || '');
  const [capital, setCapital] = useState(inputData.available_capital || 100000);
  const [errors, setErrors] = useState({});

  // Deterministic preview calculation (Rules: Project Cost = Capital / 10%, Max Loan = 90%)
  const numericCapital = Number(capital) || 0;
  const projectCost = numericCapital > 0 ? numericCapital / 0.1 : 0;
  const maxLoan = projectCost * 0.9;
  const isMicroFinance = projectCost <= 140000;
  const schemeName = isMicroFinance ? 'Micro Finance Scheme' : 'Term Loan Scheme';
  const interestRate = isMicroFinance ? '6.5%' : '8.0%';
  const tenure = isMicroFinance ? '3 Years' : '7 Years';
  const moratorium = isMicroFinance ? '3 Months' : '6 Months';

  const handlePresetCapital = (amount) => {
    setCapital(amount);
  };

  const handleApplyDefaultScenario = () => {
    setLocation(DEFAULT_DEMO_SCENARIO.location);
    setCategory(DEFAULT_DEMO_SCENARIO.business_category);
    setCapital(DEFAULT_DEMO_SCENARIO.available_capital);
    setErrors({});
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const newErrors = {};

    if (!location.trim()) {
      newErrors.location = 'Please provide a location (e.g. Anand, Gujarat)';
    }
    if (!category.trim()) {
      newErrors.category = 'Please choose a business category';
    }
    if (!numericCapital || numericCapital < 1000) {
      newErrors.capital = 'Minimum margin capital is ₹1,000';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    // Save into state context
    setInputData({
      location: location.trim(),
      business_category: category.trim(),
      available_capital: numericCapital,
    });

    navigate('/analysis');
  };

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      <SectionHeader
        title="Business Profile & Capital Input"
        subtitle="Provide your location, business category, and available margin capital to structure your loan and feasibility insights."
        icon={Store}
        badge={
          <Badge variant="primary" size="md">
            Step 1 of 4
          </Badge>
        }
        action={
          <Button
            variant="outline"
            size="sm"
            onClick={handleApplyDefaultScenario}
            icon={RotateCcw}
          >
            Reset to Anand Demo
          </Button>
        }
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        {/* Input Form (2 cols) */}
        <div className="lg:col-span-2">
          <Card>
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Location Input */}
              <div>
                <Input
                  label="1. Geographic Location (Town / District, State)"
                  id="business-location"
                  placeholder="e.g. Anand, Gujarat"
                  value={location}
                  onChange={(e) => {
                    setLocation(e.target.value);
                    if (errors.location) setErrors({ ...errors, location: null });
                  }}
                  icon={MapPin}
                  error={errors.location}
                  helper="Hyper-local analysis will evaluate nearby rural demand clusters."
                />

                {/* Popular Location Chips */}
                <div className="mt-2.5 flex items-center gap-1.5 flex-wrap">
                  <span className="text-[11px] text-slate-600 font-semibold">
                    Quick suggestions:
                  </span>
                  {POPULAR_LOCATIONS.map((loc) => (
                    <button
                      key={loc}
                      type="button"
                      onClick={() => setLocation(loc)}
                      className={`text-xs px-2.5 py-1 rounded-lg border transition-colors cursor-pointer ${
                        location === loc
                          ? 'bg-emerald-100 text-emerald-900 border-emerald-300 font-bold'
                          : 'bg-slate-50 text-slate-600 border-slate-200 hover:bg-slate-100'
                      }`}
                    >
                      {loc}
                    </button>
                  ))}
                </div>
              </div>

              {/* Business Category */}
              <div>
                <Select
                  label="2. Proposed Business Category"
                  id="business-category"
                  placeholder="Select a category"
                  options={BUSINESS_CATEGORIES}
                  value={category}
                  onChange={(e) => {
                    setCategory(e.target.value);
                    if (errors.category) setErrors({ ...errors, category: null });
                  }}
                  error={errors.category}
                  helper="Select the sector matching your proposed enterprise."
                />
              </div>

              {/* Available Margin Capital */}
              <div>
                <Input
                  label="3. Available Margin Capital (Your Contribution)"
                  id="available-capital"
                  type="number"
                  min="1000"
                  step="500"
                  placeholder="100000"
                  prefix="₹"
                  value={capital}
                  onChange={(e) => {
                    setCapital(e.target.value);
                    if (errors.capital) setErrors({ ...errors, capital: null });
                  }}
                  error={errors.capital}
                  helper="By official guidelines, your capital represents 10% of the total project size."
                />

                {/* Quick boundary condition presets */}
                <div className="mt-2.5 space-y-1.5">
                  <span className="text-[11px] text-slate-600 font-semibold block">
                    Test Scheme Routing Boundary Conditions:
                  </span>
                  <div className="flex items-center gap-2 flex-wrap">
                    <button
                      type="button"
                      onClick={() => handlePresetCapital(10000)}
                      className="text-xs px-2.5 py-1 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200 hover:bg-emerald-100 cursor-pointer font-medium"
                    >
                      ₹10k (Micro: ₹1L Cost)
                    </button>
                    <button
                      type="button"
                      onClick={() => handlePresetCapital(14000)}
                      className="text-xs px-2.5 py-1 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200 hover:bg-emerald-100 cursor-pointer font-medium"
                    >
                      ₹14k (Micro Boundary: ₹1.4L)
                    </button>
                    <button
                      type="button"
                      onClick={() => handlePresetCapital(14001)}
                      className="text-xs px-2.5 py-1 rounded-lg bg-amber-50 text-amber-800 border border-amber-200 hover:bg-amber-100 cursor-pointer font-medium"
                    >
                      ₹14,001 (Term Loan Boundary)
                    </button>
                    <button
                      type="button"
                      onClick={() => handlePresetCapital(100000)}
                      className="text-xs px-2.5 py-1 rounded-lg bg-emerald-700 text-white font-semibold hover:bg-emerald-800 cursor-pointer"
                    >
                      ₹1 Lakh (Demo Default)
                    </button>
                  </div>
                </div>
              </div>

              {/* Submit Button */}
              <div className="pt-2">
                <Button
                  type="submit"
                  variant="primary"
                  size="lg"
                  icon={ArrowRight}
                  className="w-full"
                >
                  Analyze Feasibility & Generate Financial Plan
                </Button>
              </div>
            </form>
          </Card>
        </div>

        {/* Live Calculation Preview Sidebar (1 col) */}
        <div className="space-y-4">
          <Card
            title="Instant Sizing Preview"
            subtitle="Deterministic 10% Margin Rule"
            badge={
              <Badge variant={isMicroFinance ? 'info' : 'primary'} size="sm">
                {schemeName}
              </Badge>
            }
          >
            <div className="space-y-3.5 text-sm">
              <div className="flex justify-between items-center py-1.5 border-b border-slate-100">
                <span className="text-slate-500">Your Margin (10%):</span>
                <span className="font-bold text-slate-800">
                  {formatCurrency(numericCapital)}
                </span>
              </div>

              <div className="flex justify-between items-center py-1.5 border-b border-slate-100">
                <span className="text-slate-500">Total Project Cost:</span>
                <span className="font-extrabold text-emerald-900 text-base">
                  {formatCurrency(projectCost)}
                </span>
              </div>

              <div className="flex justify-between items-center py-1.5 border-b border-slate-100">
                <span className="text-slate-500">Maximum Loan (90%):</span>
                <span className="font-bold text-slate-800">
                  {formatCurrency(maxLoan)}
                </span>
              </div>

              <div className="flex justify-between items-center py-1.5 border-b border-slate-100">
                <span className="text-slate-500">Interest Rate:</span>
                <span className="font-bold text-amber-700">{interestRate} p.a.</span>
              </div>

              <div className="flex justify-between items-center py-1.5 border-b border-slate-100">
                <span className="text-slate-500">Loan Tenure:</span>
                <span className="font-medium text-slate-700">{tenure}</span>
              </div>

              <div className="flex justify-between items-center py-1.5">
                <span className="text-slate-500">Moratorium:</span>
                <span className="font-medium text-slate-700">{moratorium}</span>
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-slate-200 bg-slate-50 -mx-5 -mb-5 p-4 rounded-b-2xl text-[11px] text-slate-500 leading-tight">
              Project sizing is calculated deterministically as Margin / 10% as per official micro-enterprise lending guidelines.
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default BusinessInput;
