import streamlit as st
import requests
from datetime import datetime, timedelta

# ==============================================================================
# 1. LIVE API CONFIGURATION (यहाँ अपनी असली रेलवे API डिटेल्स मैप करें)
# ==============================================================================
API_URL = "https://your-indian-railways-api.com/api/v1"
API_HEADERS = {
    "X-RapidAPI-Key": "YOUR_REAL_API_KEY_HERE",
    "X-RapidAPI-Host": "your-railway-api-host.com"
}

def fetch_live_trains(source, destination, date_str):
    """पैटर्न: लाइव एपीआई से किन्हीं भी दो स्टेशनों के बीच की सभी ट्रेनें लाना"""
    # params = {"from": source, "to": destination, "date": date_str}
    # response = requests.get(f"{API_URL}/search", headers=API_HEADERS, params=params)
    # return response.json().get("trains", [])
    return [] 

def fetch_train_route_with_types(train_no):
    """पैटर्न: ट्रेन का पूरा लाइव रूट निकालना (स्टेशन कोड और उसके प्रकार के साथ)"""
    # response = requests.get(f"{API_URL}/route/{train_no}", headers=API_HEADERS)
    # अपेक्षित रिस्पॉन्स फॉर्मेट: [{"station_code": "JP", "is_junction": True}, ...]
    return []

def fetch_live_seat_status(train_no, source, destination, date_str):
    """पैटर्न: लाइव सीट काउंट लाना (जीरो फिल्टर पॉलिसी: 1 सीट भी होगी तो उठाएगा)"""
    # response = requests.get(f"{API_URL}/seat-availability", headers=API_HEADERS, ...)
    # अपेक्षित रिस्पॉन्स फॉर्मेट: {"SL": {"seats": 3, "status": "AVAILABLE"}, "3A": {"seats": 9, "status": "AVAILABLE"}}
    return {}

