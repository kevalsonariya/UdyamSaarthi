import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 5000,
});

/**
 * Deterministic financial calculator adhering to the official financial rules
 * used as a resilient client-side service fallback when the backend service is offline.
 */
export const calculateDeterministicFinancials = (availableCapital) => {
  const marginPercentage = 10.0;
  const capital = Math.max(1000, Number(availableCapital) || 100000);
  const projectCost = Math.round((capital / (marginPercentage / 100.0)) * 100) / 100;
  const maxLoanAmount = Math.round(projectCost * 0.9 * 100) / 100;

  // Boundary condition check: <= 1.40 Lakh vs > 1.40 Lakh
  const isMicroFinance = projectCost <= 140000.0;

  const scheme = isMicroFinance
    ? {
        scheme_name: 'Micro Finance Scheme',
        scheme_code: 'MFS-RURAL-01',
        interest_rate_percent: 6.5,
        tenure_years: 3,
        tenure_months: 36,
        moratorium_months: 3,
        max_agency_funding: 125000.0,
        eligible_funding: Math.min(maxLoanAmount, 125000.0),
        governing_body: 'National Rural Livelihood Mission (NRLM) / Micro-credit Division',
        eligibility_criteria: [
          'Project cost must not exceed INR 1.40 Lakh.',
          'Rural micro-entrepreneurs, self-help groups (SHGs), and solo artisans.',
          'Simple Aadhaar & Village Panchayat / Ward recommendation required.',
          'No collateral security required up to scheme ceiling.',
        ],
        key_benefits: [
          'Concessional 6.5% per annum fixed interest rate.',
          '3-month initial moratorium to setup production and sales.',
          'Low paperwork with direct bank disbursement.',
          'Eligibility for prompt repayment incentive rebate (up to 1%).',
        ],
      }
    : {
        scheme_name: 'Term Loan Scheme',
        scheme_code: 'TLS-MSME-02',
        interest_rate_percent: 8.0,
        tenure_years: 7,
        tenure_months: 84,
        moratorium_months: 6,
        max_agency_funding: 4500000.0,
        eligible_funding: Math.min(maxLoanAmount, 4500000.0),
        governing_body: 'CGTMSE / Rural Enterprise Development Board / PMEGP',
        eligibility_criteria: [
          'Project cost above INR 1.40 Lakh and up to INR 50.00 Lakh.',
          'Formal or semi-formal micro enterprises in rural/peri-urban locations.',
          'Udyam Registration Certificate & basic project report required.',
          'Covered under Credit Guarantee cover without third-party collateral.',
        ],
        key_benefits: [
          'Attractive 8.0% annual interest rate for long-term capital deployment.',
          'Extended 7-year repayment tenure for relaxed liquidity management.',
          '6-month moratorium period during initial gestation and ramp-up.',
          'Covers both machinery capital expenditure and initial working capital.',
        ],
      };

  const principal = scheme.eligible_funding;
  const totalMonths = scheme.tenure_months;
  const moratoriumMonths = scheme.moratorium_months;
  const postMoratoriumMonths = totalMonths - moratoriumMonths;
  const monthlyRate = scheme.interest_rate_percent / 100.0 / 12.0;

  const moratoriumMonthlyInterest = Math.round(principal * monthlyRate * 100) / 100;

  let monthlyEmi = 0;
  if (monthlyRate > 0 && postMoratoriumMonths > 0) {
    const factor = Math.pow(1.0 + monthlyRate, postMoratoriumMonths);
    monthlyEmi = Math.round(((principal * monthlyRate * factor) / (factor - 1.0)) * 100) / 100;
  } else {
    monthlyEmi = Math.round((principal / Math.max(1, postMoratoriumMonths)) * 100) / 100;
  }

  // Generate repayment schedule items
  const schedule = [];
  let currentBalance = principal;
  let totalRepaymentInterest = 0;

  for (let m = 1; m <= moratoriumMonths; m++) {
    const yearNum = Math.floor((m - 1) / 12) + 1;
    const interestComp = Math.round(currentBalance * monthlyRate * 100) / 100;
    const principalComp = 0.0;
    totalRepaymentInterest += interestComp;

    schedule.push({
      month: m,
      year: yearNum,
      is_moratorium: true,
      opening_balance: currentBalance,
      installment_amount: interestComp,
      principal_component: principalComp,
      interest_component: interestComp,
      closing_balance: currentBalance,
    });
  }

  for (let m = moratoriumMonths + 1; m <= totalMonths; m++) {
    const yearNum = Math.floor((m - 1) / 12) + 1;
    const interestComp = Math.round(currentBalance * monthlyRate * 100) / 100;
    let principalComp = 0;
    let closingBalance = 0;
    let installment = monthlyEmi;

    if (m === totalMonths) {
      principalComp = currentBalance;
      installment = Math.round((principalComp + interestComp) * 100) / 100;
      closingBalance = 0.0;
    } else {
      principalComp = Math.round((monthlyEmi - interestComp) * 100) / 100;
      if (principalComp > currentBalance) {
        principalComp = currentBalance;
      }
      closingBalance = Math.round((currentBalance - principalComp) * 100) / 100;
    }

    totalRepaymentInterest += interestComp;
    schedule.push({
      month: m,
      year: yearNum,
      is_moratorium: false,
      opening_balance: currentBalance,
      installment_amount: installment,
      principal_component: principalComp,
      interest_component: interestComp,
      closing_balance: Math.max(0, closingBalance),
    });

    currentBalance = closingBalance;
    if (currentBalance <= 0.01) currentBalance = 0;
  }

  const totalInterestPayable = Math.round(totalRepaymentInterest * 100) / 100;
  const totalRepaymentAmount = Math.round((principal + totalInterestPayable) * 100) / 100;

  const emi = {
    principal_amount: principal,
    annual_interest_rate_percent: scheme.interest_rate_percent,
    tenure_months: totalMonths,
    moratorium_months: moratoriumMonths,
    post_moratorium_tenure_months: postMoratoriumMonths,
    monthly_emi: monthlyEmi,
    moratorium_monthly_interest: moratoriumMonthlyInterest,
    total_interest_payable: totalInterestPayable,
    total_repayment_amount: totalRepaymentAmount,
  };

  const monthlyRawMaterials = Math.round(projectCost * 0.045 * 100) / 100;
  const monthlyLabor = Math.round(projectCost * 0.025 * 100) / 100;
  const monthlyRent = Math.round(projectCost * 0.012 * 100) / 100;
  const monthlyLogistics = Math.round(projectCost * 0.008 * 100) / 100;
  const monthlyContingency = Math.round(projectCost * 0.005 * 100) / 100;
  const totalMonthlyOpex = Math.round(
    (monthlyRawMaterials + monthlyLabor + monthlyRent + monthlyLogistics + monthlyContingency) * 100
  ) / 100;

  const workingCapital = {
    monthly_raw_materials: monthlyRawMaterials,
    monthly_labor_wages: monthlyLabor,
    monthly_rent_utilities: monthlyRent,
    monthly_logistics_packaging: monthlyLogistics,
    monthly_contingency_buffer: monthlyContingency,
    total_monthly_operating_expense: totalMonthlyOpex,
    recommended_3_months_reserve: Math.round(totalMonthlyOpex * 3.0 * 100) / 100,
    projected_monthly_revenue: Math.round((totalMonthlyOpex + monthlyEmi) * 1.35 * 100) / 100,
    projected_monthly_net_profit: Math.round(
      ((totalMonthlyOpex + monthlyEmi) * 1.35 - totalMonthlyOpex - monthlyEmi) * 100
    ) / 100,
    break_even_monthly_revenue: Math.round((totalMonthlyOpex + monthlyEmi) * 100) / 100,
    break_even_occupancy_or_capacity_percent: 74.0,
  };

  return {
    financial: {
      available_capital: capital,
      margin_percentage: marginPercentage,
      project_cost: projectCost,
      promoter_contribution: capital,
      max_loan_amount: maxLoanAmount,
      subsidy_or_grant_estimate: Math.round(projectCost * 0.15 * 100) / 100,
      financial_disclaimer:
        'Indicative calculation for planning purposes. Verify applicable scheme terms before making financial decisions.',
    },
    scheme,
    emi,
    repayment: schedule,
    working_capital: workingCapital,
  };
};

