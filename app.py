import streamlit as st
import pandas as pd
import hashlib
import html

from utils.image_validator import validate_image
from services.image_processor import process_image
from services.image_statistics import calculate_image_statistics
from services.ai_image_detector import detect_ai_image
from services.risk_analyzer import assess_image_risk


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="TrustChecker | Image Security",
    page_icon="🛡️",
    layout="wide"
)

# Add your deployed main website URL here when it is ready.
# Example: MAIN_WEBSITE_URL = "https://your-trustchecker-site.com"
MAIN_WEBSITE_URL = ""


# =========================================================
# LANGUAGE TEXT
# =========================================================

TEXT = {
    "English": {
        "title": "TrustChecker",
        "subtitle": "AI-Powered Image Security & Scam Screening",
        "tagline": "Analyze images. Detect suspicious signals. Make safer decisions.",
        "upload": "Upload an image to begin analysis",
        "upload_help": "Supported formats: JPG, JPEG, PNG and WEBP. Maximum file size: 5 MB.",
        "preview": "Uploaded Image",
        "statistics": "Image Information",
        "technical_details": "Image Technical Details",
        "analyze": "Analyze Image",
        "processing": "Analyzing your image. Please wait...",
        "results": "Analysis Overview",
        "origin": "AI Origin Analysis",
        "scam": "Scam Risk Screening",
        "confidence": "Confidence Level",
        "summary": "Analysis Summary",
        "evidence": "Supporting Visual Evidence",
        "counter": "Additional Observations",
        "limitations": "Analysis Limitations",
        "recommendation": "Recommended Next Steps",
        "scam_evidence": "Potential Scam Indicators",
        "suspicious": "Suspicious Elements",
        "extracted": "Extracted Image Text",
        "verification": "Suggested Verification Steps",
        "dimensions": "Dimensions",
        "resolution": "Resolution",
        "size": "File Size",
        "format": "Format",
        "ratio": "Aspect Ratio",
        "brightness": "Brightness",
        "contrast": "Contrast",
        "saturation": "Saturation",
        "chart": "Image Technical Properties",
        "scam_chart": "Scam Screening Overview",
        "no_evidence": "No specific evidence was reported.",
        "no_items": "No additional information was reported.",
        "no_results": "Upload an image and select Analyze Image to view the results.",
        "disclaimer": "Important: This is an AI-assisted screening tool, not forensic verification. No obvious scam indicators does not mean an image or offer is verified as safe.",
        "footer": "TrustChecker | Intelligent Image Security",
        "invalid": "Image validation or analysis failed:",
        "high": "High",
        "medium": "Medium",
        "low": "Low",
        "not_available": "Not available",
        "safety": "Safety Recommendation",
        "visual_note": "Image statistics describe visual properties. They do not prove whether an image is AI-generated or fraudulent.",
        "how_it_works": "How It Works",
        "how_description": "Upload an image, let TrustChecker analyze its visual content, and review the AI-origin assessment and potential scam indicators.",
        "about": "About TrustChecker",
        "about_description": "TrustChecker is an AI-assisted digital safety project designed to help users identify potentially suspicious content.",
        "main_website": "Main Website",
        "coming_soon": "Main Website · Coming soon",
        "screening_result": "Current screening result",
        "chart_note": "This chart highlights the model's screening category. It does not represent a percentage or probability of fraud.",
        "steps_upload": "Choose an image from your device.",
        "steps_analyze": "Let the AI-assisted system examine the image.",
        "steps_review": "Understand the findings and suggested safety steps.",
        "language_changed": "Language changed. Select Analyze Image again to generate results in the selected language."
    },

    "Hindi": {
        "title": "TrustChecker",
        "subtitle": "AI इमेज और धोखाधड़ी की जाँच",
        "tagline": "तस्वीरों का विश्लेषण करें। संदिग्ध संकेत पहचानें। सुरक्षित निर्णय लें।",
        "upload": "विश्लेषण के लिए तस्वीर अपलोड करें",
        "upload_help": "JPG, JPEG, PNG और WEBP। अधिकतम 5 MB।",
        "preview": "अपलोड की गई तस्वीर",
        "statistics": "तस्वीर की जानकारी",
        "technical_details": "तस्वीर की तकनीकी जानकारी",
        "analyze": "तस्वीर की जाँच करें",
        "processing": "तस्वीर का विश्लेषण हो रहा है...",
        "results": "विश्लेषण के परिणाम",
        "origin": "AI तस्वीर स्रोत की जाँच",
        "scam": "संभावित धोखाधड़ी की जाँच",
        "confidence": "विश्वास स्तर",
        "summary": "विश्लेषण का सारांश",
        "evidence": "दृश्य प्रमाण",
        "counter": "अन्य निरीक्षण",
        "limitations": "विश्लेषण की सीमाएँ",
        "recommendation": "सुझाए गए अगले कदम",
        "scam_evidence": "धोखाधड़ी के संभावित संकेत",
        "suspicious": "संदिग्ध तत्व",
        "extracted": "तस्वीर से पहचाना गया टेक्स्ट",
        "verification": "सत्यापन के चरण",
        "dimensions": "तस्वीर का आकार",
        "resolution": "रिज़ॉल्यूशन",
        "size": "फाइल का आकार",
        "format": "फॉर्मेट",
        "ratio": "लंबाई और चौड़ाई का अनुपात",
        "brightness": "चमक",
        "contrast": "कॉन्ट्रास्ट",
        "saturation": "रंगों की तीव्रता",
        "chart": "तस्वीर के तकनीकी गुण",
        "scam_chart": "धोखाधड़ी जाँच का सारांश",
        "no_evidence": "कोई विशेष प्रमाण नहीं बताया गया।",
        "no_items": "कोई अतिरिक्त जानकारी नहीं मिली।",
        "no_results": "तस्वीर अपलोड करें और परिणाम देखने के लिए जाँच बटन दबाएँ।",
        "disclaimer": "महत्वपूर्ण: यह AI की सहायता से की गई प्रारंभिक जाँच है, फॉरेंसिक सत्यापन नहीं। स्पष्ट धोखाधड़ी संकेत न मिलने का अर्थ यह नहीं है कि तस्वीर या प्रस्ताव सुरक्षित है।",
        "footer": "TrustChecker | बुद्धिमान दृश्य सुरक्षा",
        "invalid": "तस्वीर की जाँच असफल रही:",
        "high": "अधिक",
        "medium": "मध्यम",
        "low": "कम",
        "not_available": "उपलब्ध नहीं",
        "safety": "सुरक्षा संबंधी सलाह",
        "visual_note": "तस्वीर के आँकड़े उसके दृश्य गुण बताते हैं। वे AI निर्माण या धोखाधड़ी का प्रमाण नहीं हैं।",
        "how_it_works": "यह कैसे काम करता है",
        "how_description": "तस्वीर अपलोड करें, TrustChecker को उसका विश्लेषण करने दें और AI स्रोत तथा संभावित धोखाधड़ी संकेतों की जाँच करें।",
        "about": "TrustChecker के बारे में",
        "about_description": "TrustChecker एक AI आधारित डिजिटल सुरक्षा परियोजना है, जो उपयोगकर्ताओं को संदिग्ध सामग्री पहचानने में सहायता करती है।",
        "main_website": "मुख्य वेबसाइट",
        "coming_soon": "मुख्य वेबसाइट जल्द उपलब्ध होगी",
        "screening_result": "वर्तमान जाँच परिणाम",
        "chart_note": "यह चार्ट मॉडल की जाँच श्रेणी दिखाता है। यह धोखाधड़ी की संभावना का प्रतिशत नहीं है।",
        "steps_upload": "अपने डिवाइस से तस्वीर चुनें।",
        "steps_analyze": "AI आधारित सिस्टम को तस्वीर का विश्लेषण करने दें।",
        "steps_review": "परिणाम और सुरक्षा संबंधी सुझाव देखें।",
        "language_changed": "भाषा बदल गई है। चुनी गई भाषा में परिणाम पाने के लिए फिर से जाँच करें।"
    },

    "Marathi": {
        "title": "TrustChecker",
        "subtitle": "AI प्रतिमा आणि फसवणूक तपासणी",
        "tagline": "प्रतिमांचे विश्लेषण करा. संशयास्पद संकेत ओळखा. सुरक्षित निर्णय घ्या.",
        "upload": "विश्लेषणासाठी प्रतिमा अपलोड करा",
        "upload_help": "JPG, JPEG, PNG आणि WEBP. कमाल 5 MB.",
        "preview": "अपलोड केलेली प्रतिमा",
        "statistics": "प्रतिमेची माहिती",
        "technical_details": "प्रतिमेची तांत्रिक माहिती",
        "analyze": "प्रतिमा तपासा",
        "processing": "प्रतिमेचे विश्लेषण सुरू आहे...",
        "results": "विश्लेषणाचे निकाल",
        "origin": "AI प्रतिमा स्रोत तपासणी",
        "scam": "संभाव्य फसवणूक तपासणी",
        "confidence": "विश्वास पातळी",
        "summary": "विश्लेषणाचा सारांश",
        "evidence": "दृश्य पुरावे",
        "counter": "इतर निरीक्षणे",
        "limitations": "विश्लेषणाच्या मर्यादा",
        "recommendation": "सुचवलेली पुढील कृती",
        "scam_evidence": "फसवणुकीचे संभाव्य संकेत",
        "suspicious": "संशयास्पद घटक",
        "extracted": "प्रतिमेतून ओळखलेला मजकूर",
        "verification": "पडताळणीचे टप्पे",
        "dimensions": "प्रतिमेचा आकार",
        "resolution": "रिझोल्यूशन",
        "size": "फाइलचा आकार",
        "format": "फाइल प्रकार",
        "ratio": "लांबी आणि रुंदीचे प्रमाण",
        "brightness": "प्रकाशमानता",
        "contrast": "कॉन्ट्रास्ट",
        "saturation": "रंगांची तीव्रता",
        "chart": "प्रतिमेचे तांत्रिक गुणधर्म",
        "scam_chart": "फसवणूक तपासणीचा आढावा",
        "no_evidence": "विशिष्ट पुरावे नोंदवले गेले नाहीत.",
        "no_items": "अतिरिक्त माहिती नोंदवली गेली नाही.",
        "no_results": "प्रतिमा अपलोड करा आणि निकाल पाहण्यासाठी तपासणी बटण दाबा.",
        "disclaimer": "महत्त्वाचे: ही AI च्या मदतीने केलेली प्राथमिक तपासणी आहे, फॉरेन्सिक पडताळणी नाही. फसवणुकीचे स्पष्ट संकेत नसणे म्हणजे प्रतिमा किंवा ऑफर सुरक्षित असल्याचा पुरावा नाही.",
        "footer": "TrustChecker | बुद्धिमान दृश्य सुरक्षा",
        "invalid": "प्रतिमेची तपासणी अयशस्वी:",
        "high": "जास्त",
        "medium": "मध्यम",
        "low": "कमी",
        "not_available": "उपलब्ध नाही",
        "safety": "सुरक्षेसाठी सूचना",
        "visual_note": "प्रतिमेची आकडेवारी तिचे दृश्य गुणधर्म दर्शवते. ती AI निर्मिती किंवा फसवणुकीचा पुरावा नाही.",
        "how_it_works": "हे कसे कार्य करते",
        "how_description": "प्रतिमा अपलोड करा, TrustChecker ला तिचे विश्लेषण करू द्या आणि AI स्रोत व संभाव्य फसवणुकीचे संकेत तपासा.",
        "about": "TrustChecker बद्दल",
        "about_description": "TrustChecker हा AI आधारित डिजिटल सुरक्षा प्रकल्प आहे, जो संशयास्पद सामग्री ओळखण्यास मदत करतो.",
        "main_website": "मुख्य वेबसाइट",
        "coming_soon": "मुख्य वेबसाइट लवकरच उपलब्ध होईल",
        "screening_result": "सध्याचा तपासणी निकाल",
        "chart_note": "हा आलेख मॉडेलची तपासणी श्रेणी दर्शवतो. तो फसवणुकीची टक्केवारी किंवा शक्यता दर्शवत नाही.",
        "steps_upload": "तुमच्या डिव्हाइसमधून प्रतिमा निवडा.",
        "steps_analyze": "AI आधारित प्रणालीला प्रतिमेचे विश्लेषण करू द्या.",
        "steps_review": "निकाल आणि सुरक्षिततेसाठीच्या सूचना समजून घ्या.",
        "language_changed": "भाषा बदलली आहे. निवडलेल्या भाषेत निकाल मिळवण्यासाठी पुन्हा तपासणी करा."
    }
}


