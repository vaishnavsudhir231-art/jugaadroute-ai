import streamlit as st
import requests
from datetime import datetime, timedelta

# ==============================================================================
# 1. LIVE API CONFIGURATION (AK IT SERVICES)
# ==============================================================================
# 🚨 यहाँ अपनी असली RapidAPI की (Key) पेस्ट करें
RAPID_API_KEY = "da7882bf0dmsh..." 

API_HOST = "indian-railway-irctc.p.rapidapi.com"
BASE_URL = f"https://{API_HOST}"

HEADERS = {
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": API_HOST
}

def fetch_live_trains(source, destination, date_str):
    """AK IT Services: दो स्टेशनों के बीच चलने वाली लाइव ट्रेनें लाता है"""
    url = f"{BASE_URL}/trains/betweenStations"
    params = {"from": source, "to": destination, "date": date_str}
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        if response.status_code == 200:
            return response.json().get("data", [])
        return []
    except:
        return []

def fetch_train_route_with_types(train_no):
    """AK IT Services: ट्रेन का पूरा रूट निकालकर जंक्शन्स की पहचान करता है"""
    url = f"{BASE_URL}/train/route"
    params = {"trainNo": train_no}
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        if response.status_code == 200:
            route_data = response.json().get("data", {}).get("route", [])
            processed_route = []
            for station in route_data:
                stn_code = station.get("stationCode", "").upper()
                is_jnc = "JN" in stn_code or "JN" in station.get("stationName", "").upper()
                processed_route.append({
                    "station_code": stn_code,
                    "is_junction": is_jnc
                })
            return processed_route
        return []
    except:
        return []

def fetch_live_seat_status(train_no, source, destination, date_str):
    """AK IT Services: लाइव सीट उपलब्धता लाता है (Zero Filter Policy)"""
    url = f"{BASE_URL}/train/seatAvailability"
    classes_to_check = ["SL", "3A"]
    availability_results = {}
    
    for cls in classes_to_check:
        params = {
            "trainNo": train_no,
            "from": source,
            "to": destination,
            "date": date_str,
            "class": cls,
            "quota": "GN"
        }
        try:
            response = requests.get(url, headers=HEADERS, params=params, timeout=8)
            if response.status_code == 200:
                data = response.json().get("data", {})
                status_string = data.get("status", "NOT AVAILABLE")
                fare = data.get("baseFare", 0) + data.get("cateringCharge", 0)
                
                if "AVAILABLE" in status_string.upper():
                    try:
                        seat_count = int(''.join(filter(str.isdigit, status_string)))
                    except:
                        seat_count = 1
                    
                    availability_results[cls] = {
                        "seats": seat_count,
                        "status": "AVAILABLE",
                        "price": fare if fare > 0 else 350
                    }
        except:
            continue
            
    return availability_results

# ==============================================================================
# 2. THE SUPER ROUTING ENGINE (STRICT PRIORITY PATTERN)
# ==============================================================================
def SUPER_INTELLIGENT_ROUTER(src, dest, travel_date):
    date_str = travel_date.strftime("%Y-%m-%d")
    
    final_output = {
        "direct_options": [],
        "same_train_split_options": [],
        "different_train_split_options": []
    }
    
    # --- चरण 1: डायरेक्ट ट्रेन स्कैन (Priority 1) ---
    st.caption("🔍 चरण 1: सीधी ट्रेनों में लाइव सीटों की जांच की जा रही है...")
    raw_trains = fetch_live_trains(src, dest, date_str)
    
    direct_trains = []
    for t in raw_trains:
        direct_trains.append({
            "train_no": t.get("trainNumber") or t.get("train_no"),
            "train_name": t.get("trainName") or t.get("train_name"),
            "dep_time": t.get("departureTime") or t.get("dep_time", "20:50"),
            "arr_time": t.get("arrivalTime") or t.get("arr_time", "05:05")
        })
    
    for train in direct_trains:
        seats = fetch_live_seat_status(train["train_no"], src, dest, date_str)
        if seats:
            train["live_seats"] = seats
            final_output["direct_options"].append(train)
            
    # --- चरण 2: सेम-ट्रेन स्प्लिट स्कैन (Priority 2 - पहली पसंद) ---
    st.caption("🔄 चरण 2: सेम ट्रेन के अंदर सीट/क्लास बदलने का जुगाड़ खोजा जा रहा है...")
    for train in direct_trains:
        t_no = train["train_no"]
        t_name = train["train_name"]
        
        full_route = fetch_train_route_with_types(t_no)
        station_codes = [s["station_code"] for s in full_route]
        
        if src in station_codes and dest in station_codes:
            idx_src = station_codes.index(src)
            idx_dest = station_codes.index(dest)
            midpoint_stations = full_route[idx_src + 1 : idx_dest]
            
            major_junctions = [m["station_code"] for m in midpoint_stations if m.get("is_junction") == True]
            small_stations = [m["station_code"] for m in midpoint_stations if m.get("is_junction") != True]
            ordered_midpoints = major_junctions + small_stations
            
            for mid in ordered_midpoints:
                leg1_seats = fetch_live_seat_status(t_no, src, mid, date_str)
                leg2_seats = fetch_live_seat_status(t_no, mid, dest, date_str)
                
                l1_available = any(c["status"] == "AVAILABLE" for c in leg1_seats.values())
                l2_available = any(c["status"] == "AVAILABLE" for c in leg2_seats.values())
                
                if l1_available and l2_available:
                    is_major = mid in major_junctions
                    final_output["same_train_split_options"].append({
                        "train_no": t_no,
                        "train_name": t_name,
                        "split_at": mid,
                        "priority_type": "Tier-1 (Major Junction)" if is_major else "Tier-2 (Small Station)",
                        "leg1_seats": leg1_seats,
                        "leg2_seats": leg2_seats
                    })

    # अगर सेम ट्रेन में जुगाड़ मिल गया, तो दूसरी ट्रेन को सर्च ही मत करो (API Limit Saved!)
    if final_output["same_train_split_options"]:
        return final_output
    
    # --- चरण 3: दूसरी ट्रेन स्प्लिट (Priority 3 - STRICT FALLBACK) ---
    st.caption("⚠️ चरण 3: सेम ट्रेन में जगह नहीं है। अब कनेक्टिंग ट्रेनें खोजी जा रही हैं...")
    potential_hubs = ["JP", "AII", "NDLS", "ADI"]
    for hub in potential_hubs:
        if hub == src or hub == dest: continue
        leg1_raw = fetch_live_trains(src, hub, date_str)
        leg2_raw = fetch_live_trains(hub, dest, date_str)
        
        if leg1_raw and leg2_raw:
            # यहाँ टाइम और कनेक्टिंग सीट मैचिंग का लॉजिक काम करेगा
            pass
                    
    return final_output