export const bizApi = {
  // Analyze business feasibility and hyper-local insights
  analyzeBusiness: async (payload) => {
    try {
      const response = await apiClient.post('/business/analyze', payload);
      return response.data;
    } catch (err) {
      console.warn('Backend /business/analyze unavailable; using domain prototype fallback data.', err.message);
      const fallback = calculateDeterministicFinancials(payload.available_capital);
      return {
        is_verified: false,
        source: 'prototype_simulation',
        ...fallback,
      };
    }
  },

  // Fetch full financial structuring plan from backend or fallback service
  getFinancialPlan: async (payload) => {
    try {
      // First attempt to call the backend endpoints
      const [finRes, schRes, emiRes, wcRes] = await Promise.all([
        apiClient.post('/financial/calculate', payload),
        apiClient.post('/scheme/recommend', payload),
        apiClient.post('/emi/calculate', payload),
        apiClient.post('/working-capital/calculate', payload),
      ]);

      // If backend endpoints succeeded, get repayment schedule from full analysis or fallback
      let repaymentSchedule = [];
      try {
        const full = await apiClient.post('/business/analyze', payload);
        repaymentSchedule = full.data.repayment || [];
      } catch (e) {
        const local = calculateDeterministicFinancials(payload.available_capital);
        repaymentSchedule = local.repayment;
      }

      return {
        financial: finRes.data,
        scheme: schRes.data,
        emi: emiRes.data,
        repayment: repaymentSchedule,
        working_capital: wcRes.data,
      };
    } catch (err) {
      console.warn(
        'Backend financial endpoints unavailable; using deterministic service calculations.',
        err.message
      );
      return calculateDeterministicFinancials(payload.available_capital);
    }
  },

  // Generate ReportLab PDF dossier
  generateReport: async (payload) => {
    return apiClient.post('/report/generate', payload, {
      responseType: 'blob',
    });
  },
};

export default apiClient;
