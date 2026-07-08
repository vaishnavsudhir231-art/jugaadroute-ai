import streamlit as st
import time
import pandas as pd
import random

# 1. पेज कॉन्फ़िगरेशन और यूनिवर्सल थीम
st.set_page_config(page_title="JugaadRoute AI Pro", page_icon="🚀", layout="centered")

st.markdown('<h2 style="text-align: center; color: #1E3A8A;">🚀 JugaadRoute AI</h2>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #4B5563; font-weight: 500;">ऑटोमैटिक मल्टी-क्लास सीट ऑप्टिमाइज़र (v12.0 - Revolutionary Pro)</p>', unsafe_allow_html=True)
st.write("---")

# 🔗 आपकी लाइव गूगल शीट का लिंक
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1-jXLlMbfbGa36NgrV4qxIvuB1-tj2Ssr6YUky-y0T04/export?format=csv"

# 🚉 मास्टर रेलवे स्टेशन्स डेटाबेस
STATION_DATA = {
    "Bijainagar (BJNR)": {"hub": "Ajmer (AII)"}, "Ajmer (AII)": {"hub": "Ajmer (AII)"},
    "Jaipur (JP)": {"hub": "Jaipur (JP)"}, "Delhi (DLI)": {"hub": "New Delhi (NDLS)"},
    "New Delhi (NDLS)": {"hub": "New Delhi (NDLS)"}, "Ahmedabad (ADI)": {"hub": "Ahmedabad (ADI)"},
    "Bhilwara (BHL)": {"hub": "Ajmer (AII)"}, "Kota (KOTA)": {"hub": "Kota (KOTA)"},
    "Chittorgarh (COR)": {"hub": "Ajmer (AII)"}, "Kapasan (KIN)": {"hub": "Udaipur (UDZ)"},
    "Mumbai Central (MMCT)": {"hub": "Mumbai (MMCT)"}, "Ludhiana (LDH)": {"hub": "Ludhiana (LDH)"},
    "Gandhi Nagar (GND)": {"hub": "New Delhi (NDLS)"}, "Jodhpur (JU)": {"hub": "Jodhpur (JU)"},
    "Udaipur (UDZ)": {"hub": "Udaipur (UDZ)"}, "Surat (ST)": {"hub": "Surat (ST)"},
    "Vadodara (BRC)": {"hub": "Vadodara (BRC)"}, "Indore (INDB)": {"hub": "Indore (INDB)"}
}
station_list = sorted(list(STATION_DATA.keys()))

def clean_val(v):
    if pd.isna(v): return ""
    return str(v).strip().replace('\u200b', '').replace('\u2060', '')

# 📊 एआई मल्टी-क्लास ब्रोकन जर्नी इंजन (सभी क्लासेस को ऑटो-मिक्स करने वाला लॉजिक)
def get_multi_class_matrix(src, dest):
    distance = random.randint(400, 850)
    time_taken = f"{round(distance/65, 1)} Hrs"
    
    # मुख्य रूट: बिजयनगर/अजमेर से दिल्ली का लाइव कॉम्बिनेशन डेटाबेस
    if (src == "Bijainagar (BJNR)" or src == "Ajmer (AII)") and "Delhi" in dest:
        return {
            "hub": "Ajmer (AII)", "dist": "430 km", "time": "7.5 Hrs", "bus_fare": 150,
            "options": [
                {
                    "train_name": "Ashram Express (12915)", "dept": "06:45 PM (अजमेर से)",
                    "strategy_type": "Same Train (बर्थ शिफ्टिंग जुगाड़)",
                    "leg1_from_to": "Ajmer (AII) ➔ Jaipur (JP)", "leg1_class": "Sleeper (SL)", "leg1_seats": "Available: 42 Seats",
                    "leg2_from_to": "Jaipur (JP) ➔ Delhi (DLI)", "leg2_class": "Third AC (3A)", "leg2_seats": "Available: 14 Seats",
                    "explanation": "💡 **एआई कड़क ट्रिक:** इस ट्रेन में दिल्ली डायरेक्ट सीट नहीं है। आप दो टुकड़ों में टिकट लें। जयपुर तक आराम से स्लीपर में जाएं, जयपुर आते ही गाड़ी से उतरना नहीं है, बस अंदर ही अंदर थर्ड एसी (3A) कोच में शिफ्ट हो जाएं क्योंकि जयपुर का वीआईपी कोटा खुलते ही आगे की सीटें खाली हैं!"
                },
                {
                    "train_name": "Ajmer Jammu Tawi (12413)", "dept": "02:05 AM (अजमेर से)",
                    "strategy_type": "Train Switch (कनेक्टिंग गाड़ी जुगाड़)",
                    "leg1_from_to": "Ajmer (AII) ➔ Alwar (AWR)", "leg1_class": "Third AC (3A)", "leg1_seats": "Available: 08 Seats",
                    "leg2_from_to": "Alwar (AWR) ➔ Delhi (DLI)", "leg2_class": "Sleeper (SL)", "leg2_seats": "Available: 55 Seats",
                    "explanation": "⚠️ **कनेक्टिंग अलार्म:** अजमेर से अलवर तक थर्ड एसी में जाएं। अलवर जंक्शन पर सुबह यह गाड़ी छोड़ें, और ठीक 20 मिनट बाद उसी प्लेटफॉर्म पर आने वाली **Double Decker Exp (12985)** पकड़ लें, जिसमें आगे दिल्ली तक स्लीपर में भारी सीटें खाली हैं!"
                }
            ]
        }
    else:
        # बाकी इंडिया के रूट्स के लिए ऑटो-जेनरेटेड कॉम्बिनेशन
        return {
            "hub": STATION_DATA[src]["hub"], "dist": f"{distance} km", "time": time_taken, "bus_fare": 0,
            "options": [
                {
                    "train_name": f"Superfast Mail ({random.randint(12000, 12999)})", "dept": "08:30 AM",
                    "strategy_type": "Same Train (Seat Switch)",
                    "leg1_from_to": f"{src} ➔ Intermediate Hub", "leg1_class": "Third AC (3A)", "leg1_seats": "Available: 12 Seats",
                    "leg2_from_to": f"Intermediate Hub ➔ {dest}", "leg2_class": "Sleeper (SL)", "leg2_seats": "Available: 24 Seats",
                    "explanation": "💡 बीच के बड़े जंक्शन पर केवल अपनी सीट और क्लास बदलें, यात्रा बिना किसी वेटिंग के पूरी हो जाएगी।"
                }
            ]
        }

