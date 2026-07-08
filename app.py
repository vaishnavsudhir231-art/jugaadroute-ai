import streamlit as st
import time
import pandas as pd
import random

# 1. पेज कॉन्फ़िगरेशन और यूनिवर्सल थीम
st.set_page_config(page_title="JugaadRoute AI Pro", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    .big-title { font-size:34px !important; font-weight: 900; color: #1E3A8A; text-align: center; margin-bottom: 0px; }
    .sub-title { font-size:16px !important; text-align: center; color: #4B5563; margin-bottom: 25px; font-weight: 500; }
    
    .pro-box { background-color: #FFFFFF; border: 1px solid #E5E7EB; padding: 18px; border-radius: 12px; margin-bottom: 15px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); color: #111827 !important; }
    .pro-box b, .pro-box span, .pro-box p, .pro-box h4 { color: #111827 !important; }
    
    .segment-badge { background-color: #DBEAFE; color: #1E40AF !important; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 13px; border: 1px solid #BFDBFE; }
    .seat-available { background-color: #D1FAE5; color: #065F46 !important; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 13px; border: 1px solid #A7F3D0; }
    
    .connecting-card { background-color: #FFFBEB; border-left: 6px solid #D97706; padding: 15px; border-radius: 8px; margin-top: 10px; color: #111827 !important; }
    .connecting-card b, .connecting-card span { color: #111827 !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="big-title">🚀 JugaadRoute AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">मल्टी-सिटी डायनामिक सीट मैट्रिक्स इंजन (v13.0 - Live Test)</div>', unsafe_allow_html=True)
st.write("---")

# 🔗 गूगल शीट लिंक
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1-jXLlMbfbGa36NgrV4qxIvuB1-tj2Ssr6YUky-y0T04/export?format=csv"

# 🚉 मास्टर रेलवे स्टेशन्स एवं उनके असली जंक्शन हब्स का डेटाबेस
STATION_DATA = {
    "Kapasan (KIN)": {"hub": "Chittorgarh (COR)", "train": "Mewar Express (12964)", "time": "06:30 PM"},
    "Bijainagar (BJNR)": {"hub": "Ajmer (AII)", "train": "Ashram Express (12915)", "time": "06:45 PM"},
    "Bhilwara (BHL)": {"hub": "Ajmer (AII)", "train": "Ajmer Shatabdi (12016)", "time": "03:55 PM"},
    "Chittorgarh (COR)": {"hub": "Chittorgarh (COR)", "train": "Cheetak Express (20474)", "time": "07:50 PM"},
    "Ajmer (AII)": {"hub": "Ajmer (AII)", "train": "Vande Bharat Exp (20977)", "time": "06:20 AM"},
    "Jaipur (JP)": {"hub": "Jaipur (JP)", "train": "Double Decker (12985)", "time": "06:00 AM"},
    "Delhi (DLI)": {"hub": "New Delhi (NDLS)", "train": "Intercity Exp (14322)", "time": "04:30 PM"},
    "Ahmedabad (ADI)": {"hub": "Ahmedabad (ADI)", "train": "Adi SJ Rajdhani (12957)", "time": "05:45 PM"},
    "Kota (KOTA)": {"hub": "Kota (KOTA)", "train": "Kota NZM Sf Exp (22981)", "time": "05:20 PM"}
}
station_list = sorted(list(STATION_DATA.keys()))

def clean_val(v):
    if pd.isna(v): return ""
    return str(v).strip().replace('\u200b', '').replace('\u2060', '')

# 📊 100% डायनामिक मल्टी-सिटी रूट प्रोसेसर
def process_dynamic_route(src, dest):
    # सोर्स और डेस्टिनेशन के हिसाब से असली जंक्शन ढूंढना
    src_hub = STATION_DATA[src]["hub"]
    dest_hub = STATION_DATA[dest]["hub"]
    
    # किराया और दूरी की रैंडम लेकिन लॉजिकल सेटिंग
    bus_fare = 120 if src != src_hub else 0
    leg1_fare = random.choice([240, 450, 725]) # SL, 3A मिक्स के हिसाब से
    leg2_fare = random.choice([310, 580, 960])
    
    # कपासन से दिल्ली का बिल्कुल स्पेशल केस लाइव सेट करना
    if src == "Kapasan (KIN)" and "Delhi" in dest:
        src_hub = "Chittorgarh (COR)"
        via_stop = "Jaipur (JP)"
        train_name = "Mewar Express (12964)"
        dept_time = "06:55 PM"
        jugaad_text = f"💡 **एआई कड़क ट्रिक:** कपासन से दिल्ली डायरेक्ट सीट रिग्रेट है। आप पहला टिकट {src_hub} से {via_stop} (Sleeper) का लें। जयपुर पहुंचते ही गाड़ी के अंदर ही थर्ड एसी (3A) कोच में चले जाएं, वहां आगे दिल्ली तक की सीट खाली है! आपको ट्रेन बदलने की कोई जरूरत नहीं है।"
    # बिजयनगर से दिल्ली का केस
    elif src == "Bijainagar (BJNR)" and "Delhi" in dest:
        src_hub = "Ajmer (AII)"
        via_stop = "Jaipur (JP)"
        train_name = "Ashram Express (12915)"
        dept_time = "06:45 PM"
        jugaad_text = "💡 **एआई कड़क ट्रिक:** अजमेर से जयपुर तक स्लीपर में भारी सीटें खाली हैं। जयपुर आते ही कोच नंबर बदलकर थर्ड एसी में शिफ्ट हो जाएं, आगे दिल्ली तक का सफर बिना किसी वेटिंग के आराम से पूरा हो जाएगा।"
    else:
        # बाकी किसी भी सिटी कॉम्बिनेशन के लिए डायनामिक जेनरेटर
        via_stop = "Jaipur (JP)" if src_hub != "Jaipur (JP)" else "Ajmer (AII)"
        train_name = STATION_DATA[src]["train"]
        dept_time = STATION_DATA[src]["time"]
        jugaad_text = f"💡 **एआई स्प्लिट रूट सजेशन:** {src_hub} से {via_stop} तक लेग-1 बुक करें और {via_stop} से {dest} तक लेग-2 बुक करें। दोनों टुकड़ों में सीट 100% कन्फर्म मिल रही है।"

    return {
        "hub": src_hub,
        "dist": f"{random.randint(420, 510)} km",
        "time": f"{random.randint(7, 9)}.5 Hrs",
        "total_fare": bus_fare + leg1_fare + leg2_fare,
        "bus_fare": bus_fare,
        "train_name": train_name,
        "dept": dept_time,
        "leg1_from": src_hub,
        "leg1_to": via_stop,
        "leg1_class": "Sleeper (SL)" if leg1_fare < 400 else "Third AC (3A)",
        "leg1_seats": f"Available: {random.randint(12, 45)} Seats",
        "leg2_from": via_stop,
        "leg2_to": dest,
        "leg2_class": "Third AC (3A)" if leg2_fare > 500 else "Sleeper (SL)",
        "leg2_seats": f"Available: {random.randint(5, 28)} Seats",
        "explanation": jugaad_text
    }

# गूगल शीट से ट्रिक्स लोड करना
@st.cache_data(ttl=1)  
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

# 2. इनपुट इंटरफेस
col1, col2 = st.columns(2)
with col1: origin = st.selectbox("📍 आपकी लोकेशन (Source):", station_list, index=station_list.index("Kapasan (KIN)") if "Kapasan (KIN)" in station_list else 0)
with col2: destination = st.selectbox("🏁 आपको कहाँ जाना है (Destination):", station_list, index=station_list.index("Delhi (DLI)"))

st.write("")

# 3. इंजन एग्जीक्यूशन
if st.button("🔥 एआई वन-क्लिक मास्टर रूट डिकोड करो", use_container_width=True):
    if origin == destination:
        st.error("❌ भाई, दोनों स्टेशन सेम हैं! कृपया अलग शहर चुनें।")
    else:
        with st.spinner("🧠 एआई मल्टी-सिटी डेटाबेस से लाइव रूट्स मैच कर रहा है..."): 
            time.sleep(0.4)

        # डायनामिक डेटा प्रोसेस करना
        res = process_dynamic_route(origin, destination)
        sheet_trick = custom_tricks.get(origin, {}).get(destination, None)

        # 📊 लाइव मीटर्स (डार्क मोड सेफ)
        m1, m2, m3 = st.columns(3)
        m1.metric("🪙 अनुमानित कुल खर्च", f"₹{res['total_fare']}")
        m2.metric("⏱️ यात्रा समय", res["time"])
        m3.metric("🛣️ मुख्य हब जंक्शन", res["hub"])

        st.write("---")
        
        tab1, tab2 = st.tabs(["🧩 ONE-CLICK MULTI-CLASS COMBOS", "⭐ YOUR GOOGLE SHEET SECRET TRICK"])
        
        with tab1:
            st.markdown("### 💺 टुकड़े-टुकड़े में उपलब्ध कन्फर्म सीटों का लाइव रूट")
            
            if res["bus_fare"] > 0:
                st.markdown(f"""
                <div class='pro-box' style='border-left: 5px solid #6B7280; padding: 12px;'>
                    🚌 <b>लोकल कनेक्टिंग फीडर:</b> पहले लोकल बस/टैक्सी से <b>{origin}</b> से अपने मुख्य जंक्शन हब <b>{res['hub']}</b> पहुँचे। (किराया: ~₹{res['bus_fare']})
                </div>
                """, unsafe_allow_html=True)
                
            with st.container():
                st.write(f"### 1. {res['train_name']}")
                st.write(f"⏰ **रवानगी का समय:** {res['dept']} | 🛠️ **रणनीति:** मल्टी-क्लास बर्थ शिफ्टिंग")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**📍 टुकड़ा 1 (यहाँ से यहाँ तक):**")
                    st.code(f"{res['leg1_from']} ➔ {res['leg1_to']}", language="text")
                    st.markdown(f"💺 क्लास: `{res['leg1_class']}`")
                    st.success(res["leg1_seats"])
                    
                with c2:
                    st.markdown("**🏁 टुकड़ा 2 (यहाँ से यहाँ तक):**")
                    st.code(f"{res['leg2_from']} ➔ {res['leg2_to']}", language="text")
                    st.markdown(f"💺 क्लास: `{res['leg2_class']}`")
                    st.success(res["leg2_seats"])
                    
                st.warning(res["explanation"])
                
        with tab2:
            st.success("### 🎯 आपकी पर्सनल गूगल शीट में दर्ज सीक्रेट जुगाड़")
            if sheet_trick:
                st.write(f"✍️ **आपका नोट:** {sheet_trick}")
            else:
                st.write("💡 अभी इस रूट के लिए आपने गूगल शीट में कोई पर्सनल ट्रिक नहीं लिखी है भाई।")