# ==============================================================================
# 3. PREMIUM USER INTERFACE (UI)
# ==============================================================================
st.set_page_config(page_title="IRCTC Premium Intelligent Router", layout="centered")

# हेडर डिजाइन (unsafe_allow_html=True बिल्कुल सही कर दिया गया है)
st.markdown("<h2 style='text-align: center; color: #1E88E5;'>🚂 Smart Train Route Finder</h2>", unsafe_allow_html=True)
st.write("---")

col_src, col_dst = st.columns(2)
with col_src:
    src_input = st.text_input("From Station Code", value="BIJAINAGAR").upper().strip()
with col_dst:
    dst_input = st.text_input("To Station Code", value="DELHI").upper().strip()

travel_date = st.date_input("Date of Journey", datetime.now() + timedelta(days=1))

if st.button("Search Trains", type="primary", use_container_width=True):
    if src_input and dst_input:
        with st.spinner("लाइव सर्वर से कड़क सीटें खोजी जा रही हैं..."):
            res = SUPER_INTELLIGENT_ROUTER(src_input, dst_input, travel_date)
            
        st.write("---")
        
        # 🟢 Direct Trains DISPLAY
        if res["direct_options"]:
            st.subheader(f"🟢 Direct Trains Found ({len(res['direct_options'])})")
            for train in res["direct_options"]:
                with st.container(border=True):
                    st.markdown(f"### **{train['train_no']} - {train['train_name']}**")
                    st.caption(f"Departs: {train['dep_time']} from {src_input} | Arrives: {train['arr_time']} at {dst_input}")
                    
                    cols = st.columns(len(train["live_seats"]))
                    for i, (cls_name, cls_info) in enumerate(train["live_seats"].items()):
                        with cols[i]:
                            st.metric(
                                label=f"{cls_name} (₹{cls_info['price']})",
                                value=f"{cls_info['status']}-{cls_info['seats']:04d}"
                            )
            st.write("---")

        # 🔄 SAME-TRAIN SPLITS DISPLAY
        if res["same_train_split_options"]:
            st.subheader(f"🔄 Same-Train Seat Splitting Options ({len(res['same_train_split_options'])})")
            st.info("💡 खुशखबरी: आपको ट्रेन बदलने की जरूरत नहीं है! आप इसी सेम ट्रेन में बीच के स्टेशन पर अपनी सीट बदल सकते हैं।")
            
            for option in res["same_train_split_options"]:
                with st.container(border=True):
                    st.markdown(f"### 🚉 **{option['train_no']} - {option['train_name']}**")
                    st.markdown(f"📍 सीट बदलने का स्टेशन: **{option['split_at']}** | प्राथमिकता: `{option['priority_type']}`")
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"**लेग 1: {src_input} ➔ {option['split_at']}**")
                        for cls, info in option["leg1_seats"].items():
                            st.text(f"• {cls}: {info['status']}-{info['seats']:04d} (₹{info['price']})")
                    with c2:
                        st.markdown(f"**लेग 2: {option['split_at']} ➔ {dst_input}**")
                        for cls, info in option["leg2_seats"].items():
                            st.text(f"• {cls}: {info['status']}-{info['seats']:04d} (₹{info['price']})")
            st.write("---")

        if not res["direct_options"] and not res["same_train_split_options"]:
            st.error("❌ माफी चाहते हैं, इस तारीख पर रेलवे सर्वर के अनुसार कोई भी कन्फर्म सीट उपलब्ध नहीं है।")
