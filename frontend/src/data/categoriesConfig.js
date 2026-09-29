/**
 * Centralized Business Category Configuration (Phase B7)
 * Consolidates all 31 supported rural micro-enterprise categories with structured metadata.
 * Provides sector categorization, capex benchmarks, subcategories, and search parameters.
 */

export const BUSINESS_CATEGORIES = [
  // ------------------------------------------------------------------------
  // Sector 1: Agriculture & Allied Sectors
  // ------------------------------------------------------------------------
  {
    id: 'agriculture',
    value: 'Agriculture',
    sector: 'Agriculture & Allied',
    typicalCapexMin: 50000,
    typicalCapexMax: 1500000,
    subcategories: ['Commercial Horticulture', 'Organic Cash Crops', 'Protected Polyhouse', 'Seed Multiplier'],
    competitorSearchTerms: ['progressive farmers', 'contract farming agents', 'APMC traders', 'farm mandis'],
    tags: ['farming', 'horticulture', 'crops', 'organic', 'soil'],
    icon: '🌾',
  },
  {
    id: 'dairy',
    value: 'Dairy',
    sector: 'Agriculture & Allied',
    typicalCapexMin: 75000,
    typicalCapexMax: 2000000,
    subcategories: ['Milk Collection Centre', 'Livestock Rearing', 'Paneer & Curd Processing', 'Desi Bilona Ghee'],
    competitorSearchTerms: ['Amul village society', 'private dairy aggregators', 'dudh mandali', 'sweet makers'],
    tags: ['milk', 'livestock', 'paneer', 'ghee', 'cattle'],
    icon: '🥛',
  },
  {
    id: 'poultry',
    value: 'Poultry',
    sector: 'Agriculture & Allied',
    typicalCapexMin: 80000,
    typicalCapexMax: 1800000,
    subcategories: ['Broiler Farming (Meat)', 'Layer Farming (Eggs)', 'Country Fowl (Desi Murghi)', 'Chick Brooding'],
    competitorSearchTerms: ['commercial broiler integration', 'wholesale egg merchants', 'local poultry farms'],
    tags: ['chicken', 'eggs', 'broiler', 'layer', 'poultry'],
    icon: '🐔',
  },
  {
    id: 'goat_farming',
    value: 'Goat Farming',
    sector: 'Agriculture & Allied',
    typicalCapexMin: 60000,
    typicalCapexMax: 1200000,
    subcategories: ['Stall-Fed Goat Unit (20+1)', 'Breeding Farm (Sirohi/Barbari)', 'Therapeutic Goat Milk', 'Festive Fattening'],
    competitorSearchTerms: ['local goat herders', 'livestock mandis', 'festive meat buyers'],
    tags: ['goat', 'bakri', 'livestock', 'stall-fed', 'breeding'],
    icon: '🐐',
  },
  {
    id: 'fisheries',
    value: 'Fisheries',
    sector: 'Agriculture & Allied',
    typicalCapexMin: 90000,
    typicalCapexMax: 2200000,
    subcategories: ['Inland Pond Aquaculture', 'Biofloc Intensive Fish Farming', 'Prawn/Shrimp Culture', 'Ornamental Fish'],
    competitorSearchTerms: ['district fish mandis', 'panchayat pond leaseholders', 'freshwater hatcheries'],
    tags: ['fish', 'aquaculture', 'biofloc', 'rohu', 'shrimp'],
    icon: '🐟',
  },
  {
    id: 'beekeeping',
    value: 'Beekeeping',
    sector: 'Agriculture & Allied',
    typicalCapexMin: 40000,
    typicalCapexMax: 600000,
    subcategories: ['Raw Multiflora Honey', 'Monofloral Mustard/Litchi Honey', 'Bee Wax Extraction', 'Orchard Crop Pollination'],
    competitorSearchTerms: ['Khadi honey units', 'migratory beekeepers', 'organic honey packers'],
    tags: ['honey', 'bees', 'apiary', 'wax', 'pollination'],
    icon: '🐝',
  },
  {
    id: 'nursery_plant',
    value: 'Nursery & Plant Business',
    sector: 'Agriculture & Allied',
    typicalCapexMin: 50000,
    typicalCapexMax: 1000000,
    subcategories: ['Vegetable Pro-Tray Seedlings', 'Fruit Tree Grafting', 'Ornamental & Balcony Plants', 'Herbal Saplings'],
    competitorSearchTerms: ['government horticulture nursery', 'roadside plant nurseries', 'seedling growers'],
    tags: ['plants', 'seedlings', 'nursery', 'grafting', 'gardening'],
    icon: '🌱',
  },
  {
    id: 'agri_equipment_rental',
    value: 'Agricultural Equipment Rental',
    sector: 'Agriculture & Allied',
    typicalCapexMin: 100000,
    typicalCapexMax: 2500000,
    subcategories: ['Custom Hiring Centre (CHC)', 'Tractor & Rotavator Rental', 'Thresher & Harvester', 'Drone Precision Spraying'],
    competitorSearchTerms: ['tractor owners', 'village custom hiring centres', 'combine thresher hirers'],
    tags: ['tractor', 'rotavator', 'thresher', 'implements', 'drone'],
    icon: '🚜',
  },
  {
    id: 'agri_input_store',
    value: 'Agricultural Input Store',
    sector: 'Agriculture & Allied',
    typicalCapexMin: 75000,
    typicalCapexMax: 2000000,
    subcategories: ['Certified Seeds & Hybrid Grains', 'Fertilizers & Bio-Nutrients', 'Crop Protection Spray', 'Drip Spares & Tools'],
    competitorSearchTerms: ['IFFCO societies', 'taluka agro agencies', 'private pesticide dealers'],
    tags: ['seeds', 'fertilizer', 'pesticide', 'drip irrigation', 'agro store'],
    icon: '🧪',
  },

  // ------------------------------------------------------------------------
  // Sector 2: Food & Agro-Processing
  // ------------------------------------------------------------------------
  {
    id: 'grocery',
    value: 'Grocery / Kirana',
    sector: 'Retail & Provision',
    typicalCapexMin: 50000,
    typicalCapexMax: 1500000,
    subcategories: ['Daily Staples & Grains', 'Packaged FMCG & Personal Care', 'Loose Spices & Pulses', 'Village Quick Delivery'],
    competitorSearchTerms: ['village general stores', 'taluka supermarkets', 'PDS ration shops'],
    tags: ['kirana', 'grocery', 'ration', 'fmcg', 'staples'],
    icon: '🛒',
  },
  {
    id: 'food_processing',
    value: 'Food Processing',
    sector: 'Food & Processing',
    typicalCapexMin: 60000,
    typicalCapexMax: 2500000,
    subcategories: ['Spice Pulverizing & Blending', 'Extruded Snack Production', 'Grain Sorting & Grading', 'Traditional Mixes'],
    competitorSearchTerms: ['spice brands', 'namkeen factories', 'regional millers'],
    tags: ['spices', 'pulverizer', 'snacks', 'processing', 'flour'],
    icon: '⚙️',
  },
  {
    id: 'bakery',
    value: 'Bakery',
    sector: 'Food & Processing',
    typicalCapexMin: 65000,
    typicalCapexMax: 1800000,
    subcategories: ['Fresh Daily Bread & Pav', 'Tea Rusk & Khari Biscuits', 'Custom Birthday Cakes', 'Artisanal Cookies'],
    competitorSearchTerms: ['packaged bread vendors', 'town bakeries', 'tea stall suppliers'],
    tags: ['bread', 'pav', 'rusk', 'cakes', 'oven'],
    icon: '🍞',
  },
  {
    id: 'snacks_namkeen',
    value: 'Snacks & Namkeen',
    sector: 'Food & Processing',
    typicalCapexMin: 50000,
    typicalCapexMax: 1400000,
    subcategories: ['Sev, Ganthiya & Bhavnagari', 'Banana & Potato Wafers', 'Spiced Chivda & Mixtures', 'Impulse ₹5/₹10 Packets'],
    competitorSearchTerms: ['Balaji distributors', 'farsan shops', 'haat vendors'],
    tags: ['namkeen', 'farsan', 'sev', 'ganthiya', 'wafers'],
    icon: '🥨',
  },
  {
    id: 'pickles_papad',
    value: 'Pickles & Papad',
    sector: 'Food & Processing',
    typicalCapexMin: 35000,
    typicalCapexMax: 800000,
    subcategories: ['Traditional Mango & Lime Pickles', 'Moong/Urad Dal Papad', 'Khakhra & Thepla', 'Chutneys & Murabba'],
    competitorSearchTerms: ['Lijjat papad sellers', 'pickle brands', 'SHG home producers'],
    tags: ['pickle', 'papad', 'achar', 'khakhra', 'shg'],
    icon: '🏺',
  },
  {
    id: 'flour_mill',
    value: 'Flour Mill',
    sector: 'Food & Processing',
    typicalCapexMin: 45000,
    typicalCapexMax: 900000,
    subcategories: ['Wheat Atta Grinding', 'Multi-grain & Millet (Bajra/Jowar)', 'Besan Pulverizing', 'Custom Jobwork Chakki'],
    competitorSearchTerms: ['neighborhood chakkis', 'packaged atta brands', 'commercial mills'],
    tags: ['atta', 'chakki', 'millet', 'besan', 'grinding'],
    icon: '🌾',
  },
  {
    id: 'fruit_veg_processing',
    value: 'Fruit & Vegetable Processing',
    sector: 'Food & Processing',
    typicalCapexMin: 80000,
    typicalCapexMax: 2400000,
    subcategories: ['Mango/Guava Pulp Canning', 'Solar Dehydrated Onion/Garlic Flakes', 'Jams, Squashes & Ketchups', 'Frozen Veggies'],
    competitorSearchTerms: ['industrial pulp processors', 'onion dehydration plants', 'canning units'],
    tags: ['pulp', 'mango', 'dehydration', 'onion flakes', 'canning'],
    icon: '🍅',
  },

  // ------------------------------------------------------------------------
  // Sector 3: Textiles, Manufacturing & Crafts
  // ------------------------------------------------------------------------
  {
    id: 'textile_clothing',
    value: 'Textile & Clothing',
    sector: 'Textiles & Apparel',
    typicalCapexMin: 50000,
    typicalCapexMax: 1500000,
    subcategories: ['Readymade Garment Store', 'Alterations & Fitting', 'Ethnic Wear & Sarees', 'School Uniforms on Contract'],
    competitorSearchTerms: ['town clothing showrooms', 'weekly textile haats', 'tailor shops'],
    tags: ['clothing', 'garments', 'kurti', 'saree', 'uniform'],
    icon: '👕',
  },
  {
    id: 'tailoring_embroidery',
    value: 'Tailoring & Embroidery',
    sector: 'Textiles & Apparel',
    typicalCapexMin: 35000,
    typicalCapexMax: 800000,
    subcategories: ['Designer Blouse & Kurti Stitching', 'Computerized Multi-Head Embroidery', 'Zari, Aari & Mirror Detailing', 'Bridal Lehengas'],
    competitorSearchTerms: ['boutiques', 'embroidery jobwork', 'home seamstresses'],
    tags: ['tailoring', 'embroidery', 'blouse', 'zari', 'stitching'],
    icon: '🪡',
  },
  {
    id: 'handicrafts',
    value: 'Handicrafts',
    sector: 'Artisan & Crafts',
    typicalCapexMin: 40000,
    typicalCapexMax: 1000000,
    subcategories: ['Handloom Weaving & Block Print', 'Artisan Cultural Decor', 'Traditional Woodcraft', 'Eco-friendly Festival Art'],
    competitorSearchTerms: ['artisan cooperatives', 'handicraft emporiums', 'craft traders'],
    tags: ['handicraft', 'artisan', 'handloom', 'heritage', 'decor'],
    icon: '🎨',
  },
  {
    id: 'pottery',
    value: 'Pottery',
    sector: 'Artisan & Crafts',
    typicalCapexMin: 30000,
    typicalCapexMax: 750000,
    subcategories: ['Terracotta Water Dispensers (Matka)', 'Natural Clay Cookware (Biryani pots)', 'Decorative Garden Planters', 'Festive Clay Diyas'],
    competitorSearchTerms: ['kumhar clusters', 'roadside nurseries', 'festive clay stalls'],
    tags: ['pottery', 'clay', 'matka', 'terracotta', 'diyas'],
    icon: '🪴',
  },
  {
    id: 'furniture',
    value: 'Furniture',
    sector: 'Wood & Manufacturing',
    typicalCapexMin: 75000,
    typicalCapexMax: 2000000,
    subcategories: ['Solid Wood Beds & Storage Almirahs', 'Modular Kitchen Cabinetry', 'School Desks & Benches', 'Re-Upholstery & Polishing'],
    competitorSearchTerms: ['timber merchants', 'furniture showrooms', 'carpenter workshops'],
    tags: ['furniture', 'wood', 'bed', 'almirah', 'carpentry'],
    icon: '🪑',
  },
  {
    id: 'bamboo_products',
    value: 'Bamboo Products',
    sector: 'Artisan & Crafts',
    typicalCapexMin: 35000,
    typicalCapexMax: 850000,
    subcategories: ['Eco-friendly Baskets & Hampers', 'Treated Bamboo Fencing & Gazebos', 'Bamboo Dining Ware', 'Lamp Shades & Blinds'],
    competitorSearchTerms: ['plastic crate sellers', 'basket weavers', 'eco packaging suppliers'],
    tags: ['bamboo', 'baskets', 'eco-friendly', 'fencing', 'cane'],
    icon: '🎋',
  },
  {
    id: 'leather_products',
    value: 'Leather Products',
    sector: 'Artisan & Crafts',
    typicalCapexMin: 45000,
    typicalCapexMax: 950000,
    subcategories: ['Traditional Handcrafted Juttis & Chappals', 'Heavy-Duty Agrarian Work Boots', 'Leather Belts & Wallets', 'Livestock Harnesses'],
    competitorSearchTerms: ['shoe stores', 'synthetic footwear sellers', 'cobbler workshops'],
    tags: ['leather', 'footwear', 'chappals', 'boots', 'belts'],
    icon: '👞',
  },

  // ------------------------------------------------------------------------
  // Sector 4: Services, Repair & Digital
  // ------------------------------------------------------------------------
  {
    id: 'mobile_repair',
    value: 'Mobile Repair',
    sector: 'Repairs & Technical',
    typicalCapexMin: 40000,
    typicalCapexMax: 700000,
    subcategories: ['Smartphone Screen & Folder Repair', 'Charging Jack & Mic SMD Soldering', 'Battery Replacement', 'Accessories & Tempered Glass'],
    competitorSearchTerms: ['town mobile centers', 'brand service outlets', 'recharge kiosks'],
    tags: ['mobile', 'smartphone', 'repair', 'screen', 'soldering'],
    icon: '📱',
  },
  {
    id: 'electronics_repair',
    value: 'Electronics Repair',
    sector: 'Repairs & Technical',
    typicalCapexMin: 45000,
    typicalCapexMax: 850000,
    subcategories: ['Home Inverter & Solar Controller PCB', 'LED TV Power Supply Boards', 'Submersible Pump Starter Panels', 'Appliance Motor Rewinding'],
    competitorSearchTerms: ['village electricians', 'TV service centres', 'motor rewinding shops'],
    tags: ['electronics', 'inverter', 'solar', 'tv', 'pump starter'],
    icon: '⚡',
  },
  {
    id: 'two_wheeler_repair',
    value: 'Two-Wheeler Repair',
    sector: 'Repairs & Technical',
    typicalCapexMin: 60000,
    typicalCapexMax: 1200000,
    subcategories: ['Motorcycle Periodic Servicing & Oil Change', 'Engine Valve & Piston Overhaul', 'Tubeless Puncture & Tire Fitment', 'Electric Scooter Diagnostics'],
    competitorSearchTerms: ['OEM dealer service points', 'roadside mechanics', 'spare parts garages'],
    tags: ['bike', 'motorcycle', 'service', 'engine oil', 'scooter'],
    icon: '🛵',
  },
  {
    id: 'computer_printing',
    value: 'Computer / Printing Centre',
    sector: 'Services & Digital',
    typicalCapexMin: 45000,
    typicalCapexMax: 900000,
    subcategories: ['High-Volume Document Photocopy & Binding', 'Flex Banner & Vinyl Signage', 'Passport Photos & Lamination', 'Stationery Supplies'],
    competitorSearchTerms: ['xerox centers', 'flex banner printers', 'court stationers'],
    tags: ['photocopy', 'xerox', 'printing', 'flex banner', 'lamination'],
    icon: '🖨️',
  },
  {
    id: 'digital_services',
    value: 'Digital Services',
    sector: 'Services & Digital',
    typicalCapexMin: 40000,
    typicalCapexMax: 650000,
    subcategories: ['CSC Government Scheme Portals', 'AePS Biometric Cash Withdrawal / Micro-ATM', 'PAN/Aadhaar/Voter Card Support', 'Online Exam & Job Applications'],
    competitorSearchTerms: ['panchayat e-gram', 'post office', 'banking correspondent CSPs'],
    tags: ['csc', 'aeps', 'micro-atm', 'schemes', 'aadhaar'],
    icon: '💻',
  },
  {
    id: 'transport_logistics',
    value: 'Transport / Local Logistics',
    sector: 'Services & Digital',
    typicalCapexMin: 85000,
    typicalCapexMax: 2200000,
    subcategories: ['Farm-to-Mandi Produce Freight', 'Village Kirana Delivery Routes', 'E-commerce Last-Mile Delivery Hub', 'Passenger Rural Feeder Auto'],
    competitorSearchTerms: ['tempo unions', 'pickup truck drivers', 'courier delivery franchisees'],
    tags: ['transport', 'logistics', 'tempo', 'delivery', 'mandi freight'],
    icon: '🚚',
  },
  {
    id: 'beauty_salon',
    value: 'Beauty & Salon',
    sector: 'Personal Grooming',
    typicalCapexMin: 40000,
    typicalCapexMax: 900000,
    subcategories: ['Bridal Makeover & Wedding Makeup', 'Men Hair Styling & Grooming', 'Herbal Facial & Skin Care', 'Hair Treatments & Mehendi'],
    competitorSearchTerms: ['village barbers', 'home parlors', 'town salons'],
    tags: ['salon', 'parlour', 'beauty', 'bridal', 'grooming'],
    icon: '💇',
  },
  {
    id: 'services',
    value: 'Services',
    sector: 'Repairs & Technical',
    typicalCapexMin: 50000,
    typicalCapexMax: 1000000,
    subcategories: ['Welding & Metal Fabrication', 'Tractor Trolley & Gate Making', 'Plumbing & Hardware Maintenance', 'Custom Mechanical Repairs'],
    competitorSearchTerms: ['fabrication workshops', 'welding garages', 'general technicians'],
    tags: ['welding', 'fabrication', 'repairs', 'maintenance', 'gate'],
    icon: '🛠️',
  },
];

/**
 * Helper utilities for working with business categories.
 */

export function getAllCategories() {
  return BUSINESS_CATEGORIES;
}

export function getCategoryById(id) {
  if (!id) return null;
  return BUSINESS_CATEGORIES.find((c) => c.id.toLowerCase() === id.toLowerCase()) || null;
}

export function getCategoryByValue(value) {
  if (!value) return null;
  const v = value.trim().toLowerCase();
  return (
    BUSINESS_CATEGORIES.find((c) => c.value.toLowerCase() === v) ||
    BUSINESS_CATEGORIES.find((c) => c.subcategories.some((s) => s.toLowerCase() === v)) ||
    null
  );
}

export function getCategoriesBySector(sector) {
  if (!sector) return BUSINESS_CATEGORIES;
  return BUSINESS_CATEGORIES.filter((c) => c.sector.toLowerCase() === sector.toLowerCase());
}

export function getSectors() {
  const sectors = new Set(BUSINESS_CATEGORIES.map((c) => c.sector));
  return Array.from(sectors);
}
