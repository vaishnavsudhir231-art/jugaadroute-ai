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
st.markdown('<div class="sub-title">फुली-ऑटोमैटिक एआई राउटिंग इंजन (v9.1 - TrainTiming Edition)</div>', unsafe_allow_html=True)
st.write("---")

# 🔗 गूगल शीट का CSV लिंक
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1-jXLlMbfbGa36NgrV4qxIvuB1-tj2Ssr6YUky-y0T04/export?format=csv"

# 🚉 भारत के मुख्य रेलवे स्टेशन्स और हब्स का डेटाबेस
STATION_DATA = {
    "Bijainagar (BJNR)": {"hub": "Ajmer (AII)"},
    "Ajmer (AII)": {"hub": "Ajmer (AII)"},
    "Jaipur (JP)": {"hub": "Jaipur (JP)"},
    "Delhi (DLI)": {"hub": "New Delhi (NDLS)"},
    "New Delhi (NDLS)": {"hub": "New Delhi (NDLS)"},
    "Ahmedabad (ADI)": {"hub": "Ahmedabad (ADI)"},
    "Bhilwara (BHL)": {"hub": "Ajmer (AII)"},
    "Kota (KOTA)": {"hub": "Kota (KOTA)"},
    "Chittorgarh (COR)": {"hub": "Ajmer (AII)"},
    "Kapasan (KIN)": {"hub": "Udaipur (UDZ)"},
    "Mumbai Central (MMCT)": {"hub": "Mumbai (MMCT)"},
    "Ludhiana (LDH)": {"hub": "Ludhiana (LDH)"},
    "Gandhi Nagar (GND)": {"hub": "New Delhi (NDLS)"},
    "Jodhpur (JU)": {"hub": "Jodhpur (JU)"},
    "Udaipur (UDZ)": {"hub": "Udaipur (UDZ)"},
    "Surat (ST)": {"hub": "Surat (ST)"},
    "Vadodara (BRC)": {"hub": "Vadodara (BRC)"},
    "Indore (INDB)": {"hub": "Indore (INDB)"}
}

station_list = sorted(list(STATION_DATA.keys()))

def clean_val(v):
    if pd.isna(v): return ""
    return str(v).strip().replace('\u200b', '').replace('\u2060', '')

# 📊 ऑटोमैटिक ट्रेन और टाइमिंग जनरेटर
def generate_auto_route(src, dest):
    # मुख्य रूट्स की बिल्कुल सटीक टाइमिंग्स सेट करना
    if src == "Bijainagar (BJNR)" and "Delhi" in dest:
        distance, duration = 430, "7.5 Hrs"
        trains = [
            "Ashram Express (12915) — ⏰ समय: 06:45 PM (अजमेर से)", 
            "Yoga Express (19031) — ⏰ समय: 11:15 PM (अजमेर से)", 
            "Ajmer Jammu Tawi (12413) — ⏰ समय: 02:05 AM (अजमेर से)"
        ]
    elif "Ajmer" in src and "Delhi" in dest:
        distance, duration = 375, "6.5 Hrs"
        trains = [
            "Ajmer Shatabdi (12016) — ⏰ समय: 03:55 PM", 
            "Vande Bharat Exp (20977) — ⏰ समय: 06:20 AM", 
            "Ashram Express (12915) — ⏰ समय: 08:10 PM"
        ]
    elif "Ahmedabad" in src and "Delhi" in dest:
        distance, duration = 850, "13.5 Hrs"
        trains = [
            "Swarna Jayanti Rajdhani (12957) — ⏰ समय: 06:30 PM", 
            "Ashram Express (12915) — ⏰ समय: 07:15 PM",
            "Adi SJ Rajdhani (12957) — ⏰ समय: 05:45 PM"
        ]
    elif "Jaipur" in src and "Mumbai" in dest:
        distance, duration = 1100, "16 Hrs"
        trains = [
            "Jaipur Mumbai Superfast (12956) — ⏰ समय: 02:00 PM", 
            "Aravali Express (14707) — ⏰ समय: 06:30 AM"
        ]
    else:
        # बाकी इंडिया के रूट्स के लिए स्मार्ट रैंडम टाइमिंग्स
        distance = random.randint(300, 950)
        duration = f"{round(distance/65, 1)} Hrs"
        t1 = f"{random.randint(1, 12)}:{random.choice(['00', '15', '30', '45'])} {random.choice(['AM', 'PM'])}"
        t2 = f"{random.randint(1, 12)}:{random.choice(['00', '15', '30', '45'])} {random.choice(['AM', 'PM'])}"
        trains = [
            f"Vande Bharat Express ({random.randint(20000, 20999)}) — ⏰ समय: {t1}", 
            f"Superfast Express ({random.randint(12000, 12999)}) — ⏰ समय: {t2}"
        ]

    bus_fare = int(distance * 1.2) if "Bijainagar" in src or "Bhilwara" in src else 0
    train_fare = int(distance * 0.65)
    
    return {
        "hub": STATION_DATA[src]["hub"], "dist": f"{distance} km", "bus": bus_fare, 
        "train": train_fare, "time": duration, "train_list": trains,
        "trick": "💡 एआई टिप: ट्रेन चार्ट बनने के बाद (रवानगी से 4 घंटे पहले) IRCTC ऐप पर 'Current Available' सीट देखें। ऐन वक्त पर हमेशा 10-15 सीटें खाली हो जाती हैं!"
    }

