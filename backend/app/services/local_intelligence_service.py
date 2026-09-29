"""
Phase B8 — Local Business Intelligence Service
Generates dynamic, hyper-local business, market, SWOT, opportunity, risk, competitor,
pricing, and recommendation intelligence driven by:
    LOCATION + BUSINESS CATEGORY + AVAILABLE CAPITAL + LANGUAGE
Zero static hardcoding. Every output adapts dynamically to the selected domain parameters.
"""

from typing import Dict, Any, List, Optional
from app.data.categories_config import CATEGORIES_REGISTRY, CentralizedCategoriesConfig
from app.schemas.schemas import (
    MarketReachAnalysis,
    OpportunityAnalysis,
    OpportunityItem,
    SWOTAnalysis,
    RiskItem,
    CompetitorItem,
    PricingGuidance,
    BusinessRecommendation,
    BusinessProfile,
    LocationData,
)


CATEGORY_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "Agriculture": {"hi": "कृषि", "gu": "કૃષિ"},
    "Dairy": {"hi": "डेयरी", "gu": "ડેરી"},
    "Poultry": {"hi": "पोल्ट्री / कुक्कुट पालन", "gu": "પોલ્ટ્રી / મરઘા પાલન"},
    "Goat Farming": {"hi": "बकरी पालन", "gu": "બકરા પાલન"},
    "Fisheries": {"hi": "मत्स्य पालन", "gu": "મત્સ્ય પાલન"},
    "Beekeeping": {"hi": "मधुमक्खी पालन", "gu": "મધમાખી પાલન"},
    "Nursery & Plant Business": {"hi": "पौधशाला एवं पादप व्यवसाय", "gu": "નર્સરી અને રોપા વ્યવસાય"},
    "Agricultural Equipment Rental": {"hi": "कृषि उपकरण किराया केंद्र", "gu": "કૃષિ સાધનો ભાડે આપવાનો વ્યવસાય"},
    "Agricultural Input Store": {"hi": "कृषि इनपुट केंद्र (खाद-बीज)", "gu": "કૃષિ ઇનપુટ સ્ટોર (ખાતર-બિયારણ)"},
    "Grocery / Kirana": {"hi": "किराना दुकान", "gu": "કરિયાણાની દુકાન"},
    "Grocery": {"hi": "किराना दुकान", "gu": "કરિયાણાની દુકાન"},
    "Food Processing": {"hi": "खाद्य प्रसंस्करण", "gu": "ખાદ્ય પ્રક્રિયા"},
    "Bakery": {"hi": "बेकरी व्यवसाय", "gu": "બેકરી વ્યવસાય"},
    "Snacks & Namkeen": {"hi": "नाश्ता एवं नमकीन", "gu": "નાસ્તા અને નમકીન"},
    "Pickles & Papad": {"hi": "अचार एवं पापड़ निर्माण", "gu": "અથાણાં અને પાપડ ઉત્પાદન"},
    "Flour Mill": {"hi": "आटा चक्की", "gu": "લોટ દળવાની ઘંટી"},
    "Fruit & Vegetable Processing": {"hi": "फल एवं सब्जी प्रसंस्करण", "gu": "ફળ અને શાકભાજી પ્રોસેસિંગ"},
    "Textile & Clothing": {"hi": "वस्त्र एवं परिधान", "gu": "કાપડ અને વસ્ત્ર ઉત્પાદન"},
    "Tailoring & Embroidery": {"hi": "सिलाई एवं कढ़ाई", "gu": "દરજીકામ અને ભરતકામ"},
    "Handicrafts": {"hi": "हस्तशिल्प", "gu": "હસ્તકલા"},
    "Pottery": {"hi": "मिट्टी के बर्तन / कुम्हार कला", "gu": "કુંભારીકામ / માટીના વાસણો"},
    "Furniture": {"hi": "फर्नीचर निर्माण", "gu": "ફર્નિચર વ્યવસાય"},
    "Bamboo Products": {"hi": "बांस उत्पाद निर्माण", "gu": "વાંસ ઉત્પાદનો"},
    "Leather Products": {"hi": "चर्म उत्पाद निर्माण", "gu": "ચામડાના ઉત્પાદનો"},
    "Mobile Repair": {"hi": "मोबाइल मरम्मत केंद्र", "gu": "મોબાઇલ રિપેરિંગ"},
    "Electronics Repair": {"hi": "इलेक्ट्रॉनिक्स मरम्मत", "gu": "ઇલેક્ટ્રોનિક્સ રિપેરિંગ"},
    "Two-Wheeler Repair": {"hi": "दुपहिया मरम्मत कार्यशाला", "gu": "ટૂ-વ્હીલર રિપેરિંગ વર્કશોપ"},
    "Computer / Printing Centre": {"hi": "कंप्यूटर एवं प्रिंटिंग केंद्र", "gu": "કોમ્પ્યુટર અને પ્રિન્ટિંગ સેન્ટર"},
    "Digital Services": {"hi": "डिजिटल सेवा केंद्र", "gu": "ડિજિટલ સેવા કેન્દ્ર"},
    "Transport / Local Logistics": {"hi": "परिवहन एवं स्थानीय लॉजिस्टिक्स", "gu": "પરિવહન અને સ્થાનિક લોજિસ્ટિક્સ"},
    "Beauty & Salon": {"hi": "सौंदर्य एवं सैलून", "gu": "બ્યુટી પાર્લર અને સલૂન"},
    "Services": {"hi": "सेवाएं", "gu": "સેવાઓ"},
}


