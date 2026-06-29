from typing import Dict, List, Any
import time

# Pre-defined translation map for key terms to demonstrate local language mapping (hi, mr, ta)
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # Hindi
    "hi": {
        "Tomato": "टमाटर",
        "Wheat": "गेहूं",
        "Rice": "चावल",
        "Soil Nutrient & Fertilizer Plan": "मृदा पोषक तत्व और उर्वरक योजना",
        "Market Price Alert": "बाजार मूल्य चेतावनी",
        "Yield Projection": "फसल पैदावार अनुमान",
        "Crop Sowing Suitability": "फसल बुआई उपयुक्तता",
        "Disease Diagnosis": "रोग निदान",
        "Nearby Government Health Centers": "निकटतम सरकारी स्वास्थ्य केंद्र",
        "Immunization Tracker for Child": "बाल प्रतिरक्षण (टीकाकरण) ट्रैकर",
        "Upcoming Free Health Camps": "आगामी मुफ्त चिकित्सा शिविर",
        "Dietary & Nutritional Plan": "आहार और पोषण संबंधी योजना",
        "Health Care Guide": "स्वास्थ्य देखभाल गाइड",
        "Nearby Schools & Colleges": "निकटतम स्कूल और कॉलेज",
        "Eligibility Verification": "पात्रता सत्यापन रिपोर्ट",
        "Career Guidance Report": "करियर मार्गदर्शन रिपोर्ट",
        "Borewell Drilling Feasibility Analysis": "सटीक बोरवेल ड्रिलिंग व्यवहार्यता विश्लेषण",
        "Water Quality Test Results": "जल गुणवत्ता परीक्षण परिणाम",
        "Domestic Rainwater Harvesting Design": "घरेलू वर्षा जल संचयन डिजाइन ब्लूप्रिंट",
        "Agronomic Irrigation Scheduling": "कृषि सिंचाई समय-सारणी",
        "Regional Aquifer & Groundwater Assessment": "क्षेत्रीय भूजल स्तर एवं जलभृत मूल्यांकन",
        "PWD Road Quality Assessment": "सड़क गुणवत्ता मूल्यांकन",
        "State Electricity Board Grid status": "राज्य विद्युत बोर्ड ग्रिड स्थिति",
        "Telecom Tower Signal Assessment": "दूरसंचार नेटवर्क सिग्नल मूल्यांकन",
        "Government Development Projects": "सरकारी विकास परियोजनाएं",
        "Welfare Scheme Details": "सरकारी कल्याणकारी योजना विवरण",
        "Rural Credit Loan Qualification": "ग्रामीण ऋण पात्रता रिपोर्ट",
        "EMI Calculation": "ऋण मासिक किस्त (EMI) गणना विवरण",
        "Rural Subsidies": "ग्रामीण कृषि सब्सिडी विवरण",
        "Eligible Government Welfare Schemes": "पात्र सरकारी कल्याणकारी योजनाएं",
        "System Error": "सिस्टम त्रुटि"
    },
    # Marathi
    "mr": {
        "Tomato": "टोमॅटो",
        "Wheat": "गहू",
        "Rice": "तांदूळ",
        "Soil Nutrient & Fertilizer Plan": "मातीचे पोषक तत्व आणि खत योजना",
        "Market Price Alert": "बाजारभाव चेतावणी",
        "Yield Projection": "पीक उत्पादनाचा अंदाज",
        "Crop Sowing Suitability": "पीक पेरणी योग्यता",
        "Disease Diagnosis": "रोग निदान",
        "Nearby Government Health Centers": "जवळचे सरकारी आरोग्य केंद्र",
        "Immunization Tracker for Child": "बालकांचे लसीकरण ट्रॅकर",
        "Upcoming Free Health Camps": "आगामी मोफत आरोग्य शिबिर",
        "Dietary & Nutritional Plan": "आहार आणि पोषण नियोजन",
        "Health Care Guide": "आरोग्य सेवा मार्गदर्शक",
        "Nearby Schools & Colleges": "जवळच्या शाळा आणि महाविद्यालये",
        "Eligibility Verification": "पात्रता पडताळणी अहवाल",
        "Career Guidance Report": "करिअर मार्गदर्शन अहवाल",
        "Borewell Drilling Feasibility Analysis": "बोअरवेल खोदकाम व्यवहार्यता विश्लेषण",
        "Water Quality Test Results": "पाण्याची गुणवत्ता चाचणी अहवाल",
        "Domestic Rainwater Harvesting Design": "घरगुती पावसाचे पाणी साठवणूक डिझाईन",
        "Agronomic Irrigation Scheduling": "कृषी सिंचन वेळापत्रक",
        "Regional Aquifer & Groundwater Assessment": "प्रादेशिक भूजल पातळी आणि साठा मूल्यांकन",
        "PWD Road Quality Assessment": "रस्त्यांच्या गुणवत्तेचे मूल्यांकन",
        "State Electricity Board Grid status": "राज्य विद्युत मंडळ ग्रिड स्थिती",
        "Telecom Tower Signal Assessment": "दूरसंचार नेटवर्क सिग्नल मूल्यांकन",
        "Government Development Projects": "सरकारी विकास प्रकल्प",
        "Welfare Scheme Details": "सरकारी कल्याणकारी योजना तपशील",
        "Rural Credit Loan Qualification": "ग्रामीण कर्ज पात्रता अहवाल",
        "EMI Calculation": "कर्जाचे हप्ते (EMI) मोजणी तपशील",
        "Rural Subsidies": "ग्रामीण कृषी अनुदान तपशील",
        "Eligible Government Welfare Schemes": "पात्र सरकारी कल्याणकारी योजना",
        "System Error": "सिस्टम एरर"
    },
    # Tamil
    "ta": {
        "Tomato": "தக்காளி",
        "Wheat": "கோதுமை",
        "Rice": "அரிசி",
        "Soil Nutrient & Fertilizer Plan": "மண் ஊட்டச்சத்து மற்றும் உரத் திட்டம்",
        "Market Price Alert": "சந்தை விலை விழிப்புணர்வு",
        "Yield Projection": "மகசூல் கணிப்பு அறிக்கை",
        "Crop Sowing Suitability": "பயிர் விதைப்பு உகந்த நிலை",
        "Disease Diagnosis": "பயிர் நோய் கண்டறிதல்",
        "Nearby Government Health Centers": "அருகிலுள்ள அரசு சுகாதார நிலையங்கள்",
        "Immunization Tracker for Child": "குழந்தை தடுப்பூசி அட்டவணை",
        "Upcoming Free Health Camps": "இலவச மருத்துவ முகாம்கள்",
        "Dietary & Nutritional Plan": "உணவு & ஊட்டச்சத்து வழிகாட்டி",
        "Health Care Guide": "சுகாதார வழிகாட்டி",
        "Nearby Schools & Colleges": "அருகிலுள்ள பள்ளிகள் & கல்லூரிகள்",
        "Eligibility Verification": "தகுதி சரிபார்ப்பு அறிக்கை",
        "Career Guidance Report": "தொழில் வழிகாட்டுதல் அறிக்கை",
        "Borewell Drilling Feasibility Analysis": "ஆழ்துளை கிணறு அமைப்பதற்கான சாத்தியக்கூறு",
        "Water Quality Test Results": "நீர் தர சோதனை முடிவுகள்",
        "Domestic Rainwater Harvesting Design": "வீட்டு மழைநீர் சேகரிப்பு கட்டமைப்பு",
        "Agronomic Irrigation Scheduling": "பயிர் நீர்ப்பாசன கால அட்டவணை",
        "Regional Aquifer & Groundwater Assessment": "நிலத்தடி நீர் மட்ட மதிப்பீடு",
        "PWD Road Quality Assessment": "சாலை தரம் மதிப்பீடு",
        "State Electricity Board Grid status": "மின்சார வாரிய கிரிட் நிலைமை",
        "Telecom Tower Signal Assessment": "மொபைல் நெட்வொர்க் சிக்னல் தரம்",
        "Government Development Projects": "அரசு வளர்ச்சி திட்டங்கள்",
        "Welfare Scheme Details": "அரசு நலத்திட்ட விவரங்கள்",
        "Rural Credit Loan Qualification": "கிராமப்புற கடன் தகுதி அறிக்கை",
        "EMI Calculation": "மாதாந்திர தவணை (EMI) கணக்கீடு",
        "Rural Subsidies": "விவசாய மானியங்கள் விவரங்கள்",
        "Eligible Government Welfare Schemes": "தகுதியான அரசு நலத்திட்டங்கள்",
        "System Error": "கணினி பிழை"
    }
}