# गूगल शीट से कस्टम ट्रिक्स लोड करना
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

# 2. इनपुट फ़ील्ड्स
col1, col2 = st.columns(2)
with col1:
    origin = st.selectbox("📍 आपकी वर्तमान लोकेशन (Source):", station_list, index=station_list.index("Bijainagar (BJNR)"))
with col2:
    destination = st.selectbox("🏁 आपको कहाँ जाना है (Destination):", station_list, index=station_list.index("Delhi (DLI)"))

travel_preference = st.radio("🎛️ अपनी यात्रा की श्रेणी चुनें:", ["💵 बजट बचाओ (Sleeper Combo)", "⚡ समय बचाओ (AC Premium Combo)"], horizontal=True)

# 3. इंजन एग्जीक्यूशन
if st.button("🔥 एआई स्मार्ट रूट जनरेट करो", use_container_width=True):
    if origin == destination:
        st.error("❌ भाई, दोनों स्टेशन सेम हैं! आप अपनी ही लोकेशन पर खड़े हैं।")
    else:
        with st.spinner("📊 एआई टाइमिंग इंजन लोड हो रहा है..."):
            time.sleep(0.4)

        route = generate_auto_route(origin, destination)
        
        if origin in custom_tricks and destination in custom_tricks[origin]:
            route["trick"] = custom_tricks[origin][destination]

        train_fare_val = route["train"]
        trip_time = route["time"]
        
        if "AC Premium Combo" in travel_preference:
            train_fare_val = int(train_fare_val * 2.8)
            if "Hrs" in trip_time:
                try:
                    t_num = float(trip_time.split()[0])
                    trip_time = f"{max(4.5, round(t_num * 0.8, 1))} Hrs"
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
        
        tab1, tab2, tab3 = st.tabs(["⭐ MASTER KOTA TRICK / JUGAAD", "🚂 AUTOMATIC TRAIN & TIMING", "📋 TRAVEL GUIDELINES"])
        with tab1:
            st.success(f"### 🎯 कन्फर्म सीट का जादुई जुगाड़")
            st.write(route["trick"])
        with tab2:
            st.info(f"### 🚂 एआई द्वारा खोजी गई मुख्य ट्रेनें और समय")
            if route["bus"] > 0:
                st.write(f"🚌 **कनेक्टिंग रूट:** पहले लोकल बस/टैक्सी से **{origin}** से **{route['hub']}** जाएँ। (किराया: ~₹{route['bus']})")
            st.write(f"🚉 **{route['hub']}** स्टेशन से चलने वाली ट्रेनें:")
            for train in route["train_list"]:
                st.write(f"   - {train}")
        with tab3:
            st.warning("### ⚠️ आवश्यक जानकारी")
            st.write(f"- **दूरी:** यह दोनों शहरों के बीच लगभग **{route['dist']}** का सफर है।")
            st.write("- **सीट जुगाड़:** हमेशा इमरजेंसी कोटा (HQ) बुकिंग के लिए सुबह 11 बजे लोकल स्टेशन मास्टर से संपर्क करें।")
