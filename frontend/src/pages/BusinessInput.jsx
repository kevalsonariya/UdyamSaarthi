import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  MapPin,
  Store,
  Banknote,
  ArrowRight,
  RotateCcw,
  CheckCircle2,
  FileCheck,
  AlertCircle,
  Sparkles,
} from 'lucide-react';
import {
  Button,
  Card,
  Input,
  Select,
  SectionHeader,
  Badge,
} from '../components/common';
import {
  BUSINESS_CATEGORIES,
  POPULAR_LOCATIONS,
  DEFAULT_DEMO_SCENARIO,
} from '../data/defaultData';
import { formatCurrency } from '../utils/formatters';
import { useBizSahayak } from '../hooks/useBizSahayak';

export const BusinessInput = () => {
  const navigate = useNavigate();
  const { inputData, setInputData } = useBizSahayak();

  const [location, setLocation] = useState(inputData.location || '');
  const [category, setCategory] = useState(inputData.business_category || '');
  const [capital, setCapital] = useState(inputData.available_capital || '');
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Capital parsing
  const numericCapital = Number(capital);

  // Quick preset chips for boundary conditions & demo
  const handlePresetCapital = (amount) => {
    setCapital(amount);
    if (errors.capital) {
      setErrors((prev) => ({ ...prev, capital: null }));
    }
  };

  const handleResetToDemo = () => {
    setLocation(DEFAULT_DEMO_SCENARIO.location);
    setCategory(DEFAULT_DEMO_SCENARIO.business_category);
    setCapital(DEFAULT_DEMO_SCENARIO.available_capital);
    setErrors({});
  };

  // Form Validation
  const validateForm = () => {
    const newErrors = {};

    if (!location || !location.trim()) {
      newErrors.location = 'Location is required. Please specify your town, district, or region.';
    }

    if (!category || !category.trim()) {
      newErrors.category = 'Business category is required. Please select a category.';
    }

    if (capital === '' || capital === null || capital === undefined) {
      newErrors.capital = 'Available margin capital is required.';
    } else if (isNaN(numericCapital) || numericCapital <= 0) {
      newErrors.capital = 'Available capital must be a valid amount greater than ₹0.';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    // Save into shared frontend state for downstream analysis & financial screens
    const preparedPayload = {
      location: location.trim(),
      business_category: category.trim(),
      available_capital: numericCapital,
    };

    setInputData(preparedPayload);

    // Smooth navigation transition
    setTimeout(() => {
      setIsSubmitting(false);
      navigate('/analysis');
    }, 400);
  };

  const isFormComplete =
    location.trim().length > 0 &&
    category.trim().length > 0 &&
    !isNaN(numericCapital) &&
    numericCapital > 0;

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      {/* Page Header */}
      <SectionHeader
        title="Business Profile & Margin Capital"
        subtitle="Enter your enterprise details and available promoter contribution to begin hyper-local feasibility and financial structuring."
        icon={Store}
        badge={
          <Badge variant="primary" size="md">
            Step 1 of 4 • Input
          </Badge>
        }
        action={
          <Button
            variant="outline"
            size="sm"
            onClick={handleResetToDemo}
            icon={RotateCcw}
          >
            Load Anand Demo
          </Button>
        }
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        {/* Form Container (2 cols) */}
        <div className="lg:col-span-2">
          <Card>
            <form onSubmit={handleSubmit} className="space-y-6" noValidate>
              {/* 1. Location */}
              <div>
                <Input
                  label="1. Geographic Location"
                  id="location-input"
                  placeholder="e.g. Anand, Gujarat"
                  value={location}
                  onChange={(e) => {
                    setLocation(e.target.value);
                    if (errors.location) setErrors((prev) => ({ ...prev, location: null }));
                  }}
                  icon={MapPin}
                  error={errors.location}
                  helper="Enter the village, town, district, or state where you plan to establish the business."
                />

                {/* Popular Location Suggestions */}
                <div className="mt-2.5 flex items-center gap-1.5 flex-wrap">
                  <span className="text-[11px] text-slate-500 font-semibold">
                    Quick suggestions:
                  </span>
                  {POPULAR_LOCATIONS.map((loc) => (
                    <button
                      key={loc}
                      type="button"
                      onClick={() => {
                        setLocation(loc);
                        if (errors.location) setErrors((prev) => ({ ...prev, location: null }));
                      }}
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

              {/* 2. Business Category */}
              <div>
                <Select
                  label="2. Business Category"
                  id="category-select"
                  placeholder="Select proposed business category"
                  options={BUSINESS_CATEGORIES}
                  value={category}
                  onChange={(e) => {
                    setCategory(e.target.value);
                    if (errors.category) setErrors((prev) => ({ ...prev, category: null }));
                  }}
                  error={errors.category}
                  helper="Choose the industry sector closest to your proposed micro-enterprise."
                />
              </div>

              {/* 3. Available Margin Capital */}
              <div>
                <Input
                  label="3. Available Margin Capital (INR)"
                  id="capital-input"
                  type="number"
                  min="1"
                  step="500"
                  placeholder="100000"
                  prefix="₹"
                  value={capital}
                  onChange={(e) => {
                    setCapital(e.target.value);
                    if (errors.capital) setErrors((prev) => ({ ...prev, capital: null }));
                  }}
                  error={errors.capital}
                  helper="Your self-financed promoter margin contribution in Indian Rupees (INR)."
                />

                {/* Boundary condition presets */}
                <div className="mt-2.5 space-y-1.5">
                  <span className="text-[11px] text-slate-500 font-semibold block">
                    Quick capital presets (Boundary testing):
                  </span>
                  <div className="flex items-center gap-2 flex-wrap">
                    <button
                      type="button"
                      onClick={() => handlePresetCapital(10000)}
                      className="text-xs px-2.5 py-1 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200 hover:bg-emerald-100 font-medium cursor-pointer"
                    >
                      ₹10,000
                    </button>
                    <button
                      type="button"
                      onClick={() => handlePresetCapital(14000)}
                      className="text-xs px-2.5 py-1 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200 hover:bg-emerald-100 font-medium cursor-pointer"
                    >
                      ₹14,000 (Boundary)
                    </button>
                    <button
                      type="button"
                      onClick={() => handlePresetCapital(14001)}
                      className="text-xs px-2.5 py-1 rounded-lg bg-amber-50 text-amber-800 border border-amber-200 hover:bg-amber-100 font-medium cursor-pointer"
                    >
                      ₹14,001 (Boundary)
                    </button>
                    <button
                      type="button"
                      onClick={() => handlePresetCapital(100000)}
                      className="text-xs px-2.5 py-1 rounded-lg bg-emerald-700 text-white font-semibold hover:bg-emerald-800 cursor-pointer shadow-2xs"
                    >
                      ₹1,00,000 (Demo Default)
                    </button>
                  </div>
                </div>
              </div>

              {/* Submit CTA */}
              <div className="pt-2">
                <Button
                  type="submit"
                  variant="primary"
                  size="lg"
                  loading={isSubmitting}
                  icon={ArrowRight}
                  className="w-full text-base py-3 font-bold"
                >
                  Generate Business Analysis
                </Button>
              </div>
            </form>
          </Card>
        </div>

        {/* Summary Card Before Submission (1 col) */}
        <div className="space-y-4">
          <Card
            title="Profile Summary"
            subtitle="Verify your inputs before generation"
            badge={
              <Badge
                variant={isFormComplete ? 'success' : 'default'}
                size="sm"
              >
                {isFormComplete ? 'Ready' : 'Incomplete'}
              </Badge>
            }
          >
            <div className="space-y-4 text-xs">
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
                <span className="text-slate-500 font-medium block">Location</span>
                <span className="font-bold text-slate-800 text-sm block">
                  {location.trim() || '— Not specified yet —'}
                </span>
              </div>

              <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
                <span className="text-slate-500 font-medium block">Enterprise Category</span>
                <span className="font-bold text-slate-800 text-sm block">
                  {category || '— Not selected yet —'}
                </span>
              </div>

              <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
                <span className="text-slate-500 font-medium block">Margin Capital</span>
                <span className="font-bold text-emerald-800 text-sm block">
                  {!isNaN(numericCapital) && numericCapital > 0
                    ? formatCurrency(numericCapital)
                    : '— Awaiting INR input —'}
                </span>
              </div>

              <div className="p-3.5 bg-emerald-50/70 rounded-xl border border-emerald-200 text-slate-700 space-y-1.5">
                <div className="flex items-center gap-1.5 font-bold text-emerald-950 text-xs">
                  <Sparkles className="w-4 h-4 text-emerald-700 shrink-0" />
                  What happens next?
                </div>
                <p className="text-[11px] text-slate-600 leading-relaxed">
                  Upon clicking <strong>"Generate Business Analysis"</strong>, your inputs will be evaluated for local feasibility, SWOT, and risk, followed by deterministic loan sizing and scheme routing on the next pages.
                </p>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default BusinessInput;