# =========================================================
# CUSTOM DESIGN — WHITE & OLIVE GREEN
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --olive: #3F4A2F;
    --olive-light: #697653;
    --olive-soft: #DCE3D2;
    --ivory: #F5F6EF;
    --text: #252B22;
    --muted: #73796D;
    --border: #E5E8DE;
}

html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

.stApp {
    background: var(--ivory);
    color: var(--text);
}

.block-container {
    max-width: 1180px;
    padding-top: 1.3rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4 {
    color: var(--olive) !important;
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
    letter-spacing: -0.4px;
}

h1 { font-weight: 800 !important; }
h2, h3, h4 { font-weight: 700 !important; }

/* Brand and navigation */
.tc-brand {
    color: var(--olive);
    font-size: 25px;
    font-weight: 800;
    letter-spacing: -0.7px;
    padding-top: 5px;
}

.tc-brand span { color: var(--olive-light); }

.tc-nav-link {
    display: block;
    text-align: center;
    color: var(--olive);
    text-decoration: none;
    font-size: 13px;
    font-weight: 650;
    padding: 10px 5px;
    border-radius: 8px;
}

.tc-nav-link:hover {
    background: #E9EDE2;
    color: var(--olive);
}

.tc-main-link {
    display: block;
    text-align: center;
    background: var(--olive);
    color: #FFFFFF !important;
    text-decoration: none;
    font-size: 12px;
    font-weight: 650;
    padding: 10px 8px;
    border-radius: 8px;
}

/* Hero */
.main-header {
    background: linear-gradient(120deg, #3F4A2F 0%, #697653 100%);
    padding: 36px;
    border-radius: 18px;
    color: #FFFFFF;
    margin: 15px 0 22px 0;
    box-shadow: 0 8px 22px rgba(63, 74, 47, 0.12);
}

.main-header h1 {
    color: #FFFFFF !important;
    font-size: 36px;
    margin: 0 0 7px 0;
}

.main-header h3 {
    color: #F0F2E9 !important;
    font-size: 17px;
    margin: 0 0 12px 0;
}

.main-header p {
    color: #E3E8D9;
    font-size: 14px;
    margin: 0;
    line-height: 1.7;
}

.hero-tag {
    display: inline-block;
    background: rgba(255,255,255,0.13);
    border: 1px solid rgba(255,255,255,0.22);
    color: #F4F6EE;
    padding: 6px 11px;
    border-radius: 30px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 13px;
}

/* Notices */
.info-note {
    background: #EEF1E8;
    border-left: 4px solid var(--olive-light);
    padding: 14px 17px;
    border-radius: 8px;
    color: #46513B;
    margin-bottom: 20px;
    font-size: 13px;
}

.warning-note {
    background: #F4F1E7;
    border-left: 4px solid #A18B50;
    padding: 16px 18px;
    border-radius: 9px;
    color: #5D5338;
    margin: 15px 0;
    line-height: 1.7;
}

/* Result cards */
.result-card {
    background: #FFFFFF;
    padding: 23px;
    border-radius: 14px;
    border: 1px solid var(--border);
    min-height: 170px;
    box-shadow: 0 4px 15px rgba(63, 74, 47, 0.045);
}

.ai-card { border-top: 4px solid #697653; }
.scam-card { border-top: 4px solid #A18B50; }

.result-label {
    color: #73796D;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.result-value {
    color: var(--olive);
    font-size: 21px;
    font-weight: 750;
    margin-top: 13px;
    line-height: 1.4;
}

.result-description {
    color: #73796D;
    font-size: 13px;
    margin-top: 9px;
    line-height: 1.6;
}

/* Detail cards and metrics */
.section-card {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 22px;
    margin: 14px 0;
    box-shadow: 0 3px 12px rgba(63, 74, 47, 0.035);
}

div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid var(--border);
    padding: 15px;
    border-radius: 11px;
}

div[data-testid="stMetricLabel"] {
    color: #73796D;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: var(--olive);
    font-weight: 750;
}

/* Upload */
div[data-testid="stFileUploader"] {
    background: #FFFFFF;
    border: 1px dashed #AAB49A;
    border-radius: 13px;
    padding: 12px;
}

/* Buttons */
.stButton button {
    background: var(--olive);
    color: #FFFFFF;
    border: 1px solid var(--olive);
    border-radius: 9px;
    font-weight: 650;
    min-height: 46px;
    transition: all 0.2s ease;
}

.stButton button:hover {
    background: var(--olive-light);
    border-color: var(--olive-light);
    color: #FFFFFF;
}

/* Select boxes */
div[data-baseweb="select"] > div {
    border-color: #D8DECF;
    border-radius: 9px;
}

/* Footer */
hr {
    border-color: var(--border);
}

.footer {
    text-align: center;
    color: #858B7D;
    padding-top: 28px;
    font-size: 12px;
    line-height: 1.7;
}

@media (max-width: 700px) {
    .main-header { padding: 25px 20px; }
    .main-header h1 { font-size: 28px; }
    .tc-nav-link { font-size: 11px; }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER AND NAVIGATION
# =========================================================

nav_col, lang_col = st.columns([3, 1.3], vertical_alignment="center")

with nav_col:
    st.markdown(
        """
        <div class="tc-brand">
            🛡️ Trust<span>Checker</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with lang_col:
    language = st.selectbox(
        "Language",
        ["English", "Hindi", "Marathi"],
        key="interface_language"
    )

t = TEXT[language]

st.markdown(
    '<hr style="border:0;border-top:1px solid #E5E8DE;margin:8px 0 12px 0;">',
    unsafe_allow_html=True
)

link_cols = st.columns([0.7, 1.35, 1.15, 0.7, 1.35])

navigation = [
    ("Home", "#top"),
    ("Image Detection", "#image-detection"),
    ("How It Works", "#how-it-works"),
    ("About", "#about")
]

for col, (label, anchor) in zip(link_cols[:4], navigation):
    with col:
        st.markdown(
            f'<a class="tc-nav-link" href="{anchor}">{label}</a>',
            unsafe_allow_html=True
        )

with link_cols[4]:
    if MAIN_WEBSITE_URL:
        st.markdown(
            f'<a class="tc-main-link" href="{html.escape(MAIN_WEBSITE_URL, quote=True)}" '
            'target="_blank" rel="noopener noreferrer">Main Website ↗</a>',
            unsafe_allow_html=True
        )
    else:
        st.caption(t["coming_soon"])

st.markdown('<div id="top"></div>', unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="main-header">
        <div class="hero-tag">TRUSTCHECKER IMAGE SECURITY</div>
        <h1>{t["title"]}</h1>
        <h3>{t["subtitle"]}</h3>
        <p>{t["tagline"]}</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="info-note">ℹ️ {t["disclaimer"]}</div>',
    unsafe_allow_html=True
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def display_list(title, items, empty_message):
    st.markdown(f"#### {title}")

    if isinstance(items, list) and items:
        for item in items:
            st.markdown(f"- {html.escape(str(item))}")
    else:
        st.caption(empty_message)


def confidence_label(value):
    return t.get(str(value).lower(), t["not_available"])


def display_result_card(title, result, description, card_class):
    safe_title = html.escape(str(title))
    safe_result = html.escape(str(result))
    safe_description = html.escape(str(description))

    st.markdown(
        f"""
        <div class="result-card {card_class}">
            <div class="result-label">{safe_title}</div>
            <div class="result-value">{safe_result}</div>
            <div class="result-description">{safe_description}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# IMAGE UPLOAD
# =========================================================

st.markdown('<div id="image-detection"></div>', unsafe_allow_html=True)
st.subheader(t["upload"])

uploaded_file = st.file_uploader(
    t["upload"],
    type=["jpg", "jpeg", "png", "webp"],
    help=t["upload_help"],
    key="trustchecker_upload"
)


if uploaded_file is None:
    st.info(t["no_results"])

else:
    valid, message = validate_image(uploaded_file)

    if not valid:
        st.error(message)

    else:
        try:
            processed_image = process_image(uploaded_file)

            statistics = calculate_image_statistics(
                processed_image,
                uploaded_file.size,
                uploaded_file.type.split("/")[-1].upper()
            )

            image_hash = hashlib.sha256(
                uploaded_file.getvalue()
            ).hexdigest()

            # Clear previous results when a different image is uploaded.
            if st.session_state.get("image_hash") != image_hash:
                st.session_state["image_hash"] = image_hash
                st.session_state.pop("analysis", None)
                st.session_state.pop("risk", None)
                st.session_state.pop("analysis_hash", None)
                st.session_state.pop("analysis_language", None)

            # Image preview and key details.
            st.divider()

            image_col, details_col = st.columns([1.15, 1])

            with image_col:
                st.subheader(t["preview"])
                st.image(processed_image, use_container_width=True)

            with details_col:
                st.subheader(t["statistics"])

                a, b = st.columns(2)
                a.metric(
                    t["dimensions"],
                    f'{statistics["width"]} × {statistics["height"]}'
                )
                b.metric(
                    t["resolution"],
                    f'{statistics["megapixels"]} MP'
                )

                c, d = st.columns(2)
                c.metric(
                    t["size"],
                    f'{statistics["file_size_kb"]} KB'
                )
                d.metric(t["format"], statistics["format"])

            # Keep technical image properties available but secondary.
            with st.expander(t["technical_details"], expanded=False):
                st.write(f'**{t["ratio"]}:** {statistics["aspect_ratio"]}:1')
                st.write(f'**{t["brightness"]}:** {statistics["brightness"]}')
                st.write(f'**{t["contrast"]}:** {statistics["contrast"]}')
                st.write(f'**{t["saturation"]}:** {statistics["saturation"]}')
                st.caption(t["visual_note"])

            # Analyze button.
            st.divider()

            if st.button(
                "🔍 " + t["analyze"],
                type="primary",
                use_container_width=True
            ):
                try:
                    with st.spinner(t["processing"]):
                        analysis = detect_ai_image(
                            processed_image,
                            language=language
                        )

                        risk = assess_image_risk(
                            analysis,
                            language=language
                        )

                        st.session_state["analysis"] = analysis
                        st.session_state["risk"] = risk
                        st.session_state["analysis_hash"] = image_hash
                        st.session_state["analysis_language"] = language

                except Exception as error:
                    st.error(f'{t["invalid"]} {error}')

            # =================================================
            # DISPLAY RESULTS
            # =================================================

            if (
                "analysis" in st.session_state
                and st.session_state.get("analysis_hash") == image_hash
            ):

                if st.session_state.get("analysis_language") != language:
                    st.info(t["language_changed"])

                else:
                    analysis = st.session_state["analysis"]
                    risk = st.session_state["risk"]

                    st.divider()
                    st.header(t["results"])

                    # Main assessment cards.
                    col_ai, col_scam = st.columns(2)

                    with col_ai:
                        display_result_card(
                            "🧠 " + t["origin"],
                            risk["ai_title"],
                            risk["ai_description"],
                            "ai-card"
                        )
                        st.write(
                            f'**{t["confidence"]}:** '
                            f'{confidence_label(analysis.get("confidence"))}'
                        )

                    with col_scam:
                        display_result_card(
                            "🛡️ " + t["scam"],
                            risk["scam_title"],
                            risk["scam_description"],
                            "scam-card"
                        )
                        st.write(
                            f'**{t["confidence"]}:** '
                            f'{confidence_label(analysis.get("scam_confidence"))}'
                        )

                    # Scam category visualization.
                    st.markdown(f"### 📊 {t['scam_chart']}")

                    scam_status = analysis.get(
                        "scam_assessment",
                        "insufficient_information"
                    )

                    scam_categories = {
                        "no_obvious_scam_indicators": "No obvious scam indicators",
                        "insufficient_information": "Insufficient information",
                        "suspicious_needs_verification": "Suspicious — verification needed",
                        "likely_scam": "Likely scam indicators"
                    }

                    # Categorical display only. This is NOT a probability score.
                    category_values = {
                        category: (
                            1 if category == scam_status else 0
                        )
                        for category in scam_categories
                    }

                    scam_chart_data = pd.DataFrame(
                        {"Screening result": category_values}
                    )

                    st.bar_chart(
                        scam_chart_data,
                        horizontal=True,
                        color="#697653"
                    )

                    st.markdown(
                        f'**{t["screening_result"]}:** '
                        f'{scam_categories.get(scam_status, "Unknown result")}'
                    )

                    st.caption(t["chart_note"])

                    # AI origin details.
                    st.markdown(
                        '<div class="section-card">',
                        unsafe_allow_html=True
                    )

                    st.subheader("🧠 " + t["origin"])
                    st.markdown(f"**{t['summary']}**")
                    st.write(
                        analysis.get("summary") or t["no_evidence"]
                    )

                    display_list(
                        t["evidence"],
                        analysis.get("visual_evidence", []),
                        t["no_evidence"]
                    )

                    display_list(
                        t["counter"],
                        analysis.get("counter_indicators", []),
                        t["no_items"]
                    )

                    display_list(
                        t["limitations"],
                        analysis.get("limitations", []),
                        t["no_items"]
                    )

                    st.markdown("</div>", unsafe_allow_html=True)

                    # Scam screening details.
                    st.markdown(
                        '<div class="section-card">',
                        unsafe_allow_html=True
                    )

                    st.subheader("🛡️ " + t["scam"])
                    st.markdown(f"**{t['summary']}**")
                    st.write(
                        analysis.get("scam_summary") or t["no_evidence"]
                    )

                    display_list(
                        t["scam_evidence"],
                        analysis.get("scam_evidence", []),
                        t["no_evidence"]
                    )

                    display_list(
                        t["suspicious"],
                        analysis.get("suspicious_elements", []),
                        t["no_items"]
                    )

                    display_list(
                        t["extracted"],
                        analysis.get("extracted_text", []),
                        t["no_items"]
                    )

                    display_list(
                        t["verification"],
                        analysis.get("verification_steps", []),
                        t["no_items"]
                    )

                    st.markdown("</div>", unsafe_allow_html=True)

                    # Safety recommendation.
                    st.subheader("💡 " + t["safety"])

                    safe_recommendation = html.escape(
                        str(risk.get("safety_recommendation", ""))
                    )
                    safe_scam_recommendation = html.escape(
                        str(analysis.get("scam_recommendation", ""))
                    )

                    st.markdown(
                        f"""
                        <div class="warning-note">
                            <b>{t["recommendation"]}</b><br>
                            {safe_recommendation}
                            <br><br>
                            {safe_scam_recommendation}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.caption(t["disclaimer"])

        except Exception as error:
            st.error(f'{t["invalid"]} {error}')


# =========================================================
# HOW IT WORKS AND ABOUT
# =========================================================

st.divider()
st.markdown('<div id="how-it-works"></div>', unsafe_allow_html=True)

st.subheader(t["how_it_works"])

step1, step2, step3 = st.columns(3)

with step1:
    st.markdown("### 01")
    st.markdown("**Upload**")
    st.caption(t["steps_upload"])

with step2:
    st.markdown("### 02")
    st.markdown("**Analyze**")
    st.caption(t["steps_analyze"])

with step3:
    st.markdown("### 03")
    st.markdown("**Review**")
    st.caption(t["steps_review"])

st.markdown('<div id="about"></div>', unsafe_allow_html=True)
st.subheader(t["about"])
st.write(t["about_description"])


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    f"""
    <div class="footer">
        <strong>🛡️ TrustChecker</strong><br>
        {t["footer"]}<br>
        AI-assisted screening · Always verify important information independently.
    </div>
    """,
    unsafe_allow_html=True
)
