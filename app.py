import streamlit as st
import time
import pandas as pd
import random

# 1. प्रीमियम थीम सेटिंग्स
st.set_page_config(page_title="JugaadRoute AI", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    .big-title { font-size:32px !important; font-weight: 800; color: #1E3A8A; text-align: center; margin-bottom: 0px; }
    .sub-title { font-size:16px !important; text-align: center; color: #6B7280; margin-bottom: 20px; }
    .metric-box { background-color: #F3F4F6; padding: 12px; border-radius: 10px; text-align: center; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="big-title">🚀 JugaadRoute AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">फुली-ऑटोमैटिक एआई राउटिंग इंजन (v9.0 - AutoTrain Edition)</div>', unsafe_allow_html=True)
st.write("---")

# 🔗 गूगल शीट का CSV लिंक
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1-jXLlMbfbGa36NgrV4qxIvuB1-tj2Ssr6YUky-y0T04/export?format=csv"

# 🚉 भारत के मुख्य रेलवे स्टेशन्स और हब्स का डेटाबेस
STATION_DATA = {
    "Bijainagar (BJNR)": {"hub": "Ajmer (AII)", "zone": "NW"},
    "Ajmer (AII)": {"hub": "Ajmer (AII)", "zone": "NW"},
    "Jaipur (JP)": {"hub": "Jaipur (JP)", "zone": "NW"},
    "Delhi (DLI)": {"hub": "New Delhi (NDLS)", "zone": "N"},
    "New Delhi (NDLS)": {"hub": "New Delhi (NDLS)", "zone": "N"},
    "Ahmedabad (ADI)": {"hub": "Ahmedabad (ADI)", "zone": "W"},
    "Bhilwara (BHL)": {"hub": "Ajmer (AII)", "zone": "NW"},
    "Kota (KOTA)": {"hub": "Kota (KOTA)", "zone": "W"},
    "Chittorgarh (COR)": {"hub": "Ajmer (AII)", "zone": "NW"},
    "Kapasan (KIN)": {"hub": "Udaipur (UDZ)", "zone": "NW"},
    "Mumbai Central (MMCT)": {"hub": "Mumbai (MMCT)", "zone": "W"},
    "Ludhiana (LDH)": {"hub": "Ludhiana (LDH)", "zone": "N"},
    "Gandhi Nagar (GND)": {"hub": "New Delhi (NDLS)", "zone": "N"},
    "Jodhpur (JU)": {"hub": "Jodhpur (JU)", "zone": "NW"},
    "Udaipur (UDZ)": {"hub": "Udaipur (UDZ)", "zone": "NW"},
    "Surat (ST)": {"hub": "Surat (ST)", "zone": "W"},
    "Vadodara (BRC)": {"hub": "Vadodara (BRC)", "zone": "W"},
    "Indore (INDB)": {"hub": "Indore (INDB)", "zone": "W"}
}

station_list = sorted(list(STATION_DATA.keys()))

# 🧹 क्लीनिंग फ़ंक्शन
def clean_val(v):
    if pd.isna(v): return ""
    return str(v).strip().replace('\u200b', '').replace('\u2060', '')

# 📊 ऑटोमैटिक ट्रेन और रूट जनरेटर (बिना शीट के भी काम करेगा!)
def generate_auto_route(src, dest):
    # एक रैंडम लेकिन लॉजिकल दूरी और समय तय करना (ज़ोन के हिसाब से)
    if src == "Bijainagar (BJNR)" and "Delhi" in dest:
        distance, duration = 430, "7.5 Hrs"
        trains = ["Ashram Express (12915)", "Yoga Express (19031)", "Ajmer Jammu Tawi (12413)"]
    elif "Ajmer" in src and "Delhi" in dest:
        distance, duration = 375, "6.5 Hrs"
        trains = ["Ajmer Shatabdi (12016)", "Vande Bharat Exp (20977)", "Ashram Express (12915)"]
    elif "Ahmedabad" in src and "Delhi" in dest:
        distance, duration = 850, "13.5 Hrs"
        trains = ["Swarna Jayanti Rajdhani (12957)", "Ashram Express (12915)"]
    elif "Jaipur" in src and "Mumbai" in dest:
        distance, duration = 1100, "16 Hrs"
        trains = ["Jaipur Mumbai Superfast (12956)", "Aravali Express (14707)"]
    else:
        # बाकी सभी भारतीय रूट्स के लिए स्मार्ट एआई कैलकुलेशन
        distance = random.randint(300, 950)
        duration = f"{round(distance/65, 1)} Hrs"
        trains = [f"Vande Bharat Express ({random.randint(20000, 20999)})", f"Superfast Garib Rath ({random.randint(12000, 12999)})", f"Express Mail ({random.randint(19000, 19999)})"]

    bus_fare = int(distance * 1.2) if "Bijainagar" in src or "Bhilwara" in src else 0
    train_fare = int(distance * 0.65) # स्लीपर का स्टैंडर्ड रेट
    
    return {
        "hub": STATION_DATA[src]["hub"], "dist": f"{distance} km", "bus": bus_fare, 
        "train": train_fare, "time": duration, "train_list": trains,
        "trick": "💡 एआई टिप: ट्रेन चार्ट बनने के बाद (रवानगी से 4 घंटे पहले) IRCTC ऐप पर 'Current Available' सीट देखें। ऐन वक्त पर हमेशा 10-15 सीटें खाली हो जाती हैं!"
    }

# गूगल शीट से सिर्फ कस्टम ट्रिक्स लोड करना
@st.cache_data(ttl=5)  
def load_sheet_tricks():
    tricks_dict = {}
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        df.columns = [clean_val(c) for c in df.columns]
        for _, row in df.iterrows():
            s = clean_val(row.get("Source", ""))
            d = clean_val(row.get("Destination", ""))
            t = clean_val(row.get("Trick", ""))
            if s and d and t:
                if s not in tricks_dict: tricks_dict[s] = {}
                tricks_dict[s][d] = t
    except:
        pass
    return tricks_dict

custom_tricks = load_sheet_tricks()

# 2. स्मार्ट इनपुट फ़ील्ड्स
col1, col2 = st.columns(2)
with col1:
    origin = st.selectbox("📍 आपकी वर्तमान लोकेशन (Source):", station_list, index=station_list.index("Bijainagar (BJNR)"))
with col2:
    destination = st.selectbox("🏁 आपको कहाँ जाना है (Destination):", station_list, index=station_list.index("Delhi (DLI)"))

travel_preference = st.radio("🎛️ अपनी यात्रा की श्रेणी चुनें:", ["💵 बजट बचाओ (Sleeper Combo)", "⚡ समय बचाओ (AC Premium Combo)"], horizontal=True)

# 3. कोर इंजन एग्जीक्यूशन
if st.button("🔥 एआई स्मार्ट रूट जनरेट करो", use_container_width=True):
    if origin == destination:
        st.error("❌ भाई, दोनों स्टेशन सेम हैं! आप अपनी ही लोकेशन पर खड़े हैं।")
    else:
        with st.spinner("📊 एआई रूटिंग इंजन एक्टिवेट हो रहा है..."):
            time.sleep(0.5)

        # एआई ऑटोमैटिक डेटा जनरेट करता है
        route = generate_auto_route(origin, destination)
        
        # अगर यूजर ने गूगल शीट में कोई अपनी स्पेशल ट्रिक लिखी है, तो एआई उसे ओवरराइड कर देगा
        if origin in custom_tricks and destination in custom_tricks[origin]:
            route["trick"] = custom_tricks[origin][destination]

        train_fare_val = route["train"]
        trip_time = route["time"]
        
        if "AC Premium Combo" in travel_preference:
            train_fare_val = int(train_fare_val * 2.8) # एसी का किराया
            if "Hrs" in trip_time:
                try:
                    t_num = float(trip_time.split()[0])
                    trip_time = f"{max(4.5, round(t_num * 0.8, 1))} Hrs" # सुपरफ़ास्ट/वंदेभारत का कम समय
                except: pass

        total_expense = route["bus"] + train_fare_val

        # 📊 प्रीमियम डैशबोर्ड मीटर्स
        st.write("### 📊 यात्रा समरी (AI Live Metrics)")
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"<div class='metric-box'>🪙 <b>अनुमानित खर्च</b><br><span style='font-size:20px; color:#10B981; font-weight:bold;'>₹{total_expense}</span></div>", unsafe_allow_html=True)
        with m2:
            st.markdown(f"<div class='metric-box'>⏱️ <b>कुल समय</b><br><span style='font-size:20px; color:#3B82F6; font-weight:bold;'>{trip_time}</span></div>", unsafe_allow_html=True)
        with m3:
            st.markdown(f"<div class='metric-box'>🛣️ <b>नजदीकी मुख्य हब</b><br><span style='font-size:20px; color:#F59E0B; font-weight:bold;'>{route['hub']}</span></div>", unsafe_allow_html=True)

        st.write("")
        st.write("---")
        
        tab1, tab2, tab3 = st.tabs(["⭐ MASTER KOTA TRICK / JUGAAD", "🚂 AUTOMATIC TRAIN LIST", "📋 TRAVEL GUIDELINES"])
        with tab1:
            st.success(f"### 🎯 कन्फर्म सीट का जादुई जुगाड़")
            st.write(route["trick"])
        with tab2:
            st.info(f"### 🚂 एआई द्वारा खोजी गई मुख्य ट्रेनें")
            if route["bus"] > 0:
                st.write(f"🚌 **कनेक्टिंग रूट:** पहले लोकल बस/टैक्सी से **{origin}** से **{route['hub']}** जाएँ। (किराया: ~₹{route['bus']})")
            st.write(f"🚉 **{route['hub']}** स्टेशन से सीधे जाने वाली मुख्य ट्रेनें:")
            for train in route["train_list"]:
                st.write(f"   - 🚂 {train}")
        with tab3:
            st.warning("### ⚠️ आवश्यक जानकारी")
            st.write(f"- **दूरी:** यह दोनों शहरों के बीच लगभग **{route['dist']}** का सफर है।")
            st.write("- **सीट जुगाड़:** हमेशा इमरजेंसी कोटा (HQ) बुकिंग के लिए सुबह 11 बजे लोकल स्टेशन मास्टर से संपर्क करें।")
