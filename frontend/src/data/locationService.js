/**
 * Centralized Location Data Model & Search Service (Phase B7)
 * Implements safe provider abstraction for rural village/town/taluka search.
 * Ensures offline resilience with zero hardcoded API keys and zero committed secrets.
 */

export function createLocationModel({
  raw_input = '',
  village_town_city = '',
  taluka_subdistrict = '',
  district = '',
  state = '',
  country = 'India',
  latitude = null,
  longitude = null,
  formatted_address = '',
  provider = 'local_catalog',
} = {}) {
  const parts = [village_town_city, taluka_subdistrict, district, state, country].filter(Boolean);
  const formatted = formatted_address || parts.join(', ') || raw_input;

  return {
    raw_input: raw_input || formatted,
    village_town_city,
    taluka_subdistrict,
    district,
    state,
    country,
    latitude,
    longitude,
    formatted_address: formatted,
    provider,
  };
}

export const RURAL_LOCATIONS_DATABASE = [
  // Gujarat - Anand & Kheda Hubs
  {
    village_town_city: 'Anand',
    taluka_subdistrict: 'Anand Taluka',
    district: 'Anand',
    state: 'Gujarat',
    country: 'India',
    latitude: 22.5645,
    longitude: 72.9289,
    tags: ['dairy hub', 'amul', 'charotar', 'vidyanagar', 'central gujarat'],
  },
  {
    village_town_city: 'Vallabh Vidyanagar',
    taluka_subdistrict: 'Anand Taluka',
    district: 'Anand',
    state: 'Gujarat',
    country: 'India',
    latitude: 22.5458,
    longitude: 72.9304,
    tags: ['education', 'charotar', 'engineering', 'youth market'],
  },
  {
    village_town_city: 'Petlad',
    taluka_subdistrict: 'Petlad Taluka',
    district: 'Anand',
    state: 'Gujarat',
    country: 'India',
    latitude: 22.4742,
    longitude: 72.8021,
    tags: ['textile', 'rural trade', 'tobacco', 'mandi'],
  },
  {
    village_town_city: 'Khambhat',
    taluka_subdistrict: 'Khambhat Taluka',
    district: 'Anand',
    state: 'Gujarat',
    country: 'India',
    latitude: 22.3129,
    longitude: 72.6192,
    tags: ['agate', 'coastal', 'halvasan', 'handicrafts', 'fisheries'],
  },
  {
    village_town_city: 'Borsad',
    taluka_subdistrict: 'Borsad Taluka',
    district: 'Anand',
    state: 'Gujarat',
    country: 'India',
    latitude: 22.4116,
    longitude: 72.9009,
    tags: ['charotar', 'tobacco', 'spices', 'agro mandi'],
  },
  {
    village_town_city: 'Nadiad',
    taluka_subdistrict: 'Nadiad Taluka',
    district: 'Kheda',
    state: 'Gujarat',
    country: 'India',
    latitude: 22.6916,
    longitude: 72.8634,
    tags: ['santram', 'textile', 'kheda', 'commercial town'],
  },
  {
    village_town_city: 'Dakor',
    taluka_subdistrict: 'Thasra Taluka',
    district: 'Kheda',
    state: 'Gujarat',
    country: 'India',
    latitude: 22.7547,
    longitude: 73.1501,
    tags: ['temple town', 'pilgrimage', 'gota', 'cottage industry', 'sweets'],
  },

  // Gujarat - Surat & South Gujarat Hubs
  {
    village_town_city: 'Bardoli',
    taluka_subdistrict: 'Bardoli Taluka',
    district: 'Surat',
    state: 'Gujarat',
    country: 'India',
    latitude: 21.1214,
    longitude: 73.1118,
    tags: ['sugar cooperative', 'satyagraha', 'agro processing', 'south gujarat'],
  },
  {
    village_town_city: 'Mandvi (Surat)',
    taluka_subdistrict: 'Mandvi Taluka',
    district: 'Surat',
    state: 'Gujarat',
    country: 'India',
    latitude: 21.2581,
    longitude: 73.3039,
    tags: ['tribal belt', 'agriculture', 'forestry', 'tapi'],
  },
  {
    village_town_city: 'Navsari',
    taluka_subdistrict: 'Navsari Taluka',
    district: 'Navsari',
    state: 'Gujarat',
    country: 'India',
    latitude: 20.9467,
    longitude: 72.952,
    tags: ['diamonds', 'chikoo', 'agriculture', 'textile'],
  },
  {
    village_town_city: 'Bilimora',
    taluka_subdistrict: 'Gandevi Taluka',
    district: 'Navsari',
    state: 'Gujarat',
    country: 'India',
    latitude: 20.76,
    longitude: 72.95,
    tags: ['chikoo processing', 'mango pulp', 'coastal trade'],
  },
  {
    village_town_city: 'Vyara',
    taluka_subdistrict: 'Vyara Taluka',
    district: 'Tapi',
    state: 'Gujarat',
    country: 'India',
    latitude: 21.1167,
    longitude: 73.4,
    tags: ['tribal crafts', 'bamboo', 'paddy', 'dairy'],
  },
  {
    village_town_city: 'Ahwa',
    taluka_subdistrict: 'Ahwa Taluka',
    district: 'Dang',
    state: 'Gujarat',
    country: 'India',
    latitude: 20.7578,
    longitude: 73.6841,
    tags: ['dang', 'bamboo handicrafts', 'forest produce', 'tribal artisans'],
  },
  {
    village_town_city: 'Ankleshwar',
    taluka_subdistrict: 'Ankleshwar Taluka',
    district: 'Bharuch',
    state: 'Gujarat',
    country: 'India',
    latitude: 21.6264,
    longitude: 73.0152,
    tags: ['industrial', 'msme cluster', 'logistics hub'],
  },
  {
    village_town_city: 'Rajpipla',
    taluka_subdistrict: 'Nandod Taluka',
    district: 'Narmada',
    state: 'Gujarat',
    country: 'India',
    latitude: 21.8711,
    longitude: 73.5028,
    tags: ['statue of unity corridor', 'tourism handicrafts', 'horticulture'],
  },

  // Gujarat - Saurashtra & Kutch Hubs
  {
    village_town_city: 'Rajkot',
    taluka_subdistrict: 'Rajkot Taluka',
    district: 'Rajkot',
    state: 'Gujarat',
    country: 'India',
    latitude: 22.3039,
    longitude: 70.8022,
    tags: ['engineering', 'auto components', 'diesel engines', 'saurashtra'],
  },
  {
    village_town_city: 'Gondal',
    taluka_subdistrict: 'Gondal Taluka',
    district: 'Rajkot',
    state: 'Gujarat',
    country: 'India',
    latitude: 21.9619,
    longitude: 70.7997,
    tags: ['chilli mandi', 'groundnut', 'oil mills', 'heritage tourism'],
  },
  {
    village_town_city: 'Morbi',
    taluka_subdistrict: 'Morbi Taluka',
    district: 'Morbi',
    state: 'Gujarat',
    country: 'India',
    latitude: 22.812,
    longitude: 70.8378,
    tags: ['ceramics', 'clock manufacturing', 'wall tiles', 'export cluster'],
  },
  {
    village_town_city: 'Bhuj',
    taluka_subdistrict: 'Bhuj Taluka',
    district: 'Kutch',
    state: 'Gujarat',
    country: 'India',
    latitude: 23.242,
    longitude: 69.6669,
    tags: ['kutch embroidery', 'handicrafts', 'rogan art', 'handloom', 'heritage'],
  },
  {
    village_town_city: 'Mandvi (Kutch)',
    taluka_subdistrict: 'Mandvi Taluka',
    district: 'Kutch',
    state: 'Gujarat',
    country: 'India',
    latitude: 22.8333,
    longitude: 69.35,
    tags: ['wooden shipbuilding', 'coastal port', 'dates harvesting'],
  },
  {
    village_town_city: 'Anjar',
    taluka_subdistrict: 'Anjar Taluka',
    district: 'Kutch',
    state: 'Gujarat',
    country: 'India',
    latitude: 23.1139,
    longitude: 70.0278,
    tags: ['textile', 'cutlery', 'metalcrafts', 'kutch trade'],
  },
  {
    village_town_city: 'Junagadh',
    taluka_subdistrict: 'Junagadh Taluka',
    district: 'Junagadh',
    state: 'Gujarat',
    country: 'India',
    latitude: 21.5222,
    longitude: 70.4579,
    tags: ['gir nar', 'kesar mango', 'groundnut oil', 'agro mandi'],
  },
  {
    village_town_city: 'Veraval',
    taluka_subdistrict: 'Patan-Veraval Taluka',
    district: 'Gir Somnath',
    state: 'Gujarat',
    country: 'India',
    latitude: 20.9,
    longitude: 70.3667,
    tags: ['fisheries port', 'fish processing', 'somnath temple'],
  },
  {
    village_town_city: 'Amreli',
    taluka_subdistrict: 'Amreli Taluka',
    district: 'Amreli',
    state: 'Gujarat',
    country: 'India',
    latitude: 21.6032,
    longitude: 71.2221,
    tags: ['cotton ginning', 'diamond polishing', 'groundnut'],
  },
  {
    village_town_city: 'Bhavnagar',
    taluka_subdistrict: 'Bhavnagar Taluka',
    district: 'Bhavnagar',
    state: 'Gujarat',
    country: 'India',
    latitude: 21.7645,
    longitude: 72.1519,
    tags: ['onion dehydration', 'ganthiya snacks', 'diamond'],
  },
  {
    village_town_city: 'Mahuva',
    taluka_subdistrict: 'Mahuva Taluka',
    district: 'Bhavnagar',
    state: 'Gujarat',
    country: 'India',
    latitude: 21.0914,
    longitude: 71.7634,
    tags: ['dehydrated onion', 'garlic', 'wooden toys', 'coconut farming'],
  },
  {
    village_town_city: 'Surendranagar',
    taluka_subdistrict: 'Wadhwan Taluka',
    district: 'Surendranagar',
    state: 'Gujarat',
    country: 'India',
    latitude: 22.7277,
    longitude: 71.637,
    tags: ['cotton hub', 'ginning', 'salt production'],
  },

  // Gujarat - North & Central Gujarat Hubs
  {
    village_town_city: 'Gandhinagar',
    taluka_subdistrict: 'Gandhinagar Taluka',
    district: 'Gandhinagar',
    state: 'Gujarat',
    country: 'India',
    latitude: 23.2156,
    longitude: 72.6369,
    tags: ['capital', 'it hub', 'green city', 'electronics'],
  },
  {
    village_town_city: 'Sanand',
    taluka_subdistrict: 'Sanand Taluka',
    district: 'Ahmedabad',
    state: 'Gujarat',
    country: 'India',
    latitude: 22.9868,
    longitude: 72.3813,
    tags: ['auto manufacturing', 'semiconductor', 'fmcg cluster'],
  },
  {
    village_town_city: 'Mehsana',
    taluka_subdistrict: 'Mehsana Taluka',
    district: 'Mehsana',
    state: 'Gujarat',
    country: 'India',
    latitude: 23.588,
    longitude: 72.3693,
    tags: ['dudh sagar dairy', 'oil and gas', 'spices mandi', 'cumin'],
  },
  {
    village_town_city: 'Unjha',
    taluka_subdistrict: 'Unjha Taluka',
    district: 'Mehsana',
    state: 'Gujarat',
    country: 'India',
    latitude: 23.8039,
    longitude: 72.3925,
    tags: ['asia largest spice market', 'cumin', 'isabgol', 'mustard'],
  },
  {
    village_town_city: 'Palanpur',
    taluka_subdistrict: 'Palanpur Taluka',
    district: 'Banaskantha',
    state: 'Gujarat',
    country: 'India',
    latitude: 24.1724,
    longitude: 72.4346,
    tags: ['banas dairy', 'potato cold storage', 'attar perfumes'],
  },
  {
    village_town_city: 'Deesa',
    taluka_subdistrict: 'Deesa Taluka',
    district: 'Banaskantha',
    state: 'Gujarat',
    country: 'India',
    latitude: 24.2586,
    longitude: 72.1797,
    tags: ['potato hub', 'cold storage cluster', 'groundnut'],
  },
  {
    village_town_city: 'Himatnagar',
    taluka_subdistrict: 'Himatnagar Taluka',
    district: 'Sabarkantha',
    state: 'Gujarat',
    country: 'India',
    latitude: 23.5977,
    longitude: 72.9698,
    tags: ['sabar dairy', 'ceramic tiles', 'cotton'],
  },
  {
    village_town_city: 'Dahod',
    taluka_subdistrict: 'Dahod Taluka',
    district: 'Dahod',
    state: 'Gujarat',
    country: 'India',
    latitude: 22.8375,
    longitude: 74.2536,
    tags: ['tribal hub', 'locomotive', 'maize', 'pulses'],
  },
  {
    village_town_city: 'Godhra',
    taluka_subdistrict: 'Godhra Taluka',
    district: 'Panchmahal',
    state: 'Gujarat',
    country: 'India',
    latitude: 22.7758,
    longitude: 73.6149,
    tags: ['panchamrut dairy', 'flour mills', 'timber'],
  },
  {
    village_town_city: 'Chhota Udaipur',
    taluka_subdistrict: 'Chhota Udaipur Taluka',
    district: 'Chhota Udaipur',
    state: 'Gujarat',
    country: 'India',
    latitude: 22.3089,
    longitude: 74.015,
    tags: ['pithora painting', 'tribal crafts', 'dolomite'],
  },

  // Key National Agrarian & Rural Hubs
  {
    village_town_city: 'Kolhapur',
    taluka_subdistrict: 'Karveer Taluka',
    district: 'Kolhapur',
    state: 'Maharashtra',
    country: 'India',
    latitude: 16.705,
    longitude: 74.2433,
    tags: ['kolhapuri chappal', 'jaggery mandi', 'sugarcane'],
  },
  {
    village_town_city: 'Baramati',
    taluka_subdistrict: 'Baramati Taluka',
    district: 'Pune',
    state: 'Maharashtra',
    country: 'India',
    latitude: 18.1517,
    longitude: 74.577,
    tags: ['agro tourism', 'sugarcane', 'dairy', 'poultry'],
  },
  {
    village_town_city: 'Varanasi',
    taluka_subdistrict: 'Varanasi Taluka',
    district: 'Varanasi',
    state: 'Uttar Pradesh',
    country: 'India',
    latitude: 25.3176,
    longitude: 82.9739,
    tags: ['banarasi saree', 'silk weaving', 'handloom cluster'],
  },
  {
    village_town_city: 'Gorakhpur',
    taluka_subdistrict: 'Gorakhpur Sadar',
    district: 'Gorakhpur',
    state: 'Uttar Pradesh',
    country: 'India',
    latitude: 26.7606,
    longitude: 83.3732,
    tags: ['terracotta craft', 'agro mandi', 'sugarcane'],
  },
  {
    village_town_city: 'Indore',
    taluka_subdistrict: 'Indore Taluka',
    district: 'Indore',
    state: 'Madhya Pradesh',
    country: 'India',
    latitude: 22.7196,
    longitude: 75.8577,
    tags: ['soybean mandi', 'namkeen snacks', 'textile'],
  },
  {
    village_town_city: 'Jodhpur',
    taluka_subdistrict: 'Jodhpur Taluka',
    district: 'Jodhpur',
    state: 'Rajasthan',
    country: 'India',
    latitude: 26.2389,
    longitude: 73.0243,
    tags: ['wooden furniture export', 'handicrafts', 'spices'],
  },
  {
    village_town_city: 'Coimbatore',
    taluka_subdistrict: 'Coimbatore South',
    district: 'Coimbatore',
    state: 'Tamil Nadu',
    country: 'India',
    latitude: 11.0168,
    longitude: 76.9558,
    tags: ['textile machinery', 'motor pumps', 'poultry'],
  },
];

