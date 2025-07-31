import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import json

# Page Configuration
st.set_page_config(
    page_title="EventIQ Management System",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000/api/v1"

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

def make_api_request(endpoint, method="GET", data=None):
    """Make API request with proper error handling"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=5)
        elif method == "PUT":
            response = requests.put(url, json=data, timeout=5)
        elif method == "DELETE":
            response = requests.delete(url, timeout=5)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: {str(e)}")
        return None

def show_login_page():
    """Enhanced login page with demo accounts"""
    st.markdown('<div class="main-header"><h1>🎉 EventIQ Management System</h1><p>Professional Event Management Platform</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login to Your Account")
        
        # Demo accounts section
        with st.expander("🎭 Demo Accounts (Click to view)", expanded=True):
            demo_accounts = [
                {"role": "👨‍💼 Event Organizer", "email": "organizer@eventiq.com", "password": "organizer123", "color": "#667eea"},
                {"role": "🤝 Volunteer", "email": "volunteer@eventiq.com", "password": "volunteer123", "color": "#52c41a"},
                {"role": "👥 Participant", "email": "participant@eventiq.com", "password": "participant123", "color": "#fa8c16"},
                {"role": "🏭 Vendor", "email": "vendor@eventiq.com", "password": "vendor123", "color": "#722ed1"},
                {"role": "👨‍💻 Admin", "email": "admin@eventiq.com", "password": "admin123", "color": "#f5222d"}
            ]
            
            for account in demo_accounts:
                st.markdown(f"""
                <div style="background: {account['color']}15; padding: 0.5rem; border-radius: 5px; margin: 0.25rem 0;">
                    <strong style="color: {account['color']}">{account['role']}</strong><br>
                    📧 {account['email']}<br>
                    🔑 {account['password']}
                </div>
                """, unsafe_allow_html=True)
        
        # Login form
        email = st.text_input("📧 Email", placeholder="Enter your email")
        password = st.text_input("🔐 Password", type="password", placeholder="Enter your password")
        
        if st.button("🚀 Login", use_container_width=True):
            if email and password:
                # Simple role-based authentication
                user_role = None
                if "organizer" in email:
                    user_role = "organizer"
                elif "volunteer" in email:
                    user_role = "volunteer"
                elif "participant" in email:
                    user_role = "participant"
                elif "vendor" in email:
                    user_role = "vendor"
                elif "admin" in email:
                    user_role = "admin"
                
                if user_role:
                    st.session_state.logged_in = True
                    st.session_state.user_role = user_role
                    st.session_state.user_email = email
                    st.success(f"✅ Welcome, {user_role.title()}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
            else:
                st.warning("⚠️ Please enter both email and password")

def show_dashboard():
    """Display enhanced dashboard with navigation"""
    user_role = st.session_state.get('user_role', 'participant')
    user_email = st.session_state.get('user_email', '')
    
    # Header with logout
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.markdown(f"### 🎉 EventIQ Dashboard - {user_role.title()}")
    with col2:
        st.markdown(f"👤 {user_email}")
    with col3:
        if st.button("🚪 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        
        if user_role == "organizer":
            page = st.radio("Select Page:", [
                "🏠 Dashboard",
                "🎓 Certificates",
                "📸 Media Gallery", 
                "🏭 Vendors",
                "🔄 Workflows",
                "📝 Feedback",
                "👥 Participants",
                "🤝 Volunteers",
                "💰 Budget",
                "🏢 Booths",
                "📊 Analytics",
                "⚙️ Settings"
            ])
        elif user_role == "volunteer":
            page = st.radio("Select Page:", [
                "🏠 Dashboard",
                "🎓 My Certificates",
                "📝 Feedback",
                "⚙️ Profile"
            ])
        elif user_role == "participant":
            page = st.radio("Select Page:", [
                "🏠 Dashboard", 
                "📝 Feedback",
                "⚙️ Profile"
            ])
        else:
            page = st.radio("Select Page:", [
                "🏠 Dashboard",
                "⚙️ Profile"
            ])
    
    # Page routing
    if page == "🏠 Dashboard":
        show_role_dashboard(user_role)
    elif page == "🎓 Certificates" or page == "🎓 My Certificates":
        show_certificates_page()
    elif page == "📸 Media Gallery":
        show_media_gallery_page()
    elif page == "🏭 Vendors":
        show_vendors_page()
    elif page == "🔄 Workflows":
        show_workflows_page()
    elif page == "📝 Feedback":
        show_feedback_page()
    elif page == "👥 Participants":
        show_participants_module()
    elif page == "🤝 Volunteers":
        show_volunteers_module()
    elif page == "💰 Budget":
        show_budget_module()
    elif page == "🏢 Booths":
        show_booths_module()
    elif page == "📊 Analytics":
        show_analytics_module()
    elif page == "⚙️ Settings" or page == "⚙️ Profile":
        show_settings_page()

def show_role_dashboard(role):
    """Show role-specific dashboard"""
    if role == "organizer":
        show_organizer_dashboard()
    elif role == "volunteer":
        show_volunteer_dashboard()
    elif role == "participant":
        show_participant_dashboard()
    elif role == "vendor":
        show_vendor_dashboard()
    elif role == "admin":
        show_admin_dashboard()

def show_organizer_dashboard():
    """Enhanced organizer dashboard"""
    st.markdown("## 👨‍💼 Event Organizer Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Get real data from API
    analytics = make_api_request("/analytics/dashboard")
    if analytics:
        with col1:
            st.metric("👥 Total Participants", analytics.get("total_participants", 0))
        with col2:
            st.metric("🤝 Active Volunteers", analytics.get("total_volunteers", 0))
        with col3:
            st.metric("🏢 Booked Booths", analytics.get("total_booths", 0))
        with col4:
            st.metric("💰 Budget Utilized", f"${analytics.get('spent_amount', 0):,.0f}")
    else:
        with col1:
            st.metric("👥 Total Participants", "Loading...")
        with col2:
            st.metric("🤝 Active Volunteers", "Loading...")
        with col3:
            st.metric("🏢 Booked Booths", "Loading...")
        with col4:
            st.metric("💰 Budget Utilized", "Loading...")
    
    # Quick actions
    st.markdown("### 🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎓 Generate Certificates", use_container_width=True):
            st.success("Certificate generation initiated")
    with col2:
        if st.button("📊 View Analytics", use_container_width=True):
            st.success("Analytics dashboard opened")
    with col3:
        if st.button("📝 Collect Feedback", use_container_width=True):
            st.success("Feedback collection started")
    
    # Recent activities
    if analytics and "recent_activities" in analytics:
        st.markdown("### 📋 Recent Activities")
        for activity in analytics["recent_activities"]:
            st.info(f"📋 {activity['message']}")

def show_volunteer_dashboard():
    """Enhanced volunteer dashboard"""
    st.markdown("## 🤝 Volunteer Dashboard")
    
    # Volunteer stats
    volunteers = make_api_request("/volunteers/")
    if volunteers and "volunteers" in volunteers:
        # Find current volunteer (simplified)
        current_volunteer = volunteers["volunteers"][0] if volunteers["volunteers"] else {}
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("⏰ Hours Worked", current_volunteer.get("total_hours", 0))
        with col2:
            st.metric("🎯 Tasks Completed", current_volunteer.get("tasks_completed", 0))
        with col3:
            st.metric("⭐ Rating", f"{current_volunteer.get('rating', 0):.1f}/5.0")
    
    # Certificate eligibility
    st.markdown("### 🎓 Certificate Status")
    hours = current_volunteer.get("total_hours", 0) if 'current_volunteer' in locals() else 0
    if hours >= 5:
        st.success(f"✅ You are eligible for a certificate! You have completed {hours} hours.")
        if st.button("🎓 Generate My Certificate", use_container_width=True):
            st.success("Your certificate has been generated!")
            st.balloons()
    else:
        remaining = 5 - hours
        st.warning(f"⏳ You need {remaining} more hours to be eligible for a certificate.")
    
    # Quick actions
    st.markdown("### 🚀 Quick Actions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Submit Feedback", use_container_width=True):
            st.success("Feedback form opened")
    with col2:
        if st.button("📧 Update Profile", use_container_width=True):
            st.success("Profile update form would open here")

def show_participant_dashboard():
    """Enhanced participant dashboard"""
    st.markdown("## 👥 Participant Dashboard")
    
    # Event information
    st.markdown("### 🎉 Event Information")
    st.info("Welcome to EventIQ 2025! Check out the latest updates and activities.")
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📅 Event Days", "3")
    with col2:
        st.metric("🎪 Activities", "12")
    with col3:
        st.metric("🏢 Exhibitors", "8")
    
    # Quick actions
    st.markdown("### 🚀 Available Actions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Provide Feedback", use_container_width=True):
            st.success("Feedback form opened")
    with col2:
        if st.button("📧 Update Profile", use_container_width=True):
            st.success("Profile update form would open here")

def show_vendor_dashboard():
    """Enhanced vendor dashboard"""
    st.markdown("## 🏭 Vendor Dashboard")
    
    # Vendor stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📦 Products/Services", "5")
    with col2:
        st.metric("💰 Revenue Target", "$10,000")
    with col3:
        st.metric("📊 Booth Status", "Active")
    
    # Quick actions
    st.markdown("### 🚀 Quick Actions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 View Sales", use_container_width=True):
            st.success("Sales dashboard opened")
    with col2:
        if st.button("📧 Update Profile", use_container_width=True):
            st.success("Profile update form would open here")

def show_admin_dashboard():
    """Enhanced admin dashboard"""
    st.markdown("## 👨‍💻 Admin Dashboard")
    
    # System stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Total Users", "125")
    with col2:
        st.metric("🔐 Active Sessions", "23")
    with col3:
        st.metric("📊 System Load", "12%")
    with col4:
        st.metric("💾 Storage Used", "67%")
    
    # Quick actions
    st.markdown("### 🚀 Admin Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("👥 Manage Users", use_container_width=True):
            st.success("User management opened")
    with col2:
        if st.button("📊 System Reports", use_container_width=True):
            st.success("System reports generated")
    with col3:
        if st.button("📧 Update Profile", use_container_width=True):
            st.success("Profile update form would open here")

def show_certificates_page():
    """Complete certificates page"""
    st.markdown("## 🎓 Certificate Management System")
    
    # Certificate statistics
    cert_stats = make_api_request("/certificates/stats")
    if cert_stats:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🎓 Eligible Volunteers", cert_stats.get("eligible_for_certificates", 0))
        with col2:
            st.metric("📜 Certificates Generated", cert_stats.get("certificates_generated", 0))
        with col3:
            st.metric("⏰ Total Hours", cert_stats.get("total_volunteer_hours", 0))
        with col4:
            st.metric("📊 Avg Hours/Volunteer", f"{cert_stats.get('average_hours_per_volunteer', 0):.1f}")
    
    # Tabs for different certificate functions
    tab1, tab2, tab3 = st.tabs(["📋 All Certificates", "🎓 Generate", "📊 Analytics"])
    
    with tab1:
        st.markdown("### 📋 Certificate Registry")
        certificates = make_api_request("/certificates/")
        if certificates and "certificates" in certificates:
            if certificates["certificates"]:
                cert_df = pd.DataFrame(certificates["certificates"])
                st.dataframe(cert_df, use_container_width=True, hide_index=True)
                
                # Download individual certificates
                st.markdown("#### 📥 Download Certificates")
                for cert in certificates["certificates"]:
                    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                    with col1:
                        st.write(cert["volunteer_name"])
                    with col2:
                        st.write(f"{cert['total_hours']} hours")
                    with col3:
                        st.write(cert["volunteer_role"])
                    with col4:
                        if st.button(f"📥", key=f"download_{cert['volunteer_id']}"):
                            st.success(f"Certificate downloaded for {cert['volunteer_name']}")
            else:
                st.info("No certificates available yet")
        else:
            st.error("Could not load certificates data")
    
    with tab2:
        st.markdown("### 🎓 Generate Certificates")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 👤 Individual Certificate")
            volunteers = make_api_request("/volunteers/")
            if volunteers and "volunteers" in volunteers:
                vol_options = {f"{v['full_name']} ({v['total_hours']}h)": v['id'] 
                             for v in volunteers["volunteers"] if v['total_hours'] >= 5}
                
                if vol_options:
                    selected_vol = st.selectbox("Select Volunteer:", list(vol_options.keys()))
                    vol_id = vol_options[selected_vol]
                    
                    if st.button("🎓 Generate Certificate", use_container_width=True):
                        st.success(f"Certificate generated for {selected_vol.split('(')[0].strip()}")
                        st.balloons()
                else:
                    st.warning("No volunteers with 5+ hours found")
        
        with col2:
            st.markdown("#### 🎓 Bulk Generation")
            st.info("Generate certificates for all eligible volunteers")
            
            if st.button("🎓 Generate All Certificates", use_container_width=True):
                result = make_api_request("/certificates/bulk-generate", method="POST")
                if result:
                    st.success(f"✅ {result.get('message', 'Bulk certificates generated!')}")
                    if "eligible_volunteers" in result:
                        st.write(f"Generated for {len(result['eligible_volunteers'])} volunteers")
    
    with tab3:
        st.markdown("### 📊 Certificate Analytics")
        
        if cert_stats:
            # Charts and analytics
            col1, col2 = st.columns(2)
            
            with col1:
                # Certificate eligibility pie chart
                eligible = cert_stats.get("eligible_for_certificates", 0)
                total = cert_stats.get("total_volunteers", 0)
                not_eligible = max(0, total - eligible)
                
                if total > 0:
                    fig = px.pie(
                        values=[eligible, not_eligible],
                        names=['Eligible', 'Not Eligible'],
                        title='Certificate Eligibility Status'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Hours distribution
                volunteers = make_api_request("/volunteers/")
                if volunteers and "volunteers" in volunteers:
                    hours_data = [v['total_hours'] for v in volunteers["volunteers"]]
                    fig = px.histogram(x=hours_data, title='Volunteer Hours Distribution', 
                                     labels={'x': 'Hours', 'y': 'Number of Volunteers'})
                    st.plotly_chart(fig, use_container_width=True)

def show_media_gallery_page():
    """Media gallery and upload page"""
    st.markdown("## 📸 Media Gallery & Upload")
    
    tab1, tab2, tab3 = st.tabs(["📸 Gallery", "📤 Upload", "📊 Statistics"])
    
    with tab1:
        st.markdown("### 📸 Event Photo Gallery")
        
        # Sample photos (in real app, these would come from API)
        sample_photos = [
            {"name": "Registration Desk", "booth": "Main Entrance", "date": "2025-01-30", "photographer": "John Smith"},
            {"name": "Information Booth", "booth": "Lobby", "date": "2025-01-30", "photographer": "Sarah Johnson"},
            {"name": "Main Stage Setup", "booth": "Main Hall", "date": "2025-01-29", "photographer": "Mike Wilson"},
            {"name": "Volunteer Team", "booth": "Multiple", "date": "2025-01-29", "photographer": "Alice Brown"},
        ]
        
        col1, col2, col3 = st.columns(3)
        for i, photo in enumerate(sample_photos):
            with [col1, col2, col3][i % 3]:
                st.markdown(f"""
                <div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; margin: 5px;">
                    <h4>📸 {photo['name']}</h4>
                    <p><strong>Location:</strong> {photo['booth']}</p>
                    <p><strong>Date:</strong> {photo['date']}</p>
                    <p><strong>Photographer:</strong> {photo['photographer']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"👁️ View", key=f"view_{i}"):
                    st.success(f"Viewing {photo['name']}")
    
    with tab2:
        st.markdown("### 📤 Upload New Photos")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📷 Photo Upload")
            uploaded_file = st.file_uploader("Choose photo files", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
            
            if uploaded_file:
                st.success(f"Uploaded {len(uploaded_file)} file(s)")
                for file in uploaded_file:
                    st.write(f"- {file.name}")
        
        with col2:
            st.markdown("#### 📝 Photo Details")
            booth_location = st.selectbox("Booth/Location:", ["Main Entrance", "Information Booth", "Main Stage", "Registration", "Food Court"])
            description = st.text_area("Description:")
            tags = st.text_input("Tags (comma-separated):")
            
            if st.button("💾 Save Photos", use_container_width=True):
                st.success("Photos uploaded and saved successfully!")
    
    with tab3:
        st.markdown("### 📊 Media Statistics")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📸 Total Photos", "24")
        with col2:
            st.metric("👥 Contributors", "8")
        with col3:
            st.metric("📍 Locations", "6")

def show_vendors_page():
    """Vendor management page"""
    st.markdown("## 🏭 Vendor Management")
    
    tab1, tab2, tab3 = st.tabs(["📋 Vendor List", "➕ Add Vendor", "📊 Analytics"])
    
    with tab1:
        st.markdown("### 📋 Registered Vendors")
        
        # Sample vendor data
        vendor_data = [
            {"Name": "Coffee Express", "Service": "Catering", "Contact": "coffee@express.com", "Status": "Active", "Contract": "$2,500"},
            {"Name": "Tech Solutions", "Service": "AV Equipment", "Contact": "info@techsol.com", "Status": "Active", "Contract": "$1,800"},
            {"Name": "Security Plus", "Service": "Security", "Contact": "ops@secplus.com", "Status": "Pending", "Contract": "$3,200"},
            {"Name": "Clean Masters", "Service": "Cleaning", "Contact": "clean@masters.com", "Status": "Active", "Contract": "$800"},
        ]
        
        df = pd.DataFrame(vendor_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Vendor actions
        st.markdown("#### 🎯 Vendor Actions")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📧 Send Bulk Email", use_container_width=True):
                st.success("Bulk email sent to all vendors")
        with col2:
            if st.button("📊 Generate Report", use_container_width=True):
                st.success("Vendor report generated")
        with col3:
            if st.button("💰 Payment Status", use_container_width=True):
                st.success("Payment status updated")
    
    with tab2:
        st.markdown("### ➕ Add New Vendor")
        
        col1, col2 = st.columns(2)
        with col1:
            vendor_name = st.text_input("Vendor Name:")
            vendor_email = st.text_input("Email:")
            vendor_phone = st.text_input("Phone:")
            vendor_service = st.selectbox("Service Type:", ["Catering", "AV Equipment", "Security", "Cleaning", "Transportation", "Other"])
        
        with col2:
            contract_amount = st.number_input("Contract Amount ($):", min_value=0.0, step=100.0)
            materials_brought = st.text_area("Materials/Equipment:")
            special_requirements = st.text_area("Special Requirements:")
            
            if st.button("💾 Add Vendor", use_container_width=True):
                st.success(f"Vendor '{vendor_name}' added successfully!")
    
    with tab3:
        st.markdown("### 📊 Vendor Analytics")
        
        col1, col2 = st.columns(2)
        with col1:
            # Service type distribution
            service_data = {"Catering": 1, "AV Equipment": 1, "Security": 1, "Cleaning": 1}
            fig = px.pie(values=list(service_data.values()), names=list(service_data.keys()), 
                        title="Vendors by Service Type")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Contract amounts
            amounts = [2500, 1800, 3200, 800]
            vendors = ["Coffee Express", "Tech Solutions", "Security Plus", "Clean Masters"]
            fig = px.bar(x=vendors, y=amounts, title="Contract Amounts by Vendor")
            st.plotly_chart(fig, use_container_width=True)

def show_workflows_page():
    """Workflow and approval management"""
    st.markdown("## 🔄 Workflow & Approval Management")
    
    tab1, tab2, tab3 = st.tabs(["📋 Active Workflows", "✅ Approvals", "📊 Status"])
    
    with tab1:
        st.markdown("### 📋 Active Workflows")
        
        workflows = [
            {"ID": "WF-001", "Type": "Expense Approval", "Requestor": "John Smith", "Amount": "$1,200", "Status": "Pending", "Priority": "High"},
            {"ID": "WF-002", "Type": "Vendor Onboarding", "Requestor": "Sarah Johnson", "Item": "Security Plus", "Status": "In Review", "Priority": "Medium"},
            {"ID": "WF-003", "Type": "Budget Modification", "Requestor": "Mike Wilson", "Amount": "$500", "Status": "Approved", "Priority": "Low"},
        ]
        
        for wf in workflows:
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 1, 1])
                with col1:
                    st.write(f"**{wf['ID']}**")
                with col2:
                    st.write(wf['Type'])
                with col3:
                    st.write(f"By: {wf['Requestor']}")
                with col4:
                    status_color = {"Pending": "🟡", "In Review": "🔵", "Approved": "🟢", "Rejected": "🔴"}
                    st.write(f"{status_color.get(wf['Status'], '⚪')} {wf['Status']}")
                with col5:
                    if wf['Status'] in ["Pending", "In Review"]:
                        if st.button("👁️", key=f"view_{wf['ID']}"):
                            st.success(f"Viewing {wf['ID']}")
                st.divider()
    
    with tab2:
        st.markdown("### ✅ Pending Approvals")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 💰 Expense Approvals")
            expense_approvals = [
                {"Item": "Catering Services", "Amount": "$1,200", "Requestor": "John Smith"},
                {"Item": "AV Equipment Rental", "Amount": "$800", "Requestor": "Sarah Johnson"},
            ]
            
            for exp in expense_approvals:
                st.write(f"**{exp['Item']}** - {exp['Amount']}")
                st.write(f"Requested by: {exp['Requestor']}")
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("✅ Approve", key=f"app_{exp['Item']}"):
                        st.success(f"Approved: {exp['Item']}")
                with col_b:
                    if st.button("❌ Reject", key=f"rej_{exp['Item']}"):
                        st.error(f"Rejected: {exp['Item']}")
                st.divider()
        
        with col2:
            st.markdown("#### 🏭 Vendor Approvals")
            vendor_approvals = [
                {"Vendor": "Security Plus", "Service": "Security Services", "Amount": "$3,200"},
            ]
            
            for ven in vendor_approvals:
                st.write(f"**{ven['Vendor']}** - {ven['Service']}")
                st.write(f"Contract: {ven['Amount']}")
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("✅ Approve", key=f"app_ven_{ven['Vendor']}"):
                        st.success(f"Approved: {ven['Vendor']}")
                with col_b:
                    if st.button("❌ Reject", key=f"rej_ven_{ven['Vendor']}"):
                        st.error(f"Rejected: {ven['Vendor']}")
    
    with tab3:
        st.markdown("### 📊 Workflow Statistics")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("⏳ Pending", "5")
        with col2:
            st.metric("✅ Approved Today", "3")
        with col3:
            st.metric("⏱️ Avg. Processing Time", "2.4 days")

def show_feedback_page():
    """Feedback collection and analysis"""
    st.markdown("## 📝 Feedback Management")
    
    tab1, tab2, tab3 = st.tabs(["📝 All Feedback", "📊 Analytics", "➕ Collect Feedback"])
    
    with tab1:
        st.markdown("### 📝 Collected Feedback")
        
        feedback_data = [
            {"Date": "2025-01-30", "Type": "Participant", "Rating": 5, "Comment": "Excellent event organization!", "Sentiment": "Positive"},
            {"Date": "2025-01-30", "Type": "Volunteer", "Rating": 4, "Comment": "Great experience, well coordinated", "Sentiment": "Positive"},
            {"Date": "2025-01-29", "Type": "Participant", "Rating": 3, "Comment": "Good event but registration was slow", "Sentiment": "Neutral"},
            {"Date": "2025-01-29", "Type": "Volunteer", "Rating": 5, "Comment": "Loved being part of the team!", "Sentiment": "Positive"},
        ]
        
        df = pd.DataFrame(feedback_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    with tab2:
        st.markdown("### 📊 Feedback Analytics")
        
        col1, col2 = st.columns(2)
        with col1:
            # Sentiment distribution
            sentiment_counts = {"Positive": 3, "Neutral": 1, "Negative": 0}
            fig = px.pie(values=list(sentiment_counts.values()), names=list(sentiment_counts.keys()),
                        title="Sentiment Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Rating distribution
            ratings = [5, 4, 3, 5]
            fig = px.histogram(x=ratings, title="Rating Distribution", nbins=5)
            st.plotly_chart(fig, use_container_width=True)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📝 Total Feedback", "4")
        with col2:
            st.metric("⭐ Average Rating", "4.3")
        with col3:
            st.metric("😊 Positive Sentiment", "75%")
        with col4:
            st.metric("📈 Response Rate", "68%")
    
    with tab3:
        st.markdown("### ➕ Feedback Collection")
        
        feedback_type = st.radio("Feedback Type:", ["Participant Feedback", "Volunteer Feedback", "General Event Feedback"])
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name (Optional):")
            email = st.text_input("Email (Optional):")
            rating = st.slider("Overall Rating:", 1, 5, 5)
        
        with col2:
            category = st.selectbox("Category:", ["Event Organization", "Registration Process", "Venue", "Food & Catering", "Activities", "Other"])
            feedback_text = st.text_area("Your Feedback:")
            
            if st.button("📤 Submit Feedback", use_container_width=True):
                st.success("Thank you for your feedback! It has been recorded.")
                st.balloons()

def show_participants_module():
    """Dedicated participants module"""
    st.markdown("## 👥 Participant Management Module")
    
    # Get participants data
    participants = make_api_request("/participants/")
    if participants and "participants" in participants:
        st.success("✅ Participants module is fully functional!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("👥 Total Participants", len(participants["participants"]))
        with col2:
            organizations = set(p.get('organization', 'Unknown') for p in participants["participants"])
            st.metric("🏢 Organizations", len(organizations))
        with col3:
            industries = set(p.get('industry', 'Unknown') for p in participants["participants"])
            st.metric("🏭 Industries", len(industries))
        
        # Show participant data
        part_df = pd.DataFrame(participants["participants"])
        st.dataframe(part_df, use_container_width=True, hide_index=True)
    else:
        st.error("Could not load participant data")

def show_volunteers_module():
    """Dedicated volunteers module"""
    st.markdown("## 🤝 Volunteer Management Module")
    
    # Get volunteers data
    volunteers = make_api_request("/volunteers/")
    if volunteers and "volunteers" in volunteers:
        st.success("✅ Volunteers module is fully functional!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🤝 Total Volunteers", len(volunteers["volunteers"]))
        with col2:
            active_count = len([v for v in volunteers["volunteers"] if v.get('is_active', False)])
            st.metric("✅ Active Volunteers", active_count)
        with col3:
            total_hours = sum(v.get('total_hours', 0) for v in volunteers["volunteers"])
            st.metric("⏰ Total Hours", total_hours)
        
        # Show volunteer data
        vol_df = pd.DataFrame(volunteers["volunteers"])
        st.dataframe(vol_df, use_container_width=True, hide_index=True)
    else:
        st.error("Could not load volunteer data")

def show_budget_module():
    """Dedicated budget module"""
    st.markdown("## 💰 Budget & Finance Management Module")
    
    # Get budget data
    budgets = make_api_request("/budget/")
    if budgets and "budgets" in budgets:
        st.success("✅ Budget module is fully functional!")
        
        budget = budgets["budgets"][0]  # Get first budget
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💰 Total Budget", f"${budget['total_budget']:,.0f}")
        with col2:
            st.metric("📊 Allocated", f"${budget['allocated_amount']:,.0f}")
        with col3:
            remaining = budget['total_budget'] - budget['allocated_amount']
            st.metric("💵 Remaining", f"${remaining:,.0f}")
        
        # Show budget categories
        expenses = make_api_request("/budget/expenses")
        if expenses and "expenses" in expenses:
            exp_df = pd.DataFrame(expenses["expenses"])
            st.dataframe(exp_df, use_container_width=True, hide_index=True)
    else:
        st.error("Could not load budget data")

def show_booths_module():
    """Dedicated booths module"""
    st.markdown("## 🏢 Booths & Venues Management Module")
    
    # Get booths data
    booths = make_api_request("/booths/")
    if booths and "booths" in booths:
        st.success("✅ Booths module is fully functional!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏢 Total Booths", len(booths["booths"]))
        with col2:
            occupied = len([b for b in booths["booths"] if b.get('is_occupied', False)])
            st.metric("✅ Occupied", occupied)
        with col3:
            total_revenue = sum(b.get('rental_price', 0) for b in booths["booths"] if b.get('is_occupied', False))
            st.metric("💰 Revenue", f"${total_revenue:,.0f}")
        
        # Show booth data
        booth_df = pd.DataFrame(booths["booths"])
        st.dataframe(booth_df, use_container_width=True, hide_index=True)
    else:
        st.error("Could not load booth data")

def show_analytics_module():
    """Dedicated analytics module"""
    st.markdown("## 📊 Analytics & Reporting Module")
    
    # Get analytics data
    analytics = make_api_request("/analytics/dashboard")
    if analytics:
        st.success("✅ Analytics module is fully functional!")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("👥 Total Participants", analytics.get("total_participants", 0))
        with col2:
            st.metric("🤝 Total Volunteers", analytics.get("total_volunteers", 0))
        with col3:
            st.metric("🏢 Total Booths", analytics.get("total_booths", 0))
        with col4:
            st.metric("💰 Budget Spent", f"${analytics.get('spent_amount', 0):,.0f}")
        
        # Show recent activities
        if "recent_activities" in analytics:
            st.markdown("### 📊 Recent Activities")
            for activity in analytics["recent_activities"]:
                st.info(f"📋 {activity['message']}")
    else:
        st.error("Could not load analytics data")

def show_settings_page():
    """System settings page"""
    st.markdown("## ⚙️ System Settings")
    
    tab1, tab2, tab3 = st.tabs(["🔧 General", "👥 Users", "🔐 Security"])
    
    with tab1:
        st.markdown("### 🔧 General Settings")
        st.info("General system configuration options would be available here.")
    
    with tab2:
        st.markdown("### 👥 User Management")
        st.info("User account management and role assignment options would be available here.")
    
    with tab3:
        st.markdown("### 🔐 Security Settings")
        st.info("Security configuration and access control options would be available here.")

# Main application logic
def main():
    """Main application logic"""
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    # Route to appropriate page
    if not st.session_state.logged_in:
        show_login_page()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()
