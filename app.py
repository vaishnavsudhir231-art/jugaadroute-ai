import streamlit as st
import requests
import datetime

# 1. UI & Page Settings
st.set_page_config(page_title="JugaadRoute AI Master Pro", page_icon="🚀", layout="centered")

st.markdown('<h2 style="text-align: center; color: #1E3A8A; font-family: sans-serif;">🚀 JugaadRoute AI</h2>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #10B981; font-weight: 600; letter-spacing: 0.5px;">PREMIUM AI ROUTING ENGINE (v25.1)</p>', unsafe_allow_html=True)
st.write("---")

# Session State Manager for Persistent Connection
if "api_connected" not in st.session_state: st.session_state.api_connected = False
if "saved_key" not in st.session_state: st.session_state.saved_key = ""

# 🔐 1. Advanced Server Settings
with st.expander("⚙️ Advanced Server Settings (API Gateway Config)"):
    st.markdown("<p style='color: #4B5563; font-size: 13px;'>Enter your RapidAPI Key to sync the application with live cloud servers.</p>", unsafe_allow_html=True)
    user_key = st.text_input("Enter your RapidAPI Key:", type="password", value=st.session_state.saved_key)
    
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        if st.button("🔌 Connect Live Server", use_container_width=True):
            if user_key:
                st.session_state.api_connected = True
                st.session_state.saved_key = user_key
                st.success("🟢 API Connected Successfully!")
            else:
                st.error("❌ Please enter a valid API Key first!")
    with c_btn2:
        if st.button("Disconnect Server", use_container_width=True):
            st.session_state.api_connected = False
            st.warning("🔴 API Disconnected")

st.write("")

# 🗺️ 2. Main Input Screen Layout
col1, col2 = st.columns(2)
with col1: origin_input = st.text_input("📍 Boarding Station (Source):", "BJNR") # BJNR default कर दिया
with col2: dest_input = st.text_input("🏁 Destination Station:", "NDLS") # NDLS default कर दिया

# 📅 3. Interactive Month Calendar Selector
travel_date = st.date_input("📅 Select Travel Date (Month Calendar View):", value=datetime.date.today())

st.write("")

# 🔥 3. Master AI Processing Engine (बटन क्लिक लॉजिक)
if st.button("🔥 AI One-Click Master Route Decode", use_container_width=True):
    if not origin_input or not dest_input:
        st.error("❌ Error: Both station names are required!")
    elif not st.session_state.api_connected:
        st.error("⚠️ Error: Live data is locked! Please expand '⚙️ Advanced Server Settings' above and connect using your API Key.")
    else:
        src = origin_input.upper().strip()
        dest = dest_input.upper().strip()
        
        # 🎯 तारीख का फॉर्मेट बदल दिया क्योंकि आपकी API को DD-MM-YYYY चाहिए
        date_string = travel_date.strftime("%d-%m-%Y") 
        
        with st.spinner("📡 Fetching real-time trains from Live Servers..."):
            
            # 🚀 ये रहा आपकी स्क्रीन वाला असली एपीआई कोड:
            url = "https://irctc27.p.rapidapi.com/search.php"
            
            payload = {
                "source": src,
                "destination": dest,
                "date": date_string
            }
            
            headers = {
                "x-rapidapi-key": st.session_state.saved_key, # आपकी चाबी यहाँ ऑटोमैटिक आ जाएगी
                "x-rapidapi-host": "irctc27.p.rapidapi.com",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            try:
                # 📡 लाइव सर्वर को हिट मारना
                response = requests.post(url, data=payload, headers=headers, timeout=15)
                api_response_data = response.json()
                
                st.success("🟢 Live Server Connected Successfully!")
                
                # 🔍 लाइव डेटा को स्क्रीन पर देखना ताकि हम अगला कदम उठा सकें
                st.markdown("### 📊 Live API Response (चेतक और बाकी ट्रेनों का कच्चा डेटा)")
                st.json(api_response_data)
                
            except Exception as e:
                st.error(f"❌ Connection Error: {e}")