def translate_text(text: str, target_language: str) -> str:
    """Translate predefined English keywords/titles to target Indian language."""
    lang = target_language.lower().strip()
    if lang not in TRANSLATIONS:
        return text
        
    lang_dict = TRANSLATIONS[lang]
    
    # Try finding an exact match
    if text in lang_dict:
        return lang_dict[text]
        
    # Attempt partial replacements for key headers
    translated = text
    for eng_term, local_term in lang_dict.items():
        if eng_term in translated:
            translated = translated.replace(eng_term, local_term)
            
    # If no changes were made and target language is not English, leave a translation placeholder
    if translated == text and lang != "en":
        # Simulate neural translation stub fallback
        return f"[{lang.upper()}] {text}"
        
    return translated

def format_agent_response(agent_response: Dict[str, Any], language: str) -> Dict[str, Any]:
    """Uniformly format recommendations list, applying localization translations where requested."""
    recs = agent_response.get("recommendations", [])
    formatted_recs = []
    
    for r in recs:
        # Translate title
        raw_title = r.get("title", "")
        translated_title = translate_text(raw_title, language)
        
        # Translate description
        raw_desc = r.get("description", "")
        translated_desc = translate_text(raw_desc, language)
        
        formatted_recs.append({
            "title": translated_title,
            "description": translated_desc,
            "source": r.get("source", "Agent"),
            "confidence": r.get("confidence", 1.0)
        })
        
    return {
        "agent": agent_response.get("agent", "unknown"),
        "recommendations": formatted_recs,
        "sources": agent_response.get("sources", [])
    }

def create_success_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """Wrap output data in a standardized success payload layout."""
    return {
        "status": "success",
        "data": data,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

def create_error_response(error: str, status_code: int) -> Dict[str, Any]:
    """Wrap error messaging in standard failure response layout."""
    return {
        "status": "error",
        "code": status_code,
        "message": error,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
