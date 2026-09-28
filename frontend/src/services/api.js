import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const bizApi = {
  // Analyze business feasibility and hyper-local insights
  analyzeBusiness: async (payload) => {
    return apiClient.post('/business/analyze', payload);
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
