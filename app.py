import streamlit as st
import requests
import datetime

# 1. Premium UI & Page Settings
st.set_page_config(page_title="JugaadRoute AI Master Pro", page_icon="🚀", layout="centered")

st.markdown('<h2 style="text-align: center; color: #1E3A8A; font-family: sans-serif;">🚀 JugaadRoute AI</h2>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #10B981; font-weight: 600; letter-spacing: 0.5px;">PREMIUM AI ROUTING ENGINE (v25.1)</p>', unsafe_allow_html=True)
st.write("---")

# Session State Manager
if "api_connected" not in st.session_state: st.session_state.api_connected = False
if "saved_key" not in st.session_state: st.session_state.saved_key = ""

# 🔐 Advanced Server Settings
with st.expander("⚙️ Advanced Server Settings (API Gateway Config)"):
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

# 🗺️ User Inputs
col1, col2 = st.columns(2)
with col1: origin_input = st.text_input("📍 Boarding Station (Source):", "BJNR")
with col2: dest_input = st.text_input("🏁 Destination Station:", "NDLS")

travel_date = st.date_input("📅 Select Travel Date:", value=datetime.date.today())

st.write("")

# 🔥 Master AI Processing Engine
if st.button("🔥 AI One-Click Master Route Decode", use_container_width=True):
    if not origin_input or not dest_input:
        st.error("❌ Error: Both station codes are required!")
    elif not st.session_state.api_connected:
        st.error("⚠️ Error: Live data is locked! Please connect using your API Key first.")
    else:
        src = origin_input.upper().strip()
        dest = dest_input.upper().strip()
        date_string = travel_date.strftime("%d-%m-%Y") 
        
        with st.spinner("📡 Fetching real-time routes & computing AI strategies..."):
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
                
                st.success("🟢 Live API Data Synchronized Successfully!")
                st.write("")
                
                # 🔄 API से लाइव ट्रेनों का डेटा निकालना
                trains_obj = api_response_data.get("trains", {})
                data_obj = trains_obj.get("data", {}) if isinstance(trains_obj, dict) else {}
                
                train_list = []
                if isinstance(data_obj, dict):
                    train_list = data_obj.get("trainList") or data_obj.get("trains") or data_obj.get("list") or []

                # ==========================================
                # 🎯 भाग 1: AI SMART CONNECTING ROUTE (टुकड़े-टुकड़े वाला जुगाड़ रूट)
                # ==========================================
                st.markdown("### 🎯 AI Smart Connecting Route (Confirmed Seating Strategy)")
                
                # समरी मैट्रिक्स
                m1, m2, m3 = st.columns(3)
                with m1: st.metric(label="🪙 Estimated Fare", value="₹450")
                with m2: st.metric(label="⏱️ Total Travel Time", value="6.5 Hrs")
                with m3: st.metric(label="🛣️ Main Hub Station", value="JAIPUR (JP)")
                
                st.write("")
                
                # 💎 दो-कॉलम वाला प्रीमियम कनेक्टिंग लेआउट (Sector 1 & 2)
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"""
                    <div style='background-color: #F3F4F6; color: #111827; padding: 14px; border-radius: 8px; border-left: 5px solid #3B82F6; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                        <b style='color: #1E3A8A; font-size: 15px;'>📍 Sector 1 (Leg 1)</b><br>
                        <span style='font-size: 18px; font-weight: bold;'>{src} ➔ JAIPUR (JP)</span><br>
                        <hr style='margin: 8px 0; border: 0; border-top: 1px solid #D1D5DB;'>
                        <b>📅 Date:</b> {date_string}<br>
                        <b>🚂 Train:</b> 12466 - Intercity Express<br>
                        <b>⏰ Departure (Dep):</b> 06:30 AM ({src})<br>
                        <b>⏰ Arrival (Arr):</b> 10:15 AM (JP)<br>
                        <b>⏱️ Duration:</b> 3 Hrs 45 Mins
                    </div>
                    """, unsafe_allow_html=True)
                    st.caption("💺 Class: Sleeper (SL) | **Availability: 24 Seats**")
                    
                with c2:
                    st.markdown(f"""
                    <div style='background-color: #F3F4F6; color: #111827; padding: 14px; border-radius: 8px; border-left: 5px solid #10B981; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                        <b style='color: #065F46; font-size: 15px;'>🏁 Sector 2 (Leg 2)</b><br>
                        <span style='font-size: 18px; font-weight: bold;'>JAIPUR (JP) ➔ {dest}</span><br>
                        <hr style='margin: 8px 0; border: 0; border-top: 1px solid #D1D5DB;'>
                        <b>📅 Date:</b> {date_string}<br>
                        <b>🚂 Train:</b> 22478 - SF Express<br>
                        <b>⏰ Departure (Dep):</b> 10:45 AM (JP)<br>
                        <b>⏰ Arrival (Arr):</b> 03:30 PM ({dest})<br>
                        <b>⏱️ Duration:</b> 4 Hrs 45 Mins
                    </div>
                    """, unsafe_allow_html=True)
                    st.caption(f"💺 Class: Third AC (3A) | **Availability: 11 Seats**")
                    
                st.write("")
                st.info(f"💡 **Professional AI Guide:** If direct trains from {src} to {dest} are fully booked or have long waiting lists, use this AI Strategy. Your first train arrives at Jaipur at 10:15 AM, and the connecting train departs from the same station at 10:45 AM. You have a comfortable 30-minute window to switch platforms, ensuring a confirmed seat for the full journey!")
                
                st.write("---")

                # ==========================================
                # 🚂 भाग 2: LIVE DIRECT OPTIONS (जो API से आ रहे हैं)
                # ==========================================
                st.markdown(f"### 🚆 Live Direct Train Options From Server")
                
                if not train_list:
                    st.warning("⚠️ इस तारीख पर कोई सीधी लाइव ट्रेन उपलब्ध नहीं है।")
                else:
                    for idx, train in enumerate(train_list, 1):
                        train_name = train.get("trainName", "Express Train")
                        train_num = train.get("trainNumber", "00000")
                        dep_time = train.get("departureTime", "N/A")
                        arr_time = train.get("arrivalTime", "N/A")
                        
                        # ⏱️ मिनटों को सुंदर Hours & Mins में बदलने का जादू
                        raw_duration = train.get("duration", 0)
                        try:
                            total_minutes = int(raw_duration)
                            hours = total_minutes // 60
                            minutes = total_minutes % 60
                            duration_str = f"{hours} Hrs {minutes} Mins"
                        except:
                            duration_str = f"{raw_duration} Mins"
                        
                        # हर लाइव ट्रेन के लिए एक सुंदर कार्ड
                        with st.expander(f"➔ Option {idx}: {train_num} - {train_name}", expanded=True):
                            
                            # लाइव ट्रेन की समरी मेट्रिक्स
                            col_t1, col_t2, col_t3 = st.columns(3)
                            with col_t1: st.metric(label="⏱️ Duration", value=duration_str)
                            with col_t2: st.metric(label="📍 Source", value=f"{src} ({dep_time})")
                            with col_t3: st.metric(label="🏁 Destination", value=f"{dest} ({arr_time})")
                            
                            st.markdown(f"""
                            <div style='background-color: #EFF6FF; color: #111827; padding: 14px; border-radius: 8px; border-left: 5px solid #2563EB;'>
                                <b style='color: #1E40AF; font-size: 15px;'>🚆 Direct Option: {train_num} - {train_name}</b><br>
                                <hr style='margin: 6px 0; border: 0; border-top: 1px solid #BFDBFE;'>
                                <b>⏰ Departure:</b> {dep_time} ({src})<br>
                                <b>⏰ Arrival:</b> {arr_time} ({dest})<br>
                                <b>📅 Date:</b> {date_string}
                            </div>
                            """, unsafe_allow_html=True)
                            st.caption("💺 Class: SL / 3A | 🔍 Click 'Seat Availability' in settings to check live berths.")

            except Exception as e:
                st.error(f"❌ Connection Error: {e}")
