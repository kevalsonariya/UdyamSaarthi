"""
Centralized Business Category Configuration for Phase B7.
Defines all 31 supported rural micro-enterprise categories with structured metadata:
- id
- display name
- sector
- backend canonical value
- subcategories
- competitor search terms
- pricing/product profile
- market profile
- location factors
- opportunity profile
- risk profile
- capex ranges
"""

from typing import Dict, Any, List, Optional
from app.schemas.schemas import CategoryMetadataItem

CATEGORIES_REGISTRY: List[Dict[str, Any]] = [
    # -------------------------------------------------------------
    # 1. Agriculture & Allied Sectors
    # -------------------------------------------------------------
    {
        "id": "agriculture",
        "name": "Agriculture",
        "display_name": "Agriculture",
        "backend_value": "Agriculture",
        "sector": "Agriculture & Allied",
        "typical_capex_min": 50000.0,
        "typical_capex_max": 1500000.0,
        "subcategories": ["Commercial Horticulture", "Organic Cash Crops", "Protected Cultivation", "Seed Multiplying"],
        "competitor_search_terms": ["progressive farmers", "contract farming agents", "APMC traders", "local farm mandis"],
        "primary_activities": ["Land preparation and organic bed conditioning", "Drip irrigation deployment", "Harvest sorting and grading", "Direct mandi and trader dispatch"],
        "key_equipment": ["Micro-irrigation drip kits", "Solar pump set / power tiller", "Spraying equipment", "Crate storage"],
        "mandatory_licenses": ["Farmer Registration / KCC Card", "Panchayat Agriculture Clearance", "Udyam MSME (for value-add)"],
        "location_factors": {
            "water_availability": "High (borewell or canal access mandatory)",
            "soil_suitability": "Loamy/Alluvial soil optimal",
            "mandi_distance_km": 15,
            "road_connectivity": "Pukka farm-to-market road preferred"
        },
        "market_profile": {
            "catchment_radius_km": 25,
            "target_population": 45000,
            "customer_segments": ["Wholesale mandi aggregators", "Town vegetable vendors", "Rural food processing units"],
            "channels": ["Direct farm gate collection", "District APMC yards", "Local weekly haats"],
            "peak_seasons": ["Rabi post-harvest (March-April)", "Kharif post-harvest (October-November)"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["Exotic vegetables (capsicum, broccoli)", "Certified residue-free produce", "Direct farm-to-table supply"],
            "unmet_needs": ["Cold chain pre-cooling at village cluster", "Quality grading at source"],
            "ecosystem_drivers": ["State micro-irrigation subsidies", "National mission on edible oils and horticulture"]
        },
        "risk_profile": {
            "primary_risks": ["Unseasonal rainfall / hail damage", "Harvest price crash at APMC mandi"],
            "mitigation_strategies": ["Adopt staggered harvesting cycles", "Opt for PM Fasal Bima Yojana crop insurance"]
        },
        "pricing_profile": {
            "benchmark_product": "1 Quintal Grade-A Seasonal Horticultural Produce",
            "unit_cost": "₹900 - ₹1,200 / quintal",
            "retail_price": "₹1,800 - ₹2,600 / quintal",
            "target_gross_margin_percent": 52.0
        }
    },
    {
        "id": "dairy",
        "name": "Dairy",
        "display_name": "Dairy",
        "backend_value": "Dairy",
        "sector": "Agriculture & Allied",
        "typical_capex_min": 75000.0,
        "typical_capex_max": 2000000.0,
        "subcategories": ["Milk Collection Centre", "Livestock Rearing", "Paneer & Curd Processing", "Indigenous Ghee"],
        "competitor_search_terms": ["village milk cooperative society", "private dairy aggregators", "local dudh mandali", "sweet shop contractors"],
        "primary_activities": ["Hygienic morning/evening milk collection", "Fat and SNF digital testing", "Chilled bulk storage", "Local door-to-door distribution"],
        "key_equipment": ["Bulk milk chiller (300-500L)", "Digital fat analyzer", "Stainless steel 40L cans", "Cream separator"],
        "mandatory_licenses": ["FSSAI Basic Food Registration", "Panchayat Livestock Clearance", "Udyam MSME Certificate"],
        "location_factors": {
            "green_fodder_access": "Continuous green and dry fodder supply nearby",
            "veterinary_care": "Within 5 km radius of government animal dispensary",
            "power_continuity": "Three-phase electricity with backup generator"
        },
        "market_profile": {
            "catchment_radius_km": 15,
            "target_population": 30000,
            "customer_segments": ["Village & town households", "Tea stalls and canteens", "Town confectionery and sweet makers"],
            "channels": ["Daily morning/evening home delivery", "Direct milk cooperative collection", "Counter sales"],
            "peak_seasons": ["Winter flush season (November-February)", "Wedding/festive seasons"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["Desi A2 cow milk and bilona ghee", "Fresh vacuum-packed Malai Paneer"],
            "unmet_needs": ["Unadulterated morning milk delivery in peri-urban belts"],
            "ecosystem_drivers": ["Dairy cooperative infrastructure funds", "KCC concessional livestock credit"]
        },
        "risk_profile": {
            "primary_risks": ["Cattle infectious diseases", "Fodder price inflation during summer"],
            "mitigation_strategies": ["Comprehensive livestock insurance", "Silage pit fodder storage for dry months"]
        },
        "pricing_profile": {
            "benchmark_product": "1 Litre Fresh Cow/Buffalo Milk & 1 Kg Fresh Paneer",
            "unit_cost": "₹42/Litre (Milk) | ₹240/Kg (Paneer)",
            "retail_price": "₹58 - ₹64/Litre (Milk) | ₹360 - ₹420/Kg (Paneer)",
            "target_gross_margin_percent": 32.0
        }
    },
    {
        "id": "poultry",
        "name": "Poultry",
        "display_name": "Poultry",
        "backend_value": "Agriculture",
        "sector": "Agriculture & Allied",
        "typical_capex_min": 80000.0,
        "typical_capex_max": 1800000.0,
        "subcategories": ["Broiler Farming (Meat)", "Layer Farming (Eggs)", "Country Fowl (Desi Murghi)", "Day-Old Chick Brooding"],
        "competitor_search_terms": ["commercial broiler integration companies", "wholesale egg merchants", "local poultry farms"],
        "primary_activities": ["Shed climate and temperature management", "Feed rationing and water sanitization", "Vaccination schedule tracking", "Batch bird lifting by integrators/wholesalers"],
        "key_equipment": ["Deep litter poultry shed equipment", "Automatic bell drinkers & feeders", "Brooder heater lamps", "Feed storage bins"],
        "mandatory_licenses": ["Gram Panchayat NOC", "Animal Husbandry Dept Clearance", "Pollution Control Board Consent"],
        "location_factors": {
            "isolation": "At least 500m away from dense residential settlements",
            "cross_ventilation": "East-west shed orientation for natural airflow",
            "all_weather_truck_road": "Access for feed trucks and bird lifting vans"
        },
        "market_profile": {
            "catchment_radius_km": 30,
            "target_population": 60000,
            "customer_segments": ["Local chicken retail stalls", "Urban wholesale meat markets", "Dhabas and restaurants"],
            "channels": ["Direct wholesale trader contracts", "Contract farming integration agreements"],
            "peak_seasons": ["Winter months (November-February)", "Wedding and holiday seasons"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["Free-range Kadaknath and Desi eggs", "Contract broiler integration with guaranteed buyback"],
            "unmet_needs": ["Hygienic ready-to-lift bird supply in rural talukas"],
            "ecosystem_drivers": ["National Livestock Mission subsidies", "High protein dietary shifts"]
        },
        "risk_profile": {
            "primary_risks": ["Avian flu / infectious outbreaks", "Summer heatstroke bird mortality"],
            "mitigation_strategies": ["Strict bio-security gate protocols", "Fogger systems and cool pads during peak summer"]
        },
        "pricing_profile": {
            "benchmark_product": "1 Kg Live Broiler Bird / 1 Tray (30 Pcs) Farm Eggs",
            "unit_cost": "₹75 - ₹85 / kg live bird",
            "retail_price": "₹115 - ₹135 / kg live bird wholesale",
            "target_gross_margin_percent": 30.0
        }
    },
    {
        "id": "goat_farming",
        "name": "Goat Farming",
        "display_name": "Goat Farming",
        "backend_value": "Agriculture",
        "sector": "Agriculture & Allied",
        "typical_capex_min": 60000.0,
        "typical_capex_max": 1200000.0,
        "subcategories": ["Stall-Fed Goat Unit (20+1)", "Breeding Farm (Sirohi/Jamunapari/Barbari)", "Goat Milk for Therapeutic Use", "Fattening for Festive Markets"],
        "competitor_search_terms": ["local goat herders", "livestock mandis", "butcher supply traders"],
        "primary_activities": ["Elevated slotted floor housing management", "High-protein green fodder grazing and silage", "Deworming and reproductive health checks", "Festive market pre-sale conditioning"],
        "key_equipment": ["Elevated slotted wooden/bamboo flooring shed", "Fodder chaff cutter", "Weighing scale", "Vaccination gear"],
        "mandatory_licenses": ["Gram Panchayat Livestock Registration", "Veterinary Health Fitness Certificate"],
        "location_factors": {
            "dry_soil": "Well-drained land (goats are vulnerable to foot rot in waterlogged mud)",
            "grazing_commons": "Access to wasteland / grazing pasture / tree foliage",
            "water_source": "Clean potable drinking water source"
        },
        "market_profile": {
            "catchment_radius_km": 40,
            "target_population": 50000,
            "customer_segments": ["District livestock traders", "Festive Eid and wedding meat buyers", "Therapeutic goat milk consumers"],
            "channels": ["District weekly livestock haats", "Direct farm-gate festive bookings"],
            "peak_seasons": ["Eid-ul-Adha festive period", "Winter wedding season"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["Pedigree breeding stock supply to new farmers", "Stall-fed semi-intensive meat buck rearing"],
            "unmet_needs": ["Certified healthy disease-free breeding bucks"],
            "ecosystem_drivers": ["NABARD capital subsidy for small ruminants", "High rural liquid asset value"]
        },
        "risk_profile": {
            "primary_risks": ["PPR and Enterotoxemia disease vulnerability", "Predator attacks"],
            "mitigation_strategies": ["Regular scheduled vaccination calendar", "Sturdy chain-link perimeter fencing"]
        },
        "pricing_profile": {
            "benchmark_product": "1 Live Mature Meat Goat (30-35 Kg Live Weight)",
            "unit_cost": "₹3,500 - ₹4,800 (rearing, kid purchase, fodder)",
            "retail_price": "₹8,500 - ₹12,000 per animal",
            "target_gross_margin_percent": 55.0
        }
    },
    {
        "id": "fisheries",
        "name": "Fisheries",
        "display_name": "Fisheries",
        "backend_value": "Agriculture",
        "sector": "Agriculture & Allied",
        "typical_capex_min": 90000.0,
        "typical_capex_max": 2200000.0,
        "subcategories": ["Freshwater Inland Pond Aquaculture (Rohu/Catla)", "Biofloc Intensive Fish Farming", "Prawn/Shrimp Brackish Culture", "Ornamental Fish Breeding"],
        "competitor_search_terms": ["district fish mandis", "panchayat pond leaseholders", "freshwater hatcheries"],
        "primary_activities": ["Pond desilting and liming", "Fingerling seed stocking", "Commercial floating pellet feeding", "Periodic netting and aeration control"],
        "key_equipment": ["Paddlewheel aerators", "Water testing DO & pH kit", "Cast and drag fishing nets", "Insulated transport ice boxes"],
        "mandatory_licenses": ["Fisheries Dept Inland Aquaculture License", "Panchayat Water Body Lease Agreement", "Groundwater extraction clearance"],
        "location_factors": {
            "water_retention": "Clayey soil with high natural water retention capacity",
            "perennial_water": "Canal or perennial borewell water recharging",
            "road_access": "Immediate access for refrigerated/iced collection trucks"
        },
        "market_profile": {
            "catchment_radius_km": 35,
            "target_population": 80000,
            "customer_segments": ["Town retail fish markets", "Hotels and highway dhabas", "Wholesale fish processing aggregators"],
            "channels": ["Direct live-harvest pond-side auction", "Wholesale morning fish market supply"],
            "peak_seasons": ["Monsoon / Winter months", "Festive dining occasions"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["High-density Biofloc tank farming with minimal land", "Live Pangasius/Tilapia local delivery"],
            "unmet_needs": ["Fresh daily catch available at taluka levels without chemical preservatives"],
            "ecosystem_drivers": ["Pradhan Mantri Matsya Sampada Yojana (PMMSY) capital subsidies", "Growing dietary protein awareness"]
        },
        "risk_profile": {
            "primary_risks": ["Water dissolved oxygen depletion at night", "Bacterial gill disease outbreaks"],
            "mitigation_strategies": ["Deploy solar/grid battery backed aerators", "Maintain strict water probiotic management"]
        },
        "pricing_profile": {
            "benchmark_product": "1 Kg Live/Chilled Freshwater Table Fish (Rohu / Catla)",
            "unit_cost": "₹80 - ₹95 / kg (seed + floating feed + energy)",
            "retail_price": "₹150 - ₹190 / kg farm-gate wholesale",
            "target_gross_margin_percent": 45.0
        }
    },
    {
        "id": "beekeeping",
        "name": "Beekeeping",
        "display_name": "Beekeeping",
        "backend_value": "Agriculture",
        "sector": "Agriculture & Allied",
        "typical_capex_min": 40000.0,
        "typical_capex_max": 600000.0,
        "subcategories": ["Raw Multiflora Honey Production", "Monofloral Mustard/Litchi/Eucalyptus Honey", "Bee Wax & Propolis Extraction", "Crop Pollination Service for Orchards"],
        "competitor_search_terms": ["Khadi Village Industries honey", "branded packaged honey sellers", "migratory beekeepers"],
        "primary_activities": ["Apiary inspection and queen rearing", "Seasonal box migration following flora blooms", "Honey extraction via centrifugal extractor", "Natural filtration and glass jar packaging"],
        "key_equipment": ["Langstroth wooden bee boxes (20-50 units)", "Centrifugal honey extractor", "Protective bee veil suits & smokers", "Uncapping knife and stainless settling tanks"],
        "mandatory_licenses": ["KVIC / Honey Mission Certification", "FSSAI Registration for Honey Packaging", "Udyam MSME"],
        "location_factors": {
            "floral_density": "Within 2 km flight radius of mustard/sunflower/fruit orchards",
            "shade_and_water": "Tree canopy shelter and clean pesticide-free water source",
            "pesticide_isolation": "Low pesticide spray zones during active blooming"
        },
        "market_profile": {
            "catchment_radius_km": 50,
            "target_population": 40000,
            "customer_segments": ["Health-conscious town households", "Ayurvedic practitioners and pharmacies", "Bakery and confectionery producers"],
            "channels": ["Direct consumer retail via WhatsApp and organic fairs", "Supply to Khadi & natural store chains"],
            "peak_seasons": ["Mustard bloom (December-February)", "Sunflower & fruit bloom (March-May)"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["Pure raw unprocessed unheated honey", "Rental pollination services to apple/mustard growers"],
            "unmet_needs": ["Certified unadulterated honey free from high fructose corn syrup"],
            "ecosystem_drivers": ["National Beekeeping & Honey Mission (NBHM)", "Khadi Sweet Revolution incentives"]
        },
        "risk_profile": {
            "primary_risks": ["Insecticide spray poison in nearby fields", "Colony collapse / mite infestations"],
            "mitigation_strategies": ["Coordinate spray timing with neighboring farmers", "Apply organic formic/oxalic acid mite treatments"]
        },
        "pricing_profile": {
            "benchmark_product": "1 Kg Glass Jar Raw Certified Farm Honey",
            "unit_cost": "₹120 - ₹150 (comb upkeep, migration, jar packaging)",
            "retail_price": "₹350 - ₹550 / kg",
            "target_gross_margin_percent": 60.0
        }
    },
    {
        "id": "nursery_plant",
        "name": "Nursery & Plant Business",
        "display_name": "Nursery & Plant Business",
        "backend_value": "Agriculture",
        "sector": "Agriculture & Allied",
        "typical_capex_min": 50000.0,
        "typical_capex_max": 1000000.0,
        "subcategories": ["Vegetable Seedling Pro-Trays", "Fruit Graft Nursery (Mango/Guava/Lemon)", "Ornamental & Landscaping Plants", "Medicinal & Herbal Saplings"],
        "competitor_search_terms": ["government horticulture nursery", "private roadside plant nurseries", "seedling growers"],
        "primary_activities": ["Soil and vermicompost potting mix preparation", "Vegetable seed sowing in pro-trays under shade net", "Budding and air-layering graft propagation", "Retail plant display and customer advisory"],
        "key_equipment": ["50% green shade net structure", "Micro misting irrigation nozzles", "Seedling pro-trays and potting media mixer", "Grafting knives and nursery poly-bags"],
        "mandatory_licenses": ["District Horticulture Dept Nursery License", "Panchayat Trade License", "Udyam Registration"],
        "location_factors": {
            "highway_visibility": "Main roadside or highway location for walk-in retail traffic",
            "water_salinity": "Sweet water with low TDS (salt-sensitive seedlings)",
            "drainage": "Elevated gravel beds with zero water stagnancy"
        },
        "market_profile": {
            "catchment_radius_km": 30,
            "target_population": 75000,
            "customer_segments": ["Commercial vegetable farmers", "Town residential terrace gardeners", "Factory landscaping contractors"],
            "channels": ["Advance contract booking by farmers", "Direct retail highway nursery counter"],
            "peak_seasons": ["Pre-Monsoon planting (June-August)", "Pre-Rabi vegetable planting (October-November)"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["High-yielding F1 hybrid grafted vegetable seedlings", "Air-purifying indoor succulent pots for urban commuters"],
            "unmet_needs": ["Sturdy hardened seedlings with guaranteed 95%+ field survival rate"],
            "ecosystem_drivers": ["State Mission for Integrated Development of Horticulture (MIDH)", "Urban green balcony gardening trend"]
        },
        "risk_profile": {
            "primary_risks": ["Damping off fungal disease in seedling trays", "Water shortage during peak summer"],
            "mitigation_strategies": ["Use steam-sterilized cocopeat substrate", "Install rainwater harvesting tank with backup storage"]
        },
        "pricing_profile": {
            "benchmark_product": "100-Cell Pro-Tray Hybrid Tomato/Chilli Seedlings / 1 Grafted Fruit Plant",
            "unit_cost": "₹0.60 - ₹0.90 per seedling | ₹35 per fruit graft",
            "retail_price": "₹1.50 - ₹2.20 per seedling | ₹90 - ₹140 per fruit graft",
            "target_gross_margin_percent": 55.0
        }
    },
    {
        "id": "agri_equipment_rental",
        "name": "Agricultural Equipment Rental",
        "display_name": "Agricultural Equipment Rental",
        "backend_value": "Agriculture",
        "sector": "Agriculture & Allied",
        "typical_capex_min": 100000.0,
        "typical_capex_max": 2500000.0,
        "subcategories": ["Custom Hiring Centre (CHC)", "Tractor Implements (Rotavator, MB Plough)", "Harvester & Thresher Rental", "Boom Sprayer & Drone Spraying"],
        "competitor_search_terms": ["local tractor owners", "village custom hiring centres", "private implement hirers"],
        "primary_activities": ["Equipment seasonal servicing and oil change", "Farmer booking schedule management", "On-field tillage and harvesting operations", "Hourly/acreage meter tracking and billing"],
        "key_equipment": ["35-50 HP Tractor", "Rotavator (6-7 feet)", "Multi-crop Thresher / MB Plough", "Digital acreage tracker / GPS"],
        "mandatory_licenses": ["Commercial Vehicle Registration (RTO)", "Udyam MSME Certificate", "Agriculture Dept CHC Subsidy Empanelment"],
        "location_factors": {
            "central_hamlet": "Central village node with easy road access to multiple farming clusters",
            "parking_shed": "Covered high-clearance tractor and implement parking shed",
            "mechanic_proximity": "Within quick reach of diesel mechanics and spare parts"
        },
        "market_profile": {
            "catchment_radius_km": 20,
            "target_population": 35000,
            "customer_segments": ["Smallholder farmers (<2 hectares) unable to afford tractors", "Medium farmers needing specialized rotavators", "Orchard owners needing orchard sprayers"],
            "channels": ["Village WhatsApp booking group", "Direct word-of-mouth referral via village mukhi"],
            "peak_seasons": ["Pre-sowing tillage (May-June & October-November)", "Harvesting cycles (April & October)"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["Rotavator fine seedbed preparation on hire", "Drone-based precision pesticide/nano-urea spraying"],
            "unmet_needs": ["Timely tractor availability during narrow 7-day sowing windows"],
            "ecosystem_drivers": ["Sub-Mission on Agricultural Mechanization (SMAM) capital subsidies", "Labor shortages in rural agrarian pockets"]
        },
        "risk_profile": {
            "primary_risks": ["Machine breakdown during peak 10-day sowing window", "Farmer delayed seasonal payment khata"],
            "mitigation_strategies": ["Comprehensive preventative maintenance 30 days before season", "Strict partial token advance policy on booking"]
        },
        "pricing_profile": {
            "benchmark_product": "1 Hour Tractor Rotavator / Thresher Field Operation",
            "unit_cost": "₹450 - ₹550 / hour (diesel + driver + wear & tear)",
            "retail_price": "₹900 - ₹1,200 / hour rental charge",
            "target_gross_margin_percent": 50.0
        }
    },
    {
        "id": "agri_input_store",
        "name": "Agricultural Input Store",
        "display_name": "Agricultural Input Store",
        "backend_value": "Agriculture",
        "sector": "Agriculture & Allied",
        "typical_capex_min": 75000.0,
        "typical_capex_max": 2000000.0,
        "subcategories": ["Certified Seeds & Hybrid Grains", "Fertilizers & Bio-Nutrients", "Crop Protection & Agro-Chemicals", "Micro-Irrigation Fittings & Farm Tools"],
        "competitor_search_terms": ["IFFCO / KRIBHCO societies", "taluka agro agencies", "private pesticide dealers"],
        "primary_activities": ["Procurement from authorized seed and chemical distributors", "Agronomic advisory to farmers on dosage and pests", "POS digital stock and GST billing", "Seasonal credit management"],
        "key_equipment": ["Digital weighing balance", "Barcode scanner and computerized billing system", "Ventilated moisture-proof storage racks", "Safety chemical cabinets"],
        "mandatory_licenses": ["District Agriculture Dept Retail Seed License", "Retail Fertilizer Dealership License", "Insecticides / Pesticides Sale License", "GST Registration"],
        "location_factors": {
            "market_transit": "Adjacent to APMC mandi yard or prominent farmer gathering crossroad",
            "ventilated_storage": "Dry, fire-safe, moisture-barrier godown facility",
            "loading_dock": "Truck parking access for loading heavy fertilizer bags"
        },
        "market_profile": {
            "catchment_radius_km": 25,
            "target_population": 50000,
            "customer_segments": ["Village farmers across 10-15 neighboring villages", "Commercial orchard growers", "Dairy farmers needing fodder seeds"],
            "channels": ["Direct counter retail storefront", "Farmer advisory camp demos"],
            "peak_seasons": ["Kharif sowing preparation (May-July)", "Rabi sowing preparation (October-December)"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["Bio-fertilizers, neem coated urea, and nano DAP", "Drip irrigation replacement spares and fertigation mixers"],
            "unmet_needs": ["Genuine non-counterfeit pesticide advisory with digital bills"],
            "ecosystem_drivers": ["PM Kisan Samriddhi Kendras initiative", "DBT direct fertilizer subsidy integration"]
        },
        "risk_profile": {
            "primary_risks": ["Unsold seasonal seed stock expiration", "Farmers unable to repay seasonal credit due to drought"],
            "mitigation_strategies": ["Implement return-to-vendor distributor agreements for excess seed", "Cap credit exposure to max 25% of monthly sales"]
        },
        "pricing_profile": {
            "benchmark_product": "Standard Sowing Input Package (Certified Seed + Bio-fungicide + Micronutrient)",
            "unit_cost": "₹1,200 wholesale procurement",
            "retail_price": "₹1,450 - ₹1,600 retail basket",
            "target_gross_margin_percent": 20.0
        }
    },

    # -------------------------------------------------------------
    # 2. Food & Processing Sectors
    # -------------------------------------------------------------
    {
        "id": "grocery",
        "name": "Grocery / Kirana",
        "display_name": "Grocery / Kirana",
        "backend_value": "Grocery",
        "sector": "Retail & Trade",
        "typical_capex_min": 50000.0,
        "typical_capex_max": 1500000.0,
        "subcategories": ["Daily Essentials & Grains", "Packaged FMCG & Toiletries", "Loose Spices & Pulses", "Village Quick Commerce Hub"],
        "competitor_search_terms": ["village general stores", "taluka supermarkets", "fair price PDS ration shops"],
        "primary_activities": ["Bulk wholesale inventory procurement from city mandis", "Loose staples weighing and clean packaging", "Over-the-counter and WhatsApp customer sales", "Doorstep village delivery"],
        "key_equipment": ["Heavy-duty modular display racks", "Digital weighing scale", "Deep freezer for dairy & cold drinks", "POS billing terminal and barcode scanner"],
        "mandatory_licenses": ["FSSAI Basic Food Registration", "Shop and Establishment Act Registration", "Udyam MSME"],
        "location_factors": {
            "footfall_density": "Central village chowk or bus stop intersection",
            "visibility": "Ground floor corner with wide shutter entrance",
            "storage_dryness": "Damp-proof backroom godown to protect flour and grain sacks"
        },
        "market_profile": {
            "catchment_radius_km": 8,
            "target_population": 15000,
            "customer_segments": ["Daily wage earner households", "Salaried teachers and government staff", "Local tea stalls and food vendors"],
            "channels": ["Direct counter sales", "Phone/WhatsApp grocery order dispatch"],
            "peak_seasons": ["Harvest payout weeks (monthly spikes)", "Diwali, Eid, and wedding festivals"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["Unbranded high-quality regional pulses and cold-pressed oils", "WhatsApp doorstep quick delivery within 20 minutes"],
            "unmet_needs": ["Access to genuine branded personal care and hygiene products in rural belts"],
            "ecosystem_drivers": ["UPI digital soundbox penetration", "Growing demand for packaged hygienic foods"]
        },
        "risk_profile": {
            "primary_risks": ["Rodent and dampness stock shrinkage", "Excessive customer unrecovered credit khata"],
            "mitigation_strategies": ["Use elevated pallets and sealed plastic grain containers", "Keep digital ledger on Vyapar/Khatabook with weekly credit caps"]
        },
        "pricing_profile": {
            "benchmark_product": "Standard 5 Kg Household Monthly Ration Basket",
            "unit_cost": "₹480 wholesale basket cost",
            "retail_price": "₹575 - ₹610 per basket",
            "target_gross_margin_percent": 18.0
        }
    },
    {
        "id": "food_processing",
        "name": "Food Processing",
        "display_name": "Food Processing",
        "backend_value": "Food Processing",
        "sector": "Food & Processing",
        "typical_capex_min": 60000.0,
        "typical_capex_max": 2500000.0,
        "subcategories": ["Spice Grinding & Blending", "Snack & Namkeen Extrusion", "Pulse & Grain Milling", "Ready-to-Cook Traditional Mixes"],
        "competitor_search_terms": ["national FMCG spice brands", "regional namkeen factories", "local millers"],
        "primary_activities": ["Cleaning and stone-destoning of raw agricultural produce", "Milling and temperature-controlled pulverizing", "Automated nitrogen-flushed pouch packaging", "Wholesale distribution to rural kirana network"],
        "key_equipment": ["Hammer mill pulverizer (10-20 HP)", "Continuous nitrogen band sealer", "Vibratory de-stoner / grader", "Stainless steel ribbon blender"],
        "mandatory_licenses": ["FSSAI Manufacturing / State License", "Pollution Control Board Consent (Green Category)", "Udyam MSME Registration", "Water Testing Fitness Certificate"],
        "location_factors": {
            "three_phase_power": "Stable 15-25 HP industrial electric load",
            "sanitation": "Clean drainage and dust-free processing shed",
            "raw_material_proximity": "Close to spice or food grain production mandis"
        },
        "market_profile": {
            "catchment_radius_km": 40,
            "target_population": 85000,
            "customer_segments": ["Village kirana stores and provision shops", "Highway eateries, dhabas, and canteens", "Catering contractors for weddings"],
            "channels": ["Rural distributor van network", "Direct sales at weekly haat markets", "Institutional bulk pack supply"],
            "peak_seasons": ["Post-harvest crop arrival (February-April)", "Festive gift packaging season (September-November)"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["Clean, adulterant-free turmeric, chilli, and coriander powder in ₹10/₹20 packs", "Region-specific traditional snack varieties"],
            "unmet_needs": ["Affordable branded local spices with verified FSSAI lab quality marks"],
            "ecosystem_drivers": ["PM Formalisation of Micro food processing Enterprises (PMFME) scheme", "One District One Product (ODOP) focus"]
        },
        "risk_profile": {
            "primary_risks": ["Raw material spice price volatility", "Moisture contamination resulting in mold"],
            "mitigation_strategies": ["Purchase annual stock during peak harvest price lows", "Use multi-layer aluminum barrier packaging foil"]
        },
        "pricing_profile": {
            "benchmark_product": "200g Stand-up Pouch Ground Pure Spices / Traditional Snack Pack",
            "unit_cost": "₹32 - ₹42 per pouch",
            "retail_price": "₹65 - ₹85 per pouch",
            "target_gross_margin_percent": 50.0
        }
    },
    {
        "id": "bakery",
        "name": "Bakery",
        "display_name": "Bakery",
        "backend_value": "Food Processing",
        "sector": "Food & Processing",
        "typical_capex_min": 65000.0,
        "typical_capex_max": 1800000.0,
        "subcategories": ["Fresh Bread & Pav Production", "Rusk & Khari Manufacturing", "Cakes & Birthday Pastries", "Artisanal Cookies & Biscuits"],
        "competitor_search_terms": ["industrial packaged bread distributors", "town bakeries", "tea stall rusk suppliers"],
        "primary_activities": ["Dough kneading and proofing", "Rotary oven baking and temperature timing", "Slicing, cooling, and heat sealing", "Early morning dispatch to tea stalls and shops"],
        "key_equipment": ["Rotary rack baking oven (electric/diesel)", "Spiral dough kneader (25-50 kg)", "Automatic bread slicer", "Stainless steel preparation tables and baking trays"],
        "mandatory_licenses": ["FSSAI Food Business Manufacturing License", "Gram Panchayat NOC & Fire Safety Clearance", "Udyam MSME"],
        "location_factors": {
            "early_logistics": "Strategic location enabling 5:30 AM delivery to tea shops",
            "exhaust_ventilation": "High chimney / exhaust for heat and baking aromas",
            "storage_hygiene": "Rodent-free flour and yeast storage area"
        },
        "market_profile": {
            "catchment_radius_km": 20,
            "target_population": 45000,
            "customer_segments": ["Local tea stalls and dhabas (daily pav & rusk)", "School children and family breakfasts", "Youth celebration birthday cake orders"],
            "channels": ["Early morning delivery routes to 30-50 tea stalls", "Retail bakery storefront counter"],
            "peak_seasons": ["Monsoon & Winter tea consumption surge", "Wedding seasons and New Year"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["Freshly baked soft pav for vada-pav / dabeli vendors", "Custom fresh cream photo birthday cakes in rural towns"],
            "unmet_needs": ["Fresh daily bread free from artificial chemical shelf-life extenders"],
            "ecosystem_drivers": ["Rising snacking culture across rural highway corridors", "High recurring daily morning cash inflows"]
        },
        "risk_profile": {
            "primary_risks": ["Unsold daily fresh bread staling (short shelf life)", "Flour and commercial butter price inflation"],
            "mitigation_strategies": ["Convert day-old surplus bread into toasted breadcrumbs or rusk", "Maintain strict pre-order quotas with tea stall clients"]
        },
        "pricing_profile": {
            "benchmark_product": "Daily Tea Stall Pav Ladi (Pack of 12) & 500g Cake Rusk Pack",
            "unit_cost": "₹16 - ₹22 per pack",
            "retail_price": "₹32 - ₹45 per pack",
            "target_gross_margin_percent": 48.0
        }
    },
    {
        "id": "snacks_namkeen",
        "name": "Snacks & Namkeen",
        "display_name": "Snacks & Namkeen",
        "backend_value": "Food Processing",
        "sector": "Food & Processing",
        "typical_capex_min": 50000.0,
        "typical_capex_max": 1400000.0,
        "subcategories": ["Sev, Ganthiya & Bhavnagari Gathiya", "Banana, Potato & Tapioca Wafers", "Chivda & Roasted Mixture", "Frying & Seasoning Unit"],
        "competitor_search_terms": ["Balaji / Haldiram distributor", "local farsan shops", "haat snack vendors"],
        "primary_activities": ["Gram flour dough preparation and consistency checking", "Deep frying in automated temperature-controlled fryers", "Tumbling drum spice seasoning", "Form-fill-seal pouch packaging with nitrogen"],
        "key_equipment": ["Commercial gas/diesel deep fryer with oil filter", "Rotary namkeen extruder / sev maker", "Spice seasoning coating drum", "Nitrogen pouch packing machine"],
        "mandatory_licenses": ["FSSAI Food Processing License", "Pollution Control Board NOC", "Udyam MSME"],
        "location_factors": {
            "chimney_exhaust": "Industrial hood and oil fume exhaust chimney",
            "gas_supply": "Commercial LPG bank or biomass pellet burner access",
            "dry_storage": "Moisture-free oil and besan godown"
        },
        "market_profile": {
            "catchment_radius_km": 30,
            "target_population": 65000,
            "customer_segments": ["Rural pan shops and petty kiosks (₹5/₹10 impulse packs)", "Town residential households for evening tea farsan", "Festive corporate and family bulk orders"],
            "channels": ["Weekly van supply to 150+ village pan shops", "Factory gate retail sales"],
            "peak_seasons": ["Diwali and Holi festive gifting", "Winter and rainy monsoon months"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["High-turnover ₹5 and ₹10 impulse namkeen packets with high retail margin", "Fresh warm morning Ganthiya & Jalebi takeaway"],
            "unmet_needs": ["Fresh palm-oil free / groundnut oil premium namkeen options"],
            "ecosystem_drivers": ["PMFME micro enterprise support", "High rural appetite for savory extruded snacks"]
        },
        "risk_profile": {
            "primary_risks": ["Edible oil price sudden market swings", "Oil rancidity in packaged packets if exposed to sunlight"],
            "mitigation_strategies": ["Use metallized BOPP barrier foil and nitrogen flush", "Short batch production with maximum 30-day stock turnaround"]
        },
        "pricing_profile": {
            "benchmark_product": "1 Kg Traditional Besan Sev / Ganthiya Bulk Pack",
            "unit_cost": "₹90 - ₹115 (besan, groundnut oil, spices, fuel)",
            "retail_price": "₹190 - ₹240 / kg",
            "target_gross_margin_percent": 50.0
        }
    },
    {
        "id": "pickles_papad",
        "name": "Pickles & Papad",
        "display_name": "Pickles & Papad",
        "backend_value": "Food Processing",
        "sector": "Food & Processing",
        "typical_capex_min": 35000.0,
        "typical_capex_max": 800000.0,
        "subcategories": ["Traditional Mango & Lemon Pickles", "Moong & Urad Dal Papad", "Khakhra & Dry Thepla", "Spicy Chutneys & Murabba"],
        "competitor_search_terms": ["Lijjat papad distributors", "commercial pickle brands", "SHG home producers"],
        "primary_activities": ["Seasonal raw fruit grading, washing, and sun drying", "Oil and spice curing in ceramic barnis", "Dough rolling and shade-drying of papad", "Hygienic jar and pouch vacuum sealing"],
        "key_equipment": ["Dough kneader and papad rolling machines", "Stainless steel mixing tubs", "Solar drying greenhouse tunnel", "Induction cap sealing machine"],
        "mandatory_licenses": ["FSSAI Registration / State License", "Udyam MSME", "Gram Panchayat Clearance"],
        "location_factors": {
            "sunlight_availability": "Unobstructed open rooftop or solar drying yard",
            "hygienic_shed": "Fly-proof netted curing room with tiled walls",
            "storage_temp": "Cool, dry ambient storage for oil-cured jars"
        },
        "market_profile": {
            "catchment_radius_km": 35,
            "target_population": 40000,
            "customer_segments": ["Rural and town family households", "Hostel and college mess canteens", "Highway dhabas and Gujarati thali restaurants"],
            "channels": ["Direct sales to local grocery stores", "Women SHG exhibition stalls and digital orders"],
            "peak_seasons": ["Summer raw mango season (April-June)", "Festive winter food seasons"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["Authentic grandmother-style preservative-free cold-pressed mustard oil pickles", "Roasted vacuum-packed diet khakhras"],
            "unmet_needs": ["Traditional regional tastes that multinational corporate brands fail to replicate"],
            "ecosystem_drivers": ["Women entrepreneurship subsidies via NRLM/DAY-NRLM", "Vocal for Local promotion"]
        },
        "risk_profile": {
            "primary_risks": ["Fungal spoilage due to moisture or insufficient oil cover", "Seasonal raw mango crop failure"],
            "mitigation_strategies": ["Strict salt and oil ratio quality control", "Contract directly with local orchards before harvest"]
        },
        "pricing_profile": {
            "benchmark_product": "500g Jar Authentic Mango Pickle & 1 Kg Urad Dal Papad",
            "unit_cost": "₹55 (Pickle jar) | ₹110 (Papad kg)",
            "retail_price": "₹120 - ₹150 (Pickle) | ₹210 - ₹260 (Papad)",
            "target_gross_margin_percent": 54.0
        }
    },
    {
        "id": "flour_mill",
        "name": "Flour Mill",
        "display_name": "Flour Mill",
        "backend_value": "Food Processing",
        "sector": "Food & Processing",
        "typical_capex_min": 45000.0,
        "typical_capex_max": 900000.0,
        "subcategories": ["Wheat Atta Grinding", "Multi-grain & Millet (Bajra/Jowar) Milling", "Gram Flour (Besan) Pulverizing", "Spices & Rice Crushing"],
        "competitor_search_terms": ["neighborhood chakki shops", "packaged atta brands (Aashirvaad)", "commercial grain mills"],
        "primary_activities": ["Grain destoning and cleaning", "Cold/slow stone grinding to preserve grain nutrients", "Flour sieve grading and bagging", "Custom grinding jobwork billing"],
        "key_equipment": ["Stone flour mill (Chakki) with 10 HP motor", "Chilly/Spice pulverizer machine", "De-stoner and air aspirator", "Electronic platform weighing scale"],
        "mandatory_licenses": ["Gram Panchayat Shop License", "FSSAI Basic Registration", "Electricity Board Industrial Connection"],
        "location_factors": {
            "residential_access": "Within easy walking distance for women and elders carrying grain bags",
            "power_stability": "Three-phase commercial power supply without voltage dips",
            "vibration_absorption": "Reinforced concrete plinth for heavy stone grinders"
        },
        "market_profile": {
            "catchment_radius_km": 5,
            "target_population": 12000,
            "customer_segments": ["Village and residential town families", "Local snack and farsan makers (besan)", "Tea stall operators and small dhabas"],
            "channels": ["Direct walk-in customer jobwork service", "Own-brand packaged freshly ground atta counter sales"],
            "peak_seasons": ["Wheat harvest season (April-May)", "Winter millet consumption months (November-January)"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["Fresh stone-ground diabetic multi-grain and ragi flour packs", "Dedicated turmeric and coriander spice grinding slots"],
            "unmet_needs": ["Fresh, warm, 100% whole wheat chakki atta without maida adulteration"],
            "ecosystem_drivers": ["International Year of Millets awareness", "Stable year-round household daily utility"]
        },
        "risk_profile": {
            "primary_risks": ["Electric power cuts disrupting daily milling schedules", "Abrasive stone wear reducing grinding efficiency"],
            "mitigation_strategies": ["Schedule stone dressing every 30 days", "Install solar rooftop net-metering to lower electric tariff"]
        },
        "pricing_profile": {
            "benchmark_product": "Wheat Milling Jobwork (per Kg) & 5 Kg Premium Chakki Fresh Atta Pack",
            "unit_cost": "₹1.50 / kg electricity & stone wear cost",
            "retail_price": "₹4.50 - ₹6.00 / kg milling charge | ₹195 per 5 Kg pack",
            "target_gross_margin_percent": 65.0
        }
    },
    {
        "id": "fruit_veg_processing",
        "name": "Fruit & Vegetable Processing",
        "display_name": "Fruit & Vegetable Processing",
        "backend_value": "Food Processing",
        "sector": "Food & Processing",
        "typical_capex_min": 80000.0,
        "typical_capex_max": 2400000.0,
        "subcategories": ["Fruit Pulp & Puree (Mango/Guava/Tomato)", "Solar Dehydrated Vegetables (Onion/Garlic flakes)", "Squashes, Syrups & Jams", "Ready-to-Cook Frozen/Vacuum Veggies"],
        "competitor_search_terms": ["industrial canning units", "mango pulp export factories", "dehydrated food suppliers"],
        "primary_activities": ["Washing, peeling, and mechanical pulping", "Pasteurization and aseptic vacuum canning", "Solar tunnel dehydration of sliced vegetables", "B2B supply to ice cream, bakery, and hotel chains"],
        "key_equipment": ["Fruit pulper with stainless sieve", "Steam jacketed cooking kettle", "Solar tunnel dryer with auxiliary blower", "Can seamer / sterile packaging line"],
        "mandatory_licenses": ["FSSAI State Manufacturing License", "Pollution Control Board Consent", "Udyam MSME", "Boiler Inspection Certificate (if steam boiler used)"],
        "location_factors": {
            "orchard_cluster": "Situated in fruit belts (e.g. Kesar mango in Junagadh, Chikoo in Navsari)",
            "effluent_treatment": "Soak pit or organic wastewater drainage facility",
            "cold_room": "Insulated cold room for temporary raw fruit staging"
        },
        "market_profile": {
            "catchment_radius_km": 50,
            "target_population": 90000,
            "customer_segments": ["Ice-cream and dairy processing factories", "Bakeries and confectionery manufacturers", "Urban supermarkets and institutional caterers"],
            "channels": ["B2B bulk food service contracts", "Consumer retail jars via distributor networks"],
            "peak_seasons": ["Summer mango season (April-June)", "Winter tomato and vegetable glut (December-February)"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["Solar-dehydrated onion and ginger flakes for export and city kitchens", "Pure aseptic Kesar/Alphonso mango pulp cans"],
            "unmet_needs": ["Preventing distress crop dump during harvest gluts by immediate processing at source"],
            "ecosystem_drivers": ["PM Kisan Sampada Yojana mega food park & cold chain grants", "Strong export demand for Indian tropical fruit pulp"]
        },
        "risk_profile": {
            "primary_risks": ["Short 45-day operational raw fruit harvesting window", "Sterilization failures causing can bulging"],
            "mitigation_strategies": ["Multi-crop processing line (Mango in summer, Tomato in winter, Onion in spring)", "Adhere to strict thermal sterilization charts"]
        },
        "pricing_profile": {
            "benchmark_product": "3.1 Kg Can Aseptic Mango Pulp / 1 Kg Dehydrated Onion Flakes",
            "unit_cost": "₹160 (Canned pulp) | ₹140 (Onion flakes)",
            "retail_price": "₹310 - ₹380 per can | ₹280 - ₹350 per kg flakes",
            "target_gross_margin_percent": 48.0
        }
    },

    # -------------------------------------------------------------
    # 3. Manufacturing, Textiles & Crafts
    # -------------------------------------------------------------
    {
        "id": "textile_clothing",
        "name": "Textile & Clothing",
        "display_name": "Textile & Clothing",
        "backend_value": "Textile & Clothing",
        "sector": "Manufacturing & Crafts",
        "typical_capex_min": 50000.0,
        "typical_capex_max": 1500000.0,
        "subcategories": ["Readymade Garment Retail", "Rural Tailoring & Alteration Unit", "Ethnic Wear & Festive Costumes", "School Uniform Contract Manufacturing"],
        "competitor_search_terms": ["town readymade showrooms", "weekly textile haats", "independent village tailors"],
        "primary_activities": ["Wholesale fabric procurement from textile hubs (Surat/Ahmedabad)", "Pattern cutting and garment stitching", "Display merchandising and customer fittings", "Institutional school uniform stitching"],
        "key_equipment": ["Industrial high-speed stitching machines (Juki/Jack)", "Fabric cutting table and heavy shears", "Steam iron station and vacuum ironing board", "Mannequins and modular clothing display racks"],
        "mandatory_licenses": ["Shop and Establishment Act Registration", "Udyam MSME Certificate", "GST Registration (if turnover exceeds statutory limit)"],
        "location_factors": {
            "retail_footfall": "Prime high street market near town bus station or female apparel stores",
            "lighting": "High-lumen bright LED lighting for true fabric color matching",
            "fitting_room": "Dedicated private fitting space for women customers"
        },
        "market_profile": {
            "catchment_radius_km": 18,
            "target_population": 40000,
            "customer_segments": ["Rural and semi-urban women and youth", "School management committees for student uniforms", "Festival shoppers during wedding seasons"],
            "channels": ["Storefront retail sales", "School and corporate uniform bulk contracts", "Weekly haat pop-up stall"],
            "peak_seasons": ["Diwali and Navratri festive season", "School reopening months (June-July)", "Winter wedding season"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["Customized designer kurti alteration and fast fashion sets", "Annual school uniform contracts with upfront margin guarantee"],
            "unmet_needs": ["Affordable trending garments in rural towns with immediate same-day tailoring fit"],
            "ecosystem_drivers": ["PM MITRA textile clusters", "Direct train and road connectivity to Surat wholesale textile mandis"]
        },
        "risk_profile": {
            "primary_risks": ["Fast fashion dead stock if design trends shift", "Seasonal credit extensions to wedding customers"],
            "mitigation_strategies": ["Operate lean inventory with weekly replenishment from wholesale mandis", "Adopt 50% advance policy on customized stitching orders"]
        },
        "pricing_profile": {
            "benchmark_product": "Cotton Daily Kurti / Agrarian Work Shirt & Complete School Uniform Set",
            "unit_cost": "₹160 - ₹210 (fabric + stitching + trim)",
            "retail_price": "₹340 - ₹450 per garment",
            "target_gross_margin_percent": 50.0
        }
    },
    {
        "id": "tailoring_embroidery",
        "name": "Tailoring & Embroidery",
        "display_name": "Tailoring & Embroidery",
        "backend_value": "Textile & Clothing",
        "sector": "Manufacturing & Crafts",
        "typical_capex_min": 35000.0,
        "typical_capex_max": 800000.0,
        "subcategories": ["Women Designer Blouse & Kurti Tailoring", "Computerized Multi-Head Embroidery", "Zari, Aari & Mirror Work", "Bridal Lehengas & Saree Fall Piko"],
        "competitor_search_terms": ["boutique tailoring shops", "embroidery jobwork units", "home-based seamstresses"],
        "primary_activities": ["Customer measurement and design drafting", "Computerized or manual aari-work embroidery", "Precision stitching, lining, and zipper attachment", "Quality finishing and trial fit checks"],
        "key_equipment": ["Single/Multi-head computerized embroidery machine", "Direct-drive lockstitch sewing machine", "Overlock (interlock) 4-thread machine", "Embroidery design digitization software"],
        "mandatory_licenses": ["Shop & Establishment Registration", "Udyam MSME Registration"],
        "location_factors": {
            "boutique_corridor": "Close to women cloth markets, jewelry stores, and cosmetics shops",
            "air_conditioned": "Clean, dust-free environment for delicate bridal silks",
            "stable_power": "UPS battery backup for computerized embroidery machine"
        },
        "market_profile": {
            "catchment_radius_km": 15,
            "target_population": 30000,
            "customer_segments": ["Brides and wedding party guests", "Working women, college students, and homemakers", "Garment retail boutiques outsourcing embroidery"],
            "channels": ["Direct boutique walk-in orders", "Instagram and WhatsApp portfolio showcases"],
            "peak_seasons": ["Wedding season (November-February & April-May)", "Navratri festival embroidery rush"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["High-margin bridal designer blouses (₹1,500 - ₹4,000 stitching charges)", "Computerized custom logo and ethnic motif embroidery"],
            "unmet_needs": ["Reliable delivery on committed dates without wedding deadline delays"],
            "ecosystem_drivers": ["Growing social media driven wedding fashion aspirations in rural towns", "Micro enterprise support for women artisans"]
        },
        "risk_profile": {
            "primary_risks": ["Customer dissatisfaction over garment fit or sizing", "Needle breaks causing fabric tears on expensive silks"],
            "mitigation_strategies": ["Provide formal paper measurement receipts and intermediate trial fittings", "Use industrial ballpoint needles and stabilizers on delicate fabrics"]
        },
        "pricing_profile": {
            "benchmark_product": "Embroidered Designer Blouse / Custom Bridal Kurti Set",
            "unit_cost": "₹280 (thread, canvas, lining, power, labor)",
            "retail_price": "₹750 - ₹1,800 stitching and embroidery charge",
            "target_gross_margin_percent": 65.0
        }
    },
    {
        "id": "handicrafts",
        "name": "Handicrafts",
        "display_name": "Handicrafts",
        "backend_value": "Handicrafts",
        "sector": "Manufacturing & Crafts",
        "typical_capex_min": 40000.0,
        "typical_capex_max": 1000000.0,
        "subcategories": ["Traditional Heritage Crafts", "Handloom Weaving & Block Printing", "Wood Carving & Marquetry", "Eco-friendly Festive Art"],
        "competitor_search_terms": ["artisan cooperatives", "state handicraft emporiums", "heritage craft traders"],
        "primary_activities": ["Ethical raw material gathering and natural dye preparation", "Artisan handcrafting and carving", "Eco-friendly cardboard gift packaging", "Exhibition stall participation and e-commerce shipping"],
        "key_equipment": ["Handloom / Wood carving chisel tools", "Natural dye processing vats", "Precision detailing worktables", "Photobox for product cataloging"],
        "mandatory_licenses": ["Artisan Pehchan ID Card (Ministry of Textiles)", "Udyam MSME Registration", "GST (exempt for select direct artisan sales)"],
        "location_factors": {
            "artisan_cluster": "Situated in traditional artisan hamlets (e.g. Kutch, Dahod, Dang)",
            "raw_material_access": "Proximity to sustainable wood, clay, or cotton spinning",
            "tourist_access": "Near heritage tourist circuits or craft haats"
        },
        "market_profile": {
            "catchment_radius_km": 60,
            "target_population": 50000,
            "customer_segments": ["Domestic and international heritage tourists", "Corporate gifting managers", "Urban conscious decor shoppers"],
            "channels": ["Direct SARAS and craft melas", "E-commerce (ONDC, Amazon Karigar, Etsy)", "State emporiums"],
            "peak_seasons": ["Tourist season (October-March)", "Corporate Diwali gifting period"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["Corporate customized artisan gift boxes with artisan story cards", "Direct international D2C export via postal courier"],
            "unmet_needs": ["Eliminating predatory middlemen to allow artisans to capture full retail value"],
            "ecosystem_drivers": ["PM Vishwakarma Scheme credit and toolkits", "Geographical Indication (GI) tag promotion"]
        },
        "risk_profile": {
            "primary_risks": ["Middlemen exploitation suppressing artisan purchase rates", "Damage in transit during postal shipping"],
            "mitigation_strategies": ["Direct selling via UPI on digital catalogs", "Use honeycomb paper bubble-free protective packaging"]
        },
        "pricing_profile": {
            "benchmark_product": "Handcrafted Artisan Heritage Decor Piece / Embroidered Shawl",
            "unit_cost": "₹180 - ₹280 (artisan raw materials + labor)",
            "retail_price": "₹550 - ₹1,200 retail | ₹2,500+ (luxury/export)",
            "target_gross_margin_percent": 65.0
        }
    },
    {
        "id": "pottery",
        "name": "Pottery",
        "display_name": "Pottery",
        "backend_value": "Handicrafts",
        "sector": "Manufacturing & Crafts",
        "typical_capex_min": 30000.0,
        "typical_capex_max": 750000.0,
        "subcategories": ["Terracotta Water Coolers (Matka)", "Clay Cooking Utensils & Tawa", "Decorative Garden Planters", "Diwali Diyas & Festive Artifacts"],
        "competitor_search_terms": ["traditional kumhar clusters", "roadside planter nurseries", "festive clay stalls"],
        "primary_activities": ["Clay slaking, sieving, and kneaded pugging", "Motorized potter wheel throwing and shaping", "Solar drying and wood/gas kiln firing", "Lead-free food-safe slip glazing"],
        "key_equipment": ["Electric variable-speed potter wheel", "Clay pug mill (for smooth bubble-free clay)", "Updraft energy-efficient pottery kiln", "Terracotta polishing tools"],
        "mandatory_licenses": ["Gram Panchayat Artisan Clearance", "PM Vishwakarma Scheme Registration", "Udyam MSME"],
        "location_factors": {
            "clay_quarry_proximity": "Proximity to silt/clay rich pond banks",
            "smoke_clearance": "Kiln ventilation situated clear of immediate residential clotheslines",
            "drying_yard": "Spacious covered sun-drying racks to prevent cracking"
        },
        "market_profile": {
            "catchment_radius_km": 25,
            "target_population": 35000,
            "customer_segments": ["Rural and urban households seeking natural clay refrigeration", "Organic food restaurants and chai kulhad stalls", "Nursery garden enthusiasts and urban landscapers"],
            "channels": ["Direct workshop retail counter", "Bulk supply to roadside highway nurseries", "Festive mela sales"],
            "peak_seasons": ["Summer season (March-June for water matkas)", "Diwali festive season (for clay diyas and idols)"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["Food-grade microwave-safe natural clay biryani pots and tawas", "Biodegradable single-use clay kulhads for railway tea vendors"],
            "unmet_needs": ["Non-toxic lead-free tested clay cookware with durable crack resistance"],
            "ecosystem_drivers": ["Ban on single-use plastics promoting clay kulhads", "Health trend moving toward alkaline clay water storage"]
        },
        "risk_profile": {
            "primary_risks": ["Kiln firing breakage due to thermal shock", "Monsoon rain preventing open-air firing"],
            "mitigation_strategies": ["Upgrade to LPG/electric controlled kilns", "Stockpile fired inventory before monsoon onset"]
        },
        "pricing_profile": {
            "benchmark_product": "Natural Clay Tap Water Dispenser (10L) & Pack of 50 Clay Kulhads",
            "unit_cost": "₹60 (clay, firing wood, brass tap)",
            "retail_price": "₹220 - ₹350 per water dispenser",
            "target_gross_margin_percent": 68.0
        }
    },
    {
        "id": "furniture",
        "name": "Furniture",
        "display_name": "Furniture",
        "backend_value": "Handicrafts",
        "sector": "Manufacturing & Crafts",
        "typical_capex_min": 75000.0,
        "typical_capex_max": 2000000.0,
        "subcategories": ["Solid Wood Beds & Storage Almirahs", "Modular Kitchen & Wardrobe Joinery", "Office Desks & School Benches", "Restoration & Re-Upholstery"],
        "competitor_search_terms": ["town timber merchants", "flat-pack furniture retailers", "local carpenter workshops"],
        "primary_activities": ["Timber seasoning and moisture checking", "Precision sawing, planing, and mortise-tenon joinery", "Laminate pressing and edge-banding", "Wood stain polishing and PU lacquer finishing"],
        "key_equipment": ["Circular table saw and thickness planer", "Router and biscuit joiner machine", "Pneumatic nailer & air compressor", "Portable edge banding machine"],
        "mandatory_licenses": ["Shop & Establishment Registration", "Forest Dept Timber Transit Permit (if raw timber used)", "Udyam MSME Certificate"],
        "location_factors": {
            "timber_access": "Within easy hauling distance of regional timber sawmills",
            "loading_clearance": "Spacious ground floor loading bay for tempo delivery",
            "fire_safety": "Compliant fire extinguisher setup for wood shavings"
        },
        "market_profile": {
            "catchment_radius_km": 25,
            "target_population": 45000,
            "customer_segments": ["New rural home builders and renovators", "Wedding dowry furniture buyers", "Local schools, panchayat offices, and dispensaries"],
            "channels": ["Direct custom order commission workshop", "Highway furniture display showroom"],
            "peak_seasons": ["Post-harvest home construction months (January-May)", "Wedding seasons"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["Custom termite-proof storage almirahs and hydraulic storage beds", "Institutional school bench and desk manufacturing contracts"],
            "unmet_needs": ["Solid wood durability at prices competitive with fragile particle board imports"],
            "ecosystem_drivers": ["PM Vishwakarma carpenter support", "Booming rural pucca housing under PMAY"]
        },
        "risk_profile": {
            "primary_risks": ["Timber warping if unseasoned wood is used", "Carpenter skilled craftsman absenteeism"],
            "mitigation_strategies": ["Use digital wood moisture meters (max 10-12% moisture)", "Cross-train apprentices and use precision power tools"]
        },
        "pricing_profile": {
            "benchmark_product": "Queen Size Solid Teak/Babool Storage Bed / 3-Door Almirah",
            "unit_cost": "₹8,500 - ₹12,000 (wood, hardware, polish, labor)",
            "retail_price": "₹18,000 - ₹26,000 per unit",
            "target_gross_margin_percent": 52.0
        }
    },
    {
        "id": "bamboo_products",
        "name": "Bamboo Products",
        "display_name": "Bamboo Products",
        "backend_value": "Handicrafts",
        "sector": "Manufacturing & Crafts",
        "typical_capex_min": 35000.0,
        "typical_capex_max": 850000.0,
        "subcategories": ["Eco-friendly Bamboo Baskets & Hampers", "Bamboo Gazebos & Agro Shade Fencing", "Bamboo Furniture & Lamp Shades", "Bamboo Toothbrushes & Dining Ware"],
        "competitor_search_terms": ["plastic crate sellers", "rural basket weavers", "eco-friendly packaging suppliers"],
        "primary_activities": ["Bamboo pole curing and boric acid preservative treatment", "Mechanical slivering, split making, and knot shaving", "Hand weaving and structural joinery", "Anti-fungal clear varnish finishing"],
        "key_equipment": ["Bamboo cross-cutting and splitting machine", "Bamboo stick / sliver making machine", "Hot air treatment chamber / chemical dip tank", "Pneumatic stapler and finishing sander"],
        "mandatory_licenses": ["Gram Panchayat Cottage Industry NOC", "Forest Dept Bamboo Sourcing Clearance", "Udyam MSME"],
        "location_factors": {
            "bamboo_groves": "Situated near tribal or riverbank bamboo clusters (e.g. Dang, Tapi, Narmada)",
            "water_tanks": "Tanks for soaking bamboo in eco-friendly salt preservatives",
            "shade_shed": "Good natural ventilation to dry treated bamboo"
        },
        "market_profile": {
            "catchment_radius_km": 40,
            "target_population": 40000,
            "customer_segments": ["Agro produce traders (packaging baskets)", "Eco-resorts, farm stays, and cafes", "Urban lifestyle zero-waste packaging buyers"],
            "channels": ["Wholesale fruit and vegetable market basket supply", "Direct supply to tourism resorts and exhibitions"],
            "peak_seasons": ["Harvest season (fruit/onion packaging)", "Wedding and holiday tourism season"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["Bamboo fruit packaging hampers replacing banned single-use plastic crates", "Aesthetic bamboo gazebos and fencing for highway restaurants"],
            "unmet_needs": ["Chemically treated borer-free bamboo products guaranteed to last 5+ years"],
            "ecosystem_drivers": ["National Bamboo Mission capital incentives", "Rapid shift toward biodegradable sustainable materials"]
        },
        "risk_profile": {
            "primary_risks": ["Powder post beetle insect attacks on untreated bamboo", "Fire hazards in dry bamboo storage yards"],
            "mitigation_strategies": ["Mandatory borax-boric acid vacuum soak treatment", "Maintain strict spark-free no-smoking storage safety zones"]
        },
        "pricing_profile": {
            "benchmark_product": "Set of 5 Treated Agricultural Baskets / 1 Handcrafted Bamboo Lamp",
            "unit_cost": "₹120 (Bamboo culms, treatment, labor)",
            "retail_price": "₹320 - ₹480 per set",
            "target_gross_margin_percent": 62.0
        }
    },
    {
        "id": "leather_products",
        "name": "Leather Products",
        "display_name": "Leather Products",
        "backend_value": "Handicrafts",
        "sector": "Manufacturing & Crafts",
        "typical_capex_min": 45000.0,
        "typical_capex_max": 950000.0,
        "subcategories": ["Traditional Footwear (Juttis/Chappals)", "Heavy-Duty Agrarian Work Boots", "Leather Belts, Wallets & Bags", "Livestock Saddlery & Harnesses"],
        "competitor_search_terms": ["commercial shoe stores", "synthetic footwear sellers", "traditional cobbler artisans"],
        "primary_activities": ["Vegetable tanned leather inspection and grading", "Pattern stamping and clicker die cutting", "Hand skiving, edge-stitching, and riveting", "Buffing, creasing, and natural wax finishing"],
        "key_equipment": ["Heavy-duty cylinder arm leather sewing machine", "Leather strap cutter and skiving machine", "Hand punches, riveting tools, and lasting iron", "Shoe lasting stands and wooden lasts"],
        "mandatory_licenses": ["PM Vishwakarma Leather Artisan Enrollment", "Udyam MSME Registration", "Shop and Establishment Act"],
        "location_factors": {
            "tannery_access": "Access to certified vegetable tanned leather supplies (Kolhapur/Agra/Chennai)",
            "commercial_strip": "High street footwear shopping market",
            "ventilation": "Adequate airflow for adhesive and wax fumes"
        },
        "market_profile": {
            "catchment_radius_km": 25,
            "target_population": 35000,
            "customer_segments": ["Farmers needing durable thorn-resistant agrarian work footwear", "Ethnic fashion enthusiasts seeking handcrafted juttis", "Motorcyclists and youth buying durable leather accessories"],
            "channels": ["Retail workshop storefront", "District weekly haats and temple festival fairs"],
            "peak_seasons": ["Wedding and festival seasons", "Post-harvest agrarian footwear replacement period"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["Orthopedic cushioned pure leather chappals for rural elders", "Custom hand-stitched durable farmer leather boots"],
            "unmet_needs": ["Breathable 100% pure leather durable footwear at prices competitive with short-lived plastic PVC shoes"],
            "ecosystem_drivers": ["PM Vishwakarma Charmkar artisan toolkit and low-interest credit", "Heritage GI revival for regional leather crafts"]
        },
        "risk_profile": {
            "primary_risks": ["Competition from cheap Chinese synthetic rexine imports", "Leather raw hide price fluctuations"],
            "mitigation_strategies": ["Highlight '100% Pure Vegetable Tanned Leather' stamp and 1-year stitch warranty", "Direct wholesale hide sourcing from certified cluster tanneries"]
        },
        "pricing_profile": {
            "benchmark_product": "Handcrafted Leather Chappal Pair / Heavy Work Boot",
            "unit_cost": "₹240 - ₹340 (leather, insole, sole, hardware)",
            "retail_price": "₹650 - ₹1,100 per pair",
            "target_gross_margin_percent": 64.0
        }
    },

    # -------------------------------------------------------------
    # 4. Repair, Technology & Digital Services
    # -------------------------------------------------------------
    {
        "id": "mobile_repair",
        "name": "Mobile Repair",
        "display_name": "Mobile Repair",
        "backend_value": "Services",
        "sector": "Repairs & Maintenance",
        "typical_capex_min": 40000.0,
        "typical_capex_max": 700000.0,
        "subcategories": ["Smartphone Screen Replacement (Touch Glass/Folder)", "Charging Port & Mic Chip-Level Micro-Soldering", "Battery Replacement & Power IC Repair", "Accessories (Chargers, Tempered Glass, OTG)"],
        "competitor_search_terms": ["taluka mobile centers", "authorized brand service outlets", "local mobile recharge shops"],
        "primary_activities": ["Component-level diagnostics using digital multimeter", "Hot-air rework station SMD IC de-soldering", "OCA screen laminating and bubble removing", "Rapid same-day handset delivery to farmers"],
        "key_equipment": ["SMD Hot Air Rework Station (Quick 857D)", "Regulated DC Power Supply (30V/5A)", "LCD Separator & OCA Laminator Machine", "Digital stereo microscope and precision screwdrivers"],
        "mandatory_licenses": ["Shop & Establishment Registration", "Udyam MSME Certificate"],
        "location_factors": {
            "bus_stand_crossroad": "Adjacent to town bus stand or high-traffic market entrance",
            "anti_static": "ESD anti-static matting and grounding setup",
            "high_lighting": "Magnifier LED work lights for micro-soldering precision"
        },
        "market_profile": {
            "catchment_radius_km": 15,
            "target_population": 40000,
            "customer_segments": ["Farmers dependent on smartphones for DBT/Kisan apps/UPI", "Students and youth consuming mobile video", "Local shopkeepers and drivers needing GPS phones"],
            "channels": ["Direct walk-in repair desk", "High-margin accessory cross-selling at checkout"],
            "peak_seasons": ["Monsoon season (water damage repairs surge 300%)", "Harvest festival payout weeks"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["Same-day screen folder replacement while farmer finishes weekly mandi shopping", "Fast-moving accessory bundles (braided cables + 33W fast chargers)"],
            "unmet_needs": ["Honest transparent repairs where original camera/battery parts are not swapped"],
            "ecosystem_drivers": ["Massive rural smartphone penetration driven by UPI and YouTube", "Lack of authorized service centers within 30 km radius"]
        },
        "risk_profile": {
            "primary_risks": ["Motherboard damage during delicate SMD IC heating", "Accumulating uncollected repaired phones of non-paying customers"],
            "mitigation_strategies": ["Test all handset functions with customer present before issuing job sheet", "Collect upfront parts advance on all major display jobs"]
        },
        "pricing_profile": {
            "benchmark_product": "Smartphone Display Folder Replacement / Charging Jack Repair",
            "unit_cost": "₹450 (Folder part) | ₹35 (Charging port component)",
            "retail_price": "₹1,150 - ₹1,400 (Folder) | ₹250 - ₹350 (Jack repair)",
            "target_gross_margin_percent": 62.0
        }
    },
    {
        "id": "electronics_repair",
        "name": "Electronics Repair",
        "display_name": "Electronics Repair",
        "backend_value": "Services",
        "sector": "Repairs & Maintenance",
        "typical_capex_min": 45000.0,
        "typical_capex_max": 850000.0,
        "subcategories": ["Inverter & Solar Charge Controller Repair", "LED TV & SMPS Power Board Repair", "Water Pump Motor Starter & Control Panel", "Home Appliance (Mixer, Fan, Microwave) Rewinding"],
        "competitor_search_terms": ["village electrician", "authorized TV service franchise", "submersible motor rewinding shops"],
        "primary_activities": ["Circuit trace testing and component replacement (Capacitor/MOSFET)", "Submersible starter panel rewiring and contactor replacement", "LED backlight strip replacement and firmware flashing", "On-site farmer solar pump inverter troubleshooting"],
        "key_equipment": ["Digital Storage Oscilloscope (DSO)", "LCR component tester and variable AC variac", "Automatic wire stripping and crimping tool", "Heavy-duty 60W soldering iron & desoldering pump"],
        "mandatory_licenses": ["Electrical Contractor / Wireman License", "Shop and Establishment Act", "Udyam MSME"],
        "location_factors": {
            "vehicle_access": "Ground floor parking for farmers unloading heavy inverters and motors",
            "three_phase_bench": "Three-phase testing testbed with circuit breaker safety",
            "burn_in_rack": "Burn-in testing rack for 24-hour inverter load trials"
        },
        "market_profile": {
            "catchment_radius_km": 20,
            "target_population": 45000,
            "customer_segments": ["Farmers with agricultural submersible pump panels and solar systems", "Rural households relying on home inverters during load shedding", "Local institutions, schools, and health sub-centers"],
            "channels": ["Workshop walk-in repair intake", "On-call field visits to farm tube-wells"],
            "peak_seasons": ["Summer season (inverter and ceiling fan repairs surge)", "Monsoon lightning strike surge on electrical boards"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["Solar rooftop inverter and agricultural PM-KUSUM pump controller servicing", "LED TV backlight restoration at 1/4th the price of new TVs"],
            "unmet_needs": ["Certified technician able to repair modern digital microcontroller boards instead of forcing full board replacement"],
            "ecosystem_drivers": ["PM Surya Ghar Muft Bijli Yojana installation boom", "Heavy reliance on solar water pumping in rural agriculture"]
        },
        "risk_profile": {
            "primary_risks": ["High-voltage shock hazard during live board testing", "Shortages of specific microcontroller ICs"],
            "mitigation_strategies": ["Install 1:1 isolation transformer on all testing workbenches", "Build relationships with wholesale electronics parts suppliers in regional tech markets"]
        },
        "pricing_profile": {
            "benchmark_product": "Home Inverter PCB Board Repair / LED TV Power Board Restoration",
            "unit_cost": "₹120 - ₹250 (MOSFETs, capacitors, relay, solder)",
            "retail_price": "₹650 - ₹1,200 standard repair labor charge",
            "target_gross_margin_percent": 75.0
        }
    },
    {
        "id": "two_wheeler_repair",
        "name": "Two-Wheeler Repair",
        "display_name": "Two-Wheeler Repair",
        "backend_value": "Services",
        "sector": "Repairs & Maintenance",
        "typical_capex_min": 60000.0,
        "typical_capex_max": 1200000.0,
        "subcategories": ["Periodic Engine Servicing & Oil Change", "Engine Overhaul & Piston Valve Tuning", "Tubeless Puncture & Radial Tire Replacement", "Electric Scooter & Battery Pack Diagnostics"],
        "competitor_search_terms": ["authorized OEM dealer service center", "roadside mechanics", "spare parts counter garages"],
        "primary_activities": ["Pressure jet vehicle washing", "Engine oil drainage and multi-point safety check", "Carburetor/Fuel injector ultrasonic cleaning", "Brake shoe replacement and chain adjustment"],
        "key_equipment": ["Hydraulic two-wheeler motorcycle ramp lift", "Commercial air compressor (3 HP)", "High-pressure water jet washer", "Pneumatic impact wrench and specialty pullers"],
        "mandatory_licenses": ["Gram Panchayat Workshop License", "Pollution Control Board Waste Oil Disposal Clearance", "Udyam MSME"],
        "location_factors": {
            "highway_frontage": "Direct highway or state road frontage for breakdown walk-ins",
            "concrete_forecourt": "Spacious concrete wash bay with oil-water separator trap",
            "spares_storage": "Secured parts racks for genuine fast-moving oils and filters"
        },
        "market_profile": {
            "catchment_radius_km": 15,
            "target_population": 35000,
            "customer_segments": ["Commuter motorcycle owners (Hero Splendor, Bajaj Platina, Honda Activa)", "Rural delivery agents and milk collectors", "Agricultural laborers traveling to fields"],
            "channels": ["Direct garage drive-in service", "Breakdown roadside emergency rescue service"],
            "peak_seasons": ["Monsoon mud season (chain and brake servicing)", "Post-harvest festival maintenance rush"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["High-margin engine oil + oil filter replacement packages", "Servicing emerging rural electric two-wheelers"],
            "unmet_needs": ["Quick 45-minute scheduled service without the long waiting lines and high labor costs of town dealer franchises"],
            "ecosystem_drivers": ["Two-wheelers are the primary lifeline for rural mobility in India", "Consistent daily recurring cash inflows"]
        },
        "risk_profile": {
            "primary_risks": ["Environmental penalties for improper engine oil disposal", "Slow-moving inventory in non-standard spare parts"],
            "mitigation_strategies": ["Contract with authorized recyclers to sell spent engine oil at ₹20/L", "Stock only top 30 universal high-turnover parts (plugs, brakes, 4T oils)"]
        },
        "pricing_profile": {
            "benchmark_product": "Comprehensive Motorcycle Periodic Service + 4T Synthetic Blend Engine Oil",
            "unit_cost": "₹280 (1 Litre 4T oil, filter, degreaser, wash water)",
            "retail_price": "₹600 - ₹750 complete service package",
            "target_gross_margin_percent": 58.0
        }
    },
    {
        "id": "computer_printing",
        "name": "Computer / Printing Centre",
        "display_name": "Computer / Printing Centre",
        "backend_value": "Services",
        "sector": "Repairs & Maintenance",
        "typical_capex_min": 45000.0,
        "typical_capex_max": 900000.0,
        "subcategories": ["High-Speed Photocopy & Document Binding", "Flex Banner & Vinyl Signage Printing", "Color Photo Printing & Lamination", "Stationery & School Project Supplies"],
        "competitor_search_terms": ["taluka xerox centres", "city flex printers", "stationery stores near court"],
        "primary_activities": ["High-volume black & white laser photocopying", "Document scanning, spiral binding, and hot pouch lamination", "Large-format flex banner designing and solvent printing", "Urgent passport photo capturing and color printing"],
        "key_equipment": ["Heavy-duty digital multifunctional photocopier (Canon/Kyocera)", "Inkjet 6-color photo printer with continuous ink tank", "Electric roll thermal laminator", "Industrial heavy-duty paper guillotine cutter"],
        "mandatory_licenses": ["Shop and Establishment Act", "Udyam MSME Registration"],
        "location_factors": {
            "institutional_vicinity": "Within 200m of taluka court, tehsil office, college, or bank branches",
            "air_conditioned": "Dust-free climate control to prevent photocopier roller paper jams",
            "power_continuity": "Pure sine wave online UPS for uninterrupted printing"
        },
        "market_profile": {
            "catchment_radius_km": 12,
            "target_population": 30000,
            "customer_segments": ["Citizens filing revenue, land registry (7/12), and court affidavits", "College and high school students preparing exam projects", "Local political and business clients ordering flex banners"],
            "channels": ["Direct shop walk-in counter", "WhatsApp document printing queue"],
            "peak_seasons": ["School/College admission season (June-August)", "Panchayat/State election campaign flex banner boom"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["High-margin instant flex banner printing for local business openings and festivals", "Complete legal documentation sets (Stamp paper + notary + photocopying)"],
            "unmet_needs": ["Fast automated photocopying without 20-minute waiting lines on court/tehsil days"],
            "ecosystem_drivers": ["Growing requirement of documentation for DBT government schemes", "Local political and commercial advertisement growth"]
        },
        "risk_profile": {
            "primary_risks": ["Photocopier drum and toner breakdown during peak morning filing hours", "Paper wastage during print setup errors"],
            "mitigation_strategies": ["Keep spare toner cartridges and imaging unit on site", "Enforce digital PDF print preview checks before large volume runs"]
        },
        "pricing_profile": {
            "benchmark_product": "100 Sheets Double-Sided B&W Photocopy / 1 Flex Banner (6x4 Feet)",
            "unit_cost": "₹0.60 per page | ₹120 (flex media + solvent ink)",
            "retail_price": "₹2.00 per page | ₹360 (Flex banner retail)",
            "target_gross_margin_percent": 68.0
        }
    },
    {
        "id": "digital_services",
        "name": "Digital Services",
        "display_name": "Digital Services",
        "backend_value": "Services",
        "sector": "Repairs & Maintenance",
        "typical_capex_min": 40000.0,
        "typical_capex_max": 650000.0,
        "subcategories": ["Common Service Centre (CSC) Government Portals", "AePS Biometric Cash Withdrawal & Micro-ATM", "Aadhaar / PAN / Voter Card Updates", "Online Job & College Application Filings"],
        "competitor_search_terms": ["gram panchayat e-gram center", "rural post office", "customer service points (CSP)"],
        "primary_activities": ["Facilitating central and state government scheme applications", "Biometric AePS micro-ATM cash dispatches for rural seniors", "Railway (IRCTC) and bus ticket reservation bookings", "Utility electricity/water bill payments and insurance renewals"],
        "key_equipment": ["Desktop PC / Core i5 Laptop with high-speed 4G/fiber net", "STQC certified Biometric fingerprint & iris scanner", "Micro-ATM POS card swipe device", "High-security thermal receipt printer"],
        "mandatory_licenses": ["CSC Village Level Entrepreneur (VLE) ID", "Banking Correspondent (BC) Agent Certification", "IRCTC Authorized Agent License", "Udyam MSME"],
        "location_factors": {
            "panchayat_proximity": "Adjacent to Gram Panchayat office or main village bus stand",
            "seating_area": "Comfortable sheltered seating for elderly pension seekers",
            "data_speed": "High-reliability dual-SIM fiber/broadband connectivity"
        },
        "market_profile": {
            "catchment_radius_km": 10,
            "target_population": 25000,
            "customer_segments": ["Rural seniors receiving social pensions via DBT", "Farmers applying for PM-KISAN, crop insurance, and solar pump grants", "Youth applying for competitive government job recruitments"],
            "channels": ["Fixed village CSC storefront", "Mobile camp visits to remote tribal hamlets on pension payout days"],
            "peak_seasons": ["Government scheme rollout deadlines", "Monthly direct benefit transfer (DBT) pension disbursement weeks"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["Convenient doorstep AePS cash withdrawal saving villagers ₹100 bus fare to town banks", "End-to-end Udyam registration and Ayushman Bharat golden card enrollment"],
            "unmet_needs": ["Honest, helpful digital assistance for illiterate villagers who cannot navigate complex government portals"],
            "ecosystem_drivers": ["Digital India mission pushing 100% paperless DBT transfers", "Widespread bank branch consolidation in remote rural regions"]
        },
        "risk_profile": {
            "primary_risks": ["Biometric mismatch for elderly farm laborers with worn fingerprints", "Portal server downtime on scheme cutoff dates"],
            "mitigation_strategies": ["Equip station with dual iris scanners in addition to fingerprint scanners", "Submit applications 5-7 days ahead of announced government cutoff dates"]
        },
        "pricing_profile": {
            "benchmark_product": "Government Scheme Online Application Processing & AePS Cash Dispense",
            "unit_cost": "₹15 (electricity, paper, internet bandwidth overhead)",
            "retail_price": "₹60 - ₹120 citizen service charge + bank commission",
            "target_gross_margin_percent": 75.0
        }
    },
    {
        "id": "transport_logistics",
        "name": "Transport / Local Logistics",
        "display_name": "Transport / Local Logistics",
        "backend_value": "Services",
        "sector": "Repairs & Maintenance",
        "typical_capex_min": 85000.0,
        "typical_capex_max": 2200000.0,
        "subcategories": ["Rural Goods Delivery (Three-Wheeler / Small Commercial Vehicle)", "Agro-Produce Mandi Freight Transport", "E-commerce Last-Mile Delivery Hub", "Passenger Rural Feeder Auto/Van Service"],
        "competitor_search_terms": ["village tempo unions", "private pickup truck operators", "parcel courier franchisees"],
        "primary_activities": ["Early morning farm-to-mandi crate transport", "Afternoon wholesale shop delivery rounds", "Last-mile package distribution for major courier companies", "Daily scheduled vehicle inspection and route optimization"],
        "key_equipment": ["Small Commercial Vehicle (Tata Ace / Mahindra Bolero Maxi / Electric Cargo)", "Digital route planner and GPS tracker", "Heavy-duty tie-down straps and waterproof tarpaulins", "Hand pallet trolley for cargo handling"],
        "mandatory_licenses": ["Commercial Driving License (LMV-Transport)", "RTO Commercial Vehicle Fitness & Permit", "Goods Carriage Permit", "Motor Vehicle Comprehensive Insurance"],
        "location_factors": {
            "highway_access": "Immediate access to arterial bypass road connecting farm mandis",
            "parking_security": "Gated secured parking overnight for loaded cargo vehicles",
            "fuel_station": "Close proximity to commercial CNG / diesel / EV charging station"
        },
        "market_profile": {
            "catchment_radius_km": 35,
            "target_population": 50000,
            "customer_segments": ["Vegetable and milk farmers requiring early morning mandi transit", "Village kirana store owners procuring stock from town wholesale mandis", "E-commerce courier networks delivering online orders"],
            "channels": ["Dedicated monthly supply contracts with farmer groups", "On-demand phone bookings via local transporter union"],
            "peak_seasons": ["Harvest season (April-May & October-November)", "Pre-Diwali wholesale stock building"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["Shared milk and vegetable collective transport reducing individual farmer freight by 40%", "Dedicated last-mile delivery partner for Amazon/Flipkart/Delhivery in rural pincodes"],
            "unmet_needs": ["Reliable, punctual morning freight that reaches mandi before the 7:00 AM auction starts"],
            "ecosystem_drivers": ["PM Gram Sadak Yojana all-weather rural road connectivity", "Booming rural e-commerce and retail consumer goods delivery"]
        },
        "risk_profile": {
            "primary_risks": ["Diesel/CNG fuel price volatility", "Vehicle accidental breakdown during transit with perishable goods"],
            "mitigation_strategies": ["Index contract freight rates to prevailing fuel price formulas", "Keep tie-ups with backup tempo operators for emergency cargo trans-shipment"]
        },
        "pricing_profile": {
            "benchmark_product": "Full Trip Cargo Transport (25 Km roundtrip with 1-tonne capacity)",
            "unit_cost": "₹420 (fuel, maintenance, driver time allowance)",
            "retail_price": "₹950 - ₹1,300 per trip charge",
            "target_gross_margin_percent": 55.0
        }
    },
    {
        "id": "beauty_salon",
        "name": "Beauty & Salon",
        "display_name": "Beauty & Salon",
        "backend_value": "Services",
        "sector": "Repairs & Maintenance",
        "typical_capex_min": 40000.0,
        "typical_capex_max": 900000.0,
        "subcategories": ["Women Beauty Parlour & Bridal Makeover", "Men Grooming Salon & Barber Shop", "Hair Styling, Coloring & Scalp Treatments", "Skin Care, Facials & Mehendi Art"],
        "competitor_search_terms": ["traditional village barbers", "home-based parlor ladies", "town beauty studios"],
        "primary_activities": ["Hair styling, cutting, and conditioning", "Herbal and gold bridal facials and skin cleansing", "Wedding and festive bridal makeovers and saree draping", "Sanitization of scissors, trimmers, and styling tools"],
        "key_equipment": ["Hydraulic salon styling chairs", "Hair steamer and professional blow dryers", "UV tool sterilizer cabinet", "Full-length illuminated LED vanity mirrors"],
        "mandatory_licenses": ["Shop & Establishment Registration", "Udyam MSME Certificate"],
        "location_factors": {
            "privacy": "First-floor or frosted-glass storefront ensuring privacy for female clients",
            "continuous_water": "Uninterrupted running hot and cold water for hair washing",
            "ambient_cooling": "Air-conditioned reception and styling zone"
        },
        "market_profile": {
            "catchment_radius_km": 12,
            "target_population": 25000,
            "customer_segments": ["Brides and bridal party members", "College youth and working professionals", "Homemakers seeking monthly grooming maintenance"],
            "channels": ["Direct salon appointment booking", "Doorstep wedding bridal service packages"],
            "peak_seasons": ["Wedding season (November-February & May-June)", "Festive occasions (Navratri, Eid, Karwa Chauth)"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["High-value bridal makeover packages (₹3,500 - ₹10,000 per wedding)", "Modern youth grooming (beard styling, hair spa, anti-dandruff treatments)"],
            "unmet_needs": ["Hygienic, air-conditioned professional grooming with sterilized instruments in rural talukas"],
            "ecosystem_drivers": ["Aspiration for camera-ready grooming driven by social media and wedding shoots", "Rising disposable income among rural youth"]
        },
        "risk_profile": {
            "primary_risks": ["Skin allergies caused by low-quality bleach or hair dyes", "Seasonal revenue slump during non-wedding months"],
            "mitigation_strategies": ["Always perform 24-hour patch tests before chemical dye applications", "Offer attractive off-season monthly membership subscription packages"]
        },
        "pricing_profile": {
            "benchmark_product": "Complete Bridal Makeover Package / Standard Men Grooming Combo",
            "unit_cost": "₹800 (Bridal cosmetic consumables) | ₹40 (Men combo supplies)",
            "retail_price": "₹3,500 - ₹7,000 (Bridal) | ₹250 - ₹400 (Men combo)",
            "target_gross_margin_percent": 75.0
        }
    },
    {
        "id": "services",
        "name": "Services",
        "display_name": "Services",
        "backend_value": "Services",
        "sector": "Repairs & Maintenance",
        "typical_capex_min": 50000.0,
        "typical_capex_max": 1000000.0,
        "subcategories": ["Rural Equipment Maintenance", "Welding & Metal Fabrication", "Plumbing & Sanitary Installation", "Custom Fabrication Workshop"],
        "competitor_search_terms": ["village fabrication shops", "general maintenance technicians", "local welding garages"],
        "primary_activities": ["Tractor trolley and farm gate welding fabrication", "Structural angle iron cutting and assembly", "Emergency on-site breakdown repair for farmers", "Painting and anti-rust primer application"],
        "key_equipment": ["Inverter ARC welding machine (250-400 Amp)", "Heavy-duty chop saw and angle grinder", "Bench drill press", "Pneumatic spray paint gun"],
        "mandatory_licenses": ["Shop & Establishment Registration", "Udyam MSME Certificate"],
        "location_factors": {
            "heavy_power": "Three-phase electric connection supporting heavy welding surges",
            "unobstructed_yard": "Spacious open yard for tractor trolley and gate fabrication",
            "fire_protection": "Clear concrete floor free from dry straw or combustible fuels"
        },
        "market_profile": {
            "catchment_radius_km": 20,
            "target_population": 40000,
            "customer_segments": ["Farmers needing tractor trolley, cultivator, and shed fabrication", "Rural house builders requiring window grills and iron gates", "Local businesses needing repair of rolling shutters"],
            "channels": ["Direct fabrication yard walk-in commissions", "Word-of-mouth referral by building contractors"],
            "peak_seasons": ["Pre-harvest machinery overhaul (March & September)", "Pre-monsoon shed roof fabrication"]
        },
        "opportunity_profile": {
            "high_growth_segments": ["Lightweight high-strength tractor tipping trolley bodies", "Custom prefabricated solar pump iron mounting structures"],
            "unmet_needs": ["Fast turnaround emergency welding repairs during active crop harvesting"],
            "ecosystem_drivers": ["Booming rural infrastructure construction", "Continuous wear and tear on agricultural implements"]
        },
        "risk_profile": {
            "primary_risks": ["Eye injury from welding arc flash and grinding sparks", "Steel raw material wholesale price fluctuations"],
            "mitigation_strategies": ["Provide mandatory auto-darkening welding helmets and leather safety gauntlets", "Price client fabrication quotes based on prevailing steel price per kg + fixed labor markup"]
        },
        "pricing_profile": {
            "benchmark_product": "Standard Iron Entrance Gate Fabrication (10x6 Feet) & Farm Welding Service",
            "unit_cost": "₹4,200 (angles, square pipes, welding rods, primer)",
            "retail_price": "₹7,500 - ₹9,500 fabricated gate",
            "target_gross_margin_percent": 48.0
        }
    }
]


class CentralizedCategoriesConfig:
    """Helper service for querying the centralized business categories registry."""

    @classmethod
    def get_all_categories(cls) -> List[Dict[str, Any]]:
        return CATEGORIES_REGISTRY

    @classmethod
    def get_category_by_id(cls, category_id: str) -> Optional[Dict[str, Any]]:
        cid = category_id.strip().lower()
        for cat in CATEGORIES_REGISTRY:
            if cat["id"].lower() == cid:
                return cat
        return None

    @classmethod
    def get_category_by_name(cls, name: str) -> Optional[Dict[str, Any]]:
        n = name.strip().lower()
        for cat in CATEGORIES_REGISTRY:
            if cat["name"].lower() == n or cat["display_name"].lower() == n:
                return cat
            # Check subcategories
            for sub in cat.get("subcategories", []):
                if sub.lower() == n:
                    return cat
        return None

    @classmethod
    def get_categories_by_sector(cls, sector: str) -> List[Dict[str, Any]]:
        s = sector.strip().lower()
        return [cat for cat in CATEGORIES_REGISTRY if cat.get("sector", "").lower() == s]

    @classmethod
    def get_supported_names(cls) -> List[str]:
        return [cat["name"] for cat in CATEGORIES_REGISTRY]
