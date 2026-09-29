import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { translations, SUPPORTED_LANGUAGES } from '../data/translations';
import { Globe, Check } from 'lucide-react';

const STORAGE_KEY = 'udyamsaarthi_language';

const LanguageContext = createContext(null);

export const LanguageProvider = ({ children }) => {
  const [language, setLanguageState] = useState(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored && ['en', 'hi', 'gu'].includes(stored)) {
        return stored;
      }
    } catch (e) {
      // Local storage not accessible, default to en
    }
    return 'en';
  });

  const setLanguage = useCallback((newLang) => {
    if (['en', 'hi', 'gu'].includes(newLang)) {
      setLanguageState(newLang);
      try {
        localStorage.setItem(STORAGE_KEY, newLang);
      } catch (e) {
        console.warn('Failed to persist language in localStorage', e);
      }
    }
  }, []);

  // Safe nested translation lookup with automatic English fallback and string interpolation
  const t = useCallback(
    (keyPath, params = {}) => {
      if (!keyPath || typeof keyPath !== 'string') return '';

      const keys = keyPath.split('.');

      const resolveValue = (dict) => {
        let current = dict;
        for (const k of keys) {
          if (current && typeof current === 'object' && k in current) {
            current = current[k];
          } else {
            return undefined;
          }
        }
        return typeof current === 'string' ? current : undefined;
      };

      // 1. Try selected language
      let text = resolveValue(translations[language]);

      // 2. Fallback to English if missing
      if (text === undefined && language !== 'en') {
        text = resolveValue(translations.en);
      }

      // 3. Fallback to key itself if not found anywhere (prevents undefined / null in UI)
      if (text === undefined) {
        text = keys[keys.length - 1] || keyPath;
      }

      // 4. Interpolate {paramName} placeholders
      if (params && typeof params === 'object') {
        Object.entries(params).forEach(([k, v]) => {
          text = text.replace(new RegExp(`\\{${k}\\}`, 'g'), String(v ?? ''));
        });
      }

      return text;
    },
    [language]
  );

  // Helper for category display labels (display label != backend value)
  const getCategoryLabel = useCallback(
    (backendCategory) => {
      if (!backendCategory) return '';
      const translated = t(`categories.${backendCategory}`);
      return translated || backendCategory;
    },
    [t]
  );

  return (
    <LanguageContext.Provider
      value={{
        language,
        setLanguage,
        t,
        getCategoryLabel,
        supportedLanguages: SUPPORTED_LANGUAGES,
      }}
    >
      {children}
    </LanguageContext.Provider>
  );
};

export const useTranslation = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useTranslation must be used within a LanguageProvider');
  }
  return context;
};

/**
 * Reusable Language Selector Component
 * Display options: English | हिंदी | ગુજરાતી
 */
export const LanguageSelector = ({ className = '', compact = false }) => {
  const { language, setLanguage, supportedLanguages } = useTranslation();

  return (
    <div
      className={`inline-flex items-center bg-slate-100/90 p-1 rounded-xl border border-slate-200/90 shadow-2xs ${className}`}
      role="group"
      aria-label="Language selector"
    >
      <div className="flex items-center gap-1">
        {supportedLanguages.map((lang) => {
          const isActive = language === lang.code;
          return (
            <button
              key={lang.code}
              type="button"
              onClick={() => setLanguage(lang.code)}
              className={`px-2.5 py-1 text-xs font-bold rounded-lg transition-all cursor-pointer ${
                isActive
                  ? 'bg-emerald-800 text-white shadow-xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-white/60'
              }`}
              title={lang.label}
              aria-pressed={isActive}
            >
              {lang.nativeLabel}
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default LanguageContext;
