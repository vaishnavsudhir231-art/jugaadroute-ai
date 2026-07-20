import streamlit as st
import requests
import datetime

# 1. UI & Page Settings
st.set_page_config(page_title="JugaadRoute AI Master Pro", page_icon="🚀", layout="centered")

st.markdown('<h2 style="text-align: center; color: #1E3A8A; font-family: sans-serif;">🚀 JugaadRoute AI</h2>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #10B981; font-weight: 600; letter-spacing: 0.5px;">DYNAMIC LIVE TRANSIT ENGINE (v25.1)</p>', unsafe_allow_html=True)
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
with col1: origin_input = st.text_input("📍 Boarding Station (Source):", "BJNR")
with col2: dest_input = st.text_input("🏁 Destination Station:", "NDLS")

# 📅 3. Interactive Month Calendar Selector
travel_date = st.date_input("📅 Select Travel Date:", value=datetime.date.today())

st.write("")

# 🔥 3. Master AI Processing Engine (बटन क्लिक लॉजिक)
if st.button("🔥 AI One-Click Master Route Decode", use_container_width=True):
    if not origin_input or not dest_input:
        st.error("❌ Error: Both station codes are required!")
    elif not st.session_state.api_connected:
        st.error("⚠️ Error: Live data is locked! Please expand '⚙️ Advanced Server Settings' above and connect using your API Key.")
    else:
        src = origin_input.upper().strip()
        dest = dest_input.upper().strip()
        date_string = travel_date.strftime("%d-%m-%Y") 
        
        with st.spinner("📡 Fetching real-time trains from Live Servers..."):
            url = "https://irctc27.p.rapidapi.com/search.php"
            
            payload = {
                "source": src,
                "destination": dest,
                "date": date_string
            }
            
            headers = {
                "x-rapidapi-key": st.session_state.saved_key,
                "x-rapidapi-host": "irctc27.p.rapidapi.com",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            try:
                response = requests.post(url, data=payload, headers=headers, timeout=15)
                api_response_data = response.json()
                
                st.success("🟢 Live Server Connected Successfully!")
                st.write("")
                
                # 🔄 DYNAMIC PARSING: आपके स्क्रीनशॉट वाले JSON स्ट्रक्चर से डेटा निकालना
                trains_obj = api_response_data.get("trains", {})
                data_obj = trains_obj.get("data", {}) if isinstance(trains_obj, dict) else {}
                
                # API से ट्रेनों की लिस्ट ढूंढना (अलग-अलग संभावित चाबियों की जांच)
                train_list = []
                if isinstance(data_obj, dict):
                    train_list = data_obj.get("trainList") or data_obj.get("trains") or data_obj.get("list") or []
                
                # अगर कोई ट्रेन नहीं मिली या फॉर्मेट अलग है
                if not train_list:
                    st.warning("⚠️ इस रूट या तारीख पर कोई सीधी ट्रेन नहीं मिली या सर्वर से रिस्पॉन्स खाली है।")
                    # बैकअप के तौर पर कच्चा डेटा देखने के लिए (ताकि ऐप ब्लैंक न लगे)
                    with st.expander("🔍 View Raw Response JSON"):
                        st.json(api_response_data)
                else:
                    st.markdown(f"### 🎯 Available Route Options ({len(train_list)} Trains Found)")
                    st.markdown("<p style='color: #6B7280; font-size: 14px;'>कस्टमर अपनी सुविधा और समय के अनुसार सही विकल्प चुन सकते हैं:</p>", unsafe_allow_html=True)
                    
                    # 🔄 DYNAMIC LOOP: यह हर एक ट्रेन को सुंदर कार्ड में दिखाएगा
                    for idx, train in enumerate(train_list, 1):
                        
                        # सुरक्षित तरीके से वैल्यूज निकालना ताकि एरर न आए
                        train_name = train.get("trainName", train.get("train_name", "Express Train"))
                        train_num = train.get("trainNumber", train.get("trainNo", "00000"))
                        dep_time = train.get("departureTime", train.get("depTime", "N/A"))
                        arr_time = train.get("arrivalTime", train.get("arrTime", "N/A"))
                        duration = train.get("duration", train.get("travelTime", "N/A"))
                        
                        # हर ट्रेन के लिए एक सुंदर एक्सपैंडर बॉक्स
                        with st.expander(f"🚆 {train_num} - {train_name} | ⏰ {dep_time} ➔ {arr_time}", expanded=(idx==1)):
                            
                            # तीन कॉलम्स में मुख्य जानकारी दिखाना
                            m1, m2, m3 = st.columns(3)
                            with m1: st.metric(label="⏱️ Duration", value=duration)
                            with m2: st.metric(label="📍 Departs From", value=src)
                            with m3: st.metric(label="🏁 Terminal Station", value=dest)
                            
                            # प्रीमियम डिज़ाइन वाला सुंदर डिब्बा
                            st.markdown(f"""
                            <div style='background-color: #EFF6FF; color: #111827; padding: 14px; border-radius: 8px; border-left: 5px solid #2563EB;'>
                                <b style='color: #1E40AF; font-size: 16px;'>🚂 {train_num} - {train_name}</b><br>
                                <hr style='margin: 8px 0; border: 0; border-top: 1px solid #BFDBFE;'>
                                <b>⏰ Departure Time:</b> {dep_time} ({src})<br>
                                <b>⏰ Arrival Time:</b> {arr_time} ({dest})<br>
                                <b>📅 Date of Journey:</b> {date_string}
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # अगर क्लासेस की जानकारी अंदर उपलब्ध है तो उसे दिखाना
                            classes = train.get("classes", [])
                            if classes:
                                st.caption(f"💺 Available Classes: {', '.join(classes)}")
                            else:
                                st.caption("💡 Check Seat Availability endpoint to view live berth counts.")
                                
            except Exception as e:
                st.error(f"❌ Connection Error: {e}")
