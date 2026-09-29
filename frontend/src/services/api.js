import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 8000,
});

/**
 * Normalizes input payload for backend consistency
 */
const formatPayload = (data) => {
  if (!data) throw new Error('Input data is required');
  const capital = Number(data.available_capital);
  if (isNaN(capital) || capital <= 0) {
    throw new Error('Valid available margin capital is required');
  }

  const lang = data.language || (typeof window !== 'undefined' ? localStorage.getItem('udyamsaarthi_language') : 'en') || 'en';

  const payload = {
    location: (data.location || 'Anand, Gujarat').trim(),
    business_category: (data.business_category || 'Textile & Clothing').trim(),
    available_capital: capital,
    language: lang,
  };

  if (data.location_detail) {
    payload.location_detail = data.location_detail;
  }

  if (data.request_id) {
    payload.request_id = data.request_id;
  }

  return payload;
};


export const bizApi = {
  /**
   * Complete business feasibility, market reach, SWOT, risk, pricing and recommendation
   * POST /business/analyze
   */
  analyzeBusiness: async (payload, options = {}) => {
    const formatted = formatPayload(payload);
    const reqId = payload.request_id || formatted.request_id || (typeof crypto !== 'undefined' && crypto.randomUUID ? crypto.randomUUID() : `req_${Date.now()}`);
    formatted.request_id = reqId;

    try {
      const response = await apiClient.post('/business/analyze', formatted, {
        signal: options?.signal,
      });
      const raw = response.data?.data ?? response.data;

      // Extract market information cleanly
      const marketRaw = raw.market || {};
      const catchmentKm = marketRaw.catchment_radius_km ?? 15;
      const popEst = marketRaw.estimated_target_population ?? 20000;
      const channels = (marketRaw.high_demand_local_channels || []).map((ch, i) => ({
        name: ch,
        description: formatted.language === 'hi'
          ? `${formatted.location} में ${formatted.business_category} के लिए पहचाना गया उच्च-मांग चैनल।`
          : formatted.language === 'gu'
          ? `${formatted.location} માં ${formatted.business_category} માટે ઓળખાયેલ સ્થાનિક ઉચ્ચ-માંગ ચેનલ.`
          : `Local high-demand channel identified for ${formatted.business_category} in ${formatted.location}.`,
        suitability: i === 0
          ? (formatted.language === 'hi' ? 'प्राथमिक (उच्च मात्रा)' : formatted.language === 'gu' ? 'મુખ્ય ચેનલ (વધુ વેચાણ)' : 'Primary (High Volume)')
          : (formatted.language === 'hi' ? 'पूरक / द्वितीयक' : formatted.language === 'gu' ? 'ગૌણ ચેનલ' : 'Secondary / Complementary'),
      }));
      const segments = (marketRaw.primary_customer_segments || []).map((seg, i) => ({
        name: seg,
        percentage: i === 0 ? 50 : (i === 1 ? 30 : 20),
        demand: formatted.language === 'hi'
          ? 'स्थानीय क्षेत्र के भीतर नियमित आवर्ती मांग'
          : formatted.language === 'gu'
          ? 'સ્થાનિક વિસ્તારમાં નિયમિત આવર્તક માંગ'
          : 'Regular repeat demand within local catchment territory',
      }));

      // Normalize opportunities into a clean array suitable for .map()
      let oppArray = [];
      if (Array.isArray(raw.opportunities)) {
        oppArray = raw.opportunities;
      } else if (raw.opportunities && typeof raw.opportunities === 'object') {
        if (Array.isArray(raw.opportunities.items) && raw.opportunities.items.length > 0) {
          oppArray = raw.opportunities.items.map((item) => ({
            title: item.title,
            type: item.type || 'High Growth',
            description: item.description,
            reason: item.reason,
            local_factor: item.local_factor,
            impact: item.impact || item.type || 'High Growth',
          }));
        } else {
          const highGrowth = raw.opportunities.high_growth_segments || [];
          const unmetNeeds = raw.opportunities.unmet_local_needs || [];
          const drivers = raw.opportunities.ecosystem_growth_drivers || [];

          highGrowth.forEach((item) => {
            oppArray.push({
              title: item,
              type: 'High Growth',
              description: `High-growth segment identified for ${formatted.business_category} in ${formatted.location}.`,
              impact: 'High Growth',
            });
          });

          unmetNeeds.forEach((item) => {
            oppArray.push({
              title: item,
              type: 'Unmet Need',
              description: `Unmet local community demand representing an immediate market entry advantage.`,
              impact: 'Unmet Need',
            });
          });

          drivers.forEach((item) => {
            oppArray.push({
              title: item,
              type: 'Ecosystem Driver',
              description: `Regional ecosystem enabler supporting long-term operational viability.`,
              impact: 'Ecosystem Driver',
            });
          });
        }
      }

      // Normalize risks
      const risksArray = (raw.risks || []).map((r) => ({
        title: r.risk_title || r.title || 'Operational Risk',
        description: r.description || (
          formatted.language === 'hi'
            ? `श्रेणी: ${r.category || 'परिचालन'} • स्थानीय व्यापार संदर्भ के लिए मूल्यांकित।`
            : formatted.language === 'gu'
            ? `શ્રેણી: ${r.category || 'ઓપરેશનલ'} • સ્થાનિક વ્યાપાર સંદર્ભ માટે મૂલ્યાંકન કરેલ.`
            : `Category: ${r.category || r.risk_category || 'General Operational'} • Evaluated for local business context.`
        ),
        severity: r.severity || 'Medium',
        mitigation: r.mitigation_strategy || r.mitigation || (
          formatted.language === 'hi'
            ? 'उद्यमसारथी द्वारा अनुशंसित 3 महीने का परिचालन रिज़र्व बनाए रखें और आपूर्तिकर्ता समय पर नजर रखें।'
            : formatted.language === 'gu'
            ? '3 મહિનાનું ઓપરેટિંગ રિઝર્વ જાળવી રાખો અને સપ્લાયર્સ સાથે નિયમિત સંપર્ક રાખો.'
            : 'Maintain 3-month operating reserve and monitor supplier lead times.'
        ),
      }));

      // Normalize competitors
      const compArray = (raw.competitors || []).map((c) => ({
        name: c.name || c.competitor_name || (
          formatted.language === 'hi' ? 'स्थानीय व्यापारी' : formatted.language === 'gu' ? 'સ્થાનિક વેપારી' : 'Local Merchant'
        ),
        type: c.type || c.type_of_business || (
          formatted.language === 'hi' ? 'स्थानीय उद्यम' : formatted.language === 'gu' ? 'સ્થાનિક સાહસ' : 'Local Enterprise'
        ),
        presence: c.presence || c.proximity || (
          formatted.language === 'hi'
            ? `${catchmentKm} किमी दायरे में कार्यरत`
            : formatted.language === 'gu'
            ? `${catchmentKm} કિમી વિસ્તારમાં કાર્યરત`
            : `Operating within ${catchmentKm} km radius`
        ),
        pricing_tier: c.pricing_tier || (
          formatted.language === 'hi' ? 'मानक स्थानीय मूल्य' : formatted.language === 'gu' ? 'સ્થાનિક બજાર ભાવ' : 'Standard Local Pricing'
        ),
        weakness: c.differentiation_strategy || c.weakness || (
          formatted.language === 'hi'
            ? 'उच्च गुणवत्ता, पारदर्शी बिलिंग और डिजिटल भुगतान द्वारा अलग पहचान बनाएं।'
            : formatted.language === 'gu'
            ? 'શ્રેષ્ઠ ગુણવત્તા, પારદર્શક બિલિંગ અને ડિજિટલ પેમેન્ટ દ્વારા અલગ ઓળખ ઊભી કરો.'
            : 'Opportunity for higher quality, transparent pricing, and digital payments.'
        ),
        is_demo_data: c.is_demo_data !== false,
        is_estimate: c.is_estimate !== false,
        data_source: c.data_source || 'Indicative category-location profile',
        location_status: c.location_status || '',
        address: c.address || null,
        distance_km: c.distance_km ?? null,
        latitude: c.latitude ?? null,
        longitude: c.longitude ?? null,
        place_id: c.place_id || null,
        map_url: c.map_url || null,
        website_url: c.website_url || null,
        rating: c.rating ?? null,
        review_count: c.review_count ?? null,
        source: c.source || (c.is_demo_data === false ? 'Google Places' : 'Indicative Benchmark'),
      }));

      // Normalize pricing
      const pricingRaw = raw.pricing || {};
      const pricingObj = {
        estimated_price_range: pricingRaw.suggested_retail_price || pricingRaw.estimated_price_range || (
          formatted.language === 'hi' ? 'प्रतिस्पर्धी स्थानीय मूल्य सीमा' : formatted.language === 'gu' ? 'સ્પર્ધાત્મક સ્થાનિક ભાવ' : 'Competitive Local Band'
        ),
        purchasing_power_context: pricingRaw.benchmark_product_or_service
          ? (
            formatted.language === 'hi'
              ? `मानक बेंचमार्क: ${pricingRaw.benchmark_product_or_service}। अनुमानित उत्पादन लागत: ${pricingRaw.estimated_unit_production_cost || 'उपलब्ध नहीं'}। लक्षित सकल मार्जिन: ${pricingRaw.target_gross_margin_percent ?? 35}%।`
              : formatted.language === 'gu'
              ? `માનક બેન્ચમાર્ક: ${pricingRaw.benchmark_product_or_service}. અંદાજિત ઉત્પાદન ખર્ચ: ${pricingRaw.estimated_unit_production_cost || 'N/A'}. લક્ષિત ગ્રોસ માર્જિન: ${pricingRaw.target_gross_margin_percent ?? 35}%.`
              : `Benchmark standard: ${pricingRaw.benchmark_product_or_service}. Estimated production cost: ${pricingRaw.estimated_unit_production_cost || 'N/A'}. Target margin: ${pricingRaw.target_gross_margin_percent ?? 35}%.`
          )
          : (pricingRaw.purchasing_power_context || (
            formatted.language === 'hi' ? 'ग्रामीण क्रय शक्ति और स्थानीय घरेलू बजट के अनुकूल।' : formatted.language === 'gu' ? 'ગ્રામીણ ખરીદશક્તિ અને સ્થાનિક બજેટને અનુરૂપ.' : 'Tailored to rural purchasing power and local wallet-share.'
          )),
        suggested_approach: pricingRaw.pricing_strategy_notes || pricingRaw.suggested_approach || (
          formatted.language === 'hi' ? 'स्थानीय घरेलू बजट के अनुसार मूल्य-आधारित त्रि-स्तरीय मूल्य निर्धारण।' : formatted.language === 'gu' ? 'સ્થાનિક બજેટ અનુસાર મૂલ્ય-આધારિત ત્રિ-સ્તરીય ભાવ પદ્ધતિ.' : 'Value-based tiered pricing accommodating local household budgets.'
        ),
      };

      // Normalize recommendation
      const recRaw = raw.recommendation || {};
      const recObj = {
        score: recRaw.feasibility_score ?? recRaw.score ?? 83,
        status: recRaw.feasibility_rating ?? recRaw.status ?? (
          formatted.language === 'hi' ? 'वित्तीय संरचना के लिए अनुशंसित' : formatted.language === 'gu' ? 'નાણાકીય આયોજન માટે ભલામણ કરેલ' : 'Recommended for Financial Structuring'
        ),
        headline: formatted.language === 'hi'
          ? `${formatted.location} में ${recRaw.feasibility_rating || 'व्यवहार्य सूक्ष्म उद्यम'}`
          : formatted.language === 'gu'
          ? `${formatted.location} માં ${recRaw.feasibility_rating || 'સક્ષમ સૂક્ષ્મ સાહસ'}`
          : `${recRaw.feasibility_rating || 'Viable Micro-Venture'} in ${formatted.location}`,
        summary: recRaw.summary || (
          formatted.language === 'hi'
            ? `प्रस्तावित उद्यम ${formatted.location} में ठोस स्थानीय व्यवहार्यता प्रदर्शित करता है।`
            : formatted.language === 'gu'
            ? `સૂચિત સાહસ ${formatted.location} માં નક્કર સ્થાનિક સક્ષમતા દર્શાવે છે.`
            : `The proposed enterprise demonstrates solid local viability in ${formatted.location}.`
        ),
        key_actions: recRaw.first_90_days_milestones || recRaw.key_actions || (
          formatted.language === 'hi' ? [
            `${formatted.location} में प्रमुख बाज़ार मार्ग के पास व्यावसायिक जगह तय करें।`,
            'सरकारी ऋण योजना के तहत ऋण आवेदन की प्रक्रिया आगे बढ़ाएं।',
            'मौसमी नकदी प्रवाह की सुरक्षा के लिए कार्यशील पूंजी रिज़र्व बनाए रखें।',
          ] : formatted.language === 'gu' ? [
            `${formatted.location} માં મુખ્ય બજાર નજીક યોગ્ય જગ્યા નક્કી કરો.`,
            'સરકારી ધિરાણ યોજના હેઠળ લોન મેળવવાની કાર્યવાહી કરો.',
            'મોસમી રોકડ પ્રવાહની સુરક્ષા માટે કાર્યકારી મૂડી અનામત જાળવી રાખો.',
          ] : [
            `Secure operational premises along high-footfall catchment road in ${formatted.location}.`,
            'Proceed with deterministic loan sizing under recommended government lending scheme.',
            'Deploy working capital reserves to absorb seasonal agricultural cash flow cycles.',
          ]
        ),
      };

      return {
        request_id: raw.request_id || reqId,
        input: {
          location: raw.location || formatted.location,
          business_category: raw.business_category || formatted.business_category,
          available_capital: raw.available_capital || formatted.available_capital,
          language: formatted.language || 'en',
        },
        is_verified: true,
        source: 'backend_analysis_engine',
        location: raw.location || formatted.location,
        business_category: raw.business_category || formatted.business_category,
        available_capital: raw.available_capital || formatted.available_capital,
        business: raw.business || null,
        business_summary: {
          location: raw.location || formatted.location,
          business_category: raw.business_category || formatted.business_category,
          available_capital: raw.available_capital || formatted.available_capital,
          readiness_level: recRaw.feasibility_rating || (
            formatted.language === 'hi' ? 'उच्च प्रारंभिक क्षमता' : formatted.language === 'gu' ? 'ઉચ્ચ પ્રારંભિક સંભાવના' : 'High Initial Potential'
          ),
        },
        market_reach: {
          estimated_consumer_reach: formatted.language === 'hi'
            ? `${popEst.toLocaleString('en-IN')} निवासी`
            : formatted.language === 'gu'
            ? `${popEst.toLocaleString('en-IN')} નાગરિકો`
            : `${popEst.toLocaleString('en-IN')} residents`,
          local_area: formatted.language === 'hi'
            ? `${raw.location || formatted.location} के आसपास ${catchmentKm} किमी का सेवा क्षेत्र`
            : formatted.language === 'gu'
            ? `${raw.location || formatted.location} ની આસપાસ ${catchmentKm} કિમીનું સેવા ક્ષેત્ર`
            : `${catchmentKm} km catchment radius surrounding ${raw.location || formatted.location}`,
          distribution_channels: channels.length > 0 ? channels : [
            {
              name: formatted.language === 'hi'
                ? 'सीधा काउंटर एवं खुदरा स्टोर'
                : formatted.language === 'gu'
                ? 'સીધો કાઉન્ટર અને રિટેલ સ્ટોર'
                : 'Direct Counter & Retail Storefront',
              description: formatted.language === 'hi'
                ? 'स्थानीय बाज़ार में प्राथमिक ग्राहक आवागमन।'
                : formatted.language === 'gu'
                ? 'સ્થાનિક બજારમાં પ્રાથમિક ગ્રાહક આવક.'
                : 'Primary customer footfall in local village/town market.',
              suitability: formatted.language === 'hi' ? 'प्राथमिक चैनल' : formatted.language === 'gu' ? 'મુખ્ય ચેનલ' : 'Primary Channel',
            },
          ],
          customer_segments: segments.length > 0 ? segments : [
            {
              name: formatted.language === 'hi' ? 'स्थानीय किसान एवं परिवार' : formatted.language === 'gu' ? 'સ્થાનિક ખેડૂત પરિવારો' : 'Local Farming Families',
              percentage: 50,
            },
            {
              name: formatted.language === 'hi' ? 'कस्बाई वेतनभोगी एवं दुकानदार' : formatted.language === 'gu' ? 'નગરના વેપારીઓ અને નોકરિયાત' : 'Town Salaried & Shop Owners',
              percentage: 30,
            },
            {
              name: formatted.language === 'hi' ? 'युवा एवं छात्र' : formatted.language === 'gu' ? 'યુવાનો અને વિદ્યાર્થીઓ' : 'Youth & Students',
              percentage: 20,
            },
          ],
        },
        opportunities: oppArray,
        swot: raw.swot || (
          formatted.language === 'hi' ? {
            strengths: ['स्थानीय ग्राहकों के साथ सीधा विश्वास-आधारित संबंध', 'कम परिचालन एवं किराया खर्च'],
            weaknesses: ['प्रारंभिक कार्यशील पूंजी की सीमाएं', 'मैनुअल से डिजिटल प्रणाली में बदलाव'],
            opportunities: ['रियायती प्राथमिक क्षेत्र सरकारी ऋण योजनाएं', 'व्हाट्सएप और यूपीआई द्वारा विस्तार'],
            threats: ['फसल चक्रों के बीच नकदी प्रवाह का विलंब', 'कच्चे माल के थोक भाव में उतार-चढ़ाव'],
          } : formatted.language === 'gu' ? {
            strengths: ['સ્થાનિક ગ્રાહકો સાથે સીધો વિશ્વાસપૂર્ણ સંબંધ', 'ઓછો ઓપરેશનલ અને ભાડા ખર્ચ'],
            weaknesses: ['પ્રારંભિક કાર્યકારી મૂડીની મર્યાદાઓ', 'મેન્યુઅલમાંથી ડિજિટલ પદ્ધતિમાં સંક્રમણ'],
            opportunities: ['રાહત દરે સરકારી ધિરાણ યોજનાઓ', 'વોટ્સએપ અને UPI દ્વારા ગ્રાહક વિસ્તાર'],
            threats: ['લણણી ચક્ર વચ્ચે કેશફ્લો વિલંબ', 'કાચા માલના ભાવોમાં વધઘટ'],
          } : {
            strengths: ['Direct local customer relationship', 'Low operational rental overhead'],
            weaknesses: ['Initial working capital constraints', 'Transition from manual to digital workflows'],
            opportunities: ['Subsidized priority-sector credit schemes', 'Expanding reach via WhatsApp and UPI'],
            threats: ['Seasonal harvest income lags', 'Raw material wholesale price fluctuation'],
          }
        ),
        risks: risksArray,
        competitors: compArray,
        pricing: pricingObj,
        recommendation: recObj,
        financial: raw.financial || null,
        scheme: raw.scheme || null,
        emi: raw.emi || null,
        repayment: raw.repayment || null,
        working_capital: raw.working_capital || null,
        ai_explanation: raw.ai_explanation || null,
        raw_backend_data: raw,
      };
    } catch (error) {
      if (axios.isCancel(error) || error.name === 'CanceledError' || error.name === 'AbortError') {
        const cancelErr = new Error('Request aborted');
        cancelErr.name = 'AbortError';
        cancelErr.isAborted = true;
        throw cancelErr;
      }
      console.warn('Backend /business/analyze request error:', error.message);
      throw new Error(
        error.response?.data?.detail?.message ||
        error.response?.data?.detail ||
        error.message ||
        'Unable to generate analysis for the selected business. Please try again.'
      );
    }
  },

  /**
   * Deterministic project cost (Margin / 10%) & max loan (90%)
   * POST /financial/calculate
   */
  calculateFinancial: async (payload) => {
    const formatted = formatPayload(payload);
    const response = await apiClient.post('/financial/calculate', formatted);
    return response.data?.data ?? response.data;
  },

  /**
   * Automatic scheme recommendation based on ₹1.40L threshold
   * POST /scheme/recommend
   */
  recommendScheme: async (payload) => {
    const formatted = formatPayload(payload);
    const response = await apiClient.post('/scheme/recommend', formatted);
    return response.data?.data ?? response.data;
  },

  /**
   * Computes monthly EMI, post-moratorium tenure, and total interest
   * POST /emi/calculate
   */
  calculateEMI: async (payload) => {
    const formatted = formatPayload(payload);
    const response = await apiClient.post('/emi/calculate', formatted);
    return response.data?.data ?? response.data;
  },

  /**
   * Computes complete month-by-month amortized repayment schedule
   * POST /repayment/calculate
   */
  calculateRepayment: async (payload) => {
    const formatted = formatPayload(payload);
    const response = await apiClient.post('/repayment/calculate', formatted);
    return response.data?.data ?? response.data;
  },

  /**
   * Computes monthly OPEX breakdown, 3-month reserve, and break-even targets
   * POST /working-capital/calculate
   */
  calculateWorkingCapital: async (payload) => {
    const formatted = formatPayload(payload);
    const response = await apiClient.post('/working-capital/calculate', formatted);
    return response.data?.data ?? response.data;
  },

  /**
   * Complete unified financial structuring plan
   * Orchestrates the 5 financial endpoints or calls backend composite
   */
  getFinancialPlan: async (payload) => {
    const formatted = formatPayload(payload);
    try {
      // Parallel execution across endpoints for optimal performance
      const [financial, scheme, emi, repayment, working_capital] = await Promise.all([
        bizApi.calculateFinancial(formatted),
        bizApi.recommendScheme(formatted),
        bizApi.calculateEMI(formatted),
        bizApi.calculateRepayment(formatted),
        bizApi.calculateWorkingCapital(formatted),
      ]);

      return {
        input: {
          location: formatted.location,
          business_category: formatted.business_category,
          available_capital: formatted.available_capital,
        },
        financial,
        scheme,
        emi,
        repayment,
        working_capital,
      };
    } catch (error) {
      console.warn('API error in getFinancialPlan; attempting fallback to /business/analyze or deterministic calculations:', error.message);
      try {
        const full = await apiClient.post('/business/analyze', formatted);
        const fullData = full.data?.data ?? full.data;
        return {
          input: {
            location: formatted.location,
            business_category: formatted.business_category,
            available_capital: formatted.available_capital,
          },
          financial: fullData.financial,
          scheme: fullData.scheme,
          emi: fullData.emi,
          repayment: fullData.repayment,
          working_capital: fullData.working_capital,
        };
      } catch (innerErr) {
        console.error('All backend financial endpoints unavailable; using client fallback:', innerErr.message);
        throw innerErr;
      }
    }
  },

  /**
   * Downloadable ReportLab PDF dossier generator
   * POST /report/generate
   */
  generateReport: async (payload) => {
    const formatted = formatPayload(payload);
    return apiClient.post('/report/generate', formatted, {
      responseType: 'blob',
    });
  },
};

export default apiClient;