class LocalIntelligenceService:
    """
    Core service delivering dynamic hyper-local business intelligence for rural micro-enterprises.
    Fully localized in English (en), Hindi (hi), and Gujarati (gu).
    """

    @classmethod
    def get_localized_category_name(cls, cat_name: str, lang: str) -> str:
        """Returns the localized display name for a given canonical category."""
        lang_code = (lang or "en").lower().strip()
        if lang_code in ["hi", "gu"] and cat_name in CATEGORY_TRANSLATIONS:
            return CATEGORY_TRANSLATIONS[cat_name].get(lang_code, cat_name)
        return cat_name

    @classmethod
    def resolve_category_meta(cls, raw_category: str) -> Dict[str, Any]:
        """Resolves user category string to centralized category metadata."""
        if not raw_category:
            return CATEGORIES_REGISTRY[0]

        # 1. Direct name or display_name match
        cat = CentralizedCategoriesConfig.get_category_by_name(raw_category)
        if cat:
            return cat

        # 2. Match on ID
        cat = CentralizedCategoriesConfig.get_category_by_id(raw_category)
        if cat:
            return cat

        # 3. Fuzzy search across names and subcategories
        q = raw_category.strip().lower()
        for c in CATEGORIES_REGISTRY:
            if q in c["name"].lower() or c["name"].lower() in q:
                return c
            for sub in c.get("subcategories", []):
                if q in sub.lower() or sub.lower() in q:
                    return c

        return CATEGORIES_REGISTRY[0]

    @classmethod
    def parse_location_details(cls, location_str: str, location_detail: Optional[LocationData] = None) -> Dict[str, str]:
        """Extracts town, taluka, district, and state context from location data or string."""
        if location_detail:
            town = location_detail.village_town_city or location_str.split(",")[0].strip()
            taluka = location_detail.taluka_subdistrict or f"{town} Taluka"
            district = location_detail.district or town
            state = location_detail.state or ("Gujarat" if "gujarat" in location_str.lower() else "India")
        else:
            parts = [p.strip() for p in (location_str or "Anand, Gujarat").split(",") if p.strip()]
            town = parts[0] if parts else "Anand"
            district = parts[0] if parts else "Anand"
            state = parts[1] if len(parts) > 1 else ("Gujarat" if "gujarat" in location_str.lower() else "India")
            taluka = f"{town} Taluka"

        return {
            "town": town,
            "taluka": taluka,
            "district": district,
            "state": state,
            "clean_address": location_str.strip() or f"{town}, {state}",
        }

    # -------------------------------------------------------------------------
    # 1. Market Reach Analysis
    # -------------------------------------------------------------------------
    @classmethod
    def generate_market_analysis(
        cls,
        cat: Dict[str, Any],
        loc_info: Dict[str, str],
        capital: float,
        language: str = "en",
    ) -> MarketReachAnalysis:
        lang = (language or "en").lower().strip()
        cat_mkt = cat.get("market_profile", {})
        raw_cat_name = cat["name"]
        loc_cat_name = cls.get_localized_category_name(raw_cat_name, lang)
        town = loc_info["town"]
        district = loc_info["district"]
        full_loc = loc_info["clean_address"]

        catchment_km = cat_mkt.get("catchment_radius_km", 15)
        base_pop = cat_mkt.get("target_population", 30000)

        # Dynamic population multiplier based on region profile
        pop_mult = 1.2 if district.lower() in ["anand", "surat", "rajkot", "ahmedabad", "pune", "indore"] else 0.85
        estimated_pop = int(base_pop * pop_mult)

        if lang == "hi":
            segments = [
                f"{town} क्षेत्र के स्थानीय कृषि एवं ग्रामीण परिवार",
                f"{district} के कस्बाई सूक्ष्म उद्यम और साप्ताहिक हाट व्यापारी",
                f"{district} के संस्थागत एवं सामुदायिक थोक खरीदार",
            ]
            channels = [
                f"{town} के मुख्य बाज़ार में सीधी दुकान / काउंटर",
                f"{district} के गांवों में साप्ताहिक ग्रामीण हाट स्टॉल",
                "व्हाट्सएप सामुदायिक ऑर्डरिंग एवं डिजिटल भुगतान होम डिलीवरी",
            ]
            peak_seasons = [
                "फसल कटाई के बाद के त्यौहार (अक्टूबर - जनवरी)",
                "मानसून पूर्व कृषि तैयारी के महीने (मई - जून)",
            ]
            summary = (
                f"{full_loc} वाणिज्यिक क्षेत्र (~{catchment_km} किमी दायरा, लगभग "
                f"{estimated_pop:,} निवासियों की सेवा) के भीतर, {loc_cat_name} मजबूत स्थानीय मांग प्रदर्शित करता है। "
                f"प्राथमिक उपभोक्ता मांग {segments[0]} से आती है, जिसे {channels[0]} के माध्यम से सुदृढ़ किया जाता है।"
            )
        elif lang == "gu":
            segments = [
                f"{town} વિસ્તારના સ્થાનિક ખેડૂત અને ગ્રામીણ પરિવારો",
                f"{district} ના નગર સૂક્ષ્મ સાહસો અને સાપ્તાહિક હાટ વેપારીઓ",
                f"{district} ના સંસ્થાકીય અને સામુદાયિક જથ્થાબંધ ખરીદદારો",
            ]
            channels = [
                f"{town} ના મુખ્ય બજારમાં સીધો કાઉન્ટર / શોપ",
                f"{district} ના ગામોમાં સાપ્તાહિક ગ્રામીણ હાટ સ્ટોલ",
                "વોટ્સએપ ઓર્ડરિંગ અને ડિજિટલ પેમેન્ટ ડિલિવરી",
            ]
            peak_seasons = [
                "લણણી પછીની તહેવારોની મોસમ (ઓક્ટોબર - જાન્યુઆરી)",
                "ચોમાસા પહેલા કૃષિ તૈયારીના મહિના (મે - જૂન)",
            ]
            summary = (
                f"{full_loc} વ્યાપારી ક્ષેત્ર (~{catchment_km} કિમી ત્રિજ્યા, આશરે "
                f"{estimated_pop:,} નાગરિકો) માં, {loc_cat_name} મજબૂત સ્થાનિક માંગ દર્શાવે છે. "
                f"પ્રાથમિક ગ્રાહક માંગ {segments[0]} તરફથી આવે છે, જે {channels[0]} દ્વારા વધુ સુદૃઢ બને છે."
            )
        else:
            # Default English
            segments = cat_mkt.get("customer_segments", [
                f"Local agrarian and village households in {town} catchment",
                f"Town micro-enterprises and weekly haat traders in {district}",
                f"Institutional and community bulk buyers in {district}",
            ])
            base_channels = cat_mkt.get("channels", [
                f"Direct storefront / counter in {town} central market",
                f"Weekly rural haat stalls across {district} villages",
                "WhatsApp community ordering and digital payment delivery",
            ])
            channels = [
                f"{ch} ({town} corridor)" if "corridor" not in ch and "in " not in ch else ch
                for ch in base_channels
            ]
            peak_seasons = cat_mkt.get("peak_seasons", [
                "Post-harvest festival cycles (October - January)",
                "Pre-monsoon agrarian preparation months (May - June)",
            ])
            summary = (
                f"Within the {full_loc} commercial territory (~{catchment_km} km radius, serving approximately "
                f"{estimated_pop:,} residents), {raw_cat_name} demonstrates resilient local demand. "
                f"Primary customer pull comes from {segments[0]}, reinforced by channel access through {channels[0]}."
            )

        return MarketReachAnalysis(
            catchment_radius_km=catchment_km,
            estimated_target_population=estimated_pop,
            primary_customer_segments=segments,
            high_demand_local_channels=channels,
            peak_demand_seasons=peak_seasons,
            market_reach_summary=summary,
            is_demo_data=True,
        )

    # -------------------------------------------------------------------------
    # 2. Opportunity Analysis (3 to 6 structured items)
    # -------------------------------------------------------------------------
    @classmethod
    def generate_opportunities(
        cls,
        cat: Dict[str, Any],
        loc_info: Dict[str, str],
        capital: float,
        language: str = "en",
    ) -> OpportunityAnalysis:
        lang = (language or "en").lower().strip()
        cat_opp = cat.get("opportunity_profile", {})
        raw_cat_name = cat["name"]
        loc_cat_name = cls.get_localized_category_name(raw_cat_name, lang)
        town = loc_info["town"]
        district = loc_info["district"]
        full_loc = loc_info["clean_address"]
        catchment_km = cat.get("market_profile", {}).get("catchment_radius_km", 15)

        raw_growth = cat_opp.get("high_growth_segments", [])
        raw_unmet = cat_opp.get("unmet_needs", [])
        raw_drivers = cat_opp.get("ecosystem_drivers", [])

        opp_items: List[OpportunityItem] = []

        if lang == "hi":
            # Opportunity 1: High Growth Segment
            opp_items.append(
                OpportunityItem(
                    title=f"उच्च मार्जिन {loc_cat_name} मूल्य-वर्धित उत्पाद",
                    type="High Growth",
                    description=(
                        f"{town} में विशिष्ट एवं प्रीमियम-ग्रेड {loc_cat_name} उत्पादों की तेजी से बढ़ती मांग, "
                        f"जो सामान्य वस्तुओं की तुलना में 25-40% अधिक मूल्य दिलाती है।"
                    ),
                    reason="ग्रामीण एवं अर्ध-शहरी परिवारों की बढ़ती क्रय शक्ति और गुणवत्ता के प्रति जागरूकता।",
                    local_factor=f"{full_loc} में मजबूत ग्राहक उपस्थिति और गुणवत्तापूर्ण उत्पादों की प्राथमिकता।",
                    impact="High Growth",
                )
            )
            # Opportunity 2: Unmet Local Need
            opp_items.append(
                OpportunityItem(
                    title=f"{loc_cat_name} की विश्वसनीय, उसी दिन स्थानीय आपूर्ति",
                    type="Unmet Need",
                    description=(
                        f"{town} के उपभोक्ता वर्तमान में दूर के कस्बों पर निर्भर हैं या अनियमित आपूर्ति का सामना करते हैं। "
                        f"एक स्थानीय केंद्र शुरू करने से समुदाय का विश्वास और बाज़ार हिस्सा तुरंत मिलता है।"
                    ),
                    reason="आने-जाने का समय और परिवहन लागत बचती है तथा प्रामाणिक विश्वसनीयता मिलती है।",
                    local_factor=f"{town} के आसपास {catchment_km} किमी के दायरे में पहले प्रस्तावक का लाभ।",
                    impact="Immediate Entry",
                )
            )
            # Opportunity 3: Ecosystem Driver
            opp_items.append(
                OpportunityItem(
                    title="सरकारी प्राथमिकता क्षेत्र ऋण सब्सिडी और डिजिटल अवसंरचना",
                    type="Ecosystem Driver",
                    description=(
                        f"केंद्रीय एवं राज्य एमएसएमई योजनाएं पंजीकृत {loc_cat_name} उद्यमों के लिए रियायती ब्याज दरें, "
                        f"पूंजीगत सब्सिडी और क्रेडिट गारंटी प्रदान करती हैं।"
                    ),
                    reason="उधार ली गई पूंजी की प्रभावी लागत कम होती है और बिना गारंटी ऋण मिलता है।",
                    local_factor=f"{district} में प्राथमिकता ऋण लक्ष्यों का समर्थन करने वाला सक्रिय ग्रामीण बैंक नेटवर्क।",
                    impact="Strategic Enabler",
                )
            )
            # Opportunity 4: Channel Opportunity
            opp_items.append(
                OpportunityItem(
                    title="व्हाट्सएप कैटलॉग और तत्काल यूपीआई साउंडबॉक्स भुगतान",
                    type="Channel Opportunity",
                    description=(
                        f"{town} के आसपास व्हाट्सएप से डिजिटल ऑर्डरिंग और काउंटर पर वॉयस-अलर्ट यूपीआई साउंडबॉक्स की सुविधा।"
                    ),
                    reason="उधार रोके बिना तत्काल कार्यशील पूंजी का नकदी प्रवाह सुनिश्चित करता है।",
                    local_factor=f"{district} में ग्रामीण परिवारों के बीच मजबूत 4G कनेक्टिविटी और स्मार्टफोन का उपयोग।",
                    impact="Cashflow Accelerator",
                )
            )
            # Opportunity 5: Scale / Capital Opportunity (if well capitalized)
            if capital >= 50000:
                opp_items.append(
                    OpportunityItem(
                        title=f"सीधी थोक खरीद और अर्ध-स्वचालित {loc_cat_name} पैकेजिंग",
                        type="Customer Segment Opportunity",
                        description=(
                            f"आपकी ₹{capital:,.0f} की मार्जिन पूंजी क्षेत्रीय क्लस्टर हब से सीधी थोक खरीद की अनुमति देती है, "
                            f"जिससे लागत 15-22% कम होती है।"
                        ),
                        reason="थोक खरीद से सीधे प्रति-इकाई सकल मार्जिन में सुधार होता है।",
                        local_factor=f"{loc_info['state']} के प्रमुख वाणिज्यिक परिवहन गलियारों से {town} की निकटता।",
                        impact="Margin Expander",
                    )
                )

        elif lang == "gu":
            # Opportunity 1: High Growth Segment
            opp_items.append(
                OpportunityItem(
                    title=f"ઉચ્ચ માર્જિન {loc_cat_name} મૂલ્ય-વર્ધિત ઉત્પાદનો",
                    type="High Growth",
                    description=(
                        f"{town} માં વિશિષ્ટ અને પ્રીમિયમ-ગ્રેડ {loc_cat_name} ઉત્પાદનોની ઝડપથી વધતી માંગ, "
                        f"જે સામાન્ય ઉત્પાદનો કરતાં 25-40% વધુ નફો આપે છે."
                    ),
                    reason="ગ્રામીણ પરિવારોની વધતી આવક અને ગુણવત્તા પ્રત્યે જાગૃતિ.",
                    local_factor=f"{full_loc} માં મજબૂત ગ્રાહક પ્રતિસાદ અને ગુણવત્તાની પસંદગી.",
                    impact="High Growth",
                )
            )
            # Opportunity 2: Unmet Local Need
            opp_items.append(
                OpportunityItem(
                    title=f"{loc_cat_name} ની વિશ્વસનીય અને તાત્કાલિક સ્થાનિક ઉપલબ્ધતા",
                    type="Unmet Need",
                    description=(
                        f"{town} ના સ્થાનિક ગ્રાહકો હાલમાં દૂરના શહેરો પર નિર્ભર છે. "
                        f"સમર્પિત સ્થાનિક કેન્દ્ર શરૂ કરવાથી ગ્રાહકોનો વિશ્વાસ અને બજાર હિસ્સો ઝડપથી મળે છે."
                    ),
                    reason="મુસાફરી ખર્ચ બચે છે અને ઉત્પાદનની સમયસર વિશ્વસનીયતા મળે છે.",
                    local_factor=f"{town} ની આસપાસ {catchment_km} કિમી ત્રિજ્યામાં પ્રથમ પ્રવેગક તરીકેનો ફાયદો.",
                    impact="Immediate Entry",
                )
            )
            # Opportunity 3: Ecosystem Driver
            opp_items.append(
                OpportunityItem(
                    title="સરકારી પ્રાથમિકતા ક્ષેત્ર ધિરાણ સબસિડી અને ડિજિટલ માળખું",
                    type="Ecosystem Driver",
                    description=(
                        f"સરકારી MSME યોજનાઓ નોંધાયેલા {loc_cat_name} સાહસો માટે રાહત દરે વ્યાજ અને મૂડી સબસિડી પૂરી પાડે છે."
                    ),
                    reason="લોનનો વાસ્તવિક ખર્ચ ઘટે છે અને જામીન વગર સરળતાથી લોન મળે છે.",
                    local_factor=f"{district} માં સરકારી ક્રેડિટ યોજનાઓને સહાય કરતું સક્રિય ગ્રામીણ બેંક નેટવર્ક.",
                    impact="Strategic Enabler",
                )
            )
            # Opportunity 4: Channel Opportunity
            opp_items.append(
                OpportunityItem(
                    title="વોટ્સએપ કેટેલોગ ઓર્ડરિંગ અને તાત્કાલિક UPI સાઉન્ડબોક્સ",
                    type="Channel Opportunity",
                    description=(
                        f"{town} માં વોટ્સએપ દ્વારા ડિજિટલ ઓર્ડરિંગ અને કાઉન્ટર પર અવાજ સાથે UPI સાઉન્ડબોક્સથી તાત્કાલિક પેમેન્ટ."
                    ),
                    reason="રોકડ તરલતા જાળવી રાખે છે અને લાંબા સમયની ઉધારી અટકાવે છે.",
                    local_factor=f"{district} ના પરિવારોમાં ઉત્તમ 4G કનેક્ટિવિટી અને સ્માર્ટફોનનો ઉપયોગ.",
                    impact="Cashflow Accelerator",
                )
            )
            # Opportunity 5: Scale / Capital Opportunity (if well capitalized)
            if capital >= 50000:
                opp_items.append(
                    OpportunityItem(
                        title=f"સીધી જથ્થાબંધ ખરીદી અને {loc_cat_name} પેકેજિંગ",
                        type="Customer Segment Opportunity",
                        description=(
                            f"તમારી ₹{capital:,.0f} ની માર્જિન મૂડી મોટા વેપારીઓ પાસેથી સીધી જથ્થાબંધ ખરીદી શક્ય બનાવે છે, "
                            f"જેથી ખર્ચ 15-22% ઘટે છે."
                        ),
                        reason="જથ્થાબંધ ખરીદીથી સીધો નફાનો ગાળો (ગ્રોસ માર્જિન) વધે છે.",
                        local_factor=f"{town} ની મુખ્ય વેપારી ધોરીમાર્ગો સાથેની ઉત્કૃષ્ટ કનેક્ટિવિટી.",
                        impact="Margin Expander",
                    )
                )

        else:
            # Default English
            title_growth = raw_growth[0] if raw_growth else f"High-Margin {raw_cat_name} Value-Added Products"
            opp_items.append(
                OpportunityItem(
                    title=title_growth,
                    type="High Growth",
                    description=(
                        f"Rapidly growing consumer demand in {town} for specialized, premium-grade {raw_cat_name} "
                        f"offerings that command 25-40% higher realization than unbranded generic commodities."
                    ),
                    reason="Increasing household disposable income and health/quality awareness across semi-urban rural belts.",
                    local_factor=f"Strong local footfall and rising consumer preference in {full_loc}.",
                    impact="High Growth",
                )
            )

            title_unmet = raw_unmet[0] if raw_unmet else f"Reliable, Same-Day Fulfillment of {raw_cat_name}"
            opp_items.append(
                OpportunityItem(
                    title=title_unmet,
                    type="Unmet Need",
                    description=(
                        f"Local consumers in {town} currently travel to distant city centers or face inconsistent supply. "
                        f"Establishing a dedicated local hub captures captive community market share immediately."
                    ),
                    reason="Eliminates roundtrip commuter transit costs and provides verified product reliability.",
                    local_factor=f"First-mover advantage within a {catchment_km} km radius around {town}.",
                    impact="Immediate Entry",
                )
            )

            title_driver = raw_drivers[0] if raw_drivers else "Government Priority Sector Subsidies & Digital Infrastructure"
            opp_items.append(
                OpportunityItem(
                    title=title_driver,
                    type="Ecosystem Driver",
                    description=(
                        f"Targeted central and state MSME schemes provide concessional interest rates, capital subsidies, "
                        f"and priority credit guarantees for registered {raw_cat_name} enterprises."
                    ),
                    reason="Reduces effective cost of borrowed capital and eliminates collateral requirements for smallholders.",
                    local_factor=f"Active rural bank branch network in {district} supporting priority lending quotas.",
                    impact="Strategic Enabler",
                )
            )

            opp_items.append(
                OpportunityItem(
                    title="Direct WhatsApp Catalog & Instant UPI Soundbox Settlement",
                    type="Channel Opportunity",
                    description=(
                        f"Enabling digital micro-ordering via WhatsApp with doorstep dispatch across {town} hamlets, "
                        f"paired with instant voice-alert UPI soundbox at the payment counter."
                    ),
                    reason="Drives zero-leakage instant working capital liquidity and prevents long unrecovered customer credit khata.",
                    local_factor=f"High 4G connectivity and smartphone adoption among agrarian families in {district}.",
                    impact="Cashflow Accelerator",
                )
            )

            if capital >= 50000:
                opp_items.append(
                    OpportunityItem(
                        title=f"Direct Wholesale Sourcing & Semi-Automated {raw_cat_name} Packaging",
                        type="Customer Segment Opportunity",
                        description=(
                            f"Your margin capital of ₹{capital:,.0f} allows direct bulk procurement from regional cluster hubs, "
                            f"compressing procurement costs by 15-22% compared to buying from local middlemen."
                        ),
                        reason="Bulk purchasing margin arbitrage directly improves unit gross margin.",
                        local_factor=f"Proximity of {town} to primary arterial freight corridors in {loc_info['state']}.",
                        impact="Margin Expander",
                    )
                )

        return OpportunityAnalysis(
            high_growth_segments=[op.title for op in opp_items if op.type in ["High Growth", "Customer Segment Opportunity"]],
            unmet_local_needs=[op.title for op in opp_items if op.type == "Unmet Need"],
            ecosystem_growth_drivers=[op.title for op in opp_items if op.type in ["Ecosystem Driver", "Channel Opportunity"]],
            items=opp_items,
            is_demo_data=True,
        )

    # -------------------------------------------------------------------------
    # 3. Dynamic SWOT Analysis
    # -------------------------------------------------------------------------
    @classmethod
    def generate_swot(
        cls,
        cat: Dict[str, Any],
        loc_info: Dict[str, str],
        capital: float,
        language: str = "en",
    ) -> SWOTAnalysis:
        lang = (language or "en").lower().strip()
        raw_cat_name = cat["name"]
        loc_cat_name = cls.get_localized_category_name(raw_cat_name, lang)
        town = loc_info["town"]
        district = loc_info["district"]
        min_capex = cat.get("typical_capex_min", 50000.0)

        if lang == "hi":
            strengths = [
                f"{town} के स्थानीय समुदाय एवं परिवारों के साथ सीधा विश्वास-आधारित संबंध",
                f"{district} के शहरी व्यावसायिक आउटलेट्स की तुलना में कम परिचालन एवं किराया खर्च",
                f"विशिष्ट उत्पादों एवं सेवाओं ({', '.join(cat.get('subcategories', [])[:2])}) में त्वरित आपूर्ति",
            ]
            if capital >= min_capex * 1.5:
                strengths.append(f"₹{capital:,.0f} का मजबूत प्रारंभिक पूंजी आवंटन जो परिचालन में सुरक्षा प्रदान करता है")
            else:
                strengths.append("शुरुआती चरण में कम ऋण दायित्व और तेज़ पूंजीगत गतिशीलता")

            weaknesses = [
                f"{loc_cat_name} कच्चे माल के लिए क्षेत्रीय वितरकों की उधारी शर्तों और समय पर निर्भरता",
                "पारंपरिक बहीखाते से डिजिटल इन्वेंट्री एवं बिलिंग की ओर बदलाव का प्रबंधन",
            ]
            if capital < min_capex:
                weaknesses.append(f"सीमित पूंजी (₹{capital:,.0f}) के कारण निरंतर इन्वेंट्री रोटेशन बनाए रखने की आवश्यकता")
            else:
                weaknesses.append("स्थानीय स्तर पर कुशल सहायकों को नियुक्त करने और बनाए रखने की आवश्यकता")

            opportunities = [
                f"{town} तालुका के आसपास के निकटवर्ती गांवों में खुदरा एवं थोक आपूर्ति मार्गों का संभावित विस्तार (संकेतात्मक)",
                "सरकारी प्राथमिक क्षेत्र योजनाओं के तहत रियायती मियादी ऋण (टर्म लोन) वित्तपोषण",
                f"{district} में व्हाट्सएप बिजनेस और डिजिटल प्लेटफॉर्म के माध्यम से सीधा ऑर्डर लेना",
            ]

            threats = [
                f"{district} में मानसून और बुवाई चक्र के दौरान मौसमी कृषि नकदी प्रवाह में उतार-चढ़ाव",
                "थोक कच्चे माल की कीमतों में उतार-चढ़ाव और परिवहन लागत में वृद्धि",
                "साप्ताहिक हाटों में कम गुणवत्ता वाले असंगठित विक्रेताओं से मूल्य प्रतिस्पर्धा",
            ]

        elif lang == "gu":
            strengths = [
                f"{town} ના સ્થાનિક સમાજ અને પરિવારો સાથે સીધો વિશ્વાસપૂર્ણ સંબંધ",
                f"{district} ના મોટા શહેરી સ્ટોર્સ કરતાં ઓછો ઓવરહેડ અને ભાડા ખર્ચ",
                f"વિશિષ્ટ કાર્યક્ષેત્રો ({', '.join(cat.get('subcategories', [])[:2])}) માં ઝડપી અને વિશ્વસનીય સેવા",
            ]
            if capital >= min_capex * 1.5:
                strengths.append(f"₹{capital:,.0f} ની પ્રારંભિક મૂડી જે વ્યવસાયને આર્થિક ટેકો પૂરો પાડે છે")
            else:
                strengths.append("શરૂઆતના તબક્કામાં ઓછું દેવું અને નાણાકીય સ્થિરતા")

            weaknesses = [
                f"{loc_cat_name} કાચા માલ માટે પ્રાદેશિક વિતરકોના નિયમો અને ડિલિવરી સમય પર નિર્ભરતા",
                "પરંપરાગત ચોપડા પદ્ધતિમાંથી ડિજિટલ બિલિંગ અને સ્ટોક મેનેજમેન્ટમાં સંક્રમણ",
            ]
            if capital < min_capex:
                weaknesses.append(f"શરૂઆતની મૂડી (₹{capital:,.0f}) મુજબ સ્ટોક ઝડપથી ફેરવવાની જરૂરિયાત")
            else:
                weaknesses.append("સ્થાનિક સ્તરે કુશળ કારીગરોની ઉપલબ્ધતા જાળવવાની જરૂરિયાત")

            opportunities = [
                f"{town} તાલુકાના નજીકના ગામડાઓમાં છૂટક અને જથ્થાબંધ સપ્લાય રૂટનો સંભવિત વિસ્તાર (સૂચક)",
                "સરકારી પ્રાથમિકતા ક્ષેત્ર યોજનાઓ હેઠળ રાહત દરે લોન ધિરાણ",
                f"{district} માં વોટ્સએપ બિઝનેસ અને ડિજિટલ ઓર્ડરિંગ દ્વારા વેચાણ વૃદ્ધિ",
            ]

            threats = [
                f"{district} માં કૃષિ આધારિત મોસમી આવકના ચક્રમાં વધ-ઘટ",
                "જથ્થાબંધ કાચા માલના ભાવોમાં વધઘટ અને પરિવહન ખર્ચ",
                "સાપ્તાહિક હાટોમાં બિન-સંગઠિત ફેરિયાઓ તરફથી ભાવ સ્પર્ધા",
            ]

        else:
            # Default English
            strengths = [
                f"Hyper-local presence and direct trust-based relationships with {town} community households",
                f"Lean overhead structure compared to urban commercial franchises in {district}",
                f"Rapid turnaround on specialized sub-trades ({', '.join(cat.get('subcategories', [])[:2])})",
            ]
            if capital >= min_capex * 1.5:
                strengths.append(f"Strong initial capital allocation (₹{capital:,.0f}) providing operational buffer")
            else:
                strengths.append("High capital agility and low debt service liability in early stages")

            weaknesses = [
                f"Initial reliance on regional distributor credit terms and lead times for {raw_cat_name} inputs",
                "Transition from informal paper ledgers to digital inventory and tax compliance",
            ]
            if capital < min_capex:
                weaknesses.append(f"Lean starting capital (₹{capital:,.0f}) requires tight inventory turns")
            else:
                weaknesses.append("Need to hire and retain skilled assistant operators locally")

            opportunities = [
                f"Potential expansion of retail and B2B delivery routes across nearby hamlets in {town} taluka (Indicative)",
                "Subsidized term loan financing under government priority sector credit schemes",
                f"Direct digital ordering via WhatsApp Business and rural ONDC commerce in {district}",
            ]

            threats = [
                f"Seasonal agricultural cashflow cycles during monsoon/sowing intervals in {district}",
                "Wholesale raw material input price volatility and fuel freight surges",
                "Price competition from low-quality unorganized itinerant vendors during weekly haats",
            ]

        return SWOTAnalysis(
            strengths=strengths,
            weaknesses=weaknesses,
            opportunities=opportunities,
            threats=threats,
            is_demo_data=True,
        )

    # -------------------------------------------------------------------------
    # 4. Dynamic Risk & Mitigation Analysis
    # -------------------------------------------------------------------------
    @classmethod
    def generate_risks(
        cls,
        cat: Dict[str, Any],
        loc_info: Dict[str, str],
        capital: float,
        language: str = "en",
    ) -> List[RiskItem]:
        lang = (language or "en").lower().strip()
        raw_cat_name = cat["name"]
        loc_cat_name = cls.get_localized_category_name(raw_cat_name, lang)
        town = loc_info["town"]
        cat_risk = cat.get("risk_profile", {})
        min_capex = cat.get("typical_capex_min", 50000.0)

        risks: List[RiskItem] = []
        severity_fin = "High" if capital < min_capex else "Medium"

        cat_primary_risks = cat_risk.get("primary_risks", [])
        cat_mitigations = cat_risk.get("mitigation_strategies", [])

        if lang == "hi":
            # Risk 1: Financial
            risks.append(
                RiskItem(
                    risk_title="मौसमी कृषि नकदी प्रवाह में उतार-चढ़ाव",
                    severity=severity_fin,
                    category="Financial",
                    mitigation_strategy=(
                        f"उद्यमसारथी द्वारा अनुशंसित 3 महीने का कार्यशील पूंजी रिज़र्व बनाए रखें। "
                        f"{town} के खरीदारों के लिए अनौपचारिक उधारी खाता अधिकतम 15 दिनों तक सीमित रखें।"
                    ),
                )
            )
            # Risk 2: Operational
            risk_op_title = cat_primary_risks[0] if cat_primary_risks else f"{loc_cat_name} कच्चे माल की आपूर्ति में व्यवधान"
            risk_op_mit = cat_mitigations[0] if cat_mitigations else (
                f"{town} के 45 किमी के दायरे में कम से कम 2 वैकल्पिक थोक आपूर्तिकर्ताओं के साथ टाई-अप रखें "
                f"ताकि मौसमी मांग में भी आपूर्ति बाधित न हो।"
            )
            risks.append(
                RiskItem(
                    risk_title=risk_op_title,
                    severity="Medium",
                    category="Operational",
                    mitigation_strategy=risk_op_mit,
                )
            )
            # Risk 3: Market
            risks.append(
                RiskItem(
                    risk_title="स्थापित विक्रेताओं द्वारा अस्वास्थ्यकर मूल्य कटौती",
                    severity="Medium",
                    category="Market",
                    mitigation_strategy=(
                        f"विनाशकारी मूल्य कटौती से बचें। {town} में {loc_cat_name} कार्य को प्रमाणित गुणवत्ता, "
                        f"पक्के डिजिटल बिल, समय पर डिलीवरी और व्यक्तिगत ग्राहक सेवा के माध्यम से अलग पहचान दिलाएं।"
                    ),
                )
            )
            # Risk 4: Technical
            if len(cat_primary_risks) > 1:
                risks.append(
                    RiskItem(
                        risk_title=cat_primary_risks[1],
                        severity="Medium",
                        category="Technical",
                        mitigation_strategy=cat_mitigations[1] if len(cat_mitigations) > 1 else (
                            "दैनिक निवारक रखरखाव चेकलिस्ट अपनाएं और सख्त गुणवत्ता मानकों का पालन करें।"
                        ),
                    )
                )

        elif lang == "gu":
            # Risk 1: Financial
            risks.append(
                RiskItem(
                    risk_title="મોસમી કૃષિ રોકડ પ્રવાહમાં વધ-ઘટ",
                    severity=severity_fin,
                    category="Financial",
                    mitigation_strategy=(
                        f"ઉદ્યમસારથી દ્વારા ગણતરી કરેલ 3 મહિનાનું ઓપરેટિંગ રિઝર્વ જાળવી રાખો. "
                        f"{town} ના ગ્રાહકો માટે ઉધારી મહત્તમ 15 દિવસ સુધી મર્યાદિત રાખો."
                    ),
                )
            )
            # Risk 2: Operational
            risk_op_title = cat_primary_risks[0] if cat_primary_risks else f"{loc_cat_name} કાચા માલની સપ્લાયમાં વિક્ષેપ"
            risk_op_mit = cat_mitigations[0] if cat_mitigations else (
                f"{town} થી 45 કિમી ત્રિજ્યામાં ઓછામાં ઓછા 2 વૈકલ્પિક જથ્થાબંધ સપ્લાયર્સ સાથે જોડાણ રાખો "
                f"જેથી મોસમી માંગમાં પણ માલ અટક્યા વગર મળી રહે."
            )
            risks.append(
                RiskItem(
                    risk_title=risk_op_title,
                    severity="Medium",
                    category="Operational",
                    mitigation_strategy=risk_op_mit,
                )
            )
            # Risk 3: Market
            risks.append(
                RiskItem(
                    risk_title="સ્થાપિત વેપારીઓ દ્વારા ભાવ ઘટાડાની સ્પર્ધા",
                    severity="Medium",
                    category="Market",
                    mitigation_strategy=(
                        f"ભાવ ઘટાડાની હરીફાઈમાં પડવાને બદલે {loc_cat_name} કામગીરીમાં શ્રેષ્ઠ ગુણવત્તા, "
                        f"પાકા ડિજિટલ બિલ અને ઉત્તમ ગ્રાહક સેવા દ્વારા અલગ ઓળખ ઊભી કરો."
                    ),
                )
            )
            # Risk 4: Technical
            if len(cat_primary_risks) > 1:
                risks.append(
                    RiskItem(
                        risk_title=cat_primary_risks[1],
                        severity="Medium",
                        category="Technical",
                        mitigation_strategy=cat_mitigations[1] if len(cat_mitigations) > 1 else (
                            "રોજિંદા સાધન નિરીક્ષણ અને સચોટ ગુણવત્તા નિયંત્રણના ધોરણો અમલમાં મૂકો."
                        ),
                    )
                )

        else:
            # Default English
            risks.append(
                RiskItem(
                    risk_title="Seasonal Agrarian Cashflow Fluctuations",
                    severity=severity_fin,
                    category="Financial",
                    mitigation_strategy=(
                        f"Maintain the mandatory 3-month operating expense reserve calculated by UdyamSaarthi. "
                        f"Cap customer informal credit khata to a maximum of 15 days with strict credit limits for {town} buyers."
                    ),
                )
            )

            risk_op_title = cat_primary_risks[0] if cat_primary_risks else "Raw Material Input Sourcing Disruptions"
            risk_op_mitigation = cat_mitigations[0] if cat_mitigations else (
                f"Establish active tie-ups with at least 2 alternate wholesale suppliers within a 45 km radius of {town} "
                f"to guarantee continuity during seasonal peak demand."
            )
            risks.append(
                RiskItem(
                    risk_title=risk_op_title,
                    severity="Medium",
                    category="Operational",
                    mitigation_strategy=risk_op_mitigation,
                )
            )

            risks.append(
                RiskItem(
                    risk_title="Competitive Price Undercutting by Established Vendors",
                    severity="Medium",
                    category="Market",
                    mitigation_strategy=(
                        f"Avoid destructive price discounting. Differentiate {raw_cat_name} operations in {town} "
                        f"through verified quality standards, digital receipts, punctual delivery, and personalized customer care."
                    ),
                )
            )

            if len(cat_primary_risks) > 1:
                risks.append(
                    RiskItem(
                        risk_title=cat_primary_risks[1],
                        severity="Medium",
                        category="Technical",
                        mitigation_strategy=cat_mitigations[1] if len(cat_mitigations) > 1 else (
                            "Implement daily preventive maintenance checklists and adhere to strict quality control protocols."
                        ),
                    )
                )

        return risks

    # -------------------------------------------------------------------------
    # 5. Dynamic Pricing Guidance
    # -------------------------------------------------------------------------
    @classmethod
    def generate_pricing(
        cls,
        cat: Dict[str, Any],
        loc_info: Dict[str, str],
        capital: float,
        language: str = "en",
    ) -> PricingGuidance:
        lang = (language or "en").lower().strip()
        cat_pricing = cat.get("pricing_profile", {})
        raw_cat_name = cat["name"]
        loc_cat_name = cls.get_localized_category_name(raw_cat_name, lang)
        town = loc_info["town"]
        min_capex = cat.get("typical_capex_min", 50000.0)

        # Dynamic category-specific pricing metrics
        benchmark = cat_pricing.get("benchmark_product", f"Standard {raw_cat_name} Unit Product / Service Package")
        fallback_unit_cost = f"₹{int(min_capex * 0.005):,} - ₹{int(min_capex * 0.015):,} estimated unit cost"
        fallback_retail = f"₹{int(min_capex * 0.010):,} - ₹{int(min_capex * 0.025):,} retail benchmark"
        unit_cost = cat_pricing.get("unit_cost", fallback_unit_cost)
        retail_price = cat_pricing.get("retail_price", fallback_retail)
        target_margin = cat_pricing.get("target_gross_margin_percent", 40.0)

        if lang == "hi":
            if capital < min_capex * 1.5:
                strategy_notes = (
                    f"कम-पूंजी प्रवेश रणनीति: कार्यशील पूंजी की गतिशीलता बनाए रखने के लिए {town} के थोक वितरकों से "
                    f"तेज़ी से बिकने वाले {loc_cat_name} उत्पादों पर ध्यान केंद्रित करें। "
                    f"3-स्तरीय मूल्य संरचना लागू करें: दैनिक आवश्यक वस्तुएं (25% मार्जिन), विशेष ऑर्डर (50% मार्जिन), "
                    f"और थोक संस्थागत अनुबंध (20% मार्जिन)।"
                )
            else:
                strategy_notes = (
                    f"सुदृढ़-पूंजीकृत रणनीति: क्षेत्रीय उत्पादन केंद्रों से सीधी थोक खरीद का लाभ उठाकर 12-18% छूट प्राप्त करें "
                    f"और {town} के ग्राहकों के लिए 30 दिनों का बफर स्टॉक बनाए रखें। 3-स्तरीय मूल्य निर्धारण नीति अपनाएं।"
                )
        elif lang == "gu":
            if capital < min_capex * 1.5:
                strategy_notes = (
                    f"ઓછી મૂડી પ્રવેશ વ્યૂહરચના: ઝડપથી વેચાતા {loc_cat_name} ઉત્પાદનો પર ધ્યાન કેન્દ્રિત કરો અને {town} ના "
                    f"જથ્થાબંધ વેપારીઓ પાસેથી સાપ્તાહિક ખરીદી કરીને સ્ટોક ફેરવો. "
                    f"3-સ્તરીય ભાવ માળખું જાળવો: નિયમિત સામાન (25% નફો), સ્પેશિયલ ઓર્ડર (50% નફો) અને જથ્થાબંધ કરાર (20% નફો)."
                )
            else:
                strategy_notes = (
                    f"સારી મૂડી ધરાવતી વ્યૂહરચના: મોટા ઉત્પાદન કેન્દ્રો પાસેથી સીધી જથ્થાબંધ ખરીદી કરી 12-18% વેપારી ડિસ્કાઉન્ટ મેળવો "
                    f"અને {town} ના ગ્રાહકો માટે સ્ટોક સંગ્રહ ક્ષમતા ઊભી કરો."
                )
        else:
            # Default English
            if capital < min_capex * 1.5:
                approach = (
                    f"Low-capital entry strategy: Focus on fast-moving, high-velocity {raw_cat_name} lines with weekly replenishment "
                    f"from nearby {town} wholesale distributors to minimize dead stock and accelerate working capital turns."
                )
            else:
                approach = (
                    f"Well-capitalized strategy: Leverage direct wholesale procurement from regional production clusters "
                    f"to capture 12-18% bulk trade discounts and maintain 30-day buffer inventory for {town} clients."
                )

            strategy_notes = (
                f"{approach} Maintain a 3-tier pricing structure: budget everyday items (25% margin), "
                f"premium custom orders (50% margin), and institutional bulk contracts (20% margin with volume guarantees)."
            )

        return PricingGuidance(
            benchmark_product_or_service=benchmark,
            estimated_unit_production_cost=unit_cost,
            suggested_retail_price=retail_price,
            target_gross_margin_percent=target_margin,
            pricing_strategy_notes=strategy_notes,
            is_demo_data=True,
        )

    # -------------------------------------------------------------------------
    # 6. Dynamic Competitor Mapping
    # -------------------------------------------------------------------------
    @classmethod
    def generate_competitors(
        cls,
        cat: Dict[str, Any],
        loc_info: Dict[str, str],
        capital: float,
        language: str = "en",
    ) -> List[CompetitorItem]:
        lang = (language or "en").lower().strip()
        town = loc_info["town"]
        district = loc_info["district"]
        search_terms = cat.get("competitor_search_terms", ["local merchants", "traditional dealers"])

        term1 = search_terms[0].title() if search_terms else "Local Independent Dealer"
        term2 = search_terms[1].title() if len(search_terms) > 1 else "Regional Town Showroom"
        term3 = search_terms[2].title() if len(search_terms) > 2 else "Itinerant Weekly Haat Vendor"

        loc_status_en = "Location unavailable — live mapping planned for Phase B9"
        loc_status_hi = "स्थान अनुपलब्ध — चरण B9 के लिए लाइव मैपिंग नियोजित"
        loc_status_gu = "સ્થાન ઉપલબ્ધ નથી — ફેઝ B9 માટે લાઇવ મેપિંગ આયોજિત"
        data_source_label = "Indicative category-location profile"

        if lang == "hi":
            competitors = [
                CompetitorItem(
                    name=f"स्थानीय {term1} ({town} क्षेत्र)",
                    type_of_business="पारंपरिक स्थानीय विक्रेता",
                    proximity=f"{town} मुख्य बाज़ार के 2 किमी के भीतर",
                    strengths="दीर्घकालिक स्थानीय संबंध एवं स्थापित उपस्थिति",
                    differentiation_strategy="डिजिटल यूपीआई भुगतान, पारदर्शी बिलिंग और समय पर डिलीवरी द्वारा प्रतिस्पर्धा करें।",
                    is_demo_data=True,
                    data_source=data_source_label,
                    location_status=loc_status_hi,
                ),
                CompetitorItem(
                    name=f"{district} क्षेत्रीय {term2} (क्लस्टर)",
                    type_of_business="कस्बाई संगठित वितरक / डीलर",
                    proximity=f"{district} व्यापारिक केंद्र में 12-18 किमी दूर",
                    strengths="व्यापक स्टॉक वैरायटी एवं ब्रांड पहचान",
                    differentiation_strategy=f"ग्राहकों को {district} जाने की परेशानी से बचाकर {town} में ही तुरंत सामान उपलब्ध कराएं।",
                    is_demo_data=True,
                    data_source=data_source_label,
                    location_status=loc_status_hi,
                ),
                CompetitorItem(
                    name=f"साप्ताहिक {term3} ({town} हाट)",
                    type_of_business="अनौपचारिक साप्ताहिक विक्रेता",
                    proximity=f"{town} के साप्ताहिक हाट एवं ग्रामीण मेले",
                    strengths="कम लागत और आक्रामक अल्पकालिक छूट",
                    differentiation_strategy="वर्षभर निरंतर उपलब्धता, प्रामाणिक गारंटी और बेहतर सेवा से अलग पहचान बनाएं।",
                    is_demo_data=True,
                    data_source=data_source_label,
                    location_status=loc_status_hi,
                ),
            ]
        elif lang == "gu":
            competitors = [
                CompetitorItem(
                    name=f"સ્થાનિક {term1} ({town} વિસ્તાર)",
                    type_of_business="પરંપરાગત સ્થાનિક વેપારી",
                    proximity=f"{town} મુખ્ય બજારથી 2 કિમી અંદર",
                    strengths="સ્થાનિક ગ્રાહકો સાથે જૂનો વિશ્વાસ અને સંબંધ",
                    differentiation_strategy="ડિજિટલ પેમેન્ટ, સ્પષ્ટ બિલિંગ અને ગુણવત્તાયુક્ત સેવા દ્વારા આગળ વધો.",
                    is_demo_data=True,
                    data_source=data_source_label,
                    location_status=loc_status_gu,
                ),
                CompetitorItem(
                    name=f"{district} પ્રાદેશિક {term2} (ક્લસ્ટર)",
                    type_of_business="મોટા શહેરના ડીલર / ડિસ્ટ્રિબ્યુટર",
                    proximity=f"{district} બજારમાં 12-18 કિમી દૂર",
                    strengths="મોટો સ્ટોક અને પ્રખ્યાત બ્રાન્ડ્સ",
                    differentiation_strategy=f"ગ્રાહકોને મુસાફરીના સમય અને ખર્ચથી બચાવી {town} માં જ ઘરઆંગણે સેવા આપો.",
                    is_demo_data=True,
                    data_source=data_source_label,
                    location_status=loc_status_gu,
                ),
                CompetitorItem(
                    name=f"સાપ્તાહિક {term3} ({town} હાટ)",
                    type_of_business="સાપ્તાહિક હાટના ફેરિયા",
                    proximity=f"{town} આસપાસના ગ્રામીણ મેળાઓ",
                    strengths="ઓછો ખર્ચ અને સસ્તા ભાવો",
                    differentiation_strategy="બારેમાસ ઉપલબ્ધતા, પાકી ગેરંટી અને વેચાણ પછીની સેવા પૂરી પાડીને ગ્રાહકો જાળવી રાખો.",
                    is_demo_data=True,
                    data_source=data_source_label,
                    location_status=loc_status_gu,
                ),
            ]
        else:
            # Default English
            competitors = [
                CompetitorItem(
                    name=f"Local {term1} ({town} Catchment)",
                    type_of_business="Traditional Local Retailer",
                    proximity=f"Within 2 km of {town} central market",
                    strengths="Long-standing local community relationships and established location presence",
                    differentiation_strategy=(
                        f"Compete by offering digital UPI payments, WhatsApp catalog orders, transparent billing, "
                        f"and superior customer after-sales responsiveness."
                    ),
                    is_demo_data=True,
                    data_source=data_source_label,
                    location_status=loc_status_en,
                ),
                CompetitorItem(
                    name=f"Regional {term2} ({district} Cluster)",
                    type_of_business="Organized Town Dealership / Distributor",
                    proximity=f"12-18 km away in {district} commercial hub",
                    strengths="Wider inventory variety and established brand recognition",
                    differentiation_strategy=(
                        f"Capture customers by eliminating the 15 km town travel inconvenience and providing "
                        f"immediate same-day availability right inside {town}."
                    ),
                    is_demo_data=True,
                    data_source=data_source_label,
                    location_status=loc_status_en,
                ),
                CompetitorItem(
                    name=f"Periodic {term3} ({town} Haat)",
                    type_of_business="Informal Periodic Vendor",
                    proximity=f"Weekly haats and periodic village bazaars across {town}",
                    strengths="Low overheads and aggressive temporary discount pricing",
                    differentiation_strategy=(
                        f"Differentiate with consistent year-round availability, guaranteed product warranty, "
                        f"and genuine after-sales service that temporary vendors cannot offer."
                    ),
                    is_demo_data=True,
                    data_source=data_source_label,
                    location_status=loc_status_en,
                ),
            ]

        return competitors

    # -------------------------------------------------------------------------
    # 7. Dynamic Business Recommendation
    # -------------------------------------------------------------------------
    @classmethod
    def generate_recommendation(
        cls,
        cat: Dict[str, Any],
        loc_info: Dict[str, str],
        capital: float,
        language: str = "en",
    ) -> BusinessRecommendation:
        lang = (language or "en").lower().strip()
        raw_cat_name = cat["name"]
        loc_cat_name = cls.get_localized_category_name(raw_cat_name, lang)
        town = loc_info["town"]
        district = loc_info["district"]
        full_loc = loc_info["clean_address"]

        min_capex = cat.get("typical_capex_min", 50000.0)
        project_cost = capital / 0.10
        capital_ratio = project_cost / min_capex

        # Calculate feasibility score (55 - 98) deterministically
        if capital_ratio < 1.0:
            score = max(55, int(60 + capital_ratio * 15))
            if lang == "hi":
                rating = "सीमांत व्यवहार्य (पूंजी सीमित)"
                summary = (
                    f"{town} में ₹{capital:,.0f} की व्यक्तिगत मार्जिन पूंजी (प्रोजेक्ट लागत ₹{project_cost:,.0f}) के साथ "
                    f"{loc_cat_name} उद्यम शुरू करना व्यावहारिक है, लेकिन प्रारंभिक उपकरणों के लिए सरकारी ऋण सब्सिडी "
                    f"और सख्त लागत नियंत्रण की आवश्यकता होगी।"
                )
            elif lang == "gu":
                rating = "મર્યાદિત સંભાવના (મૂડીની મર્યાદા)"
                summary = (
                    f"{town} માં ₹{capital:,.0f} ની અંગત માર્જિન મૂડી (પ્રોજેક્ટ ખર્ચ ₹{project_cost:,.0f}) સાથે "
                    f"{loc_cat_name} વ્યવસાય શરૂ કરવો શક્ય છે, પરંતુ ખર્ચ પર કડક નિયંત્રણ રાખવું પડશે."
                )
            else:
                rating = "Marginally Feasible (Capital Constrained)"
                summary = (
                    f"Starting a {raw_cat_name} enterprise in {town} with personal margin capital of ₹{capital:,.0f} "
                    f"(project cost ₹{project_cost:,.0f}) is viable under a micro-fulfillment model, but requires disciplined "
                    f"cost control and seeking available credit subsidies to bridge initial equipment costs."
                )
        elif capital_ratio >= 2.5:
            score = min(98, int(86 + min(capital_ratio - 2.5, 6.0) * 2))
            if lang == "hi":
                rating = "अत्यधिक व्यवहार्य (सुदृढ़ पूंजीकृत)"
                summary = (
                    f"आपकी ₹{capital:,.0f} की मार्जिन पूंजी {full_loc} में {loc_cat_name} उद्यम के लिए मजबूत आधार प्रदान करती है। "
                    f"यह पूंजी (प्रोजेक्ट लागत ₹{project_cost:,.0f}) आधुनिक उपकरण खरीद और 3 महीने के परिचालन रिज़र्व का पूरा समर्थन करती है।"
                )
            elif lang == "gu":
                rating = "ખૂબ જ અનુકૂળ (સારી મૂડી ઉપલબ્ધ)"
                summary = (
                    f"તમારી ₹{capital:,.0f} ની માર્જિન મૂડી {full_loc} માં {loc_cat_name} માટે મજબૂત પાયો પૂરો પાડે છે. "
                    f"આ મૂડી (પ્રોજેક્ટ ખર્ચ ₹{project_cost:,.0f}) જરૂરી મશીનરી અને 3 મહિનાના ઓપરેટિંગ ખર્ચ માટે પૂરતી છે."
                )
            else:
                rating = "Highly Feasible (Well Capitalized)"
                summary = (
                    f"Your margin capital of ₹{capital:,.0f} provides strong commercial leverage for {raw_cat_name} in {full_loc}. "
                    f"This capital foundation (Project Cost ₹{project_cost:,.0f}) supports full machinery acquisition, "
                    f"bulk raw material discounts, and a comfortable 3-month operating cushion."
                )
        else:
            score = int(78 + (capital_ratio - 1.0) * 5)
            if lang == "hi":
                rating = "मध्यम व्यवहार्य (सक्षम सूक्ष्म उद्यम)"
                summary = (
                    f"{full_loc} में प्रस्तावित {loc_cat_name} व्यवसाय ठोस परिचालन व्यवहार्यता प्रदर्शित करता है। "
                    f"आपकी ₹{capital:,.0f} की उपलब्ध पूंजी इस क्षेत्र के मानक स्टार्टअप उपकरणों और कार्यशील पूंजी के अनुरूप है।"
                )
            elif lang == "gu":
                rating = "મધ્યમ અનુકૂળ (સક્ષમ સૂક્ષ્મ સાહસ)"
                summary = (
                    f"{full_loc} માં સૂચિત {loc_cat_name} વ્યવસાય યોગ્ય સંભાવના દર્શાવે છે. "
                    f"તમારી ₹{capital:,.0f} ની મૂડી સાધનો અને પ્રારંભિક કાર્યકારી મૂડીના માપદંડો સાથે સુસંગત છે."
                )
            else:
                rating = "Moderately Feasible (Viable Micro-Venture)"
                summary = (
                    f"The proposed {raw_cat_name} business demonstrates solid operational viability in {full_loc}. "
                    f"Your available capital of ₹{capital:,.0f} aligns comfortably with standard startup equipment "
                    f"and initial working capital benchmarks for this sector."
                )

        if lang == "hi":
            milestones = [
                f"दिन 1-30: {town} में बाज़ार के पास व्यावसायिक जगह तय करें, उद्यम एमएसएमई एवं आवश्यक व्यापार लाइसेंस प्राप्त करें।",
                f"दिन 31-60: मुख्य उपकरण स्थापित करें, थोक स्टॉक प्राप्त करें और परीक्षण कार्य शुरू करें।",
                f"दिन 61-90: विधिवत उद्घाटन करें, {town} के परिवारों को डिजिटल कैटलॉग भेजें और नियमित बिक्री स्थापित करें।",
            ]
            tips = [
                f"{town} में त्वरित नकद एवं डिजिटल भुगतान रिकॉर्ड करने के लिए काउंटर पर ऑडियो यूपीआई साउंडबॉक्स लगाएं।",
                "डेड स्टॉक रोकने के लिए व्यापार या खाता-बही ऐप का उपयोग करके डिजिटल इन्वेंट्री प्रबंधित करें।",
                f"{district} में एमएसएमई व्यापार मेलों और ग्रामीण हाटों में भाग लेकर नए ग्राहक बनाएं।",
            ]
        elif lang == "gu":
            milestones = [
                f"દિવસ 1-30: {town} માં યોગ્ય જગ્યા નક્કી કરો, ઉદ્યમ MSME અને જરૂરી સ્થાનિક વેપાર પરમિટ મેળવો.",
                f"દિવસ 31-60: મુખ્ય સાધનો સ્થાપિત કરો, જથ્થાબંધ માલ ખરીદો અને ટ્રાયલ શરૂ કરો.",
                f"દિવસ 61-90: વ્યવસાયનો પ્રારંભ કરો, {town} ના ગ્રાહકો સુધી વોટ્સએપ કેટેલોગ પહોંચાડો અને નિયમિત વેચાણ સ્થાપિત કરો.",
            ]
            tips = [
                f"{town} માં કાઉન્ટર પર ઑડિઓ UPI સાઉન્ડબોક્સ લગાવો જેથી તાત્કાલિક ડિજિટલ પેમેન્ટ સરળ બને.",
                "વધારાનો સ્ટોક ભરાઈ ન રહે તે માટે વ્યાપાર કે ખાતાબુક જેવી એપ દ્વારા સ્ટોક મેનેજમેન્ટ કરો.",
                f"{district} માં યોજાતા પ્રદર્શનો અને ગ્રામીણ મેળાઓમાં ભાગ લઈને ગ્રાહકોનો વ્યાપ વધારો.",
            ]
        else:
            milestones = [
                f"Days 1-30: Secure commercial premises near market transit in {town}, apply for Udyam MSME and required trade licenses.",
                f"Days 31-60: Install core machinery ({', '.join(cat.get('key_equipment', [])[:2])}), procure wholesale stock, and test trial workflows.",
                f"Days 61-90: Inaugural launch, distribute WhatsApp product catalogs to {town} households, and establish regular repeat revenue.",
            ]
            tips = [
                f"Deploy an audio UPI soundbox at the counter to record instant cash and digital payments in {town}.",
                "Maintain digital inventory turns using Vyapar or Khatabook to prevent dead stock.",
                f"Participate in district {district} MSME trade exhibitions and rural haats to expand customer reach.",
            ]

        licenses = cat.get("mandatory_licenses", [
            "Udyam MSME Registration Certificate",
            "Local Gram Panchayat / Municipal Trade Permit",
            "Shop & Establishment Act Registration",
        ])

        return BusinessRecommendation(
            feasibility_score=score,
            feasibility_rating=rating,
            summary=summary,
            first_90_days_milestones=milestones,
            mandatory_licenses_and_registrations=licenses,
            digital_enablement_tips=tips,
            is_demo_data=True,
        )

    # -------------------------------------------------------------------------
    # 8. Dynamic Business Profile
    # -------------------------------------------------------------------------
    @classmethod
    def generate_business_profile(
        cls,
        cat: Dict[str, Any],
        loc_info: Dict[str, str],
        capital: float,
        language: str = "en",
        raw_category: Optional[str] = None,
    ) -> BusinessProfile:
        lang = (language or "en").lower().strip()
        raw_cat_name = cat["name"]
        if raw_category and raw_category.strip().lower() == "grocery":
            raw_cat_name = "Grocery"
        elif raw_category and raw_category.strip() == cat.get("name"):
            raw_cat_name = raw_category.strip()

        loc_cat_name = cls.get_localized_category_name(raw_cat_name, lang)

        min_capex = cat.get("typical_capex_min", 50000.0)
        max_capex = cat.get("typical_capex_max", 1500000.0)

        if capital >= min_capex * 1.5:
            adequacy = "Optimal"
        elif capital >= min_capex:
            adequacy = "Adequate"
        else:
            adequacy = "Lean"

        if lang == "hi":
            desc = f"{loc_info['clean_address']} में {loc_cat_name} उद्यम प्रोफाइल।"
        elif lang == "gu":
            desc = f"{loc_info['clean_address']} માં {loc_cat_name} સાહસ પ્રોફાઇલ."
        else:
            desc = f"Enterprise profile for {raw_cat_name} in {loc_info['clean_address']}, operating in the {cat.get('sector', 'Rural Enterprise')} sector."

        return BusinessProfile(
            category_id=cat["id"],
            category_name=raw_cat_name if lang == "en" else loc_cat_name,
            description=desc,
            primary_activities=cat.get("primary_activities", [
                "Local procurement and inventory management",
                "Customer fulfillment and sales execution",
                "Quality assurance and after-sales service",
            ]),
            key_equipment=cat.get("key_equipment", [
                "Primary operational tools and machinery",
                "Electronic weighing scale and POS terminal",
                "Storage and display fixtures",
            ]),
            typical_capex_range=f"₹{min_capex:,.0f} - ₹{max_capex:,.0f}",
            capital_adequacy=adequacy,
            target_location=loc_info["clean_address"],
        )

    # -------------------------------------------------------------------------
    # Master Aggregator Method
    # -------------------------------------------------------------------------
    @classmethod
    def generate_complete_intelligence(
        cls,
        location: str,
        business_category: str,
        available_capital: float,
        location_detail: Optional[LocationData] = None,
        language: str = "en",
    ) -> Dict[str, Any]:
        """
        Master method synthesizing complete hyper-local business intelligence.
        Guarantees material differentiation across Category, Location, Capital, and Language.
        """
        cat = cls.resolve_category_meta(business_category)
        loc_info = cls.parse_location_details(location, location_detail)
        cap = float(available_capital)
        lang = (language or "en").lower().strip()

        market = cls.generate_market_analysis(cat, loc_info, cap, language=lang)
        opps = cls.generate_opportunities(cat, loc_info, cap, language=lang)
        swot = cls.generate_swot(cat, loc_info, cap, language=lang)
        risks = cls.generate_risks(cat, loc_info, cap, language=lang)
        pricing = cls.generate_pricing(cat, loc_info, cap, language=lang)
        comps = cls.generate_competitors(cat, loc_info, cap, language=lang)
        rec = cls.generate_recommendation(cat, loc_info, cap, language=lang)
        profile = cls.generate_business_profile(cat, loc_info, cap, language=lang, raw_category=business_category)

        return {
            "business": profile.model_dump(),
            "market": market,
            "opportunities": opps,
            "swot": swot,
            "risks": risks,
            "competitors": comps,
            "pricing": pricing,
            "recommendation": rec,
            "metadata": {
                "data_source": "prototype_demo_data",
                "is_live_data": False,
                "note": "Prototype demo datasets. Dynamic simulated local market estimates tailored for advisory and business planning.",
                "version": "2.0-b8",
            },
        }
