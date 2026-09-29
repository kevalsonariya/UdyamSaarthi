import React, { useState, useEffect, useRef } from 'react';
import { useTranslation } from '../context/LanguageContext';
import { searchLocations, createLocationModel } from '../data/locationService';

export default function LocationAutocomplete({
  value = '',
  onChange,
  onLocationSelect,
  selectedLocation = null,
  error = '',
  id = 'location-autocomplete',
}) {
  const { t } = useTranslation();
  const [query, setQuery] = useState(value);
  const [suggestions, setSuggestions] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(-1);
  const containerRef = useRef(null);
  const debounceTimerRef = useRef(null);

  // Sync external value with local query
  useEffect(() => {
    setQuery(value || '');
  }, [value]);

  // Click outside listener to close dropdown
  useEffect(() => {
    function handleClickOutside(event) {
      if (containerRef.current && !containerRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Fetch suggestions with debounce
  const fetchSuggestions = (searchQuery) => {
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }

    debounceTimerRef.current = setTimeout(async () => {
      try {
        const results = await searchLocations(searchQuery, 7);
        setSuggestions(results);
        setIsOpen(true);
        setHighlightedIndex(-1);
      } catch (err) {
        console.error('Location search error:', err);
        setSuggestions([]);
      }
    }, 150);
  };

  const handleInputChange = (e) => {
    const val = e.target.value;
    setQuery(val);
    if (onChange) {
      onChange(e);
    }
    fetchSuggestions(val);
  };

  const handleFocus = () => {
    fetchSuggestions(query);
  };

  const handleSelect = (locModel) => {
    setQuery(locModel.formatted_address || locModel.raw_input);
    setIsOpen(false);

    if (onLocationSelect) {
      onLocationSelect(locModel);
    }
    if (onChange) {
      onChange({ target: { name: 'location', value: locModel.formatted_address } });
    }
  };

  const handleKeyDown = (e) => {
    if (!isOpen || suggestions.length === 0) return;

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setHighlightedIndex((prev) => (prev < suggestions.length - 1 ? prev + 1 : 0));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setHighlightedIndex((prev) => (prev > 0 ? prev - 1 : suggestions.length - 1));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (highlightedIndex >= 0 && highlightedIndex < suggestions.length) {
        handleSelect(suggestions[highlightedIndex]);
      } else if (query.trim()) {
        // Fallback custom model
        const custom = createLocationModel({
          raw_input: query.trim(),
          village_town_city: query.trim(),
          formatted_address: `${query.trim()}, India`,
          provider: 'user_custom',
        });
        handleSelect(custom);
      }
    } else if (e.key === 'Escape') {
      setIsOpen(false);
    }
  };

  const handleClear = () => {
    setQuery('');
    setIsOpen(false);
    if (onLocationSelect) {
      onLocationSelect(null);
    }
    if (onChange) {
      onChange({ target: { name: 'location', value: '' } });
    }
  };

  return (
    <div className="relative w-full" ref={containerRef}>
      <label htmlFor={id} className="block text-sm font-semibold text-slate-800 mb-1.5">
        {t('input.locationLabel', 'Business Location / Operational Catchment')}
        <span className="text-red-500 ml-1">*</span>
      </label>

      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
          <svg className="w-5 h-5 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </div>

        <input
          id={id}
          name="location"
          type="text"
          value={query}
          onChange={handleInputChange}
          onFocus={handleFocus}
          onKeyDown={handleKeyDown}
          autoComplete="off"
          placeholder={t('input.locationSearchPlaceholder', 'Search village, taluka, town, or district (e.g. Anand, Bardoli)...')}
          className={`w-full pl-10 pr-10 py-2.5 bg-white border ${
            error ? 'border-red-400 focus:ring-red-300' : 'border-slate-300 focus:border-primary-500 focus:ring-primary-100'
          } rounded-lg text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-4 transition duration-150 shadow-sm`}
        />

        {query && (
          <button
            type="button"
            onClick={handleClear}
            className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 focus:outline-none"
            title={t('input.changeLocation', 'Clear')}
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>

      {error && <p className="mt-1.5 text-xs font-medium text-red-600">{error}</p>}

      {/* Autocomplete Dropdown */}
      {isOpen && suggestions.length > 0 && (
        <div className="absolute z-50 left-0 right-0 mt-1.5 bg-white rounded-xl shadow-xl border border-slate-200 overflow-hidden max-h-72 overflow-y-auto">
          <div className="px-3 py-2 bg-slate-50 border-b border-slate-100 flex items-center justify-between text-xs text-slate-500 font-medium">
            <span>{t('input.suggestionsTitle', 'Suggested Rural & Regional Centers')}</span>
            <span className="text-[10px] bg-primary-50 text-primary-700 px-1.5 py-0.5 rounded font-semibold">
              {t('input.verifiedCenter', 'Verified Hubs')}
            </span>
          </div>

          <ul className="divide-y divide-slate-100">
            {suggestions.map((loc, idx) => {
              const isSelected = highlightedIndex === idx;
              return (
                <li
                  key={`${loc.village_town_city}-${loc.district || ''}-${idx}`}
                  onClick={() => handleSelect(loc)}
                  onMouseEnter={() => setHighlightedIndex(idx)}
                  className={`px-3.5 py-2.5 cursor-pointer transition-colors duration-100 flex items-start space-x-3 ${
                    isSelected ? 'bg-primary-50 text-primary-900' : 'hover:bg-slate-50 text-slate-800'
                  }`}
                >
                  <div className="mt-0.5 text-primary-600">
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z" />
                    </svg>
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center space-x-2">
                      <span className="font-semibold text-sm text-slate-900 truncate">
                        {loc.village_town_city}
                      </span>
                      {loc.taluka_subdistrict && (
                        <span className="text-[11px] bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded">
                          {loc.taluka_subdistrict}
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-slate-500 truncate mt-0.5">
                      {[loc.district ? `District: ${loc.district}` : '', loc.state, loc.country].filter(Boolean).join(', ')}
                    </p>
                  </div>
                  {loc.provider === 'local_catalog' ? (
                    <span className="text-[10px] text-emerald-600 font-medium bg-emerald-50 px-1.5 py-0.5 rounded self-center">
                      Verified
                    </span>
                  ) : (
                    <span className="text-[10px] text-slate-500 font-medium bg-slate-100 px-1.5 py-0.5 rounded self-center">
                      Custom
                    </span>
                  )}
                </li>
              );
            })}
          </ul>
        </div>
      )}

      {/* Selected Location Metadata Pill Display */}
      {selectedLocation && (
        <div className="mt-2.5 p-2.5 bg-emerald-50 border border-emerald-200 rounded-lg flex items-center justify-between text-xs text-emerald-900 animate-fadeIn">
          <div className="flex items-center space-x-2 truncate">
            <span className="flex-shrink-0 text-emerald-600 font-bold">✓ {t('input.selectedLocation', 'Selected Location')}:</span>
            <span className="font-semibold truncate">
              {selectedLocation.village_town_city || selectedLocation.raw_input}
            </span>
            {selectedLocation.district && (
              <span className="text-[11px] bg-emerald-100 text-emerald-800 px-1.5 py-0.5 rounded font-medium">
                {selectedLocation.district}
              </span>
            )}
            {selectedLocation.state && (
              <span className="text-[11px] text-emerald-700">({selectedLocation.state})</span>
            )}
          </div>
          <span className="text-[10px] text-emerald-600 uppercase tracking-wider font-semibold ml-2">
            Ready
          </span>
        </div>
      )}
    </div>
  );
}
