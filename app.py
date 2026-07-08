import streamlit as st
import time
import pandas as pd

# 1. पेज कॉन्फ़िगरेशन और मोबाइल प्रीमियम थीम
st.set_page_config(page_title="JugaadRoute AI", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    .big-title { font-size:32px !important; font-weight: 800; color: #1E3A8A; text-align: center; margin-bottom: 0px; }
    .sub-title { font-size:16px !important; text-align: center; color: #6B7280; margin-bottom: 20px; }
    .metric-box { background-color: #F3F4F6; padding: 12px; border-radius: 10px; text-align: center; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="big-title">🚀 JugaadRoute AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">गूगल शीट्स लाइव-सिंक्ड क्लाउड इंजन (v8.0 - iPhone Edition)</div>', unsafe_allow_html=True)
st.write("---")

# 🔗 आपकी लाइव गूगल शीट का सीक्रेट CSV एक्सपोर्ट लिंक
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1-jXLlMbfbGa36NgrV4qxIvuB1-tj2Ssr6YUky-y0T04/export?format=csv"

# 🚉 ऑल इंडिया मुख्य स्टेशनों की मास्टर लिस्ट (आपकी शीट के स्टेशन्स इसमें अपने आप जुड़ जाएंगे)
ALL_INDIA_STATIONS = [
    "Bijainagar (BJNR)", "Ajmer (AII)", "Jaipur (JP)", "Delhi (DLI)", "New Delhi (NDLS)", 
    "Ahmedabad (ADI)", "Bhilwara (BHL)", "Kota (KOTA)", "Chittorgarh (COR)", "Kapasan (KIN)", 
    "Mumbai Central (MMCT)", "Ludhiana (LDH)", "Gandhi Nagar (GND)", "Jodhpur (JU)", 
    "Udaipur (UDZ)", "Surat (ST)", "Vadodara (BRC)", "Indore (INDB)", "Agra Cantt (AGC)", 
    "Kanpur Central (CNB)", "Lucknow (LKO)", "Patna Jn (PNBE)", "Howrah (HWH)", 
    "KSR Bengaluru (SBC)", "Pune Jn (PUNE)", "Hyderabad (HYB)", "Chennai Central (MAS)"
]

# गूगल शीट से लाइव डेटा लोड करना (हर 10 सेकंड में खुद फ्रेश होगा)
@st.cache_data(ttl=10)  
def load_live_data():
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        df.columns = [c.strip() for c in df.columns]  # कॉलम के स्पेस साफ़ करना
        return df
    except Exception as e:
        return None

df_routes = load_live_data()

MASTER_ROUTES = {}
dynamic_stations = set()

if df_routes is not None and not df_routes.empty:
    for _, row in df_routes.iterrows():
        try:
            src = str(row["Source"]).strip()
            dest = str(row["Destination"]).strip()
            
            dynamic_stations.add(src)
            dynamic_stations.add(dest)
            
            if src not in MASTER_ROUTES:
                MASTER_ROUTES[src] = {}
                
            try: b_fare = int(row["BusFare"])
            except: b_fare = 0
            try: t_fare = int(row["TrainFare"])
            except: t_fare = 0
                
            MASTER_ROUTES[src][dest] = {
                "hub": str(row["Hub"]), "dist": str(row["Distance"]), "bus": b_fare, "train": t_fare, "time": str(row["Time"]),
                "train_list": [t.strip() for t in str(row["Trains"]).split(",")], "trick": str(row["Trick"])
            }
        except:
            pass

# मास्टर लिस्ट और शीट के स्टेशन्स को आपस में मिलाना
final_station_set = set(ALL_INDIA_STATIONS).union(dynamic_stations)
station_list = sorted(list(final_station_set))

# 2. स्मार्ट इनपुट फ़ील्ड्स (सर्च बार के साथ)
col1, col2 = st.columns(2)
with col1:
    origin = st.selectbox("📍 आपकी वर्तमान लोकेशन (Source):", station_list, index=station_list.index("Bijainagar (BJNR)") if "Bijainagar (BJNR)" in station_list else 0)
with col2:
    destination = st.selectbox("🏁 आपको कहाँ जाना है (Destination):", station_list, index=station_list.index("Delhi (DLI)") if "Delhi (DLI)" in station_list else 0)

travel_preference = st.radio("🎛️ अपनी यात्रा की श्रेणी चुनें:", ["💵 बजट बचाओ (Sleeper Combo)", "⚡ समय बचाओ (AC Premium Combo)"], horizontal=True)

# 3. कोर एआई राउटिंग एल्गोरिदम
if st.button("🔥 एआई स्मार्ट रूट जनरेट करो", use_container_width=True):
    
    with st.spinner("📊 लाइव गूगल शीट से डेटा सिंक हो रहा है..."):
        time.sleep(0.4)
        
    if origin == destination:
        st.error("❌ भाई, दोनों स्टेशन सेम हैं! आप अपनी ही लोकेशन पर खड़े हैं।")
        
    elif origin in MASTER_ROUTES and destination in MASTER_ROUTES[origin]:
        data = MASTER_ROUTES[origin][destination]
        train_fare_val = data["train"]
        trip_time = data["time"]
        
        if "AC Premium Combo" in travel_preference:
            train_fare_val += 450
            trip_time = "8.5 Hrs"
            
        total_expense = data["bus"] + train_fare_val

        # 📊 प्रीमियम डैशबोर्ड मीटर्स
        st.write("### 📊 यात्रा समरी (Live Metrics)")
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"<div class='metric-box'>🪙 <b>कुल खर्च</b><br><span style='font-size:20px; color:#10B981; font-weight:bold;'>₹{total_expense}</span></div>", unsafe_allow_html=True)
        with m2:
            st.markdown(f"<div class='metric-box'>⏱️ <b>कुल समय</b><br><span style='font-size:20px; color:#3B82F6; font-weight:bold;'>{trip_time}</span></div>", unsafe_allow_html=True)
        with m3:
            st.markdown(f"<div class='metric-box'>🛣️ <b>नजदीकी हब</b><br><span style='font-size:20px; color:#F59E0B; font-weight:bold;'>{data['hub']}</span></div>", unsafe_allow_html=True)

        st.write("")
        st.write("---")
        
        tab1, tab2, tab3 = st.tabs(["⭐ MASTER KOTA TRICK", "🚌 HUB CONNECT ROUTE", "📋 IMPORTANT GUIDELINES"])
        with tab1:
            st.success(f"### 🎯 बिना ट्रेन बदले कंफर्म सीट का जुगाड़")
            st.write(f"**एआई स्ट्रेटेजी:** {data['trick']}")
        with tab2:
            st.info(f"### 🚌 रोड + रेल कनेक्टिंग रूट डिटेल्स")
            st.write(f"1. **लोकल बस/टैक्सी:** {origin} से {data['hub']} जाएँ। (किराया: ~₹{data['bus']})")
            st.write(f"2. **मुख्य ट्रेन:** {data['hub']} स्टेशन पहुंचकर इनमें से कोई ट्रेन लें:")
            for train in data["train_list"]:
                st.write(f"   - 🚂 **{train}**")
        with tab3:
            st.warning("### ⚠️ यात्रा से पहले यह ध्यान रखें")
            st.write("- **करंट बुकिंग:** ट्रेन रवाना होने से ठीक 4 घंटे पहले IRCTC ऐप पर 'Current Available' सीट जरूर चेक करें।")
            
    else:
        st.error(f"❌ इस रूट का जुगाड़ अभी दर्ज नहीं है! अपने iPhone पर 'Google Sheets' ऐप खोलें और {origin} से {destination} की नई एंट्री डालें। वह तुरंत यहाँ लाइव दिखने लगेगी!")
