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
import {
  BUSINESS_CATEGORIES as FULL_CATEGORIES,
  getCategoryByValue,
  getSectors,
} from '../data/categoriesConfig';
import LocationAutocomplete from '../components/LocationAutocomplete';
import { searchLocations, createLocationModel } from '../data/locationService';
import { formatCurrency } from '../utils/formatters';
import { useBizSahayak } from '../hooks/useBizSahayak';
import { useTranslation } from '../context/LanguageContext';

export const BusinessInput = () => {
  const navigate = useNavigate();
  const { inputData, setInputData, updateInputData } = useBizSahayak();
  const { t, getCategoryLabel } = useTranslation();

  const [location, setLocation] = useState(inputData.location || '');
  const [selectedLocation, setSelectedLocation] = useState(inputData.location_detail || null);
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
    setSelectedLocation(createLocationModel({
      raw_input: "Anand, Gujarat",
      village_town_city: "Anand",
      taluka_subdistrict: "Anand Taluka",
      district: "Anand",
      state: "Gujarat",
      country: "India",
      latitude: 22.5645,
      longitude: 72.9289,
      formatted_address: "Anand, Anand Taluka, Anand, Gujarat, India",
      provider: "local_catalog",
    }));
    setCategory(DEFAULT_DEMO_SCENARIO.business_category);
    setCapital(DEFAULT_DEMO_SCENARIO.available_capital);
    setErrors({});
  };


  // Form Validation
  const validateForm = () => {
    const newErrors = {};

    if (!location || !location.trim()) {
      newErrors.location = t('input.errors.locationRequired');
    }

    if (!category || !category.trim()) {
      newErrors.category = t('input.errors.categoryRequired');
    }

    if (capital === '' || capital === null || capital === undefined) {
      newErrors.capital = t('input.errors.capitalRequired');
    } else if (isNaN(numericCapital) || numericCapital <= 0) {
      newErrors.capital = t('input.errors.capitalPositive');
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
      location_detail: selectedLocation,
    };

    updateInputData(preparedPayload);

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

  // Map category options across all 31 supported categories with localized display labels
  const categoryOptions = FULL_CATEGORIES.map((cat) => ({
    value: cat.value,
    label: `${cat.icon} ${getCategoryLabel(cat.value)}`,
  }));

  const selectedCategoryMeta = getCategoryByValue(category);

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      {/* Page Header */}
      <SectionHeader
        title={t('input.headerTitle')}
        subtitle={t('input.headerSubtitle')}
        icon={Store}
        badge={
          <Badge variant="primary" size="md">
            {t('input.stepBadge')}
          </Badge>
        }
        action={
          <Button
            variant="outline"
            size="sm"
            onClick={handleResetToDemo}
            icon={RotateCcw}
          >
            {t('input.loadDemoBtn')}
          </Button>
        }
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        {/* Form Container (2 cols) */}
        <div className="lg:col-span-2">
          <Card>
            <form onSubmit={handleSubmit} className="space-y-6" noValidate>
              {/* 1. Location Autocomplete */}
              <div>
                <LocationAutocomplete
                  id="location-autocomplete"
                  value={location}
                  onChange={(e) => {
                    setLocation(e.target.value);
                    if (errors.location) setErrors((prev) => ({ ...prev, location: null }));
                  }}
                  onLocationSelect={(locModel) => {
                    setSelectedLocation(locModel);
                    if (locModel) {
                      setLocation(locModel.formatted_address || locModel.raw_input);
                    }
                    if (errors.location) setErrors((prev) => ({ ...prev, location: null }));
                  }}
                  selectedLocation={selectedLocation}
                  error={errors.location}
                />

                {/* Popular Location Suggestions */}
                <div className="mt-2.5 flex items-center gap-1.5 flex-wrap">
                  <span className="text-[11px] text-slate-500 font-semibold">
                    {t('input.quickSuggestions', 'Quick Hubs:')}
                  </span>
                  {POPULAR_LOCATIONS.map((loc) => (
                    <button
                      key={loc}
                      type="button"
                      onClick={async () => {
                        const results = await searchLocations(loc, 1);
                        if (results && results.length > 0) {
                          setSelectedLocation(results[0]);
                          setLocation(results[0].formatted_address);
                        } else {
                          setLocation(loc);
                        }
                        if (errors.location) setErrors((prev) => ({ ...prev, location: null }));
                      }}
                      className={`text-xs px-2.5 py-1 rounded-lg border transition-colors cursor-pointer ${
                        location.includes(loc.split(',')[0])
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
                  label={t('input.categoryLabel')}
                  id="category-select"
                  placeholder={t('input.categoryPlaceholder')}
                  options={categoryOptions}
                  value={category}
                  onChange={(e) => {
                    setCategory(e.target.value);
                    if (errors.category) setErrors((prev) => ({ ...prev, category: null }));
                  }}
                  error={errors.category}
                  helper={t('input.categoryHelper')}
                />

                {/* Rich Category Preview Card */}
                {selectedCategoryMeta && (
                  <div className="mt-3 p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-2 animate-fadeIn">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                        <span className="text-base">{selectedCategoryMeta.icon}</span>
                        {getCategoryLabel(selectedCategoryMeta.value)}
                      </span>
                      <span className="text-[11px] bg-primary-100 text-primary-800 px-2 py-0.5 rounded-full font-medium">
                        {selectedCategoryMeta.sector}
                      </span>
                    </div>

                    <div className="text-xs text-slate-600 flex items-center gap-2">
                      <span className="font-semibold text-slate-500">Typical Capex:</span>
                      <span className="font-bold text-emerald-700">
                        ₹{selectedCategoryMeta.typicalCapexMin.toLocaleString('en-IN')} – ₹{selectedCategoryMeta.typicalCapexMax.toLocaleString('en-IN')}
                      </span>
                    </div>

                    <div className="flex items-center gap-1.5 flex-wrap pt-1">
                      <span className="text-[10px] text-slate-400 font-semibold uppercase">Sub-trades:</span>
                      {selectedCategoryMeta.subcategories.map((sub) => (
                        <span
                          key={sub}
                          className="text-[10px] bg-white border border-slate-200 text-slate-600 px-1.5 py-0.5 rounded"
                        >
                          {sub}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>


              {/* 3. Available Margin Capital */}
              <div>
                <Input
                  label={t('input.capitalLabel')}
                  id="capital-input"
                  type="number"
                  min="1"
                  step="500"
                  placeholder={t('input.capitalPlaceholder')}
                  prefix="₹"
                  value={capital}
                  onChange={(e) => {
                    setCapital(e.target.value);
                    if (errors.capital) setErrors((prev) => ({ ...prev, capital: null }));
                  }}
                  error={errors.capital}
                  helper={t('input.capitalHelper')}
                />

                {/* Boundary condition presets */}
                <div className="mt-2.5 space-y-1.5">
                  <span className="text-[11px] text-slate-500 font-semibold block">
                    {t('input.quickCapitalPresets')}
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
                      {t('input.boundary14k')}
                    </button>
                    <button
                      type="button"
                      onClick={() => handlePresetCapital(14001)}
                      className="text-xs px-2.5 py-1 rounded-lg bg-amber-50 text-amber-800 border border-amber-200 hover:bg-amber-100 font-medium cursor-pointer"
                    >
                      {t('input.boundary14001')}
                    </button>
                    <button
                      type="button"
                      onClick={() => handlePresetCapital(100000)}
                      className="text-xs px-2.5 py-1 rounded-lg bg-emerald-700 text-white font-semibold hover:bg-emerald-800 cursor-pointer shadow-2xs"
                    >
                      {t('input.demoPreset')}
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
                  {isSubmitting ? t('input.submittingBtn') : t('input.submitBtn')}
                </Button>
              </div>
            </form>
          </Card>
        </div>

        {/* Summary Card Before Submission (1 col) */}
        <div className="space-y-4">
          <Card
            title={t('input.summaryCardTitle')}
            subtitle={t('input.summaryCardSubtitle')}
            badge={
              <Badge
                variant={isFormComplete ? 'success' : 'default'}
                size="sm"
              >
                {isFormComplete ? t('input.statusReady') : t('input.statusIncomplete')}
              </Badge>
            }
          >
            <div className="space-y-4 text-xs">
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
                <span className="text-slate-500 font-medium block">{t('input.summaryLocation')}</span>
                <span className="font-bold text-slate-800 text-sm block">
                  {location.trim() || t('input.summaryLocationEmpty')}
                </span>
                {selectedLocation && selectedLocation.district && (
                  <span className="text-[11px] text-emerald-700 font-medium block">
                    📍 {selectedLocation.taluka_subdistrict ? `${selectedLocation.taluka_subdistrict}, ` : ''}{selectedLocation.district} ({selectedLocation.state})
                  </span>
                )}
              </div>

              <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
                <span className="text-slate-500 font-medium block">{t('input.summaryCategory')}</span>
                <span className="font-bold text-slate-800 text-sm block flex items-center gap-1.5">
                  {category ? (
                    <>
                      {selectedCategoryMeta && <span>{selectedCategoryMeta.icon}</span>}
                      {getCategoryLabel(category)}
                    </>
                  ) : (
                    t('input.summaryCategoryEmpty')
                  )}
                </span>
                {selectedCategoryMeta && (
                  <span className="text-[11px] text-primary-700 font-medium block">
                    🏷️ {selectedCategoryMeta.sector}
                  </span>
                )}
              </div>


              <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
                <span className="text-slate-500 font-medium block">{t('input.summaryCapital')}</span>
                <span className="font-bold text-emerald-800 text-sm block">
                  {!isNaN(numericCapital) && numericCapital > 0
                    ? formatCurrency(numericCapital)
                    : t('input.summaryCapitalEmpty')}
                </span>
              </div>

              <div className="p-3.5 bg-emerald-50/70 rounded-xl border border-emerald-200 text-slate-700 space-y-1.5">
                <div className="flex items-center gap-1.5 font-bold text-emerald-950 text-xs">
                  <Sparkles className="w-4 h-4 text-emerald-700 shrink-0" />
                  {t('input.whatNextTitle')}
                </div>
                <p className="text-[11px] text-slate-600 leading-relaxed">
                  {t('input.whatNextDesc')}
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
