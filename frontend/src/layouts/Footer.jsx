import React from 'react';
import { ShieldCheck, Info } from 'lucide-react';
import { useTranslation } from '../context/LanguageContext';

export const Footer = () => {
  const { t } = useTranslation();

  return (
    <footer className="bg-white border-t border-slate-200 mt-auto py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        {/* Mandatory Financial Disclaimer Banner */}
        <div className="bg-amber-50/70 border border-amber-200/80 rounded-2xl p-4 mb-6 flex items-start gap-3">
          <Info className="w-5 h-5 text-amber-700 shrink-0 mt-0.5" />
          <div className="text-xs text-amber-900 leading-relaxed">
            <span className="font-bold">{t('financial.footerDisclaimerTitle')}</span>
            {t('financial.footerDisclaimerText')}
          </div>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
          <div className="flex items-center gap-2">
            <span className="font-bold text-slate-700">{t('nav.appName')}</span>
            <span>•</span>
            <span>SIH26091 — Rural Micro-Entrepreneur Advisory & Financial Structuring</span>
          </div>
          <div className="flex items-center gap-1.5 text-slate-600">
            <ShieldCheck className="w-4 h-4 text-emerald-700" />
            <span>{t('financial.deterministicBadge')} • Government Priority Credit</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
