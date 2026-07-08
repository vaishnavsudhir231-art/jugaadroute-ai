import streamlit as st
import time
import csv
import os

# 1. पेज कॉन्फ़िगरेशन और प्रीमियम थीम लुक
st.set_page_config(page_title="JugaadRoute AI", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    .big-title { font-size:40px !important; font-weight: 800; color: #1E3A8A; text-align: center; margin-bottom: 0px; }
    .sub-title { font-size:18px !important; text-align: center; color: #6B7280; margin-bottom: 20px; }
    .metric-box { background-color: #F3F4F6; padding: 15px; border-radius: 10px; text-align: center; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="big-title">🚀 JugaadRoute AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">एक्सेल-सिंक्ड ऑटोमैटिक रूटिंग इंजन (v7.1 - Excel Fix)</div>', unsafe_allow_html=True)
st.write("---")

# 🔥 फ़िक्स: encoding="utf-8-sig" ताकि एक्सेल हिंदी भाषा को 100% सही पहचान सके
CSV_FILE = "routes.csv"

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Source", "Destination", "Hub", "Distance", "BusFare", "TrainFare", "Time", "Trains", "Trick"])
        writer.writerow(["Bijainagar (BJNR)", "Delhi (DLI)", "Ajmer (AII)", "65 km", "120", "290", "9.5 Hrs", "आश्रम एक्सप्रेस (12915), रानीखेत एक्सप्रेस (15013)", "Bhilwara (BHL) से टिकट बुक करके Boarding Point को Bijainagar (BJNR) सेट करें।"])
        writer.writerow(["Bijainagar (BJNR)", "Ahmedabad Jn (ADI)", "Bhilwara (BHL)", "60 km", "110", "340", "7.5 Hrs", "अरावली एक्सप्रेस (14701), जोधपुर-बेंगलुरु एक्सप्रेस", "Ajmer (AII) के कोटे से CURRENT बुकिंग चेक करें या भीलवाड़ा जाकर ट्रेन पकड़ें।"])

# एक्सेल फाइल से लाइव डेटा पढ़ना (यहाँ भी utf-8-sig का इस्तेमाल किया है)
all_sources = set()
all_destinations = set()
MASTER_ROUTES = {}

if os.path.exists(CSV_FILE):
    with open(CSV_FILE, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            src = row["Source"].strip()
            dest = row["Destination"].strip()
            
            all_sources.add(src)
            all_destinations.add(dest)
            
            if src not in MASTER_ROUTES:
                MASTER_ROUTES[src] = {}
                
            try: b_fare = int(row["BusFare"])
            except: b_fare = 0
            try: t_fare = int(row["TrainFare"])
            except: t_fare = 0
                
            MASTER_ROUTES[src][dest] = {
                "hub": row["Hub"], "dist": row["Distance"], "bus": b_fare, "train": t_fare, "time": row["Time"],
                "train_list": [t.strip() for t in row["Trains"].split(",")], "trick": row["Trick"]
            }

source_list = sorted(list(all_sources)) if all_sources else ["Bijainagar (BJNR)"]
dest_list = sorted(list(all_destinations)) if all_destinations else ["Delhi (DLI)"]

# 2. स्मार्ट इनपुट फ़ील्ड्स
col1, col2 = st.columns(2)
with col1:
    origin = st.selectbox("📍 आपकी वर्तमान लोकेशन (Source):", source_list)
with col2:
    destination = st.selectbox("🏁 आपको कहाँ जाना है (Destination):", dest_list)

travel_preference = st.radio("🎛️ अपनी यात्रा की श्रेणी चुनें:", ["💵 बजट बचाओ (Sleeper Combo)", "⚡ समय बचाओ (AC Premium Combo)"], horizontal=True)

# 3. कोर एआई राउटिंग एल्गोरिदम
if st.button("🔥 एआई स्मार्ट रूट जनरेट करो", use_container_width=True):
    
    with st.spinner("📊 एक्सेल डेटाबेस से रूट्स सिंक किए जा रहे हैं..."):
        time.sleep(0.3)
        
    if origin == destination:
        st.error("❌ भाई, दोनों स्टेशन सेम हैं! आप अपनी ही लोकेशन पर खड़े हैं।")
        
    elif origin in MASTER_ROUTES and destination in MASTER_ROUTES[origin]:
        data = MASTER_ROUTES[origin][destination]
        train_fare_val = data["train"]
        trip_time = data["time"]
        
        if "AC Premium Combo" in travel_preference:
            train_fare_val += 450
            trip_time = "8.5 Hrs"
            
        total_expense = data["bus"] + train_fare_val

        # 📊 प्रीमियम डैशबोर्ड मीटर्स
        st.write("### 📊 यात्रा समरी (Excel Synced Metrics)")
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"<div class='metric-box'>🪙 <b>कुल खर्च</b><br><span style='font-size:22px; color:#10B981; font-weight:bold;'>₹{total_expense}</span></div>", unsafe_allow_html=True)
        with m2:
            st.markdown(f"<div class='metric-box'>⏱️ <b>कुल समय</b><br><span style='font-size:22px; color:#3B82F6; font-weight:bold;'>{trip_time}</span></div>", unsafe_allow_html=True)
        with m3:
            st.markdown(f"<div class='metric-box'>🛣️ <b>नजदीकी हब</b><br><span style='font-size:22px; color:#F59E0B; font-weight:bold;'>{data['hub']}</span></div>", unsafe_allow_html=True)

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
        st.error(f"❌ एक्सेल शीट में {origin} से {destination} का कोई जुगाड़ रूट दर्ज नहीं है। कृपया एक्सेल फाइल खोलकर नई एंट्री करें!")
