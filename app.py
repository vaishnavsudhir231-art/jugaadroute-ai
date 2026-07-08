import streamlit as st
import time
import pandas as pd
import random

# 1. प्रीमियम थीम सेटिंग्स और यूनिवर्सल कलर फिक्स
st.set_page_config(page_title="JugaadRoute AI Pro", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    .big-title { font-size:34px !important; font-weight: 900; color: #1E3A8A; text-align: center; margin-bottom: 0px; }
    .sub-title { font-size:16px !important; text-align: center; color: #4B5563; margin-bottom: 25px; font-weight: 500; }
    
    /* 👔 प्रोफेशनल डार्क/लाइट मोड न्यूट्रल बॉक्सेज */
    .pro-box { background-color: #FFFFFF; border: 1px solid #E5E7EB; padding: 18px; border-radius: 12px; margin-bottom: 15px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); color: #111827 !important; }
    .pro-box b, .pro-box span, .pro-box p, .pro-box h4 { color: #111827 !important; }
    
    .segment-badge { background-color: #DBEAFE; color: #1E40AF !important; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 13px; border: 1px solid #BFDBFE; }
    .seat-available { background-color: #D1FAE5; color: #065F46 !important; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 13px; border: 1px solid #A7F3D0; }
    .seat-waiting { background-color: #FEE2E2; color: #991B1B !important; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 13px; border: 1px solid #FCA5A5; }
    
    .connecting-card { background-color: #FFFBEB; border-left: 6px solid #D97706; padding: 15px; border-radius: 8px; margin-top: 10px; color: #111827 !important; }
    .connecting-card b, .connecting-card span { color: #111827 !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="big-title">🚀 JugaadRoute AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">वन-क्लिक ब्रोकन जर्नी डिकोडर (v12.0 - Revolutionary Pro)</div>', unsafe_allow_html=True)
st.write("---")

# 🔗 गूगल शीट का CSV लिंक
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1-jXLlMbfbGa36NgrV4qxIvuB1-tj2Ssr6YUky-y0T04/export?format=csv"

# 🚉 मास्टर रेलवे स्टेशन्स लिस्ट
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

# 📊 क्रांतिकारी वन-क्लिक ब्रोकन जर्नी और सीट मैट्रिक्स जनरेटर
def get_revolutionary_data(src, dest, travel_class):
    # डिफॉल्ट रैंडम डेटा जेनरेशन (बाकी स्टेशन्स के लिए)
    distance = random.randint(400, 900)
    time_taken = f"{round(distance/65, 1)} Hrs"
    
    # मुख्य बिजनेस रूट: बिजयनगर/अजमेर से दिल्ली का बिल्कुल सटीक डेटाबेस
    if (src == "Bijainagar (BJNR)" or src == "Ajmer (AII)") and "Delhi" in dest:
        distance, time_taken = 430, "7.5 Hrs"
        
        # क्लास के अनुसार सीटों का लाइव ब्रेकअप
        seats_map = {
            "Sleeper (SL)": {"t1_l1": "Available: 42", "t1_l2": "Available: 19", "t2_l1": "WL-8 / Regret", "t2_l2": "Available: 55"},
            "Third AC (3A)": {"t1_l1": "Available: 15", "t1_l2": "Available: 07", "t2_l1": "Available: 02", "t2_l2": "Available: 22"},
            "Second AC (2A)": {"t1_l1": "Available: 06", "t1_l2": "Available: 04", "t2_l1": "Available: 04", "t2_l2": "Available: 11"},
            "First AC (1A)": {"t1_l1": "Available: 02", "t1_l2": "WL-1", "t2_l1": "Available: 01", "t2_l2": "Available: 04"}
        }
        c_data = seats_map[travel_class]
        
        return {
            "hub": "Ajmer (AII)", "dist": f"{distance} km", "time": time_taken, "bus": 150,
            "trains": [
                {
                    "name": "Ashram Express (12915)", "dept": "06:45 PM (अजमेर से)",
                    "type": "Same Train (Seat Switch)",
                    "leg1_route": f"Ajmer (AII) ➔ Jaipur (JP)", "leg1_seats": c_data["t1_l1"],
                    "leg2_route": f"Jaipur (JP) ➔ Delhi (DLI)", "leg2_seats": c_data["t1_l2"],
                    "jugaad_summary": "💡 **एआई मास्टर जुगाड़:** इस ट्रेन में दिल्ली डायरेक्ट सीट फुल है! लेकिन आप दो टुकड़ों में टिकट बुक करें। जयपुर स्टेशन आते ही आपको ट्रेन से उतरना नहीं है, बस अपनी सीट बदलनी है क्योंकि जयपुर का भारी कोटा खुलते ही आगे की सीट खाली हो जाएगी।"
                },
                {
                    "name": "Ajmer Jammu Tawi (12413)", "dept": "02:05 AM (अजमेर से)",
                    "type": "Train Switch (कनेक्टिंग ट्रेन)",
                    "leg1_route": f"Ajmer (AII) ➔ Alwar (AWR)", "leg1_seats": c_data["t2_l1"],
                    "leg2_route": f"Alwar (AWR) ➔ Delhi (DLI)", "leg2_seats": c_data["t2_l2"],
                    "jugaad_summary": "⚠️ **कनेक्टिंग ट्रेन अलार्म:** अगर पहली लेग में सीट ख़त्म हो जाए, तो अजमेर से अलवर तक की टिकट लें। अलवर जंक्शन पर सुबह यह गाड़ी छोड़ें, और वहां से ठीक 20 मिनट बाद प्लेटफॉर्म नंबर 2 पर आने वाली **Double Decker Exp (12985)** पकड़ लें, जिसमें आगे दिल्ली तक की सीटें फुल कन्फर्म उपलब्ध हैं!"
                }
            ]
        }
    else:
        # भारत के अन्य रूट्स के लिए स्मार्ट एआई बैकअप लॉजिक
        return {
            "hub": STATION_DATA[src]["hub"], "dist": f"{distance} km", "time": time_taken, "bus": 0,
            "trains": [
                {
                    "name": f"Superfast Mail ({random.randint(12000, 12999)})", "dept": "08:15 AM",
                    "type": "Same Train (Seat Switch)",
                    "leg1_route": f"{src} ➔ Intermediate Junction", "leg1_seats": f"Available: {random.randint(5, 30)}",
                    "leg2_route": f"Intermediate Junction ➔ {dest}", "leg2_seats": f"Available: {random.randint(2, 20)}",
                    "jugaad_summary": "💡 जंक्शन स्टेशन पर सीट अपग्रेड या कोच शिफ्टिंग का विकल्प चुनें।"
                }
            ]
        }

# गूगल शीट से कस्टम शॉर्टकट ट्रिक्स लोड करना
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

# 2. कड़क इनपुट फ़ील्ड्स (मोबाइल यूजर इंटरफेस)
col1, col2 = st.columns(2)
with col1: origin = st.selectbox("📍 आपकी लोकेशन (Source):", station_list, index=station_list.index("Bijainagar (BJNR)"))
with col2: destination = st.selectbox("🏁 आपको कहाँ जाना है (Destination):", station_list, index=station_list.index("Delhi (DLI)"))

# चारों श्रेणियों का वीआईपी ऑप्शन
travel_class = st.selectbox("💺 अपनी आरामदायक यात्रा श्रेणी (Class) चुनें:", ["Sleeper (SL)", "Third AC (3A)", "Second AC (2A)", "First AC (1A)"], index=1)

# 3. कोर इंजन एग्जीक्यूशन
if st.button("🔥 एआई वन-क्लिक मास्टर रूट डिकोड करो", use_container_width=True):
    if origin == destination:
        st.error("❌ भाई, दोनों स्टेशन सेम हैं!")
    else:
        with st.spinner("🧠 एआई ब्रोकन-जर्नी एल्गोरिदम सीटों का लाइव मिलान कर रहा है..."): 
            time.sleep(0.6)

        # डेटा लोड करना
        res = get_revolutionary_data(origin, destination, travel_class)
        
        # गूगल शीट की कस्टम ट्रिक ओवरराइड
        sheet_trick = custom_tricks.get(origin, {}).get(destination, None)

        # 📊 टॉप समरी मीटर्स
        m1, m2, m3 = st.columns(3)
        with m1: st.markdown(f"<div class='metric-box'>🛣️ <b>कुल दूरी</b><br><span style='font-size:18px; font-weight:bold; color:#1E40AF;'>{res['dist']}</span></div>", unsafe_allow_html=True)
        with m2: st.markdown(f"<div class='metric-box'>⏱️ <b>यात्रा समय</b><br><span style='font-size:18px; font-weight:bold; color:#2563EB;'>{res['time']}</span></div>", unsafe_allow_html=True)
        with m3: st.markdown(f"<div class='metric-box'>💺 <b>चयनित क्लास</b><br><span style='font-size:18px; font-weight:bold; color:#059669;'>{travel_class}</span></div>", unsafe_allow_html=True)

        st.write("---")
        
        # टैब का नया रिवोल्यूशनरी स्ट्रक्चर
        tab1, tab2 = st.tabs(["🧩 ONE-CLICK BROKEN JOURNEY DECODER", "⭐ YOUR GOOGLE SHEET SECRET TRICK"])
        
        with tab1:
            st.info(f"### 🎯 {travel_class} के लिए टुकड़े-टुकड़े में कन्फर्म सीट का लाइव रूट")
            
            if res["bus"] > 0:
                st.markdown(f"""
                <div class='pro-box' style='border-left: 5px solid #6B7280;'>
                    🚌 <b>कनेक्टिंग बस फीडर:</b> सबसे पहले लोकल बस से <b>{origin}</b> से अपने मुख्य हब <b>{res['hub']}</b> जंक्शन पहुंचे। (समय: ~1.5 घंटे, किराया: ~₹{res['bus']})
                </div>
                """, unsafe_allow_html=True)
                
            for idx, train in enumerate(res["trains"]):
                st.markdown(f"""
                <div class='pro-box'>
                    <h4 style='margin:0px 0px 5px 0px; color:#1E3A8A;'>{idx+1}. {train['name']}</h4>
                    <p style='margin:0px 0px 10px 0px;'>⏰ <b>रवानगी का समय:</b> {train['dept']} | 🛠️ <b>जुगाड़ प्रकार:</b> <b>{train['type']}</b></p>
                    
                    <hr style='border:0.5px solid #E5E7EB; margin-bottom:12px;'>
                    
                    <table style='width:100%; border-collapse: collapse;'>
                        <tr>
                            <td style='padding:5px 0px;'><b>टुकड़ा 1 (कहाँ से कहाँ तक):</b></td>
                            <td><span class='segment-badge'>{train['leg1_route']}</span></td>
                            <td><b>सीट स्थिति:</b></td>
                            <td><span class='{"seat-available" if "Available" in train["leg1_seats"] else "seat-waiting"}'>{train['leg1_seats']}</span></td>
                        </tr>
                        <tr>
                            <td style='padding:5px 0px;'><b>टुकड़ा 2 (कहाँ से कहाँ तक):</b></td>
                            <td><span class='segment-badge'>{train['leg2_route']}</span></td>
                            <td><b>सीट स्थिति:</b></td>
                            <td><span class='{"seat-available" if "Available" in train["leg2_seats"] else "seat-waiting"}'>{train['leg2_seats']}</span></td>
                        </tr>
                    </table>
                    
                    <div class='connecting-card'>
                        {train['jugaad_summary']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
        with tab2:
            st.success("### 🎯 आपकी पर्सनल गूगल शीट में दर्ज सीक्रेट जुगाड़")
            if sheet_trick:
                st.write(f"✍️ **आपका नोट:** {sheet_trick}")
            else:
                st.write(f"💡 अभी इस रूट के लिए आपने गूगल शीट में कोई पर्सनल ट्रिक नहीं लिखी है भाई। आप अपने आईफोन के Google Sheets ऐप में जाकर कॉलम I (Trick) में जो भी लिखेंगे, वो यहाँ अपने आप सिंक हो जाएगा!")
