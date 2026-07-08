import streamlit as st
import requests
from datetime import datetime, timedelta

# ==============================================================================
# 1. API CONFIGURATION (अपनी लाइव एपीआई की डिटेल्स यहाँ भरें)
# ==============================================================================
API_URL = "https://your-indian-railways-api.com/api/v1"
API_HEADERS = {
    "X-RapidAPI-Key": "YOUR_REAL_API_KEY_HERE",
    "X-RapidAPI-Host": "your-railway-api-host.com"
}

def fetch_live_trains(source, destination, date_str):
    """पैटर्न: लाइव एपीआई से दो स्टेशनों के बीच की सभी ट्रेनें लाना"""
    if source == "BIJAINAGAR" and destination == "DELHI":
        return [{"train_no": "20474", "train_name": "CHETAK EXPRESS", "dep_time": "20:50", "arr_time": "05:05", "days": "M T W T F S S"}]
    return [] 

def fetch_train_route_with_types(train_no):
    """पैटर्न: ट्रेन का पूरा लाइव रूट निकालना (स्टेशन कोड और उसके प्रकार के साथ)"""
    if train_no == "20474":
        return [
            {"station_code": "BIJAINAGAR", "is_junction": False},
            {"station_code": "AJMER", "is_junction": True},
            {"station_code": "JAIPUR", "is_junction": True},
            {"station_code": "DELHI", "is_junction": True}
        ]
    return []

def fetch_live_seat_status(train_no, source, destination, date_str):
    """पैटर्न: लाइव सीट काउंट लाना (जीरो फिल्टर पॉलिसी: 1 सीट भी होगी तो उठाएगा)"""
    if train_no == "20474" and source == "BIJAINAGAR" and destination == "DELHI":
        return {"SL": {"seats": 3, "status": "AVAILABLE", "price": 310}, "3A": {"seats": 9, "status": "AVAILABLE", "price": 785}}
    return {"SL": {"seats": 15, "status": "AVAILABLE", "price": 200}, "3A": {"seats": 8, "status": "AVAILABLE", "price": 600}}

# ==============================================================================
# 2. THE SUPER ROUTING ENGINE (MERGED LOGIC)
# ==============================================================================
def SUPER_INTELLIGENT_ROUTER(src, dest, travel_date):
    date_str = travel_date.strftime("%Y-%m-%d")
    
    final_output = {
        "direct_options": [],
        "same_train_split_options": [],
        "different_train_split_options": [],
        "api_saved_log": "Full Scan Run"
    }
    
    # --- चरण 1: डायरेक्ट ट्रेन स्कैन (Priority 1) ---
    direct_trains = fetch_live_trains(src, dest, date_str)
    for train in direct_trains:
        seats = fetch_live_seat_status(train["train_no"], src, dest, date_str)
        if any(cls["seats"] >= 1 and cls["status"] == "AVAILABLE" for cls in seats.values()):
            train["live_seats"] = seats
            final_output["direct_options"].append(train)
            
    # --- चरण 2: सेम-ट्रेन स्प्लिट स्कैन (Priority 2 - पहली पसंद) ---
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
                
                l1_available = any(c["seats"] >= 1 and c["status"] == "AVAILABLE" for c in leg1_seats.values())
                l2_available = any(c["seats"] >= 1 and c["status"] == "AVAILABLE" for c in leg2_seats.values())
                
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

    if final_output["same_train_split_options"]:
        final_output["api_saved_log"] = "Same train options found. Skipped connecting trains to save API limits."
        return final_output
    
    # --- चरण 3: दूसरी ट्रेन स्प्लिट (Priority 3 - STRICT FALLBACK) ---
    potential_hubs = ["JP", "AII", "NDLS", "ADI"]
    for hub in potential_hubs:
        if hub == src or hub == dest: continue
        leg1_trains = fetch_live_trains(src, hub, date_str)
        leg2_trains = fetch_live_trains(hub, dest, date_str)
        
        for t1 in leg1_trains:
            for t2 in leg2_trains:
                fmt = "%H:%M"
                try:
                    t1_arr = datetime.strptime(t1["arr_time"], fmt)
                    t2_dep = datetime.strptime(t2["dep_time"], fmt)
                    if t2_dep >= (t1_arr + timedelta(minutes=30)):
                        t1_seats = fetch_live_seat_status(t1["train_no"], src, hub, date_str)
                        t2_seats = fetch_live_seat_status(t2["train_no"], hub, dest, date_str)
                        if any(c["seats"] >= 1 for c in t1_seats.values()) and any(c["seats"] >= 1 for c in t2_seats.values()):
                            final_output["different_train_split_options"].append({
                                "transit_hub": hub, "t1": t1, "t2": t2, "t1_seats": t1_seats, "t2_seats": t2_seats
                            })
                except ValueError:
                    continue
                    
    return final_output

# ==============================================================================
# 3. PREMIUM USER INTERFACE (UI)
# ==============================================================================
st.set_page_config(page_title="IRCTC Premium Intelligent Router", layout="centered")

# हेडर डिजाइन - यहाँ पर 'unsafe_allow_html=True' को सही कर दिया गया है
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
        with st.spinner("लाइव डेटा ग्रिड स्कैन किया जा रहा है..."):
            res = SUPER_INTELLIGENT_ROUTER(src_input, dst_input, travel_date)
            
        st.write("---")
        
        # 🟢 DISPLAY DIRECT TRAINS
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

        # 🔄 DISPLAY SAME-TRAIN SPLITS
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

        # 🔀 DISPLAY DIFFERENT TRAIN SPLITS
        if res["different_train_split_options"]:
            st.subheader(f"🔀 Alternate Connecting Routes ({len(res['different_train_split_options'])})")
            for route in res["different_train_split_options"]:
                with st.container(border=True):
                    st.markdown(f"### 🔀 Route Via: **{route['transit_hub']}**")
                    
                    col_l1, col_l2 = st.columns(2)
                    with col_l1:
                        st.markdown(f"**ट्रेन 1:** {route['t1']['train_name']} ({route['t1']['train_no']})")
                        st.caption(f"{src_input} ({route['t1']['dep_time']}) ➔ {route['transit_hub']} ({route['t1']['arr_time']})")
                    with col_l2:
                        st.markdown(f"**ट्रेन 2:** {route['t2']['train_name']} ({route['t2']['train_no']})")
                        st.caption(f"{route['transit_hub']} ({route['t2']['dep_time']}) ➔ {dst_input} ({route['t2']['arr_time']})")

        if not res["direct_options"] and not res["same_train_split_options"] and not res["different_train_split_options"]:
            st.error("❌ माफी चाहते हैं, इस तारीख पर किसी भी रूट या ट्रेन में कोई भी सीट उपलब्ध नहीं है।")
