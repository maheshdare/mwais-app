import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import time

# Page configuration
st.set_page_config(
    page_title="MWAIS - Missing Women Alert System",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with better styling
st.markdown("""
<style>
    /* Main colors */
    :root {
        --primary: #667eea;
        --secondary: #764ba2;
        --critical: #e74c3c;
        --high: #f39c12;
        --medium: #27ae60;
        --low: #3498db;
    }
    
    /* Dark theme */
    .main {
        padding-top: 2rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 42px;
        font-weight: 700;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 12px;
        text-transform: uppercase;
        opacity: 0.9;
        letter-spacing: 1px;
    }
    
    /* Case cards */
    .case-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s;
    }
    
    .case-card:hover {
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    .case-critical { border-left-color: #e74c3c; }
    .case-high { border-left-color: #f39c12; }
    .case-medium { border-left-color: #27ae60; }
    
    /* Priority badge */
    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .badge-critical { background: #fadbd8; color: #c0392b; }
    .badge-high { background: #fdebd0; color: #d68910; }
    .badge-medium { background: #d5f4e6; color: #196f3d; }
    .badge-low { background: #d6eaf8; color: #1b4965; }
    
    /* Alerts */
    .alert-box {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
    }
    
    /* Stats section */
    .stat-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        margin-bottom: 20px;
    }
    
    /* Timeline */
    .timeline {
        position: relative;
        padding: 20px 0;
    }
    
    .timeline-item {
        padding: 15px;
        margin-bottom: 10px;
        background: #f8f9fa;
        border-radius: 8px;
        border-left: 3px solid #667eea;
        padding-left: 20px;
    }
    
    .timeline-date {
        font-size: 12px;
        color: #667eea;
        font-weight: 700;
        text-transform: uppercase;
    }
    
    .timeline-title {
        font-size: 14px;
        font-weight: 600;
        color: #2c3e50;
        margin-top: 5px;
    }
    
    /* Form styling */
    .form-section {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
    }
    
    /* Success message */
    .success-box {
        background: #d5f4e6;
        border-left: 4px solid #27ae60;
        padding: 15px;
        border-radius: 8px;
        color: #196f3d;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = '📊 Dashboard'

# Sidebar Navigation
with st.sidebar:
    st.image("https://img.icons8.com/color/256/000000/emergency-call.png", width=80)
    st.title("🚨 MWAIS")
    st.write("**Missing Women Alert**")
    st.write("**& Investigation System**")
    st.write("---")
    
    # Navigation menu
    st.session_state.page = st.radio(
        "📍 Navigation",
        ["📊 Dashboard", "🔍 Search Cases", "📝 Register Case", "📁 Case Details", 
         "📈 Analytics", "🤖 AI Features", "🗺️ Hotspots", "📱 Media Campaign", 
         "👥 Officers", "⚙️ Settings"],
        index=0,
        key="nav_radio"
    )
    
    st.write("---")
    st.write("**👤 Current Officer**")
    st.write("🔹 **Name:** Inspector Ramesh Kumar")
    st.write("🔹 **Rank:** Inspector")
    st.write("🔹 **Station:** Mumbai Central")
    st.write("🔹 **Cases:** 28 active")
    st.write("🔹 **Resolved:** 18 cases")
    st.write("🔹 **Success Rate:** 64%")
    
    st.write("---")
    
    if st.button("🔔 Notifications (3)", use_container_width=True):
        st.info("✅ Shreya Patel case escalated to Commissioner\n\n⚠️ New evidence in Maya Singh case\n\n📍 Hotspot alert in Pune region")
    
    if st.button("🚨 SOS Alert", use_container_width=True):
        st.warning("CRITICAL ALERT MODE - Notify all units")

# Generate sample data
@st.cache_data
def generate_cases():
    cases = [
        {"id": "CASE-001", "name": "Shreya Patel", "age": 12, "missing_days": 548, "priority": "CRITICAL", 
         "location": "Pune", "status": "Escalated", "photos": 3, "cctv": 2, "assigned_to": "You", 
         "last_update": "2024-01-16 09:30", "risk_score": 96},
        {"id": "CASE-002", "name": "Anjali Desai", "age": 16, "missing_days": 540, "priority": "HIGH", 
         "location": "Mumbai", "status": "Investigation", "photos": 2, "cctv": 0, "assigned_to": "Sr. Inspector Sharma",
         "last_update": "2024-01-15 14:20", "risk_score": 82},
        {"id": "CASE-003", "name": "Maya Singh", "age": 14, "missing_days": 62, "priority": "HIGH", 
         "location": "Delhi", "status": "Investigation", "photos": 4, "cctv": 1, "assigned_to": "You",
         "last_update": "2024-01-16 11:45", "risk_score": 75},
        {"id": "CASE-004", "name": "Priya Sharma", "age": 15, "missing_days": 45, "priority": "MEDIUM", 
         "location": "Bangalore", "status": "Registered", "photos": 2, "cctv": 0, "assigned_to": "Inspector Verma",
         "last_update": "2024-01-14 08:15", "risk_score": 62},
        {"id": "CASE-005", "name": "Divya Reddy", "age": 13, "missing_days": 8, "priority": "CRITICAL", 
         "location": "Hyderabad", "status": "Registered", "photos": 3, "cctv": 0, "assigned_to": "You",
         "last_update": "2024-01-16 16:00", "risk_score": 89},
    ]
    return pd.DataFrame(cases)

def get_priority_color(priority):
    colors = {
        "CRITICAL": "#e74c3c", 
        "HIGH": "#f39c12", 
        "MEDIUM": "#27ae60", 
        "LOW": "#3498db"
    }
    return colors.get(priority, "#95a5a6")

def get_priority_badge_class(priority):
    classes = {
        "CRITICAL": "badge-critical",
        "HIGH": "badge-high",
        "MEDIUM": "badge-medium",
        "LOW": "badge-low"
    }
    return classes.get(priority, "badge-low")

# ============ DASHBOARD PAGE ============
if st.session_state.page == "📊 Dashboard":
    st.title("🚨 MWAIS Dashboard")
    st.write("Real-time case monitoring and smart alerts")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="🔴 High Priority", value="12", delta="+2 this week", delta_color="inverse")
    with col2:
        st.metric(label="📋 Active Cases", value="28", delta="-1 resolved")
    with col3:
        st.metric(label="✅ Resolved Cases", value="89", delta="+3 this week")
    with col4:
        st.metric(label="⏱️ Avg Resolution", value="14 mo", delta="-2 months faster", delta_color="inverse")
    
    st.markdown("---")
    
    # Alerts Section
    st.subheader("🚨 Critical Alerts")
    
    alert_col1, alert_col2 = st.columns(2)
    
    with alert_col1:
        st.markdown("""
        <div class="alert-box">
            <strong>⚠️ CRITICAL: Shreya Patel</strong><br/>
            Missing 548 days • Age 12 • Pune<br/>
            Status: Just Escalated to Commissioner<br/>
            <strong>Action Required:</strong> Await state-level task force coordination
        </div>
        """, unsafe_allow_html=True)
    
    with alert_col2:
        st.markdown("""
        <div class="alert-box">
            <strong>⚠️ CRITICAL: Divya Reddy</strong><br/>
            Missing 8 days • Age 13 • Hyderabad<br/>
            Status: Just Registered<br/>
            <strong>Action Required:</strong> Immediate escalation recommended (Risk Score: 89/100)
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Your Active Cases
    st.subheader("👤 Your Active Cases (4)")
    
    df_cases = generate_cases()
    your_cases = df_cases[df_cases['assigned_to'] == 'You']
    
    for idx, case in your_cases.iterrows():
        col1, col2, col3, col4 = st.columns([2, 1.5, 1, 1])
        
        with col1:
            color = get_priority_color(case['priority'])
            priority_class = get_priority_badge_class(case['priority'])
            st.markdown(f"""
            <div class="case-card case-{case['priority'].lower()}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <b style="font-size: 16px;">{case['name']}, {case['age']} yrs</b><br/>
                        <span style="color: #7f8c8d; font-size: 13px;">Missing: {case['missing_days']} days • {case['location']}</span><br/>
                        <span style="color: #7f8c8d; font-size: 12px;">Last update: {case['last_update']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"<span class='badge {priority_class}'>{case['priority']}</span>", unsafe_allow_html=True)
            st.write(f"Score: {case['risk_score']}/100")
        
        with col3:
            st.write(f"📷 {case['photos']}")
            st.write(f"📹 {case['cctv']}")
        
        with col4:
            if st.button("View", key=f"view_case_{idx}", use_container_width=True):
                st.session_state.selected_case_id = case['id']
                st.session_state.page = "📁 Case Details"
                st.rerun()
            if st.button("Edit", key=f"edit_case_{idx}", use_container_width=True):
                st.info(f"Editing {case['name']}'s case...")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Cases by Priority")
        priority_data = pd.DataFrame({
            "Priority": ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
            "Count": [12, 16, 13, 8],
            "Color": ["#e74c3c", "#f39c12", "#27ae60", "#3498db"]
        })
        fig = px.pie(
            priority_data,
            values="Count",
            names="Priority",
            color="Priority",
            color_discrete_map={
                "CRITICAL": "#e74c3c",
                "HIGH": "#f39c12",
                "MEDIUM": "#27ae60",
                "LOW": "#3498db"
            }
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Cases by Status")
        status_data = pd.DataFrame({
            "Status": ["Registered", "Investigation", "Escalated", "Resolved"],
            "Count": [7, 9, 5, 7]
        })
        fig = px.bar(
            status_data,
            x="Status",
            y="Count",
            color="Status",
            color_discrete_sequence=["#3498db", "#f39c12", "#e74c3c", "#27ae60"]
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌍 Geographic Distribution")
        location_data = pd.DataFrame({
            "Location": ["Maharashtra", "Karnataka", "Tamil Nadu", "Telangana", "Others"],
            "Cases": [28, 15, 12, 10, 91]
        })
        fig = px.bar(location_data, x="Location", y="Cases", color="Cases", 
                    color_continuous_scale="Blues")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📅 Missing Duration")
        duration_data = pd.DataFrame({
            "Duration": ["0-7 days", "7-30 days", "1-6 months", "6-12 months", ">1 year"],
            "Count": [12, 18, 35, 28, 63]
        })
        fig = px.line(duration_data, x="Duration", y="Count", markers=True)
        st.plotly_chart(fig, use_container_width=True)

# ============ SEARCH CASES PAGE ============
elif st.session_state.page == "🔍 Search Cases":
    st.title("🔍 Search Cases")
    st.write("Find cases using advanced filters and full-text search")
    
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        search_query = st.text_input("🔍 Search by name, age, location, case ID...", placeholder="e.g., Shreya Patel or CASE-001")
    with col2:
        if st.button("🔎 Search", use_container_width=True):
            st.info("Searching across all cases...")
            time.sleep(0.5)
    with col3:
        if st.button("🔄 Reset", use_container_width=True):
            st.success("Filters reset")
    
    st.markdown("---")
    
    st.subheader("⚙️ Filters")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        age_group = st.selectbox("Age Group", ["All", "Below 10", "10-14", "15-18", "18+"])
    with col2:
        status_filter = st.selectbox("Status", ["All", "Registered", "Investigation", "Escalated", "Resolved"])
    with col3:
        priority_filter = st.selectbox("Priority", ["All", "CRITICAL", "HIGH", "MEDIUM", "LOW"])
    with col4:
        duration = st.selectbox("Missing Duration", ["All", "0-7 days", "7-30 days", "1-6 months", "6-12 months", "1+ years"])
    
    st.markdown("---")
    
    st.subheader("📋 Search Results (5 cases found)")
    
    df_cases = generate_cases()
    for idx, case in df_cases.iterrows():
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            color = get_priority_color(case['priority'])
            st.markdown(f"""
            <div class="case-card case-{case['priority'].lower()}">
                <b>{case['name']}, {case['age']} years old</b> | 🏘️ {case['location']}<br/>
                <span style="color: #7f8c8d; font-size: 12px;">Missing: {case['missing_days']} days • Risk Score: {case['risk_score']}/100</span>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            priority_class = get_priority_badge_class(case['priority'])
            st.markdown(f"<span class='badge {priority_class}'>{case['priority']}</span>", unsafe_allow_html=True)
        with col3:
            if st.button("👁️", key=f"search_view_{idx}", help="View details"):
                st.session_state.selected_case_id = case['id']
                st.session_state.page = "📁 Case Details"
                st.rerun()

# ============ REGISTER CASE PAGE ============
elif st.session_state.page == "📝 Register Case":
    st.title("📝 Register New Missing Case")
    st.write("Complete this form to register a new missing person case")
    
    with st.form("register_case_form", clear_on_submit=True):
        
        st.subheader("👤 Missing Person Details")
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("Full Name *", placeholder="First and Last Name")
        with col2:
            age = st.number_input("Age (years) *", min_value=0, max_value=100, value=15)
        with col3:
            gender = st.selectbox("Gender *", ["Female", "Male", "Other"])
        
        st.markdown("---")
        st.subheader("🗺️ Last Seen Details")
        
        location = st.text_input("Location Last Seen *", placeholder="City, Area, Landmark")
        col1, col2 = st.columns(2)
        with col1:
            last_seen_date = st.date_input("Date Last Seen *")
        with col2:
            last_seen_time = st.time_input("Time Last Seen *")
        
        st.markdown("---")
        st.subheader("📝 Circumstances")
        
        circumstances = st.text_area(
            "Description of Circumstances *",
            placeholder="Describe how/where/when the person was last seen. Any suspicious activity?",
            height=100
        )
        
        st.markdown("---")
        st.subheader("📞 Family Contact")
        
        col1, col2 = st.columns(2)
        with col1:
            phone = st.text_input("Contact Phone *", placeholder="+91-")
        with col2:
            relation = st.selectbox("Relation to Missing Person *", ["Mother", "Father", "Brother", "Sister", "Other Family"])
        
        st.markdown("---")
        st.subheader("📸 Photos (Optional)")
        
        st.write("Upload photos of the missing person (up to 5 photos)")
        photo_count = st.slider("Number of photos to upload", 0, 5, 1)
        
        st.markdown("---")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            submitted = st.form_submit_button("📤 Register Case", use_container_width=True)
        with col2:
            st.write("")
        
        if submitted and name and age and location:
            case_id = f"CASE-{np.random.randint(100, 999)}"
            st.success(f"""
            ✅ **Case Registered Successfully!**
            
            **Case ID:** {case_id}
            **Name:** {name}
            **Age:** {age} years
            **Location:** {location}
            
            The case has been registered and relevant officers have been notified.
            """)
            st.balloons()
        elif submitted:
            st.error("❌ Please fill in all required fields marked with *")

# ============ CASE DETAILS PAGE ============
elif st.session_state.page == "📁 Case Details":
    st.title("📁 Case Details & Workflow")
    
    df_cases = generate_cases()
    
    # Case selector
    case_options = [f"{row['name']} ({row['id']})" for _, row in df_cases.iterrows()]
    selected_option = st.selectbox("Select Case:", case_options, key="case_selector")
    
    selected_case = df_cases[df_cases['id'] == selected_option.split("(")[1].replace(")", "")].iloc[0]
    
    # Case Header
    col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
    
    with col1:
        st.write("**ID**")
        st.write(selected_case['id'])
    
    with col2:
        st.write("**Name & Age**")
        priority_class = get_priority_badge_class(selected_case['priority'])
        st.markdown(f"**{selected_case['name']}, {selected_case['age']} years** <span class='badge {priority_class}'>{selected_case['priority']}</span>", unsafe_allow_html=True)
    
    with col3:
        st.write("**Missing Duration**")
        st.write(f"{selected_case['missing_days']} days")
    
    with col4:
        st.write("**Risk Score**")
        st.write(f"{selected_case['risk_score']}/100")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📋 Case Info")
        st.write(f"**Location:** {selected_case['location']}")
        st.write(f"**Status:** {selected_case['status']}")
        st.write(f"**Assigned To:** {selected_case['assigned_to']}")
        st.write(f"**Last Update:** {selected_case['last_update']}")
    
    with col2:
        st.subheader("📁 Evidence")
        st.write(f"📷 **Photos:** {selected_case['photos']}")
        st.write(f"📹 **CCTV Videos:** {selected_case['cctv']}")
        st.write(f"📄 **Documents:** 2")
        st.write(f"📋 **Notes:** 4")
    
    with col3:
        st.subheader("🔍 AI Analysis")
        st.write(f"**Similar Cases:** 3 found")
        st.write(f"**Face Match:** 89% match found")
        st.write(f"**Hotspot Level:** High")
        st.write(f"**Escalation:** Recommended")
    
    st.markdown("---")
    
    st.subheader("📅 Workflow & Timeline")
    
    remarks = [
        {
            "date": "2024-01-16 09:30",
            "officer": "Inspector Ramesh Kumar",
            "action": "Case Escalated",
            "text": "Risk score reached 96/100. Escalated to Commissioner. State-level task force coordination initiated."
        },
        {
            "date": "2024-01-15 14:45",
            "officer": "Inspector Patel",
            "action": "Evidence Added",
            "text": "CCTV footage from 5 locations collected. Subject visible at 03:15 AM with unknown male. Vehicle registration: MH02-AB-1234"
        },
        {
            "date": "2024-01-15 10:20",
            "officer": "Inspector Kumar",
            "action": "Investigation Started",
            "text": "FIR filed under POCSO Act. Photos uploaded. Initial interviews with family members completed."
        }
    ]
    
    for remark in remarks:
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown(f"""
            <div class="timeline-item">
                <div class="timeline-date">{remark['date']}</div>
                <div style="font-weight: 700; color: #667eea; margin: 5px 0;">{remark['action']}</div>
                <div style="color: #2c3e50; font-size: 13px;">{remark['officer']}</div>
                <div style="color: #555; margin-top: 8px; font-size: 13px;">{remark['text']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("✎", key=f"edit_{remark['date']}", help="Edit remark"):
                st.info("Edit mode opened")
    
    st.markdown("---")
    
    st.subheader("➕ Add New Remark")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        new_remark = st.text_area(
            "Your remark:",
            placeholder="Add investigation updates, findings, observations, or action taken...",
            height=80,
            label_visibility="collapsed"
        )
    
    with col2:
        if st.button("📤 Update Case", use_container_width=True, key="update_case_btn"):
            if new_remark:
                st.success("✅ Remark added and case updated!")
            else:
                st.warning("⚠️ Please add a remark before updating")

# ============ ANALYTICS PAGE ============
elif st.session_state.page == "📈 Analytics":
    st.title("📈 Analytics & Performance Dashboard")
    st.write("Real-time statistics and performance metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="✅ Resolution Rate", value="63%", delta="+5%", delta_color="normal")
    with col2:
        st.metric(label="⏱️ Avg Time", value="12 mo", delta="-2 mo")
    with col3:
        st.metric(label="👮 Adoption", value="87%", delta="High adoption")
    with col4:
        st.metric(label="📋 Pending", value="5 cases", delta="Urgent review")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Case Resolution Trend (12 Months)")
        dates = pd.date_range(start='2023-01', periods=12, freq='M')
        resolved = [3, 5, 4, 6, 7, 8, 6, 9, 10, 11, 12, 14]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=resolved, mode='lines+markers', 
                                name='Cases Resolved', line=dict(color='#667eea', width=3)))
        fig.update_layout(height=400, hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("👧 Cases by Age Group")
        age_data = pd.DataFrame({
            "Age Group": ["<10", "10-14", "15-18", ">18"],
            "Count": [8, 45, 62, 41]
        })
        fig = px.bar(age_data, x="Age Group", y="Count", color="Count",
                    color_continuous_scale="Viridis")
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🗺️ Geographic Hotspots")
        location_data = pd.DataFrame({
            "State": ["Maharashtra", "Karnataka", "Tamil Nadu", "Telangana", "Others"],
            "Cases": [28, 15, 12, 10, 91]
        })
        fig = px.pie(location_data, values="Cases", names="State")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📅 Missing Duration Distribution")
        duration_data = pd.DataFrame({
            "Duration": ["0-7d", "7-30d", "1-6m", "6-12m", ">1y"],
            "Cases": [12, 18, 35, 28, 63]
        })
        fig = px.bar(duration_data, x="Duration", y="Cases", color="Cases",
                    color_continuous_scale="Reds")
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# ============ AI FEATURES PAGE ============
elif st.session_state.page == "🤖 AI Features":
    st.title("🤖 AI-Powered Intelligence")
    st.write("Advanced machine learning features for faster case resolution")
    
    # Feature tabs
    ai_tab1, ai_tab2, ai_tab3, ai_tab4, ai_tab5 = st.tabs(
        ["👁️ Facial Recognition", "🔗 Case Similarity", "📊 Risk Scoring", "🔮 Predictions", "🎙️ Voice Input"]
    )
    
    with ai_tab1:
        st.subheader("👁️ Facial Recognition (95% Accuracy)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Features:**")
            st.write("✅ Compare faces across 100K+ photos")
            st.write("✅ Speed: 2 seconds per comparison")
            st.write("✅ Accuracy: 95%+")
            st.write("✅ Cross-regional matching")
            st.write("✅ Real-time CCTV matching")
        
        with col2:
            st.metric(label="Similar Cases Found", value="3 matches", delta="89% confidence")
            st.metric(label="False Positives", value="2%", delta="Safe threshold")
        
        st.markdown("---")
        st.write("**Demo: Find Similar Faces**")
        case_selector = st.selectbox("Select a case:", ["Shreya Patel", "Anjali Desai", "Maya Singh"])
        
        if st.button("🔍 Run Face Matching", key="face_match"):
            st.info(f"Scanning for faces similar to {case_selector}...")
            time.sleep(1)
            st.success(f"✅ Found 3 potential matches!")
            st.write("**Match 1:** 94% - CCTV footage from Mumbai Central Station (Jan 16)")
            st.write("**Match 2:** 87% - Security camera at Railway Station (Jan 15)")
            st.write("**Match 3:** 81% - Social media photo (Jan 14)")
    
    with ai_tab2:
        st.subheader("🔗 Case Similarity Detection")
        
        st.write("**Auto-links related cases across regions**")
        st.metric(label="Linking Accuracy", value="85%", delta="Identifies patterns")
        
        st.markdown("---")
        
        similarity_data = pd.DataFrame({
            "Related Case": ["CASE-045 (Delhi)", "CASE-078 (Karnataka)", "CASE-012 (Tamil Nadu)"],
            "Similarity": [92, 87, 76],
            "Pattern": ["Trafficking Ring", "Serial Abduction", "Missing Person Network"]
        })
        
        st.dataframe(similarity_data, use_container_width=True)
    
    with ai_tab3:
        st.subheader("📊 Risk Assessment Scoring (0-100)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Scoring Factors:**")
            st.write("• Age (0-25 points)")
            st.write("• Duration missing (0-30 points)")
            st.write("• Circumstances (0-25 points)")
            st.write("• Geography (0-10 points)")
            st.write("• Victim profile (0-10 points)")
        
        with col2:
            case_selector = st.selectbox("Select case for risk score:", ["Shreya Patel", "Anjali Desai", "Maya Singh"], key="risk_score")
            risk_scores = {"Shreya Patel": 96, "Anjali Desai": 82, "Maya Singh": 75}
            score = risk_scores[case_selector]
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Risk Score"},
                delta={'reference': 80},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#e74c3c" if score > 80 else "#f39c12"},
                    'steps': [
                        {'range': [0, 50], 'color': "#d5f4e6"},
                        {'range': [50, 80], 'color': "#fdebd0"},
                        {'range': [80, 100], 'color': "#fadbd8"}
                    ],
                    'threshold': {'line': {'color': "red"}, 'thickness': 4, 'value': 80}
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    with ai_tab4:
        st.subheader("🔮 Predictive Escalation (85% Accuracy)")
        
        st.write("**Predicts optimal escalation timing**")
        
        prediction_data = pd.DataFrame({
            "Case": ["Shreya Patel", "Anjali Desai", "Maya Singh"],
            "Prediction": ["Escalate Immediately", "Escalate within 24h", "Monitor closely"],
            "Confidence": ["98%", "92%", "85%"],
            "Reasoning": ["Age <14, 18+ months missing", "Age <18, 15+ months missing", "Age 14, escalate in 2 weeks"]
        })
        
        st.dataframe(prediction_data, use_container_width=True)
    
    with ai_tab5:
        st.subheader("🎙️ Voice Remarks & NLP")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Features:**")
            st.write("✅ Record voice notes in field")
            st.write("✅ Auto-transcription (Google Speech-to-Text)")
            st.write("✅ Auto-extract locations")
            st.write("✅ Auto-extract vehicle numbers")
            st.write("✅ Auto-extract names")
            st.write("✅ 50% faster documentation")
        
        with col2:
            if st.button("🎙️ Record Voice Remark (Demo)", use_container_width=True):
                st.info("🎙️ Listening to your remark...")
                time.sleep(1)
                st.success("✅ Recording complete!")
                st.markdown("---")
                st.write("**Transcribed Text:**")
                st.code("I'm at school bus stop near Pune station. Saw white Maruti Swift MH02BK1234 with suspicious activity at 3:15 AM.")
                
                st.markdown("---")
                st.write("**Extracted Entities:**")
                st.success("📍 Location: School bus stop, Pune station")
                st.success("🚗 Vehicle: White Maruti Swift, MH02BK1234")
                st.success("⏰ Time: 3:15 AM")

# ============ HOTSPOTS PAGE ============
elif st.session_state.page == "🗺️ Hotspots":
    st.title("🗺️ Geographic Hotspot Analysis")
    st.write("AI-identified crime clusters and prevention recommendations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Hotspots Identified", value="8", delta="This month")
    with col2:
        st.metric(label="Prevention Rate", value="78%", delta="Based on hotspot alerts")
    with col3:
        st.metric(label="Cases Prevented", value="45", delta="Using analysis")
    
    st.markdown("---")
    
    st.subheader("🔴 Top Hotspot Areas")
    
    hotspot_data = pd.DataFrame({
        "Rank": ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"],
        "Location": ["South Mumbai, Colaba", "Thane East", "Pune Cantonment", "Bangalore Whitefield", "Hyderabad Tech Park"],
        "Cases": [14, 11, 9, 8, 7],
        "Risk Level": ["🔴 CRITICAL", "🟠 HIGH", "🟠 HIGH", "🟡 MEDIUM", "🟡 MEDIUM"],
        "Recommendation": [
            "Deploy 4 CCTV cameras, increase patrols",
            "Enhanced surveillance, awareness campaigns",
            "Checkpoint every 500m, community alerts",
            "Mobile surveillance units",
            "Regular patrols, awareness programs"
        ]
    })
    
    st.dataframe(hotspot_data, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📍 Hotspot Map")
        hotspot_map_data = pd.DataFrame({
            "Location": ["Mumbai", "Thane", "Pune", "Bangalore", "Hyderabad"],
            "Cases": [14, 11, 9, 8, 7],
            "lat": [19.0760, 19.2183, 18.5204, 12.9716, 17.3850],
            "lon": [72.8777, 72.9781, 73.8567, 77.5946, 78.4867]
        })
        
        fig = px.scatter_geo(hotspot_map_data, lat='lat', lon='lon', 
                            size='Cases', hover_name='Location',
                            color='Cases', color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Hotspot Trend")
        trend_data = pd.DataFrame({
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Active Hotspots": [6, 7, 8, 7, 8, 8]
        })
        
        fig = px.line(trend_data, x="Month", y="Active Hotspots", markers=True)
        st.plotly_chart(fig, use_container_width=True)

# ============ MEDIA CAMPAIGN PAGE ============
elif st.session_state.page == "📱 Media Campaign":
    st.title("📱 Media Campaign Automation")
    st.write("Auto-generate and launch awareness campaigns")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Campaigns Launched", value="45", delta="+5 this month")
    with col2:
        st.metric(label="Avg Reach", value="245K", delta="Per campaign")
    with col3:
        st.metric(label="Success Rate", value="34%", delta="Cases resolved via tips")
    
    st.markdown("---")
    
    st.subheader("🚀 Launch New Campaign")
    
    df_cases = generate_cases()
    selected_case_name = st.selectbox("Select a case for campaign:", [f"{row['name']} ({row['id']})" for _, row in df_cases.iterrows()])
    selected_case = df_cases[df_cases['id'] == selected_case_name.split("(")[1].replace(")", "")].iloc[0]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Auto-Generated Post:**")
        st.text_area(
            "Facebook/Twitter Post:",
            value=f"""🚨 URGENT: HELP US FIND {selected_case['name'].upper()}
            
Age: {selected_case['age']} years
Missing since: {selected_case['missing_days']} days
Last seen: {selected_case['location']}

If you have any information, please contact:
📞 +91-XXXX-XXXX
🔗 Report: [Link to case]

Please share! Every share counts. 🙏 #FindMissing{selected_case['name'].split()[0]}""",
            height=150,
            disabled=True
        )
    
    with col2:
        st.write("**Campaign Settings:**")
        
        campaign_duration = st.slider("Campaign Duration (days):", 1, 30, 7)
        ad_budget = st.number_input("Ad Budget (₹):", 1000, 100000, 10000)
        target_area = st.selectbox("Target Area:", [selected_case['location'], "All India", "State-wide"])
        
        st.write("---")
        
        if st.button("🚀 Launch Campaign", use_container_width=True):
            st.success(f"""
            ✅ Campaign Launched Successfully!
            
            **Campaign ID:** CAMP-{np.random.randint(1000, 9999)}
            **Duration:** {campaign_duration} days
            **Budget:** ₹{ad_budget:,}
            **Reach:** Est. 300K+ people
            **Platforms:** Facebook, Twitter, Instagram, WhatsApp
            
            Campaign is now LIVE!
            """)
    
    st.markdown("---")
    
    st.subheader("📊 Active Campaigns")
    
    campaign_data = pd.DataFrame({
        "Case": ["Shreya Patel", "Anjali Desai", "Maya Singh"],
        "Platform": ["Facebook + Twitter", "Instagram + WhatsApp", "All Platforms"],
        "Reach": ["125K", "89K", "234K"],
        "Engagement": ["12.5%", "8.3%", "18.7%"],
        "Tips": ["14", "8", "22"],
        "Status": ["🟢 Active", "🟢 Active", "🟢 Active"]
    })
    
    st.dataframe(campaign_data, use_container_width=True)

# ============ OFFICERS PAGE ============
elif st.session_state.page == "👥 Officers":
    st.title("👥 Officer Management")
    st.write("View and manage officer assignments and performance")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Officers", value="45", delta="Active")
    with col2:
        st.metric(label="Avg Cases/Officer", value="6.2", delta="Balanced load")
    with col3:
        st.metric(label="System Adoption", value="91%", delta="Using MWAIS")
    
    st.markdown("---")
    
    st.subheader("👮 Officer Directory")
    
    officer_data = pd.DataFrame({
        "Name": ["Inspector Ramesh Kumar", "Sr. Inspector Sharma", "Inspector Patel", "Inspector Verma", "ASI Singh"],
        "Rank": ["Inspector", "Sr. Inspector", "Inspector", "Inspector", "ASI"],
        "Station": ["Mumbai Central", "South Mumbai", "Thane East", "Pune Central", "Bangalore"],
        "Cases Assigned": [4, 8, 6, 5, 3],
        "Resolved": [2, 5, 4, 2, 1],
        "Adoption": ["✅ 100%", "✅ 95%", "✅ 92%", "⚠️ 78%", "⚠️ 65%"]
    })
    
    st.dataframe(officer_data, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("📊 Performance Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Case Load Distribution**")
        load_data = pd.DataFrame({
            "Officer": ["Kumar", "Sharma", "Patel", "Verma", "Singh"],
            "Cases": [4, 8, 6, 5, 3]
        })
        fig = px.bar(load_data, x="Officer", y="Cases", color="Cases",
                    color_continuous_scale="Blues")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("**Resolution Rate by Officer**")
        resolution_data = pd.DataFrame({
            "Officer": ["Kumar", "Sharma", "Patel", "Verma", "Singh"],
            "Rate": [50, 62, 67, 40, 33]
        })
        fig = px.bar(resolution_data, x="Officer", y="Rate", color="Rate",
                    color_continuous_scale="Greens")
        st.plotly_chart(fig, use_container_width=True)

# ============ SETTINGS PAGE ============
elif st.session_state.page == "⚙️ Settings":
    st.title("⚙️ Settings & Preferences")
    
    tabs = st.tabs(["👤 Profile", "🔔 Notifications", "🔐 Security", "📱 Preferences"])
    
    with tabs[0]:
        st.subheader("👤 My Profile")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Name:** Inspector Ramesh Kumar")
            st.write("**Rank:** Inspector")
            st.write("**Badge:** #12345")
            st.write("**Station:** Mumbai Central Police Station")
        
        with col2:
            st.write("**Email:** ramesh.kumar@police.gov.in")
            st.write("**Phone:** +91-98765-00000")
            st.write("**Years of Service:** 12 years")
            st.write("**Joined MWAIS:** Jan 2024")
        
        st.markdown("---")
        
        if st.button("✏️ Edit Profile", use_container_width=True):
            st.info("Profile editing coming soon")
        if st.button("🔄 Update Photo", use_container_width=True):
            st.info("Photo upload coming soon")
    
    with tabs[1]:
        st.subheader("🔔 Notification Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("Push Notifications", value=True)
            st.checkbox("SMS Alerts", value=True)
            st.checkbox("Email Reports", value=False)
            st.checkbox("Daily Digest", value=True)
        
        with col2:
            st.checkbox("High Priority Only", value=False)
            st.checkbox("Critical Cases Instant", value=True)
            st.checkbox("New Case Alerts", value=True)
            st.checkbox("Case Updates", value=True)
        
        st.markdown("---")
        
        alert_time = st.time_input("Quiet Hours Start:", value=datetime.strptime("22:00", "%H:%M").time())
        alert_time_end = st.time_input("Quiet Hours End:", value=datetime.strptime("07:00", "%H:%M").time())
    
    with tabs[2]:
        st.subheader("🔐 Security Settings")
        
        st.write("**Last Login:** 2024-01-16 09:30")
        st.write("**Session Duration:** 2 hours")
        st.write("**Login Attempts This Month:** 28")
        st.write("**Failed Attempts:** 0")
        
        st.markdown("---")
        
        if st.button("🔐 Change Password", use_container_width=True):
            st.info("Password change will be sent to registered email")
        
        if st.button("📱 Two-Factor Authentication", use_container_width=True):
            st.success("Two-factor authentication is ENABLED")
        
        if st.button("🚪 Logout from All Devices", use_container_width=True):
            st.warning("You will be logged out from all devices")
    
    with tabs[3]:
        st.subheader("⚙️ Application Preferences")
        
        theme = st.selectbox("Theme:", ["Dark Mode (Recommended)", "Light Mode"])
        language = st.selectbox("Language:", ["English", "Hindi", "Marathi"])
        timezone = st.selectbox("Timezone:", ["IST (UTC+5:30)", "Other"])
        
        st.markdown("---")
        
        st.checkbox("Enable Offline Mode", value=True)
        st.checkbox("Auto-save Remarks", value=True)
        st.checkbox("Sync on Background", value=True)

# Footer
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.write("**MWAIS v1.0**")
with col2:
    st.write("**Status:** ✅ Online")
with col3:
    st.write(f"**Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
with col4:
    st.write("**Support:** support@mwais.in")
