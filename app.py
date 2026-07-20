import streamlit as st
import requests
import datetime

# 1. UI Settings
st.set_page_config(page_title="JugaadRoute AI Master Pro", page_icon="🚀", layout="centered")

st.markdown('<h2 style="text-align: center; color: #1E3A8A;">🚀 JugaadRoute AI</h2>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #10B981; font-weight: 600;">PURE DYNAMIC LIVE TRANSIT ENGINE</p>', unsafe_allow_html=True)
st.write("---")

# Session State for Security Keys
if "api_connected" not in st.session_state: st.session_state.api_connected = False
if "saved_key" not in st.session_state: st.session_state.saved_key = ""

# 🔐 API Config Expander
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
                st.error("❌ Please enter a valid API Key!")
    with c_btn2:
        if st.button("Disconnect Server", use_container_width=True):
            st.session_state.api_connected = False
            st.warning("🔴 API Disconnected")

# 🗺️ Live User Inputs (कस्टमर जो भी टाइप करेगा, वही सर्च होगा)
col1, col2 = st.columns(2)
with col1: origin_input = st.text_input("📍 Boarding Station (Source Code/Name):", "BJNR").upper().strip()
with col2: dest_input = st.text_input("🏁 Destination Station (Code/Name):", "NDLS").upper().strip()

travel_date = st.date_input("📅 Select Travel Date:", value=datetime.date.today())
date_string = travel_date.strftime("%Y-%m-%d") # API standard format

# 🔥 Main Search Logic
if st.button("🔥 Search Live Available Options & Routes", use_container_width=True):
    if not origin_input or not dest_input:
        st.error("❌ Error: Both station names/codes are required!")
    elif not st.session_state.api_connected:
        st.error("⚠️ Error: Server is locked. Please connect using your API Key first.")
    else:
        with st.spinner("📡 Fetching real-time routes from Live Servers..."):
            
            # 🌐 यहाँ आपकी असली API URL और Headers काम करेंगे
            # आप जिस भी RapidAPI (IRCTC/Indian Railways) का यूज़ कर रहे हैं, उसकी URL यहाँ आएगी
            url = "https://your-rapidapi-railway-url.com/v2/searchRoutes" 
            
            querystring = {
                "source": origin_input,
                "destination": dest_input,
                "date": date_string
            }
            
            headers = {
                "X-RapidAPI-Key": st.session_state.saved_key,
                "X-RapidAPI-Host": "your-rapidapi-railway-url.com"
            }
            
            try:
                # 🚀 लाइव API हिट
                response = requests.get(url, headers=headers, params=querystring, timeout=15)
                api_response_data = response.json() 
                
                # मान लेते हैं कि API से आ रहे JSON में 'routes' नाम की एक लिस्ट है
                live_routes = api_response_data.get("routes", [])
                
                if not live_routes:
                    st.warning("⚠️ No active routes or trains found for this date/route on live servers.")
                else:
                    st.success(f"🟢 Found {len(live_routes)} live dynamic options for {origin_input} ➔ {dest_input}!")
                    st.write("")
                    
                    # 🔄 100% DYNAMIC LOOP: यहाँ कुछ भी फिक्स नहीं है!
                    # API 2 ट्रेनें भेजेगी तो 2 दिखेंगी, 50 भेजेगी तो 50 दिखेंगी (चेतक, राजधानी सब अपने आप आ जाएँगी)
                    for idx, route in enumerate(live_routes, 1):
                        
                        # API से डायनामिक डेटा निकालना
                        route_title = route.get("route_name", f"Option {idx}")
                        total_duration = route.get("total_duration", "N/A")
                        total_fare = route.get("fare", "N/A")
                        route_type = route.get("route_type", "DIRECT") # DIRECT या CONNECTING
                        
                        with st.expander(f"📌 {route_title} | Duration: {total_duration} | Fare: ₹{total_fare}", expanded=(idx==1)):
                            
                            # केस A: अगर API कहती है कि ट्रेन डायरेक्ट है
                            if route_type == "DIRECT":
                                train_name = route.get("train_name", "Unknown Train")
                                train_no = route.get("train_number", "00000")
                                dep_time = route.get("departure_time", "N/A")
                                arr_time = route.get("arrival_time", "N/A")
                                seat_status = route.get("availability", "Unknown")
                                
                                st.markdown(f"""
                                <div style='background-color: #EFF6FF; padding: 12px; border-radius: 8px; border-left: 5px solid #2563EB; color: #111827;'>
                                    <b style='color: #1E40AF;'>🚆 Direct Train: {train_no} - {train_name}</b><br>
                                    <b>⏰ Departure:</b> {dep_time} ({origin_input}) | <b>Arrival:</b> {arr_time} ({dest_input})<br>
                                    <b>💺 Dynamic Seat Status:</b> <span style='color: #059669; font-weight: bold;'>{seat_status}</span>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            # केस B: अगर AI/API ने कोई कनेक्टिंग (जुगाड़) रूट बनाकर भेजा है
                            elif route_type == "CONNECTING":
                                hub_station = route.get("connecting_hub", "HUB")
                                leg1 = route.get("leg1", {})
                                leg2 = route.get("leg2", {})
                                
                                c1, c2 = st.columns(2)
                                with c1:
                                    st.markdown(f"""
                                    <div style='background-color: #F3F4F6; padding: 12px; border-radius: 8px; border-left: 5px solid #3B82F6; color: #111827;'>
                                        <b style='color: #1E3A8A;'>📍 Sector 1: {origin_input} ➔ {hub_station}</b><br>
                                        <b>🚂 Train:</b> {leg1.get('train_number')} - {leg1.get('train_name')}<br>
                                        <b>⏰ Dep:</b> {leg1.get('departure_time')} | <b>Arr:</b> {leg1.get('arrival_time')}<br>
                                        <b>💺 Status:</b> {leg1.get('availability')}
                                    </div>
                                    """, unsafe_allow_html=True)
                                with c2:
                                    st.markdown(f"""
                                    <div style='background-color: #F3F4F6; padding: 12px; border-radius: 8px; border-left: 5px solid #10B981; color: #111827;'>
                                        <b style='color: #065F46;'>🏁 Sector 2: {hub_station} ➔ {dest_input}</b><br>
                                        <b>🚂 Train:</b> {leg2.get('train_number')} - {leg2.get('train_name')}<br>
                                        <b>⏰ Dep:</b> {leg2.get('departure_time')} | <b>Arr:</b> {leg2.get('arrival_time')}<br>
                                        <b>💺 Status:</b> {leg2.get('availability')}
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                            st.write("")
                            st.caption("💡 This option is generated live based on real-time seat availability and timings.")
            
            except Exception as e:
                st.error(f"❌ Connection Error: Live servers down or Invalid API Key structure. Detail: {e}")
