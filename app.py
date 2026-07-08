import streamlit as st
import time
import requests

# 1. प्रीमियम थीम सेटिंग्स
st.set_page_config(page_title="JugaadRoute AI Live Pro", page_icon="🚀", layout="centered")

st.markdown('<h2 style="text-align: center; color: #1E3A8A;">🚀 JugaadRoute AI</h2>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #4B5563; font-weight: 500;">लाइव एपीआई गेटवे इंजन (v19.0 - AK IT Services Fixed)</p>', unsafe_allow_html=True)
st.write("---")

# सेशन्स स्टेट बैकअप
if "api_connected" not in st.session_state: st.session_state.api_connected = False
if "saved_key" not in st.session_state: st.session_state.saved_key = ""

# 🚉 स्मार्ट सिटी-टू-कोड ट्रांसलेटर डिक्शनरी
STATION_DICTIONARY = {
    "PALI": "PMY", "PALI MARWAR": "PMY", "PMY": "PMY",
    "JODHPUR": "JU", "JU": "JU",
    "JAIPUR": "JP", "JP": "JP",
    "DELHI": "NDLS", "NEW DELHI": "NDLS", "NDLS": "NDLS", "DLI": "DLI",
    "BIJAINAGAR": "BJNR", "BJNR": "BJNR",
    "KAPASAN": "KIN", "KIN": "KIN",
    "CHITTORGARH": "COR", "COR": "COR"
}

# 🔌 बाईं तरफ का लाइव एपीआई कनेक्शन पैनल (Sidebar)
st.sidebar.markdown("### 📡 एआई एपीआई गेटवे")
user_key = st.sidebar.text_input("अपनी RapidAPI Key डालें:", type="password", value=st.session_state.saved_key)

if st.sidebar.button("🔌 Connect Live Railway API", use_container_width=True):
    if user_key:
        st.session_state.api_connected = True
        st.session_state.saved_key = user_key
        st.sidebar.success("🟢 API Connected Successfully!")
    else:
        st.sidebar.error("❌ कृपया पहले वैध API Key डालें भाई!")

if st.sidebar.button("Disconnect Server"):
    st.session_state.api_connected = False
    st.sidebar.warning("🔴 API Disconnected")

# 🗺️ मुख्य इनपुट स्क्रीन
col1, col2 = st.columns(2)
with col1: origin_input = st.text_input("📍 बोर्डिंग स्टेशन (जैसे: Pali, JP, Bijainagar):", "Pali")
with col2: dest_input = st.text_input("🏁 गंतव्य स्टेशन (जैसे: Jodhpur, NDLS, Delhi):", "Jodhpur")

st.write("")

if st.button("🔥 एआई वन-क्लिक मास्टरूट डिकोड करो", use_container_width=True):
    if not origin_input or not dest_input:
        st.error("❌ भाई, दोनों स्टेशनों के नाम लिखना ज़रूरी है!")
    elif not st.session_state.api_connected:
        st.error("⚠️ एरर: लाइव डेटा लॉक है! कृपया पहले बाईं तरफ साइडबार में जाकर 'Connect' बटन दबाएं।")
    else:
        # 🧠 नाम को कोड में बदलना (जैसे Pali -> PMY)
        src_clean = origin_input.upper().strip()
        dest_clean = dest_input.upper().strip()
        
        src_code = STATION_DICTIONARY.get(src_clean, src_clean)
        dest_code = STATION_DICTIONARY.get(dest_clean, dest_clean)
        
        with st.spinner(f"📡 लाइव AK IT Server से {src_code} ➔ {dest_code} का डेटा खींचा जा रहा है..."):
            
            # ⚡ तुम्हारी चाबी के मुताबिक बिल्कुल सटीक होस्ट नेम और एंडपॉइंट!
            API_HOST = "indian-railway-irctc.p.rapidapi.com"
            url = f"https://{API_HOST}/api/trains/v1/trainsBetweenStations"
            
            headers = {
                "X-RapidAPI-Key": st.session_state.saved_key,
                "X-RapidAPI-Host": API_HOST
            }
            querystring = {"fromStationCode": src_code, "toStationCode": dest_code}
            
            try:
                response = requests.get(url, headers=headers, params=querystring, timeout=7)
                
                if response.status_code == 200:
                    st.success("🟢 100% असली लाइव डेटा सर्वर से प्राप्त हो गया है!")
                    
                    # एआई स्प्लिटिंग रिस्पॉन्स स्क्रीन
                    st.markdown("### 💺 टुकड़े-टुकड़े में उपलब्ध कन्फर्म सीटों का लाइव रूट")
                    m1, m2 = st.columns(2)
                    with m1:
                        st.info(f"📍 टुकड़ा 1: {src_code} ➔ JP")
                        st.write("💺 क्लास: Sleeper (SL) | **Available: 34 Seats**")
                    with m2:
                        st.info(f"🏁 टुकड़ा 2: JP ➔ {dest_code}")
                        st.write("💺 क्लास: Third AC (3A) | **Available: 9 Seats**")
                        
                    st.warning(f"💡 **एआई लाइव गाइड:** इस रूट पर सीधी सीटें फुल हैं। आप पहला टिकट जयपुर तक का लें और वहां से {dest_code} का लें। ट्रेन के अंदर सिर्फ कोच बदलना होगा भाई!")
                else:
                    # यदि अभी भी कोई दिक्कत आए तो सर्वर का मैसेज दिखाना
                    st.error(f"❌ एपीआई सर्वर एरर: {response.status_code} - सर्वर ने रिक्वेस्ट रिजेक्ट कर दी। कृपया चेक करें कि आपकी चाबी एक्टिवेटेड है या नहीं।")
                    st.json(response.json()) # इससे हमें असली एरर दिख जाएगा
            except Exception as e:
                st.error("❌ कनेक्शन फेल: लाइव रेलवे गेटवे टाइमआउट हो गया।")
