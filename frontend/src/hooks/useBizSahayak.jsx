import React, { createContext, useContext, useState } from 'react';
import { DEFAULT_DEMO_SCENARIO } from '../data/defaultData';

const BizSahayakContext = createContext(null);

export const BizSahayakProvider = ({ children }) => {
  // Business input state initialized with the default demo scenario
  const [inputData, setInputData] = useState({
    location: DEFAULT_DEMO_SCENARIO.location,
    business_category: DEFAULT_DEMO_SCENARIO.business_category,
    available_capital: DEFAULT_DEMO_SCENARIO.available_capital,
  });

  // Analysis result state
  const [analysisData, setAnalysisData] = useState(null);

  // Financial result state
  const [financialData, setFinancialData] = useState(null);

  // Loading & error flags
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const resetToDemoScenario = () => {
    setInputData({
      location: DEFAULT_DEMO_SCENARIO.location,
      business_category: DEFAULT_DEMO_SCENARIO.business_category,
      available_capital: DEFAULT_DEMO_SCENARIO.available_capital,
    });
  };

  return (
    <BizSahayakContext.Provider
      value={{
        inputData,
        setInputData,
        analysisData,
        setAnalysisData,
        financialData,
        setFinancialData,
        loading,
        setLoading,
        error,
        setError,
        resetToDemoScenario,
      }}
    >
      {children}
    </BizSahayakContext.Provider>
  );
};

export const useBizSahayak = () => {
  const context = useContext(BizSahayakContext);
  if (!context) {
    throw new Error('useBizSahayak must be used within a BizSahayakProvider');
  }
  return context;
};

export default useBizSahayak;