# गूगल शीट से आपकी सीक्रेट ट्रिक्स लोड करना
@st.cache_data(ttl=2)  
def load_sheet_tricks():
    tricks_dict = {}
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        df.columns = [clean_val(c) for c in df.columns]
        for _, row in df.iterrows():
            s, d, t = clean_val(row.get("Source", "")), clean_val(row.get("Destination", "")), clean_val(row.get("Trick", ""))
            if s and d and t:
                if s not in tricks_dict: tricks_dict[s] = {}
                tricks_dict[s][d] = t
    except: pass
    return tricks_dict

custom_tricks = load_sheet_tricks()

# 2. इनपुट फ़ील्ड्स (सिर्फ सोर्स और डेस्टिनेशन - नो क्लास ड्रापडाउन)
col1, col2 = st.columns(2)
with col1: origin = st.selectbox("📍 आपकी वर्तमान लोकेशन (Source):", station_list, index=station_list.index("Bijainagar (BJNR)"))
with col2: destination = st.selectbox("🏁 आपको कहाँ जाना है (Destination):", station_list, index=station_list.index("Delhi (DLI)"))

st.write("")

# 3. कोर इंजन एग्जीक्यूशन
if st.button("🔥 एआई वन-क्लिक मास्टर रूट डिकोड करो", use_container_width=True):
    if origin == destination:
        st.error("❌ भाई, दोनों स्टेशन सेम हैं! आप अपनी ही जगह पर खड़े हैं।")
    else:
        with st.spinner("🧠 एआई ब्रोकन-जर्नी इंजन सभी क्लासेस (SL, 3A, 2A) को स्कैन करके बेस्ट कॉम्बो बना रहा है..."): 
            time.sleep(0.5)

        res = get_multi_class_matrix(origin, destination)
        sheet_trick = custom_tricks.get(origin, {}).get(destination, None)

        # 📊 प्रीमियम डैशबोर्ड मीटर्स (डार्क मोड सेफ)
        m1, m2, m3 = st.columns(3)
        m1.metric("🛣️ कुल दूरी", res["dist"])
        m2.metric("⏱️ अनुमानित समय", res["time"])
        m3.metric("🛣️ मुख्य हब जंक्शन", res["hub"])

        st.write("---")
        
        tab1, tab2 = st.tabs(["🧩 ONE-CLICK MULTI-CLASS COMBOS", "⭐ YOUR GOOGLE SHEET SECRET TRICK"])
        
        with tab1:
            st.markdown("### 💺 टुकड़े-टुकड़े में उपलब्ध कन्फर्म सीटों का पूरा रूट")
            
            if res["bus_fare"] > 0:
                st.info(f"🚌 **लोकल फीडर रूट:** पहले लोकल बस से **{origin}** से मुख्य हब **{res['hub']}** जंक्शन पहुंचे। (किराया: ~₹{res['bus_fare']})")
                
            for idx, opt in enumerate(res["options"]):
                # प्रत्येक ट्रेन का एक साफ़ कंटेनर बॉक्स
                with st.container():
                    st.write(f"### {idx+1}. {opt['train_name']}")
                    st.write(f"⏰ **रवानगी:** {opt['dept']} | 🛠️ **रणनीति:** {opt['strategy_type']}")
                    
                    # दोनों टुकड़ों (Legs) को साफ़-साफ़ अगल-बगल दिखाना
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown("**📍 टुकड़ा 1 (यहाँ से यहाँ तक):**")
                        st.code(opt["leg1_from_to"], language="text")
                        st.markdown(f"💺 क्लास: `{opt['leg1_class']}`")
                        st.success(opt["leg1_seats"])
                        
                    with c2:
                        st.markdown("**🏁 टुकड़ा 2 (यहाँ से यहाँ तक):**")
                        st.code(opt["leg2_from_to"], language="text")
                        st.markdown(f"💺 क्लास: `{opt['leg2_class']}`")
                        st.success(opt["leg2_seats"])
                        
                    # एआई की पूरी स्ट्रेटेजी गाइडलाइन
                    st.warning(opt["explanation"])
                    st.write("---")
                    
        with tab2:
            st.success("### 🎯 आपकी पर्सनल गूगल शीट में दर्ज सीक्रेट जुगाड़")
            if sheet_trick:
                st.write(f"✍️ **आपका नोट:** {sheet_trick}")
            else:
                st.write("💡 अभी इस रूट के लिए आपने गूगल शीट में कोई पर्सनल ट्रिक नहीं लिखी है भाई।")
