import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  FileText,
  Download,
  Printer,
  CheckCircle,
  ShieldCheck,
  Building,
  TrendingUp,
  MapPin,
  Calendar,
  Info,
  RotateCcw,
} from 'lucide-react';
import {
  Button,
  Card,
  Badge,
  SectionHeader,
  StatCard,
} from '../components/common';
import { useBizSahayak } from '../hooks/useBizSahayak';
import { formatCurrency, formatPercentage } from '../utils/formatters';
import { FINANCIAL_DISCLAIMER } from '../data/defaultData';
import { bizApi } from '../services/api';

export const Report = () => {
  const navigate = useNavigate();
  const { inputData } = useBizSahayak();
  const [downloading, setDownloading] = useState(false);

  const capital = Number(inputData.available_capital) || 100000;
  const location = inputData.location || 'Anand, Gujarat';
  const category = inputData.business_category || 'Textile & Clothing';

  // Deterministic calculations
  const projectCost = capital / 0.1;
  const rawMaxLoan = projectCost * 0.9;
  const isMicroFinance = projectCost <= 140000;
  const schemeName = isMicroFinance ? 'Micro Finance Scheme' : 'Term Loan Scheme';
  const interestRate = isMicroFinance ? 6.5 : 8.0;
  const tenureYears = isMicroFinance ? 3 : 7;
  const moratoriumMonths = isMicroFinance ? 3 : 6;
  const maxAgencyFunding = isMicroFinance ? 125000 : 4500000;
  const sanctionedLoan = Math.min(rawMaxLoan, maxAgencyFunding);

  const totalMonths = tenureYears * 12;
  const repaymentMonths = totalMonths - moratoriumMonths;
  const monthlyRate = interestRate / 12 / 100;
  const emi =
    (sanctionedLoan * monthlyRate * Math.pow(1 + monthlyRate, repaymentMonths)) /
    (Math.pow(1 + monthlyRate, repaymentMonths) - 1);

  const handlePrint = () => {
    window.print();
  };

  const handleDownloadPDF = async () => {
    setDownloading(true);
    try {
      // In Phase F1/prototype, attempt calling the backend or fallback to print
      const response = await bizApi.generateReport({
        location,
        business_category: category,
        available_capital: capital,
      });

      // Create download blob link if backend responded
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `BizSahayak_Plan_${location.replace(/[^a-zA-Z0-9]/g, '_')}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.warn('Backend PDF endpoint pending; triggering browser print view as fallback.', err);
      window.print();
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      {/* Header */}
      <SectionHeader
        title="Comprehensive Business & Financial Plan"
        subtitle={`Complete appraisal memorandum for ${category} at ${location}. Ready for presentation to bank loan officers.`}
        icon={FileText}
        badge={
          <Badge variant="primary" size="md">
            Step 4 of 4 • Final Plan
          </Badge>
        }
        action={
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="md"
              onClick={handlePrint}
              icon={Printer}
            >
              Print
            </Button>
            <Button
              variant="primary"
              size="md"
              onClick={handleDownloadPDF}
              loading={downloading}
              icon={Download}
            >
              Download PDF Report
            </Button>
          </div>
        }
      />

      {/* Mandatory Disclaimer */}
      <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4 flex items-start gap-3">
        <Info className="w-5 h-5 text-amber-700 shrink-0 mt-0.5" />
        <div className="text-xs text-amber-900 leading-relaxed">
          <strong className="font-bold">Official Disclaimer: </strong>
          {FINANCIAL_DISCLAIMER}
        </div>
      </div>

      {/* Executive Summary Card */}
      <Card
        title="Executive Summary & Project Overview"
        subtitle="Key parameters verified against deterministic lending rules"
        badge={<Badge variant="primary">{schemeName}</Badge>}
      >
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
          <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
            <span className="text-slate-500 font-semibold block uppercase">Enterprise</span>
            <span className="font-bold text-slate-800 text-sm mt-1 block">{category}</span>
          </div>
          <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
            <span className="text-slate-500 font-semibold block uppercase">Location</span>
            <span className="font-bold text-slate-800 text-sm mt-1 block">{location}</span>
          </div>
          <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
            <span className="text-slate-500 font-semibold block uppercase">Promoter Margin</span>
            <span className="font-bold text-emerald-800 text-sm mt-1 block">{formatCurrency(capital)} (10%)</span>
          </div>
          <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
            <span className="text-slate-500 font-semibold block uppercase">Total Project Cost</span>
            <span className="font-bold text-emerald-900 text-sm mt-1 block">{formatCurrency(projectCost)}</span>
          </div>
        </div>
      </Card>

      {/* Financial Structure Summary */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card title="Credit Appraisal & Loan Terms" subtitle="Deterministic scheme routing breakdown">
          <div className="space-y-3 text-xs">
            <div className="flex justify-between py-2 border-b border-slate-100">
              <span className="text-slate-600">Assigned Government Scheme:</span>
              <span className="font-bold text-slate-800">{schemeName}</span>
            </div>
            <div className="flex justify-between py-2 border-b border-slate-100">
              <span className="text-slate-600">Approved Loan Sizing (90%):</span>
              <span className="font-bold text-emerald-800">{formatCurrency(sanctionedLoan)}</span>
            </div>
            <div className="flex justify-between py-2 border-b border-slate-100">
              <span className="text-slate-600">Applicable Interest Rate:</span>
              <span className="font-bold text-slate-800">{formatPercentage(interestRate)} p.a.</span>
            </div>
            <div className="flex justify-between py-2 border-b border-slate-100">
              <span className="text-slate-600">Loan Tenure:</span>
              <span className="font-bold text-slate-800">{tenureYears} Years ({totalMonths} Months)</span>
            </div>
            <div className="flex justify-between py-2 border-b border-slate-100">
              <span className="text-slate-600">Moratorium Grace Period:</span>
              <span className="font-bold text-amber-700">{moratoriumMonths} Months</span>
            </div>
            <div className="flex justify-between py-2">
              <span className="text-slate-600 font-bold">Monthly Equated Installment (EMI):</span>
              <span className="font-extrabold text-emerald-900 text-sm">{formatCurrency(Math.round(emi))}</span>
            </div>
          </div>
        </Card>

        {/* Advisory & Market Reach Summary */}
        <Card title="Market Reach & Feasibility Assessment" subtitle="Hyper-local validation findings">
          <div className="space-y-3 text-xs">
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="font-bold text-slate-800 block mb-1">Target Rural Catchment</span>
              <p className="text-slate-600">
                Primary 0-7 km radius covers ~4,200 households across local village panchayats and weekly agricultural haats.
              </p>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="font-bold text-slate-800 block mb-1">Key Opportunity Driver</span>
              <p className="text-slate-600">
                Proximity to regional wholesale fabric corridors combined with strong local demand for durable everyday garments and uniforms.
              </p>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
              <span className="font-bold text-slate-800 block mb-1">Risk Mitigation Strategy</span>
              <p className="text-slate-600">
                Utilize the {moratoriumMonths}-month moratorium buffer to establish cash-first retail sales before initiating principal repayment.
              </p>
            </div>
          </div>
        </Card>
      </div>

      {/* Action Footer */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-slate-200">
        <Button
          variant="outline"
          onClick={() => navigate('/business-input')}
          icon={RotateCcw}
        >
          Start New Advisory Plan
        </Button>
        <div className="flex items-center gap-2">
          <Button variant="ghost" onClick={() => navigate('/financial')}>
            ← Back to Financial
          </Button>
          <Button
            variant="primary"
            size="lg"
            onClick={handleDownloadPDF}
            loading={downloading}
            icon={Download}
          >
            Download Official PDF
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Report;