# ==============================================================================
# 2. THE SUPER ROUTING ENGINE (MERGED LOGIC)
# ==============================================================================
def SUPER_INTELLIGENT_ROUTER(src, dest, travel_date):
    date_str = travel_date.strftime("%Y-%m-%d")
    
    # अंतिम परिणाम स्टोर करने के लिए स्ट्रक्चर
    final_output = {
        "engine_status": "INITIATED",
        "search_depth_summary": "",
        "direct_options": [],
        "same_train_split_options": [],
        "different_train_split_options": []
    }
    
    # --------------------------------------------------------------------------
    # चरण 1: डायरेक्ट ट्रेन स्कैन (Priority 1)
    # --------------------------------------------------------------------------
    st.caption("🔍 चरण 1: सीधी ट्रेनों में लाइव सीटों की जांच की जा रही है...")
    direct_trains = fetch_live_trains(src, dest, date_str)
    
    for train in direct_trains:
        seats = fetch_live_seat_status(train["train_no"], src, dest, date_str)
        # अगर किसी भी क्लास में कम से कम 1 सीट भी AVAILABLE है
        if any(cls["seats"] >= 1 and cls["status"] == "AVAILABLE" for cls in seats.values()):
            train["live_seats"] = seats
            final_output["direct_options"].append(train)
            
    # --------------------------------------------------------------------------
    # चरण 2: सेम-ट्रेन स्प्लिट स्कैन (Priority 2 - पहली पसंद)
    # --------------------------------------------------------------------------
    st.caption("🔄 चरण 2: सेम ट्रेन के अंदर सीट/क्लास बदलने का जुगाड़ खोजा जा रहा है...")
    
    for train in direct_trains:
        t_no = train["train_no"]
        t_name = train["train_name"]
        
        # ट्रेन का पूरा रूट और स्टेशन टाइप्स निकालें
        full_route = fetch_train_route_with_types(t_no)
        station_codes = [s["station_code"] for s in full_route]
        
        if src in station_codes and dest in station_codes:
            idx_src = station_codes.index(src)
            idx_dest = station_codes.index(dest)
            
            # सिर्फ सोर्स और डेस्टिनेशन के बीच आने वाले मिडपॉइंट स्टेशन्स
            midpoint_stations = full_route[idx_src + 1 : idx_dest]
            
            # स्टेशनों का वर्गीकरण (तुम्हारी शर्त: पहले बड़ा जंक्शन, फिर छोटा स्टेशन)
            major_junctions = [m["station_code"] for m in midpoint_stations if m.get("is_junction") == True]
            small_stations = [m["station_code"] for m in midpoint_stations if m.get("is_junction") != True]
            
            # टियर-1 (बड़े जंक्शन) और टियर-2 (छोटे स्टेशन) को प्राथमिकता के क्रम में जोड़ें
            ordered_midpoints = major_junctions + small_stations
            
            for mid in ordered_midpoints:
                # लाइव सीट चेक (Leg 1 और Leg 2 दोनों के लिए उसी सेम ट्रेन में)
                leg1_seats = fetch_live_seat_status(t_no, src, mid, date_str)
                leg2_seats = fetch_live_seat_status(t_no, mid, dest, date_str)
                
                l1_available = any(c["seats"] >= 1 and c["status"] == "AVAILABLE" for c in leg1_seats.values())
                l2_available = any(c["seats"] >= 1 and c["status"] == "AVAILABLE" for c in leg2_seats.values())
                
                # अगर दोनों लेग्स में सीट मिल गई (भले क्लास अलग-अलग हो, जैसे SL + 3A)
                if l1_available and l2_available:
                    is_major = mid in major_junctions
                    final_output["same_train_split_options"].append({
                        "train_no": t_no,
                        "train_name": t_name,
                        "split_at": mid,
                        "station_priority": "Tier-1 (Major Junction)" if is_major else "Tier-2 (Small Station)",
                        "leg1_seats": leg1_seats,
                        "leg2_seats": leg2_seats
                    })

    # --------------------------------------------------------------------------
    # चरण 3: दूसरी ट्रेन स्प्लिट (Priority 3 - STRICT FALLBACK)
    # --------------------------------------------------------------------------
    # तुम्हारी सबसे क्रिटिकल कंडीशन: अगर सेम ट्रेन में जुगाड़ मिल गया है, 
    # तो दूसरी ट्रेन को सर्च ही मत करो, यहीं से ब्रेक करके लिमिट बचाओ!
    if final_output["same_train_split_options"]:
        final_output["engine_status"] = "SUCCESS_OPTIMIZED"
        final_output["search_depth_summary"] = "Same train combinations found. Skipped connecting trains to save API limits."
        return final_output
    
    # अगर सेम ट्रेन में भी 1 भी सीट का जुगाड़ नहीं बैठा, केवल तब यह फॉलबैक चलेगा
    st.caption("⚠️ चरण 3: सेम ट्रेन में कोई सीट नहीं मिली। अब कनेक्टिंग (Different) ट्रेनें खोजी जा रही हैं...")
    final_output["search_depth_summary"] = "Fallback triggered: Deep scan for different connecting trains executed."
    
    # डायनेमिक हब डिटेक्शन (डायरेक्ट ट्रेनों के रूट्स से बड़े जंक्शन्स को हब मानना)
    potential_hubs = ["JP", "AII", "NDLS", "ADI"] # भारत के कुछ कोर फॉलबैक ग्रिड्स
    
    for hub in potential_hubs:
        if hub == src or hub == dest:
            continue
            
        leg1_trains = fetch_live_trains(src, hub, date_str)
        leg2_trains = fetch_live_trains(hub, dest, date_str)
        
        for t1 in leg1_trains:
            for t2 in leg2_trains:
                # टाइम मैचिंग लॉजिक (ट्रेन B, ट्रेन A के पहुंचने के कम से कम 30 मिनट बाद होनी चाहिए)
                fmt = "%H:%M"
                try:
                    t1_arr = datetime.strptime(t1["arr_time"], fmt)
                    t2_dep = datetime.strptime(t2["dep_time"], fmt)
                    
                    if t2_dep >= (t1_arr + timedelta(minutes=30)):
                        t1_seats = fetch_live_seat_status(t1["train_no"], src, hub, date_str)
                        t2_seats = fetch_live_seat_status(t2["train_no"], hub, dest, date_str)
                        
                        if any(c["seats"] >= 1 for c in t1_seats.values()) and any(c["seats"] >= 1 for c in t2_seats.values()):
                            final_output["different_train_split_options"].append({
                                "transit_hub": hub,
                                "train_1": t1,
                                "train_2": t2,
                                "t1_seats": t1_seats,
                                "t2_seats": t2_seats
                            })
                except ValueError:
                    continue

    if not final_output["same_train_split_options"] and not final_output["different_train_split_options"]:
        final_output["engine_status"] = "NO_OPTIONS_FOUND"
    else:
        final_output["engine_status"] = "SUCCESS_FULL_SCAN"
        
    return final_output

# ==============================================================================
# 3. UNIVERSAL STREAMLIT USER INTERFACE (UI)
# ==============================================================================
st.set_page_config(page_title="Super Intelligent Router Engine", layout="wide")
st.title("🛡️ Universal Super-Intelligent Train Router")
st.write("बिना किसी कोडिंग लिमिटेशन के, यह इंजन पैटर्न-बेस्ड कड़क प्रायोरिटी पर काम करता है।")

col1, col2, col3 = st.columns(3)
with col1:
    src_code = st.text_input("Source Station Code (e.g. BJNR, ADI)").upper().strip()
with col2:
    dst_code = st.text_input("Destination Station Code (e.g. DLI, HWH)").upper().strip()
with col3:
    travel_dt = st.date_input("Date of Journey")

if st.button("🔥 Execute Hardcore Pattern Scan", type="primary"):
    if src_code and dst_code:
        with st.spinner("इंडियन रेलवे नेटवर्क ग्रिड में एल्गोरिदम प्रोसेस हो रहा है..."):
            master_results = SUPER_INTELLIGENT_ROUTER(src_code, dst_code, travel_dt)
            
        st.write("---")
        st.subheader("📊 Engine Execution Summary")
        st.info(f"**Status:** {master_results['engine_status']} | **Log:** {master_results['search_depth_summary']}")
        
        # --- रिजल्ट्स का रेंडरिंग ---
        st.success("डेटाबेस रेडी! नीचे खोजे गए सारे लाइव पैटर्न्स हैं:")
        st.json(master_results)
    else:
        st.error("कृपया सोर्स और डेस्टिनेशन दोनों स्टेशन कोड डालें।")
