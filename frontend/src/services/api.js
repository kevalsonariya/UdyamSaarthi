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
 * Generates structured domain analysis for local prototyping fallback
 */
export const getFallbackAnalysis = (location, category, capital) => {
  const loc = location || 'Anand, Gujarat';
  const cat = category || 'Textile & Clothing';

  return {
    is_verified: false,
    source: 'prototype_simulation',
    disclaimer: 'Indicative prototype data. Verify applicable local parameters before execution.',
    business_summary: {
      location: loc,
      business_category: cat,
      available_capital: capital || 100000,
      readiness_level: 'High Initial Potential',
    },
    market_reach: {
      estimated_consumer_reach: '18,500 – 24,000 residents',
      local_area: `0 – 15 km catchment radius surrounding ${loc}`,
      distribution_channels: [
        {
          name: 'Direct Counter & Retail Storefront',
          description: 'High walk-in visibility on village market road or town bazaar.',
          suitability: 'Primary (60% volume)',
        },
        {
          name: 'Weekly Village Haats & Mandi Stalls',
          description: 'Access to rotating weekly agricultural gatherings in neighboring talukas.',
          suitability: 'Secondary (25% volume)',
        },
        {
          name: 'Direct Institutional & Bulk Orders',
          description: 'Orders from local schools, cooperatives, and small workshops.',
          suitability: 'High-Margin (15% volume)',
        },
      ],
      customer_segments: [
        { name: 'Agricultural Families', percentage: 45, demand: 'Durable, cost-effective essentials' },
        { name: 'Town Salaried & Shop Owners', percentage: 30, demand: 'Daily consumables & regular upgrades' },
        { name: 'Youth & Students', percentage: 25, demand: 'Modern styles & custom preferences' },
      ],
    },
    opportunities: [
      {
        title: 'Cluster Supply-Chain Advantage',
        description: `Proximity to key regional raw material corridors for ${cat} reduces transport friction and supplier lead time.`,
        impact: 'High Impact',
      },
      {
        title: 'Underserved Semi-Rural Demand',
        description: 'Local consumers travel 20-30 km to major district hubs; a nearby center retains local spending.',
        impact: 'High Impact',
      },
      {
        title: 'Seasonal Surge Capitalization',
        description: 'Agricultural harvest payouts and local festival seasons consistently deliver 2x sales peaks.',
        impact: 'Moderate Impact',
      },
    ],
    swot: {
      strengths: [
        'Direct relationship and trust with local village panchayats and community.',
        'Significantly lower operational rental overhead compared to urban establishments.',
        'High operational agility to tailor offerings to local cultural preferences.',
        'Promoter commitment with skin in the game through 10% margin equity.',
      ],
      weaknesses: [
        'Initial working capital constraints limiting bulk raw material purchases.',
        'Early reliance on manual processing prior to machinery scale-up.',
        'Informal bookkeeping that requires transition to structured digital accounting.',
        'Initial brand awareness limited to immediate 5 km radius.',
      ],
      opportunities: [
        'Leverage government interest-subsidized credit schemes with moratorium benefits.',
        'Establish direct supply agreements with local institutional cooperatives.',
        'Adopt UPI and digital cataloging via WhatsApp Business to expand radius.',
        'Introduce value-added custom services that competitors do not provide.',
      ],
      threats: [
        'Temporary cash flow delays when rural customers face harvest payment lags.',
        'Raw material wholesale price volatility during off-peak seasons.',
        'Competition from low-quality, unorganized mobile haat traders.',
        'Dependence on local power stability for machinery operations.',
      ],
    },
    risks: [
      {
        title: 'Seasonal Demand & Cashflow Fluctuations',
        description: 'Revenue peaks during post-harvest months but can soften during monsoon periods.',
        severity: 'Medium',
        mitigation: 'Utilize the 3-6 month loan moratorium to build a 2-month cash buffer and maintain multi-product lines.',
      },
      {
        title: 'Supplier Raw Material Price Volatility',
        description: 'Unanticipated increases in wholesale inputs could squeeze operating margins.',
        severity: 'Medium',
        mitigation: 'Form bulk-buying syndicates with neighboring micro-entrepreneurs and secure fixed short-term contracts.',
      },
      {
        title: 'Informal Credit Demands by Buyers',
        description: 'Rural customers often expect extended credit terms until crop sales are realized.',
        severity: 'High',
        mitigation: 'Enforce a strict cash-first or 50% advance policy on customized orders with small discounts for upfront UPI payments.',
      },
    ],
    competitors: [
      {
        name: 'Local Legacy Traders',
        type: 'Traditional Brick & Mortar',
        presence: 'Established village market location',
        pricing_tier: 'Standard / High',
        weakness: 'Limited variety, rigid payment terms, outdated product lines',
      },
      {
        name: 'Weekly Haat Vendors',
        type: 'Informal Mobile Traders',
        presence: 'Available 1-2 days per week',
        pricing_tier: 'Low / Budget',
        weakness: 'Inconsistent quality, zero after-sales service or customization',
      },
      {
        name: 'Nearby Town Retail Outlets',
        type: 'Commercial Semi-Urban Hub',
        presence: '15-20 km distance',
        pricing_tier: 'High',
        weakness: 'Inconvenient travel cost and time for routine rural purchases',
      },
    ],
    pricing: {
      estimated_price_range: '₹220 – ₹850',
      purchasing_power_context:
        'Average rural household ticket size per purchase is ₹400 – ₹700, with high willingness to pay for proven durability.',
      suggested_approach:
        'Value-Based Tiered Pricing: Price essential daily volume items at competitive entry points (₹250-₹400) to build footfall, while keeping higher margin (35-42%) offerings for festive and customized orders.',
    },
    recommendation: {
      score: 83,
      status: 'Recommended for Financial Structuring',
      headline: `Feasible Micro-Enterprise Opportunity in ${loc}`,
      summary: `The proposed ${cat} enterprise shows robust local feasibility score of 83/100. Strong regional demand, manageable competitor density, and available credit schemes make this a viable candidate for term financing.`,
      key_actions: [
        'Secure shop premise along high-footfall village connective road or haat junction.',
        'Proceed with deterministic loan sizing under recommended government lending scheme.',
        'Allocate 60% of project financing to productive machinery and 25% to initial inventory buffer.',
      ],
    },
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
      // Return structured prototype fallback
      return getFallbackAnalysis(
        payload.location,
        payload.business_category,
        payload.available_capital
      );
    }
  },

  // Calculate deterministic project cost & loan sizing
  calculateFinancial: async (payload) => {
    return apiClient.post('/financial/calculate', payload);
  },

  // Determine eligible government scheme (Micro Finance vs Term Loan)
  recommendScheme: async (payload) => {
    return apiClient.post('/scheme/recommend', payload);
  },

  // Calculate EMI
  calculateEMI: async (payload) => {
    return apiClient.post('/emi/calculate', payload);
  },

  // Compute amortized repayment schedule
  calculateRepayment: async (payload) => {
    return apiClient.post('/repayment/calculate', payload);
  },

  // Compute working capital guidelines
  calculateWorkingCapital: async (payload) => {
    return apiClient.post('/working-capital/calculate', payload);
  },

  // Trigger PDF business plan generation
  generateReport: async (payload) => {
    return apiClient.post('/report/generate', payload, {
      responseType: 'blob',
    });
  },
};

export default apiClient;