/**
 * Offline-first location search matching village, taluka, district, or tags.
 */
export async function searchLocations(query = '', limit = 8) {
  const cleanQ = (query || '').trim().toLowerCase();

  // If query is empty, return top prominent regional centers
  if (!cleanQ) {
    return RURAL_LOCATIONS_DATABASE.slice(0, 5).map((item) =>
      createLocationModel({
        ...item,
        raw_input: `${item.village_town_city}, ${item.state}`,
        provider: 'local_catalog',
      })
    );
  }

  const matches = [];

  // 1. Matches on town/village
  for (const loc of RURAL_LOCATIONS_DATABASE) {
    const city = loc.village_town_city.toLowerCase();
    if (city.startsWith(cleanQ) || city.includes(cleanQ)) {
      if (!matches.some((m) => m.village_town_city === loc.village_town_city)) {
        matches.push(loc);
      }
    }
  }

  // 2. Matches on Taluka or District
  for (const loc of RURAL_LOCATIONS_DATABASE) {
    const taluka = (loc.taluka_subdistrict || '').toLowerCase();
    const district = (loc.district || '').toLowerCase();
    const state = (loc.state || '').toLowerCase();
    if (taluka.includes(cleanQ) || district.includes(cleanQ) || state.includes(cleanQ)) {
      if (!matches.some((m) => m.village_town_city === loc.village_town_city)) {
        matches.push(loc);
      }
    }
  }

  // 3. Matches on descriptive tags
  for (const loc of RURAL_LOCATIONS_DATABASE) {
    const tags = loc.tags || [];
    if (tags.some((t) => t.toLowerCase().includes(cleanQ))) {
      if (!matches.some((m) => m.village_town_city === loc.village_town_city)) {
        matches.push(loc);
      }
    }
  }

  const results = matches.slice(0, limit).map((loc) =>
    createLocationModel({
      ...loc,
      raw_input: query,
      provider: 'local_catalog',
    })
  );

  // If no match found in database, provide a structured fallback model
  if (results.length === 0) {
    results.push(
      createLocationModel({
        raw_input: query.trim(),
        village_town_city: query.trim(),
        state: cleanQ.includes('gujarat') ? 'Gujarat' : '',
        country: 'India',
        formatted_address: `${query.trim()}, India`,
        provider: 'user_custom',
      })
    );
  }

  return results;
}
