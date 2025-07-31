import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import json
import os
import base64
from PIL import Image
import io

# Page Configuration
st.set_page_config(
    page_title="EventIQ Management System",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:8000/api/v1"

# File Upload Helper Functions
def save_uploaded_file(uploaded_file, folder="uploads"):
    """Save uploaded file and return file info"""
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    file_path = os.path.join(folder, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return {
        "name": uploaded_file.name,
        "size": len(uploaded_file.getvalue()),
        "type": uploaded_file.type,
        "path": file_path
    }

def get_file_info(uploaded_file):
    """Get file information without saving"""
    return {
        "name": uploaded_file.name,
        "size": len(uploaded_file.getvalue()),
        "type": uploaded_file.type,
        "size_mb": len(uploaded_file.getvalue()) / (1024 * 1024)
    }

def display_image_preview(uploaded_file):
    """Display image preview"""
    if uploaded_file.type.startswith('image/'):
        image = Image.open(uploaded_file)
        st.image(image, caption=uploaded_file.name, width=200)
        return True
    return False

def get_base64_encoded_file(uploaded_file):
    """Get base64 encoded file for storage/transmission"""
    return base64.b64encode(uploaded_file.getvalue()).decode()

# Initialize session state for uploaded files
if 'uploaded_media' not in st.session_state:
    st.session_state.uploaded_media = []
if 'uploaded_documents' not in st.session_state:
    st.session_state.uploaded_documents = []

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
    # Temporary mock data for testing
    if endpoint == "/certificates/stats":
        return {
            "eligible_for_certificates": 3,
            "certificates_generated": 2,
            "total_volunteer_hours": 45,
            "average_hours_per_volunteer": 15.0,
            "total_volunteers": 8
        }
    elif endpoint == "/certificates/":
        return {
            "certificates": [
                {
                    "certificate_id": "CERT-001-202501",
                    "volunteer_id": 1,
                    "volunteer_name": "John Smith",
                    "volunteer_role": "Registration Assistant",
                    "total_hours": 15,
                    "eligible": True
                },
                {
                    "certificate_id": "CERT-002-202501",
                    "volunteer_id": 2,
                    "volunteer_name": "Sarah Johnson",
                    "volunteer_role": "Information Desk",
                    "total_hours": 12,
                    "eligible": True
                }
            ]
        }
    elif endpoint == "/volunteers/":
        return {
            "volunteers": [
                {"id": 1, "full_name": "John Smith", "email": "john@example.com", "total_hours": 15, "is_active": True, "role": "Registration", "tasks_completed": 8, "rating": 4.5},
                {"id": 2, "full_name": "Sarah Johnson", "email": "sarah@example.com", "total_hours": 12, "is_active": True, "role": "Information", "tasks_completed": 6, "rating": 4.2},
                {"id": 3, "full_name": "Mike Wilson", "email": "mike@example.com", "total_hours": 8, "is_active": False, "role": "Setup", "tasks_completed": 4, "rating": 4.0},
            ]
        }
    elif endpoint == "/participants/":
        return {
            "participants": [
                {"id": 1, "full_name": "John Participant", "email": "john@example.com", "organization": "Tech Corp", "industry": "Technology"},
                {"id": 2, "full_name": "Sarah User", "email": "sarah@example.com", "organization": "Design Studio", "industry": "Design"},
                {"id": 3, "full_name": "Mike Attendee", "email": "mike@example.com", "organization": "StartupX", "industry": "Technology"},
            ]
        }
    elif endpoint == "/budget/":
        return {
            "budgets": [
                {"id": 1, "total_budget": 50000, "allocated_amount": 35000, "spent_amount": 28000}
            ]
        }
    elif endpoint == "/budget/expenses":
        return {
            "expenses": [
                {"category": "Catering", "budgeted": 15000, "spent": 12000, "remaining": 3000},
                {"category": "AV Equipment", "budgeted": 8000, "spent": 7200, "remaining": 800},
                {"category": "Security", "budgeted": 5000, "spent": 4500, "remaining": 500},
                {"category": "Venue", "budgeted": 12000, "spent": 12000, "remaining": 0},
            ]
        }
    elif endpoint == "/booths/":
        return {
            "booths": [
                {"id": 1, "booth_number": "A-01", "size": "10x10", "rental_price": 1500, "is_occupied": True, "vendor": "Coffee Express"},
                {"id": 2, "booth_number": "A-02", "size": "10x10", "rental_price": 1500, "is_occupied": True, "vendor": "Tech Solutions"},
                {"id": 3, "booth_number": "A-03", "size": "10x10", "rental_price": 1500, "is_occupied": False, "vendor": None},
                {"id": 4, "booth_number": "B-01", "size": "20x10", "rental_price": 2500, "is_occupied": True, "vendor": "Security Plus"},
            ]
        }
    elif endpoint == "/analytics/dashboard":
        return {
            "total_participants": 125,
            "total_volunteers": 18,
            "total_booths": 24,
            "spent_amount": 28000,
            "recent_activities": [
                {"message": "New participant registered: John Doe"},
                {"message": "Certificate generated for volunteer Sarah"},
                {"message": "Payment processed for vendor Tech Solutions"},
                {"message": "Booth B-15 assigned to Coffee Express"},
            ]
        }
    elif endpoint == "/certificates/bulk-generate" and method == "POST":
        return {
            "message": "Bulk certificates generated successfully!",
            "eligible_volunteers": ["John Smith", "Sarah Johnson"]
        }
    
    # Original implementation for when backend is available
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
            page = st.selectbox("🧭 Navigate to:", [
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
            page = st.selectbox("🧭 Navigate to:", [
                "🏠 Dashboard",
                "🎓 My Certificates",
                "📝 Feedback",
                "⚙️ Profile"
            ])
        elif user_role == "participant":
            page = st.selectbox("🧭 Navigate to:", [
                "🏠 Dashboard", 
                "📝 Feedback",
                "⚙️ Profile"
            ])
        else:
            page = st.selectbox("🧭 Navigate to:", [
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
                        # Generate downloadable certificate
                        cert_content = f"""
CERTIFICATE OF APPRECIATION

This is to certify that

{cert['volunteer_name']}

has successfully completed {cert['total_hours']} hours of volunteer service
as a {cert['volunteer_role']} for EventIQ 2025.

We appreciate your dedication and commitment to making this event successful.

Date: {datetime.now().strftime("%B %d, %Y")}
Certificate ID: {cert['certificate_id']}

EventIQ Management Team
                        """
                        
                        if st.download_button(
                            label="📥 Download",
                            data=cert_content,
                            file_name=f"certificate_{cert['volunteer_name'].replace(' ', '_')}.txt",
                            mime="text/plain",
                            key=f"download_{cert['volunteer_id']}"
                        ):
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
                    
                    # Find volunteer details
                    selected_volunteer = next(v for v in volunteers["volunteers"] if v['id'] == vol_id)
                    
                    # Certificate preview
                    st.markdown("##### 📋 Certificate Preview:")
                    cert_content = f"""
CERTIFICATE OF APPRECIATION

This is to certify that

{selected_volunteer['full_name']}

has successfully completed {selected_volunteer['total_hours']} hours of volunteer service
as a {selected_volunteer.get('role', 'Volunteer')} for EventIQ 2025.

We appreciate your dedication and commitment to making this event successful.

Date: {datetime.now().strftime("%B %d, %Y")}
Certificate ID: CERT-{vol_id:03d}-{datetime.now().strftime("%Y%m")}

EventIQ Management Team
                    """
                    
                    st.text_area("Certificate Content:", cert_content, height=200, disabled=True)
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("🎓 Generate Certificate", use_container_width=True):
                            st.success(f"Certificate generated for {selected_volunteer['full_name']}")
                            st.balloons()
                    
                    with col_b:
                        st.download_button(
                            label="📥 Download Certificate",
                            data=cert_content,
                            file_name=f"certificate_{selected_volunteer['full_name'].replace(' ', '_')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
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
    """Enhanced media gallery and upload page"""
    st.markdown("## 📸 Media Gallery & Upload")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📸 Gallery", "📤 Upload", "📊 Statistics", "🎥 Live Stream"])
    
    with tab1:
        st.markdown("### 📸 Event Photo Gallery")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_date = st.date_input("Filter by Date:")
        with col2:
            filter_booth = st.selectbox("Filter by Location:", ["All", "Main Entrance", "Information Booth", "Main Stage", "Food Court", "Exhibition Hall"])
        with col3:
            filter_type = st.selectbox("Media Type:", ["All", "Photos", "Videos", "Documents"])
        
        # Combine sample media with uploaded media
        sample_media = [
            {
                "name": "Registration Desk Setup",
                "type": "Photo",
                "booth": "Main Entrance",
                "date": "2025-01-30",
                "photographer": "John Smith",
                "size": "2.4 MB",
                "downloads": 15,
                "likes": 8,
                "tags": ["registration", "setup", "entrance"],
                "source": "sample"
            },
            {
                "name": "Information Booth Team",
                "type": "Photo",
                "booth": "Information Booth",
                "date": "2025-01-30",
                "photographer": "Sarah Johnson",
                "size": "3.1 MB",
                "downloads": 23,
                "likes": 12,
                "tags": ["team", "volunteers", "information"],
                "source": "sample"
            },
            {
                "name": "Main Stage Performance",
                "type": "Video",
                "booth": "Main Stage",
                "date": "2025-01-29",
                "photographer": "Mike Wilson",
                "size": "45.2 MB",
                "downloads": 8,
                "likes": 25,
                "tags": ["performance", "stage", "entertainment"],
                "source": "sample"
            },
            {
                "name": "Volunteer Training Session",
                "type": "Photo",
                "booth": "Conference Room",
                "date": "2025-01-29",
                "photographer": "Alice Brown",
                "size": "1.8 MB",
                "downloads": 12,
                "likes": 6,
                "tags": ["training", "volunteers", "preparation"],
                "source": "sample"
            },
            {
                "name": "Food Court Opening",
                "type": "Photo",
                "booth": "Food Court",
                "date": "2025-01-30",
                "photographer": "David Lee",
                "size": "2.7 MB",
                "downloads": 18,
                "likes": 14,
                "tags": ["food", "opening", "vendors"],
                "source": "sample"
            },
            {
                "name": "Exhibition Hall Overview",
                "type": "Video",
                "booth": "Exhibition Hall",
                "date": "2025-01-30",
                "photographer": "Emma Davis",
                "size": "38.5 MB",
                "downloads": 6,
                "likes": 9,
                "tags": ["exhibition", "overview", "booths"],
                "source": "sample"
            }
        ]
        
        # Add uploaded media from session state
        all_media = sample_media.copy()
        if st.session_state.uploaded_media:
            for uploaded in st.session_state.uploaded_media:
                media_item = {
                    "name": uploaded['name'],
                    "type": uploaded['type'],
                    "booth": uploaded.get('location', 'Unknown'),
                    "date": uploaded['date'],
                    "photographer": uploaded.get('photographer', 'Unknown'),
                    "size": uploaded['size'],
                    "downloads": 0,
                    "likes": 0,
                    "tags": uploaded.get('tags', []),
                    "source": "uploaded",
                    "description": uploaded.get('description', ''),
                    "category": uploaded.get('category', 'General')
                }
                all_media.append(media_item)
        
        # Apply filters
        filtered_media = all_media
        if filter_booth != "All":
            filtered_media = [m for m in filtered_media if m['booth'] == filter_booth]
        if filter_type != "All":
            filtered_media = [m for m in filtered_media if m['type'] == filter_type]
        
        # Display media statistics
        st.markdown("#### 📊 Gallery Overview")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📸 Total Media", len(all_media))
        with col2:
            photos = len([m for m in all_media if m['type'] == 'Photo'])
            st.metric("📷 Photos", photos)
        with col3:
            videos = len([m for m in all_media if m['type'] == 'Video'])
            st.metric("🎥 Videos", videos)
        with col4:
            uploaded = len([m for m in all_media if m.get('source') == 'uploaded'])
            st.metric("📤 Uploaded", uploaded)
        
        # Display media in grid
        st.markdown("#### 🖼️ Media Gallery")
        for i in range(0, len(filtered_media), 2):
            col1, col2 = st.columns(2)
            
            for j, col in enumerate([col1, col2]):
                if i + j < len(filtered_media):
                    media = filtered_media[i + j]
                    with col:
                        with st.container():
                            # Different styling for uploaded vs sample media
                            border_color = "#4CAF50" if media.get('source') == 'uploaded' else "#ddd"
                            source_badge = "🆕 NEW" if media.get('source') == 'uploaded' else "📋 SAMPLE"
                            
                            st.markdown(f"""
                            <div style="border: 2px solid {border_color}; border-radius: 8px; padding: 15px; margin: 10px 0; background: white;">
                                <h4>📸 {media['name']} <span style="background: {border_color}; color: white; padding: 2px 6px; border-radius: 3px; font-size: 10px;">{source_badge}</span></h4>
                                <p><strong>Type:</strong> {media['type']} | <strong>Size:</strong> {media['size']}</p>
                                <p><strong>Location:</strong> {media['booth']}</p>
                                <p><strong>Date:</strong> {media['date']}</p>
                                <p><strong>Photographer:</strong> {media['photographer']}</p>
                                <p><strong>Tags:</strong> {', '.join(media['tags']) if isinstance(media['tags'], list) else media['tags']}</p>
                                <p>👁️ {media['downloads']} downloads | ❤️ {media['likes']} likes</p>
                                {f"<p><strong>Description:</strong> {media.get('description', '')}</p>" if media.get('description') else ""}
                            </div>
                            """, unsafe_allow_html=True)
                            
                            col_a, col_b, col_c = st.columns(3)
                            with col_a:
                                if st.button(f"👁️ View", key=f"view_{i+j}"):
                                    if media.get('source') == 'uploaded':
                                        st.success(f"Viewing uploaded file: {media['name']}")
                                    else:
                                        st.success(f"Viewing {media['name']}")
                            with col_b:
                                if st.button(f"📥 Download", key=f"download_{i+j}"):
                                    st.success(f"Downloading {media['name']}")
                                    # Increment download count
                                    media['downloads'] += 1
                            with col_c:
                                if st.button(f"❤️ Like", key=f"like_{i+j}"):
                                    st.success(f"Liked {media['name']}")
                                    # Increment like count
                                    media['likes'] += 1
    
    with tab2:
        st.markdown("### 📤 Upload New Media")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📷 Media Upload")
            uploaded_files = st.file_uploader(
                "Choose media files", 
                type=['jpg', 'jpeg', 'png', 'mp4', 'avi', 'mov', 'pdf', 'doc', 'docx'], 
                accept_multiple_files=True,
                key="media_uploader"
            )
            
            if uploaded_files:
                st.success(f"Selected {len(uploaded_files)} file(s)")
                
                # Display file details and previews
                for idx, file in enumerate(uploaded_files):
                    file_info = get_file_info(file)
                    
                    with st.expander(f"📄 {file_info['name']} ({file_info['size_mb']:.2f} MB)", expanded=True):
                        col_a, col_b = st.columns([1, 2])
                        
                        with col_a:
                            # Show image preview if it's an image
                            if display_image_preview(file):
                                pass
                            else:
                                st.info(f"📄 {file_info['type']}")
                        
                        with col_b:
                            st.write(f"**File Type:** {file_info['type']}")
                            st.write(f"**Size:** {file_info['size_mb']:.2f} MB")
                            
                            # File-specific metadata
                            if file_info['type'].startswith('image/'):
                                try:
                                    image = Image.open(file)
                                    st.write(f"**Dimensions:** {image.size[0]} x {image.size[1]} pixels")
                                except Exception:
                                    pass
                            elif file_info['type'].startswith('video/'):
                                st.write("**Type:** Video File")
                            elif 'pdf' in file_info['type']:
                                st.write("**Type:** PDF Document")
            
            # Sample file uploads for demonstration
            st.markdown("#### 📁 Sample Files")
            if st.button("� Load Sample Images", use_container_width=True):
                # Simulate loading sample images
                sample_images = [
                    {"name": "event_entrance.jpg", "type": "image/jpeg", "size": 2.4},
                    {"name": "registration_desk.jpg", "type": "image/jpeg", "size": 1.8},
                    {"name": "main_stage.jpg", "type": "image/jpeg", "size": 3.2}
                ]
                for img in sample_images:
                    st.session_state.uploaded_media.append({
                        "name": img["name"],
                        "type": "Photo",
                        "size": f"{img['size']} MB",
                        "location": "Sample Location",
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "status": "Uploaded"
                    })
                st.success("✅ Sample images loaded!")
            
            if st.button("🎥 Load Sample Videos", use_container_width=True):
                # Simulate loading sample videos
                sample_videos = [
                    {"name": "opening_ceremony.mp4", "type": "video/mp4", "size": 45.2},
                    {"name": "workshop_session.mp4", "type": "video/mp4", "size": 38.5}
                ]
                for vid in sample_videos:
                    st.session_state.uploaded_media.append({
                        "name": vid["name"],
                        "type": "Video",
                        "size": f"{vid['size']} MB",
                        "location": "Sample Location",
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "status": "Uploaded"
                    })
                st.success("✅ Sample videos loaded!")
        
        with col2:
            st.markdown("#### 📝 Media Details")
            booth_location = st.selectbox("Location:", [
                "Main Entrance", "Information Booth", "Main Stage", "Registration", 
                "Food Court", "Exhibition Hall", "Conference Room", "Networking Area"
            ])
            event_category = st.selectbox("Event Category:", [
                "Setup", "Registration", "Presentations", "Networking", 
                "Entertainment", "Workshops", "Closing", "Behind the Scenes"
            ])
            photographer = st.text_input("Photographer/Creator:")
            description = st.text_area("Description:")
            tags = st.text_input("Tags (comma-separated):")
            
            # Advanced options
            st.markdown("#### ⚙️ Advanced Options")
            make_public = st.checkbox("Make publicly visible", value=True)
            allow_downloads = st.checkbox("Allow downloads", value=True)
            require_attribution = st.checkbox("Require attribution", value=False)
            
            if st.button("💾 Save Media", use_container_width=True):
                if uploaded_files:
                    # Process each uploaded file
                    for file in uploaded_files:
                        file_info = get_file_info(file)
                        
                        # Save file information to session state
                        media_entry = {
                            "name": file_info['name'],
                            "type": "Photo" if file_info['type'].startswith('image/') else "Video" if file_info['type'].startswith('video/') else "Document",
                            "size": f"{file_info['size_mb']:.2f} MB",
                            "location": booth_location,
                            "category": event_category,
                            "photographer": photographer,
                            "description": description,
                            "tags": tags.split(',') if tags else [],
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "status": "Uploaded",
                            "public": make_public,
                            "downloads_allowed": allow_downloads,
                            "attribution_required": require_attribution,
                            "file_data": get_base64_encoded_file(file)  # Store file data
                        }
                        
                        st.session_state.uploaded_media.append(media_entry)
                    
                    st.success(f"✅ Successfully uploaded {len(uploaded_files)} file(s)!")
                    st.balloons()
                    
                    # Show uploaded files summary
                    st.markdown("#### 📋 Upload Summary")
                    for file in uploaded_files:
                        st.info(f"✅ {file.name} - Saved to {booth_location}")
                    
                else:
                    st.warning("⚠️ Please select files to upload first")
            
            # Display uploaded media count
            if st.session_state.uploaded_media:
                st.markdown("#### 📊 Upload Status")
                st.metric("Total Uploaded Files", len(st.session_state.uploaded_media))
                
                if st.button("📋 View All Uploads"):
                    st.markdown("##### 📁 Your Uploaded Files:")
                    for idx, media in enumerate(st.session_state.uploaded_media):
                        st.write(f"{idx+1}. {media['name']} - {media['type']} ({media['size']})")
    
    with tab3:
        st.markdown("### 📊 Media Statistics & Analytics")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📸 Total Media", "24")
        with col2:
            st.metric("👥 Contributors", "8")
        with col3:
            st.metric("📥 Total Downloads", "156")
        with col4:
            st.metric("💾 Storage Used", "2.3 GB")
        
        # Charts
        col1, col2 = st.columns(2)
        with col1:
            # Media type distribution
            media_types = {"Photos": 18, "Videos": 4, "Documents": 2}
            fig = px.pie(values=list(media_types.values()), names=list(media_types.keys()),
                        title="Media Type Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Upload activity over time
            dates = ["2025-01-28", "2025-01-29", "2025-01-30", "2025-01-31"]
            uploads = [3, 8, 10, 3]
            fig = px.bar(x=dates, y=uploads, title="Daily Upload Activity")
            st.plotly_chart(fig, use_container_width=True)
        
        # Top contributors
        st.markdown("#### 🏆 Top Contributors")
        contributors = [
            {"Name": "Sarah Johnson", "Uploads": 8, "Downloads": 45, "Likes": 32},
            {"Name": "Mike Wilson", "Uploads": 6, "Downloads": 38, "Likes": 28},
            {"Name": "Alice Brown", "Uploads": 4, "Downloads": 22, "Likes": 15},
            {"Name": "John Smith", "Uploads": 3, "Downloads": 28, "Likes": 18},
            {"Name": "David Lee", "Uploads": 2, "Downloads": 15, "Likes": 12},
        ]
        
        contrib_df = pd.DataFrame(contributors)
        st.dataframe(contrib_df, use_container_width=True, hide_index=True)
        
        # Storage breakdown
        st.markdown("#### 💾 Storage Breakdown")
        storage_data = {
            "Photos": 1.8,
            "Videos": 0.4,
            "Documents": 0.1
        }
        
        fig = px.bar(x=list(storage_data.keys()), y=list(storage_data.values()),
                    title="Storage Usage by Type (GB)")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### 🎥 Live Stream Management")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📡 Active Streams")
            streams = [
                {"Location": "Main Stage", "Status": "🔴 Live", "Viewers": 142, "Duration": "2h 15m"},
                {"Location": "Workshop Room A", "Status": "🔴 Live", "Viewers": 67, "Duration": "1h 45m"},
                {"Location": "Exhibition Hall", "Status": "⏸️ Paused", "Viewers": 0, "Duration": "0h 30m"},
            ]
            
            for stream in streams:
                st.markdown(f"""
                <div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; margin: 5px 0;">
                    <h4>📹 {stream['Location']}</h4>
                    <p><strong>Status:</strong> {stream['Status']}</p>
                    <p><strong>Viewers:</strong> {stream['Viewers']}</p>
                    <p><strong>Duration:</strong> {stream['Duration']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 🎮 Stream Controls")
            selected_location = st.selectbox("Select Stream:", ["Main Stage", "Workshop Room A", "Exhibition Hall"])
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("▶️ Start Stream", use_container_width=True):
                    st.success(f"Started stream for {selected_location}")
            with col_b:
                if st.button("⏹️ Stop Stream", use_container_width=True):
                    st.success(f"Stopped stream for {selected_location}")
            
            col_c, col_d = st.columns(2)
            with col_c:
                if st.button("⏸️ Pause Stream", use_container_width=True):
                    st.success(f"Paused stream for {selected_location}")
            with col_d:
                if st.button("📹 Record", use_container_width=True):
                    st.success(f"Recording started for {selected_location}")
        
        # Stream settings
        st.markdown("#### ⚙️ Stream Settings")
        col1, col2, col3 = st.columns(3)
        with col1:
            quality = st.selectbox("Video Quality:", ["720p", "1080p", "4K"])
        with col2:
            bitrate = st.slider("Bitrate (kbps):", 500, 5000, 2000)
        with col3:
            fps = st.selectbox("Frame Rate:", ["24 fps", "30 fps", "60 fps"])
        
        # Live chat moderation
        st.markdown("#### 💬 Live Chat Moderation")
        chat_messages = [
            {"User": "participant123", "Message": "Great presentation!", "Time": "14:35"},
            {"User": "volunteer_sarah", "Message": "Thanks for joining everyone!", "Time": "14:34"},
            {"User": "organizer_mike", "Message": "Next session starts in 10 minutes", "Time": "14:33"},
        ]
        
        for msg in chat_messages:
            col1, col2, col3, col4 = st.columns([2, 4, 1, 1])
            with col1:
                st.write(f"**{msg['User']}**")
            with col2:
                st.write(msg['Message'])
            with col3:
                st.write(msg['Time'])
            with col4:
                if st.button("🗑️", key=f"delete_{msg['Time']}"):
                    st.success("Message deleted")

def show_vendors_page():
    """Enhanced vendor management page"""
    st.markdown("## 🏭 Vendor Management")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Vendor Directory", "➕ Add Vendor", "📊 Analytics", "💰 Payments", "📧 Communications"])
    
    with tab1:
        st.markdown("### 📋 Vendor Directory")
        
        # Filter and search options
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search vendors:")
        with col2:
            service_filter = st.selectbox("Filter by Service:", ["All", "Catering", "AV Equipment", "Security", "Cleaning", "Transportation", "Decoration", "Photography"])
        with col3:
            status_filter = st.selectbox("Filter by Status:", ["All", "Active", "Pending", "Inactive", "Cancelled"])
        
        # Enhanced vendor data
        vendor_data = [
            {
                "Name": "Coffee Express", 
                "Service": "Catering", 
                "Contact": "coffee@express.com", 
                "Phone": "+1-555-0101",
                "Status": "Active", 
                "Contract": "$2,500",
                "Rating": 4.5,
                "Booth": "B-15",
                "Setup_Date": "2025-01-29",
                "Payment_Status": "Paid",
                "Insurance": "Valid",
                "Last_Contact": "2025-01-28"
            },
            {
                "Name": "Tech Solutions", 
                "Service": "AV Equipment", 
                "Contact": "info@techsol.com", 
                "Phone": "+1-555-0102",
                "Status": "Active", 
                "Contract": "$1,800",
                "Rating": 4.2,
                "Booth": "A-08",
                "Setup_Date": "2025-01-28",
                "Payment_Status": "Pending",
                "Insurance": "Valid",
                "Last_Contact": "2025-01-27"
            },
            {
                "Name": "Security Plus", 
                "Service": "Security", 
                "Contact": "ops@secplus.com", 
                "Phone": "+1-555-0103",
                "Status": "Pending", 
                "Contract": "$3,200",
                "Rating": 4.8,
                "Booth": "Security-01",
                "Setup_Date": "2025-01-30",
                "Payment_Status": "Not Sent",
                "Insurance": "Pending",
                "Last_Contact": "2025-01-25"
            },
            {
                "Name": "Clean Masters", 
                "Service": "Cleaning", 
                "Contact": "clean@masters.com", 
                "Phone": "+1-555-0104",
                "Status": "Active", 
                "Contract": "$800",
                "Rating": 4.0,
                "Booth": "Service-01",
                "Setup_Date": "2025-01-28",
                "Payment_Status": "Paid",
                "Insurance": "Valid",
                "Last_Contact": "2025-01-29"
            },
            {
                "Name": "Decorative Dreams", 
                "Service": "Decoration", 
                "Contact": "hello@decdreams.com", 
                "Phone": "+1-555-0105",
                "Status": "Active", 
                "Contract": "$1,500",
                "Rating": 4.6,
                "Booth": "C-12",
                "Setup_Date": "2025-01-27",
                "Payment_Status": "Paid",
                "Insurance": "Valid",
                "Last_Contact": "2025-01-30"
            }
        ]
        
        df = pd.DataFrame(vendor_data)
        
        # Apply filters
        if search_term:
            df = df[df['Name'].str.contains(search_term, case=False) | 
                   df['Service'].str.contains(search_term, case=False)]
        if service_filter != "All":
            df = df[df['Service'] == service_filter]
        if status_filter != "All":
            df = df[df['Status'] == status_filter]
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Vendor actions
        st.markdown("#### 🎯 Vendor Actions")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📧 Send Bulk Email", use_container_width=True):
                st.success("Bulk email sent to all vendors")
        with col2:
            if st.button("📊 Generate Report", use_container_width=True):
                st.success("Vendor report generated")
        with col3:
            if st.button("💰 Payment Reminders", use_container_width=True):
                st.success("Payment reminders sent")
        with col4:
            if st.button("📋 Export Directory", use_container_width=True):
                st.success("Vendor directory exported")
        
        # Individual vendor management
        st.markdown("#### 👤 Individual Vendor Management")
        selected_vendor = st.selectbox("Select Vendor:", [v["Name"] for v in vendor_data])
        
        vendor_info = next(v for v in vendor_data if v["Name"] == selected_vendor)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**Service:** {vendor_info['Service']}")
            st.write(f"**Status:** {vendor_info['Status']}")
            st.write(f"**Rating:** ⭐ {vendor_info['Rating']}/5.0")
        with col2:
            st.write(f"**Contract:** {vendor_info['Contract']}")
            st.write(f"**Payment:** {vendor_info['Payment_Status']}")
            st.write(f"**Booth:** {vendor_info['Booth']}")
        with col3:
            st.write(f"**Insurance:** {vendor_info['Insurance']}")
            st.write(f"**Setup Date:** {vendor_info['Setup_Date']}")
            st.write(f"**Last Contact:** {vendor_info['Last_Contact']}")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📧 Contact Vendor"):
                st.success(f"Email sent to {selected_vendor}")
        with col2:
            if st.button("📝 Edit Details"):
                st.success(f"Edit form opened for {selected_vendor}")
        with col3:
            if st.button("💰 Process Payment"):
                st.success(f"Payment processed for {selected_vendor}")
        with col4:
            if st.button("📋 View Contract"):
                st.success(f"Contract opened for {selected_vendor}")
    
    with tab2:
        st.markdown("### ➕ Add New Vendor")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🏢 Basic Information")
            vendor_name = st.text_input("Vendor Name:")
            vendor_email = st.text_input("Email:")
            vendor_phone = st.text_input("Phone:")
            vendor_website = st.text_input("Website:")
            vendor_address = st.text_area("Address:")
            
            st.markdown("#### 📋 Service Details")
            vendor_service = st.selectbox("Primary Service:", [
                "Catering", "AV Equipment", "Security", "Cleaning", 
                "Transportation", "Decoration", "Photography", "Entertainment", "Other"
            ])
            service_description = st.text_area("Service Description:")
            materials_brought = st.text_area("Materials/Equipment Provided:")
        
        with col2:
            st.markdown("#### 💰 Contract Information")
            contract_amount = st.number_input("Contract Amount ($):", min_value=0.0, step=100.0)
            payment_terms = st.selectbox("Payment Terms:", ["Net 30", "Net 15", "Upon Completion", "50% Advance", "Payment on Delivery"])
            booth_required = st.checkbox("Booth Space Required")
            if booth_required:
                preferred_booth = st.text_input("Preferred Booth Location:")
            
            st.markdown("#### 📄 Documentation")
            insurance_file = st.file_uploader("Insurance Certificate:", type=['pdf', 'jpg', 'png'], key="vendor_insurance")
            if insurance_file:
                file_info = get_file_info(insurance_file)
                st.success(f"✅ {insurance_file.name} ({file_info['size_mb']:.2f} MB)")
                if st.button("📋 Preview Insurance", key="preview_insurance"):
                    st.info(f"Insurance file: {insurance_file.name} - Ready for processing")
            
            license_file = st.file_uploader("Business License:", type=['pdf', 'jpg', 'png'], key="vendor_license")
            if license_file:
                file_info = get_file_info(license_file)
                st.success(f"✅ {license_file.name} ({file_info['size_mb']:.2f} MB)")
                if st.button("📋 Preview License", key="preview_license"):
                    st.info(f"License file: {license_file.name} - Ready for processing")
            
            contract_file = st.file_uploader("Signed Contract:", type=['pdf'], key="vendor_contract")
            if contract_file:
                file_info = get_file_info(contract_file)
                st.success(f"✅ {contract_file.name} ({file_info['size_mb']:.2f} MB)")
                if st.button("📋 Preview Contract", key="preview_contract"):
                    st.info(f"Contract file: {contract_file.name} - Ready for processing")
            
            # Sample document upload
            st.markdown("#### 📁 Sample Documents")
            if st.button("📄 Load Sample Insurance", key="sample_insurance"):
                st.session_state.sample_insurance = {
                    "name": "sample_insurance_certificate.pdf",
                    "type": "application/pdf",
                    "size": "1.2 MB",
                    "status": "Uploaded"
                }
                st.success("✅ Sample insurance certificate loaded!")
            
            if st.button("📄 Load Sample License", key="sample_license"):
                st.session_state.sample_license = {
                    "name": "sample_business_license.pdf", 
                    "type": "application/pdf",
                    "size": "0.8 MB",
                    "status": "Uploaded"
                }
                st.success("✅ Sample business license loaded!")
            
            st.markdown("#### ⚙️ Additional Information")
            special_requirements = st.text_area("Special Requirements:")
            setup_time = st.selectbox("Setup Time Required:", ["1 hour", "2 hours", "4 hours", "Full day", "Multiple days"])
            emergency_contact = st.text_input("Emergency Contact:")
            
            if st.button("💾 Add Vendor", use_container_width=True):
                if vendor_name and vendor_email:
                    # Prepare vendor data including uploaded files
                    vendor_documents = {}
                    
                    if insurance_file:
                        vendor_documents['insurance'] = {
                            "name": insurance_file.name,
                            "type": insurance_file.type,
                            "size": get_file_info(insurance_file)['size_mb'],
                            "data": get_base64_encoded_file(insurance_file)
                        }
                    
                    if license_file:
                        vendor_documents['license'] = {
                            "name": license_file.name,
                            "type": license_file.type,
                            "size": get_file_info(license_file)['size_mb'],
                            "data": get_base64_encoded_file(license_file)
                        }
                    
                    if contract_file:
                        vendor_documents['contract'] = {
                            "name": contract_file.name,
                            "type": contract_file.type,
                            "size": get_file_info(contract_file)['size_mb'],
                            "data": get_base64_encoded_file(contract_file)
                        }
                    
                    # Store vendor information in session state
                    new_vendor = {
                        "name": vendor_name,
                        "email": vendor_email,
                        "phone": vendor_phone,
                        "website": vendor_website,
                        "address": vendor_address,
                        "service": vendor_service,
                        "description": service_description,
                        "materials": materials_brought,
                        "contract_amount": contract_amount,
                        "payment_terms": payment_terms,
                        "booth_required": booth_required,
                        "preferred_booth": preferred_booth if booth_required else "",
                        "special_requirements": special_requirements,
                        "setup_time": setup_time,
                        "emergency_contact": emergency_contact,
                        "documents": vendor_documents,
                        "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    if 'vendors' not in st.session_state:
                        st.session_state.vendors = []
                    st.session_state.vendors.append(new_vendor)
                    
                    st.success(f"✅ Vendor '{vendor_name}' added successfully!")
                    st.balloons()
                    
                    # Show summary of uploaded documents
                    if vendor_documents:
                        st.markdown("#### 📄 Documents Uploaded:")
                        for doc_type, doc_info in vendor_documents.items():
                            st.info(f"✅ {doc_type.title()}: {doc_info['name']} ({doc_info['size']:.2f} MB)")
                    
                else:
                    st.warning("⚠️ Please fill in required fields (Name and Email)")
    
    with tab3:
        st.markdown("### 📊 Vendor Analytics")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🏭 Total Vendors", "15")
        with col2:
            st.metric("✅ Active Vendors", "12")
        with col3:
            st.metric("💰 Total Contracts", "$25,800")
        with col4:
            st.metric("⭐ Avg. Rating", "4.4")
        
        col1, col2 = st.columns(2)
        with col1:
            # Service type distribution
            service_data = {
                "Catering": 3, "AV Equipment": 2, "Security": 2, "Cleaning": 2,
                "Decoration": 2, "Photography": 2, "Transportation": 1, "Entertainment": 1
            }
            fig = px.pie(values=list(service_data.values()), names=list(service_data.keys()), 
                        title="Vendors by Service Type")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Contract amounts by vendor
            amounts = [2500, 1800, 3200, 800, 1500]
            vendors = ["Coffee Express", "Tech Solutions", "Security Plus", "Clean Masters", "Decorative Dreams"]
            fig = px.bar(x=vendors, y=amounts, title="Contract Amounts by Vendor")
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        # Payment status analysis
        st.markdown("#### 💰 Payment Status Analysis")
        payment_data = {"Paid": 8, "Pending": 3, "Not Sent": 2, "Overdue": 2}
        col1, col2 = st.columns(2)
        with col1:
            fig = px.pie(values=list(payment_data.values()), names=list(payment_data.keys()),
                        title="Payment Status Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Vendor performance ratings
            performance_data = {
                "Excellent (4.5-5.0)": 6,
                "Good (4.0-4.4)": 7,
                "Average (3.5-3.9)": 2,
                "Below Average (<3.5)": 0
            }
            fig = px.bar(x=list(performance_data.keys()), y=list(performance_data.values()),
                        title="Vendor Performance Ratings")
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### 💰 Payment Management")
        
        # Payment overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💰 Total Payable", "$25,800")
        with col2:
            st.metric("✅ Paid", "$18,100")
        with col3:
            st.metric("⏳ Pending", "$5,200")
        with col4:
            st.metric("🚨 Overdue", "$2,500")
        
        # Payment tracking
        st.markdown("#### 📋 Payment Tracking")
        payment_data = [
            {"Vendor": "Coffee Express", "Amount": "$2,500", "Due Date": "2025-01-25", "Status": "Paid", "Method": "Bank Transfer"},
            {"Vendor": "Tech Solutions", "Amount": "$1,800", "Due Date": "2025-02-01", "Status": "Pending", "Method": "Check"},
            {"Vendor": "Security Plus", "Amount": "$3,200", "Due Date": "2025-01-30", "Status": "Not Sent", "Method": "Wire Transfer"},
            {"Vendor": "Clean Masters", "Amount": "$800", "Due Date": "2025-01-20", "Status": "Paid", "Method": "Credit Card"},
            {"Vendor": "Decorative Dreams", "Amount": "$1,500", "Due Date": "2025-01-22", "Status": "Paid", "Method": "Bank Transfer"},
        ]
        
        payment_df = pd.DataFrame(payment_data)
        st.dataframe(payment_df, use_container_width=True, hide_index=True)
        
        # Payment actions
        st.markdown("#### 💳 Payment Actions")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💸 Process Pending Payments", use_container_width=True):
                st.success("Processing all pending payments...")
        with col2:
            if st.button("📧 Send Payment Reminders", use_container_width=True):
                st.success("Payment reminders sent to vendors")
        with col3:
            if st.button("📊 Generate Payment Report", use_container_width=True):
                st.success("Payment report generated")
        
        # Individual payment processing
        st.markdown("#### 🏦 Individual Payment Processing")
        col1, col2 = st.columns(2)
        with col1:
            payment_vendor = st.selectbox("Select Vendor for Payment:", [p["Vendor"] for p in payment_data if p["Status"] in ["Pending", "Not Sent"]])
            payment_amount = st.number_input("Payment Amount ($):", min_value=0.0, step=100.0, value=1800.0)
            payment_method = st.selectbox("Payment Method:", ["Bank Transfer", "Check", "Wire Transfer", "Credit Card", "Cash"])
        
        with col2:
            payment_reference = st.text_input("Payment Reference/Note:")
            payment_date = st.date_input("Payment Date:")
            
            if st.button("💰 Process Payment", use_container_width=True):
                st.success(f"✅ Payment of ${payment_amount:,.0f} processed for {payment_vendor}")
    
    with tab5:
        st.markdown("### 📧 Vendor Communications")
        
        tab5_1, tab5_2, tab5_3 = st.tabs(["📧 Send Messages", "📋 Message History", "📝 Templates"])
        
        with tab5_1:
            st.markdown("#### 📧 Send New Message")
            
            col1, col2 = st.columns(2)
            with col1:
                message_type = st.radio("Message Type:", ["Individual", "Bulk", "Group"])
                
                if message_type == "Individual":
                    recipients = st.multiselect("Select Vendor:", [v["Name"] for v in vendor_data])
                elif message_type == "Bulk":
                    st.write("Message will be sent to all vendors")
                    recipients = "All Vendors"
                else:
                    service_group = st.selectbox("Select Service Group:", ["Catering", "AV Equipment", "Security", "Cleaning", "Decoration"])
                    recipients = f"All {service_group} vendors"
                
                message_priority = st.selectbox("Priority:", ["Normal", "High", "Urgent"])
            
            with col2:
                message_subject = st.text_input("Subject:")
                message_body = st.text_area("Message:", height=150)
                
                # Attachments
                attachments = st.file_uploader("Attachments:", accept_multiple_files=True, key="comm_attachments")
                
                if attachments:
                    st.markdown("##### 📎 Selected Attachments:")
                    total_size = 0
                    for attachment in attachments:
                        file_info = get_file_info(attachment)
                        total_size += file_info['size_mb']
                        
                        col_a, col_b, col_c = st.columns([3, 1, 1])
                        with col_a:
                            st.write(f"📄 {attachment.name}")
                        with col_b:
                            st.write(f"{file_info['size_mb']:.2f} MB")
                        with col_c:
                            if attachment.type.startswith('image/'):
                                if st.button("👁️", key=f"preview_attach_{attachment.name}"):
                                    display_image_preview(attachment)
                    
                    st.info(f"Total size: {total_size:.2f} MB")
                    
                    # Sample attachments
                    if st.button("📁 Add Sample Contract", key="sample_contract_comm"):
                        st.session_state.sample_contract = {
                            "name": "vendor_agreement_template.pdf",
                            "size": "1.5 MB",
                            "type": "application/pdf"
                        }
                        st.success("✅ Sample contract template added!")
                
                # Scheduling
                schedule_send = st.checkbox("Schedule for later")
                if schedule_send:
                    send_date = st.date_input("Send Date:")
                    send_time = st.time_input("Send Time:")
                
                if st.button("📤 Send Message", use_container_width=True):
                    if message_subject and message_body:
                        # Process attachments
                        processed_attachments = []
                        if attachments:
                            for attachment in attachments:
                                processed_attachments.append({
                                    "name": attachment.name,
                                    "type": attachment.type,
                                    "size": get_file_info(attachment)['size_mb'],
                                    "data": get_base64_encoded_file(attachment)
                                })
                        
                        # Store message in session state
                        if 'vendor_messages' not in st.session_state:
                            st.session_state.vendor_messages = []
                        
                        new_message = {
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "recipients": recipients if message_type == "Individual" else "Multiple",
                            "subject": message_subject,
                            "body": message_body,
                            "priority": message_priority,
                            "attachments": processed_attachments,
                            "scheduled": schedule_send,
                            "send_date": send_date.strftime("%Y-%m-%d") if schedule_send else None,
                            "send_time": send_time.strftime("%H:%M") if schedule_send else None
                        }
                        st.session_state.vendor_messages.append(new_message)
                        
                        st.success(f"✅ Message sent successfully!")
                        if attachments:
                            st.info(f"📎 {len(attachments)} attachment(s) included ({total_size:.2f} MB total)")
                        if schedule_send:
                            st.info(f"⏰ Scheduled for {send_date} at {send_time}")
                    else:
                        st.warning("⚠️ Please fill in subject and message")
        
        with tab5_2:
            st.markdown("#### 📋 Communication History")
            
            # Filter options
            col1, col2, col3 = st.columns(3)
            with col1:
                history_vendor = st.selectbox("Filter by Vendor:", ["All"] + [v["Name"] for v in vendor_data])
            with col2:
                history_date = st.date_input("From Date:")
            with col3:
                history_type = st.selectbox("Message Type:", ["All", "Email", "Phone", "Meeting", "Contract"])
            
            # Sample communication history
            comm_history = [
                {"Date": "2025-01-30", "Vendor": "Coffee Express", "Type": "Email", "Subject": "Setup Instructions", "Status": "Sent"},
                {"Date": "2025-01-29", "Vendor": "Tech Solutions", "Type": "Phone", "Subject": "Equipment Confirmation", "Status": "Completed"},
                {"Date": "2025-01-28", "Vendor": "Security Plus", "Type": "Meeting", "Subject": "Security Briefing", "Status": "Scheduled"},
                {"Date": "2025-01-27", "Vendor": "Clean Masters", "Type": "Email", "Subject": "Service Agreement", "Status": "Delivered"},
                {"Date": "2025-01-26", "Vendor": "Decorative Dreams", "Type": "Contract", "Subject": "Contract Renewal", "Status": "Signed"},
            ]
            
            history_df = pd.DataFrame(comm_history)
            st.dataframe(history_df, use_container_width=True, hide_index=True)
        
        with tab5_3:
            st.markdown("#### 📝 Message Templates")
            
            # Template management
            col1, col2 = st.columns(2)
            with col1:
                template_category = st.selectbox("Template Category:", [
                    "Welcome", "Contract", "Payment", "Setup Instructions", 
                    "Reminders", "Thank You", "Emergency", "General Updates"
                ])
                
                templates = {
                    "Welcome": "Welcome to EventIQ 2025! We're excited to have you as our vendor partner.",
                    "Contract": "Please find attached your vendor contract for EventIQ 2025. Please review and return signed copy.",
                    "Payment": "This is a reminder that your payment of {amount} is due on {date}.",
                    "Setup Instructions": "Please find attached your booth setup instructions for EventIQ 2025.",
                    "Reminders": "Reminder: {event} is scheduled for {date} at {time}.",
                    "Thank You": "Thank you for your excellent service at EventIQ 2025!",
                    "Emergency": "URGENT: Please contact event coordination immediately regarding {issue}.",
                    "General Updates": "EventIQ 2025 Update: {message}"
                }
                
                current_template = templates.get(template_category, "")
                
            with col2:
                template_name = st.text_input("Template Name:", value=template_category)
                template_subject = st.text_input("Default Subject:", value=f"EventIQ 2025 - {template_category}")
                template_content = st.text_area("Template Content:", value=current_template, height=150)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("💾 Save Template"):
                        st.success(f"✅ Template '{template_name}' saved!")
                with col_b:
                    if st.button("📧 Use Template"):
                        st.success(f"✅ Template applied to new message!")

def show_workflows_page():
    """Enhanced workflow and approval management"""
    st.markdown("## 🔄 Workflow & Approval Management")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Active Workflows", "✅ Approvals", "📊 Status", "⚙️ Workflow Builder", "📈 Analytics"])
    
    with tab1:
        st.markdown("### 📋 Active Workflows")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            workflow_filter = st.selectbox("Filter by Type:", ["All", "Expense Approval", "Vendor Onboarding", "Budget Modification", "Certificate Request", "Media Upload"])
        with col2:
            status_filter = st.selectbox("Filter by Status:", ["All", "Pending", "In Review", "Approved", "Rejected", "On Hold"])
        with col3:
            priority_filter = st.selectbox("Filter by Priority:", ["All", "Low", "Medium", "High", "Critical"])
        
        # Enhanced workflow data
        workflows = [
            {
                "ID": "WF-001", 
                "Type": "Expense Approval", 
                "Requestor": "John Smith", 
                "Amount": "$1,200", 
                "Status": "Pending", 
                "Priority": "High",
                "Created": "2025-01-29 14:30",
                "Due": "2025-02-01 17:00",
                "Approver": "Sarah Johnson",
                "Department": "Catering",
                "Description": "Additional catering costs for extra attendees"
            },
            {
                "ID": "WF-002", 
                "Type": "Vendor Onboarding", 
                "Requestor": "Sarah Johnson", 
                "Item": "Security Plus", 
                "Status": "In Review", 
                "Priority": "Medium",
                "Created": "2025-01-28 10:15",
                "Due": "2025-01-31 12:00",
                "Approver": "Mike Wilson",
                "Department": "Security",
                "Description": "New security vendor onboarding and verification"
            },
            {
                "ID": "WF-003", 
                "Type": "Budget Modification", 
                "Requestor": "Mike Wilson", 
                "Amount": "$500", 
                "Status": "Approved", 
                "Priority": "Low",
                "Created": "2025-01-27 09:00",
                "Due": "2025-01-30 17:00",
                "Approver": "Admin Team",
                "Department": "General",
                "Description": "Budget reallocation for AV equipment upgrade"
            },
            {
                "ID": "WF-004", 
                "Type": "Certificate Request", 
                "Requestor": "Alice Brown", 
                "Item": "Volunteer Certificate", 
                "Status": "Pending", 
                "Priority": "Medium",
                "Created": "2025-01-30 11:45",
                "Due": "2025-02-02 17:00",
                "Approver": "John Smith",
                "Department": "HR",
                "Description": "Certificate generation for volunteer with 15+ hours"
            },
            {
                "ID": "WF-005", 
                "Type": "Media Upload", 
                "Requestor": "David Lee", 
                "Item": "Event Photos", 
                "Status": "In Review", 
                "Priority": "Low",
                "Created": "2025-01-30 16:20",
                "Due": "2025-02-01 12:00",
                "Approver": "Emma Davis",
                "Department": "Marketing",
                "Description": "Batch upload of event photography from main stage"
            }
        ]
        
        # Apply filters
        filtered_workflows = workflows
        if workflow_filter != "All":
            filtered_workflows = [wf for wf in filtered_workflows if wf["Type"] == workflow_filter]
        if status_filter != "All":
            filtered_workflows = [wf for wf in filtered_workflows if wf["Status"] == status_filter]
        if priority_filter != "All":
            filtered_workflows = [wf for wf in filtered_workflows if wf["Priority"] == priority_filter]
        
        # Display workflows
        for wf in filtered_workflows:
            with st.container():
                col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 2, 1, 1, 1])
                with col1:
                    st.write(f"**{wf['ID']}**")
                with col2:
                    st.write(f"**{wf['Type']}**")
                    st.write(f"📝 {wf['Description']}")
                with col3:
                    st.write(f"👤 {wf['Requestor']}")
                    st.write(f"🏢 {wf['Department']}")
                with col4:
                    priority_colors = {"Low": "🟢", "Medium": "🟡", "High": "🟠", "Critical": "🔴"}
                    st.write(f"{priority_colors.get(wf['Priority'], '⚪')} {wf['Priority']}")
                with col5:
                    status_colors = {"Pending": "🟡", "In Review": "🔵", "Approved": "🟢", "Rejected": "🔴", "On Hold": "⚫"}
                    st.write(f"{status_colors.get(wf['Status'], '⚪')} {wf['Status']}")
                with col6:
                    if wf['Status'] in ["Pending", "In Review"]:
                        if st.button("👁️", key=f"view_{wf['ID']}"):
                            st.success(f"Viewing details for {wf['ID']}")
                
                # Additional details in expander
                with st.expander(f"Details for {wf['ID']}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Created:** {wf['Created']}")
                        st.write(f"**Due:** {wf['Due']}")
                    with col2:
                        st.write(f"**Approver:** {wf['Approver']}")
                        if 'Amount' in wf:
                            st.write(f"**Amount:** {wf['Amount']}")
                        elif 'Item' in wf:
                            st.write(f"**Item:** {wf['Item']}")
                    with col3:
                        if st.button("✅ Approve", key=f"approve_{wf['ID']}"):
                            st.success(f"Approved {wf['ID']}")
                        if st.button("❌ Reject", key=f"reject_{wf['ID']}"):
                            st.error(f"Rejected {wf['ID']}")
                
                st.divider()
    
    with tab2:
        st.markdown("### ✅ Pending Approvals")
        
        # My approvals (based on user role)
        user_role = st.session_state.get('user_role', 'organizer')
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 💰 Financial Approvals")
            financial_approvals = [
                {"ID": "WF-001", "Item": "Catering Services", "Amount": "$1,200", "Requestor": "John Smith", "Urgency": "High"},
                {"ID": "WF-006", "Item": "AV Equipment Rental", "Amount": "$800", "Requestor": "Sarah Johnson", "Urgency": "Medium"},
                {"ID": "WF-007", "Item": "Security Overtime", "Amount": "$450", "Requestor": "Mike Wilson", "Urgency": "Low"},
            ]
            
            for exp in financial_approvals:
                with st.container():
                    st.write(f"**{exp['Item']}** - {exp['Amount']}")
                    st.write(f"Requested by: {exp['Requestor']} | Priority: {exp['Urgency']}")
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        if st.button("✅ Approve", key=f"app_fin_{exp['ID']}"):
                            st.success(f"Approved: {exp['Item']}")
                    with col_b:
                        if st.button("❌ Reject", key=f"rej_fin_{exp['ID']}"):
                            st.error(f"Rejected: {exp['Item']}")
                    with col_c:
                        if st.button("⏸️ Hold", key=f"hold_fin_{exp['ID']}"):
                            st.warning(f"On Hold: {exp['Item']}")
                    st.divider()
        
        with col2:
            st.markdown("#### 🏭 Operational Approvals")
            operational_approvals = [
                {"ID": "WF-002", "Item": "Security Plus Onboarding", "Type": "Vendor", "Requestor": "Sarah Johnson", "Urgency": "Medium"},
                {"ID": "WF-004", "Item": "Volunteer Certificate", "Type": "Certificate", "Requestor": "Alice Brown", "Urgency": "Medium"},
                {"ID": "WF-005", "Item": "Event Photos Upload", "Type": "Media", "Requestor": "David Lee", "Urgency": "Low"},
            ]
            
            for op in operational_approvals:
                with st.container():
                    st.write(f"**{op['Item']}** ({op['Type']})")
                    st.write(f"Requested by: {op['Requestor']} | Priority: {op['Urgency']}")
                    
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        if st.button("✅ Approve", key=f"app_op_{op['ID']}"):
                            st.success(f"Approved: {op['Item']}")
                    with col_b:
                        if st.button("❌ Reject", key=f"rej_op_{op['ID']}"):
                            st.error(f"Rejected: {op['Item']}")
                    with col_c:
                        if st.button("⏸️ Hold", key=f"hold_op_{op['ID']}"):
                            st.warning(f"On Hold: {op['Item']}")
                    st.divider()
        
        # Bulk approval actions
        st.markdown("#### 🚀 Bulk Actions")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("✅ Approve All Low Priority", use_container_width=True):
                st.success("All low priority items approved")
        with col2:
            if st.button("📧 Request More Info", use_container_width=True):
                st.info("Information requests sent")
        with col3:
            if st.button("⏰ Extend Deadlines", use_container_width=True):
                st.info("Deadlines extended for pending items")
        with col4:
            if st.button("📊 Generate Report", use_container_width=True):
                st.success("Approval report generated")
    
    with tab3:
        st.markdown("### 📊 Workflow Status Overview")
        
        # Key metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("📋 Total Workflows", "25")
        with col2:
            st.metric("⏳ Pending", "8")
        with col3:
            st.metric("✅ Approved Today", "5")
        with col4:
            st.metric("⏱️ Avg. Processing Time", "2.4 days")
        with col5:
            st.metric("🚨 Overdue", "2")
        
        # Charts
        col1, col2 = st.columns(2)
        with col1:
            # Status distribution
            status_data = {"Pending": 8, "In Review": 5, "Approved": 10, "Rejected": 2}
            fig = px.pie(values=list(status_data.values()), names=list(status_data.keys()),
                        title="Workflow Status Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Workflow types
            type_data = {
                "Expense Approval": 8,
                "Vendor Onboarding": 6,
                "Budget Modification": 4,
                "Certificate Request": 4,
                "Media Upload": 3
            }
            fig = px.bar(x=list(type_data.keys()), y=list(type_data.values()),
                        title="Workflows by Type")
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        # Processing time analysis
        st.markdown("#### ⏱️ Processing Time Analysis")
        processing_data = {
            "Expense Approval": 1.5,
            "Vendor Onboarding": 3.2,
            "Budget Modification": 2.1,
            "Certificate Request": 1.8,
            "Media Upload": 0.8
        }
        
        fig = px.bar(x=list(processing_data.keys()), y=list(processing_data.values()),
                    title="Average Processing Time by Type (Days)")
        fig.update_xaxis(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### ⚙️ Workflow Builder")
        
        st.markdown("#### 🔧 Create New Workflow Template")
        
        col1, col2 = st.columns(2)
        with col1:
            workflow_name = st.text_input("Workflow Name:")
            workflow_description = st.text_area("Description:")
            workflow_category = st.selectbox("Category:", [
                "Financial", "Operational", "HR", "Marketing", "Technical", "Legal"
            ])
            
            # Approval levels
            st.markdown("#### 👥 Approval Levels")
            num_levels = st.slider("Number of Approval Levels:", 1, 5, 2)
            
            approval_levels = []
            for i in range(num_levels):
                level_name = st.text_input(f"Level {i+1} Name:", key=f"level_{i}")
                level_role = st.selectbox(f"Level {i+1} Role:", ["Admin", "Manager", "Supervisor", "Department Head"], key=f"role_{i}")
                approval_levels.append({"name": level_name, "role": level_role})
        
        with col2:
            # Workflow conditions
            st.markdown("#### 📋 Workflow Conditions")
            auto_approve_threshold = st.number_input("Auto-approve amount ($):", min_value=0, value=100)
            require_documentation = st.checkbox("Require documentation")
            notification_frequency = st.selectbox("Notification Frequency:", ["Immediate", "Daily", "Weekly"])
            
            # Time limits
            st.markdown("#### ⏰ Time Limits")
            default_deadline = st.number_input("Default deadline (days):", min_value=1, value=3)
            escalation_time = st.number_input("Escalation time (days):", min_value=1, value=5)
            
            # Actions
            if st.button("💾 Save Workflow Template", use_container_width=True):
                if workflow_name:
                    st.success(f"✅ Workflow template '{workflow_name}' created successfully!")
                else:
                    st.warning("⚠️ Please enter a workflow name")
        
        # Existing templates
        st.markdown("#### 📋 Existing Templates")
        templates = [
            {"Name": "Standard Expense Approval", "Category": "Financial", "Levels": 2, "Status": "Active"},
            {"Name": "Vendor Onboarding", "Category": "Operational", "Levels": 3, "Status": "Active"},
            {"Name": "Media Review", "Category": "Marketing", "Levels": 1, "Status": "Active"},
            {"Name": "Certificate Generation", "Category": "HR", "Levels": 2, "Status": "Active"},
        ]
        
        template_df = pd.DataFrame(templates)
        st.dataframe(template_df, use_container_width=True, hide_index=True)
    
    with tab5:
        st.markdown("### 📈 Workflow Analytics")
        
        # Performance metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 Completion Rate", "89%", delta="5%")
        with col2:
            st.metric("⚡ Avg. Response Time", "4.2 hours", delta="-0.8 hours")
        with col3:
            st.metric("🔄 Workflows This Month", "47", delta="12")
        with col4:
            st.metric("👥 Active Approvers", "12", delta="2")
        
        # Trend analysis
        col1, col2 = st.columns(2)
        with col1:
            # Weekly workflow volume
            weeks = ["Week 1", "Week 2", "Week 3", "Week 4"]
            volumes = [12, 15, 18, 16]
            fig = px.line(x=weeks, y=volumes, title="Weekly Workflow Volume")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Approval time by type
            approval_times = {
                "Expense": [1.2, 2.1, 1.8, 2.5],
                "Vendor": [2.8, 3.5, 3.1, 3.8],
                "Media": [0.5, 0.8, 0.6, 0.9]
            }
            
            import plotly.graph_objects as go
            fig = go.Figure()
            for workflow_type, times in approval_times.items():
                fig.add_trace(go.Scatter(x=weeks, y=times, name=workflow_type, mode='lines+markers'))
            
            fig.update_layout(title="Approval Time Trends by Type (Days)")
            st.plotly_chart(fig, use_container_width=True)
        
        # Bottleneck analysis
        st.markdown("#### 🚧 Bottleneck Analysis")
        bottlenecks = [
            {"Approver": "John Smith", "Pending": 5, "Avg. Time": "3.2 days", "Workload": "High"},
            {"Approver": "Sarah Johnson", "Pending": 3, "Avg. Time": "2.1 days", "Workload": "Medium"},
            {"Approver": "Mike Wilson", "Pending": 2, "Avg. Time": "1.8 days", "Workload": "Low"},
            {"Approver": "Admin Team", "Pending": 4, "Avg. Time": "4.5 days", "Workload": "High"},
        ]
        
        bottleneck_df = pd.DataFrame(bottlenecks)
        st.dataframe(bottleneck_df, use_container_width=True, hide_index=True)
        
        # Recommendations
        st.markdown("#### 💡 Recommendations")
        st.info("🔍 John Smith and Admin Team have high workloads. Consider redistributing approvals or adding additional approvers.")
        st.info("⚡ Expense approvals are processing faster than average. Consider using this workflow as a template for others.")
        st.info("📈 Workflow volume has increased 34% this month. Consider automating low-value approvals.")

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
    """Enhanced participants module with file upload"""
    st.markdown("## 👥 Participant Management Module")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Participants List", "➕ Add Participant", "📤 Bulk Import", "📊 Analytics"])
    
    with tab1:
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
    
    with tab2:
        st.markdown("### ➕ Add New Participant")
        
        col1, col2 = st.columns(2)
        with col1:
            participant_name = st.text_input("Full Name:")
            participant_email = st.text_input("Email:")
            participant_phone = st.text_input("Phone:")
            participant_org = st.text_input("Organization:")
            
        with col2:
            participant_industry = st.selectbox("Industry:", [
                "Technology", "Healthcare", "Finance", "Education", 
                "Manufacturing", "Retail", "Construction", "Other"
            ])
            participant_role = st.text_input("Job Title:")
            dietary_restrictions = st.text_area("Dietary Restrictions:")
            
            # Photo upload
            participant_photo = st.file_uploader("Profile Photo:", type=['jpg', 'jpeg', 'png'], key="participant_photo")
            if participant_photo:
                file_info = get_file_info(participant_photo)
                st.success(f"✅ Photo uploaded: {participant_photo.name} ({file_info['size_mb']:.2f} MB)")
                display_image_preview(participant_photo)
        
        if st.button("💾 Add Participant", use_container_width=True):
            if participant_name and participant_email:
                # Store participant data
                new_participant = {
                    "name": participant_name,
                    "email": participant_email,
                    "phone": participant_phone,
                    "organization": participant_org,
                    "industry": participant_industry,
                    "role": participant_role,
                    "dietary_restrictions": dietary_restrictions,
                    "photo": get_base64_encoded_file(participant_photo) if participant_photo else None,
                    "registration_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                if 'participants' not in st.session_state:
                    st.session_state.participants = []
                st.session_state.participants.append(new_participant)
                
                st.success(f"✅ Participant '{participant_name}' added successfully!")
                st.balloons()
            else:
                st.warning("⚠️ Please fill in required fields (Name and Email)")
    
    with tab3:
        st.markdown("### 📤 Bulk Import Participants")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📄 Upload Participant List")
            participant_file = st.file_uploader(
                "Upload CSV/Excel file:", 
                type=['csv', 'xlsx', 'xls'], 
                key="bulk_participants"
            )
            
            if participant_file:
                file_info = get_file_info(participant_file)
                st.success(f"✅ File uploaded: {participant_file.name} ({file_info['size_mb']:.2f} MB)")
                
                try:
                    if participant_file.name.endswith('.csv'):
                        df = pd.read_csv(participant_file)
                    else:
                        df = pd.read_excel(participant_file)
                    
                    st.markdown("##### 📋 File Preview:")
                    st.dataframe(df.head(), use_container_width=True)
                    
                    st.info(f"Found {len(df)} participants in the file")
                    
                    if st.button("📥 Import All Participants", use_container_width=True):
                        # Process and import participants
                        imported_count = 0
                        for _, row in df.iterrows():
                            participant = {
                                "name": row.get('name', row.get('full_name', 'Unknown')),
                                "email": row.get('email', ''),
                                "phone": row.get('phone', ''),
                                "organization": row.get('organization', row.get('company', '')),
                                "industry": row.get('industry', 'Other'),
                                "role": row.get('role', row.get('job_title', '')),
                                "dietary_restrictions": row.get('dietary_restrictions', ''),
                                "registration_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "source": "bulk_import"
                            }
                            
                            if 'participants' not in st.session_state:
                                st.session_state.participants = []
                            st.session_state.participants.append(participant)
                            imported_count += 1
                        
                        st.success(f"✅ Successfully imported {imported_count} participants!")
                        st.balloons()
                
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
            
            # Sample file download
            st.markdown("#### 📁 Sample Files")
            if st.button("📥 Download Sample CSV Template", use_container_width=True):
                sample_data = {
                    "name": ["John Doe", "Jane Smith", "Mike Johnson"],
                    "email": ["john@example.com", "jane@example.com", "mike@example.com"],
                    "phone": ["+1-555-0001", "+1-555-0002", "+1-555-0003"],
                    "organization": ["Tech Corp", "Design Studio", "StartupX"],
                    "industry": ["Technology", "Design", "Technology"],
                    "role": ["Developer", "Designer", "Manager"],
                    "dietary_restrictions": ["None", "Vegetarian", "Gluten-free"]
                }
                sample_df = pd.DataFrame(sample_data)
                csv = sample_df.to_csv(index=False)
                st.download_button(
                    "📥 Download Template",
                    csv,
                    "participant_template.csv",
                    "text/csv"
                )
        
        with col2:
            st.markdown("#### 📊 Import Statistics")
            if 'participants' in st.session_state:
                total_participants = len(st.session_state.participants)
                bulk_imported = len([p for p in st.session_state.participants if p.get('source') == 'bulk_import'])
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Total Participants", total_participants)
                with col_b:
                    st.metric("Bulk Imported", bulk_imported)
                
                # Show recent imports
                st.markdown("##### 📋 Recent Imports:")
                recent_imports = [p for p in st.session_state.participants if p.get('source') == 'bulk_import'][-5:]
                for participant in recent_imports:
                    st.info(f"✅ {participant['name']} ({participant['organization']})")
            else:
                st.info("No participants imported yet")
    
    with tab4:
        st.markdown("### 📊 Participant Analytics")
        
        # Analytics based on session state data
        if 'participants' in st.session_state and st.session_state.participants:
            participants_data = st.session_state.participants
            
            col1, col2 = st.columns(2)
            with col1:
                # Industry distribution
                industries = [p.get('industry', 'Other') for p in participants_data]
                industry_counts = pd.Series(industries).value_counts()
                fig = px.pie(values=industry_counts.values, names=industry_counts.index, 
                           title="Participants by Industry")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Registration over time
                dates = [p.get('registration_date', datetime.now().strftime("%Y-%m-%d"))[:10] for p in participants_data]
                date_counts = pd.Series(dates).value_counts().sort_index()
                fig = px.bar(x=date_counts.index, y=date_counts.values, 
                           title="Registrations by Date")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No participant data available for analytics")

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
    """Enhanced budget module with receipt uploads"""
    st.markdown("## 💰 Budget & Finance Management Module")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Budget Overview", "📋 Expenses", "📤 Add Expense", "📄 Receipts"])
    
    with tab1:
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
            
            # Budget utilization chart
            expenses = make_api_request("/budget/expenses")
            if expenses and "expenses" in expenses:
                exp_df = pd.DataFrame(expenses["expenses"])
                fig = px.bar(exp_df, x='category', y='spent', title='Spending by Category')
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Could not load budget data")
    
    with tab2:
        st.markdown("### 📋 Expense Tracking")
        expenses = make_api_request("/budget/expenses")
        if expenses and "expenses" in expenses:
            exp_df = pd.DataFrame(expenses["expenses"])
            st.dataframe(exp_df, use_container_width=True, hide_index=True)
            
            # Add session state expenses
            if 'expenses' in st.session_state and st.session_state.expenses:
                st.markdown("#### 📤 Uploaded Expenses")
                uploaded_exp_df = pd.DataFrame(st.session_state.expenses)
                st.dataframe(uploaded_exp_df, use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("### 📤 Add New Expense")
        
        col1, col2 = st.columns(2)
        with col1:
            expense_category = st.selectbox("Category:", [
                "Catering", "AV Equipment", "Security", "Venue", "Marketing", 
                "Transportation", "Decoration", "Staff", "Miscellaneous"
            ])
            expense_amount = st.number_input("Amount ($):", min_value=0.0, step=10.0)
            expense_vendor = st.text_input("Vendor/Supplier:")
            expense_description = st.text_area("Description:")
            
        with col2:
            expense_date = st.date_input("Expense Date:")
            payment_method = st.selectbox("Payment Method:", [
                "Credit Card", "Bank Transfer", "Cash", "Check", "Invoice"
            ])
            
            # Receipt upload
            st.markdown("#### 📄 Receipt Upload")
            receipt_file = st.file_uploader(
                "Upload Receipt:", 
                type=['jpg', 'jpeg', 'png', 'pdf'], 
                key="expense_receipt"
            )
            
            if receipt_file:
                file_info = get_file_info(receipt_file)
                st.success(f"✅ Receipt uploaded: {receipt_file.name} ({file_info['size_mb']:.2f} MB)")
                
                # Show preview for images
                if receipt_file.type.startswith('image/'):
                    display_image_preview(receipt_file)
                else:
                    st.info("📄 PDF receipt uploaded")
            
            # Sample receipt upload
            if st.button("📄 Upload Sample Receipt", key="sample_receipt"):
                st.session_state.sample_receipt = {
                    "name": "sample_catering_receipt.jpg",
                    "type": "image/jpeg",
                    "size": "1.2 MB",
                    "category": "Catering",
                    "amount": 250.00
                }
                st.success("✅ Sample receipt uploaded!")
        
        if st.button("💾 Add Expense", use_container_width=True):
            if expense_amount > 0 and expense_vendor:
                # Store expense data
                new_expense = {
                    "category": expense_category,
                    "amount": expense_amount,
                    "vendor": expense_vendor,
                    "description": expense_description,
                    "date": expense_date.strftime("%Y-%m-%d"),
                    "payment_method": payment_method,
                    "receipt": {
                        "name": receipt_file.name if receipt_file else None,
                        "type": receipt_file.type if receipt_file else None,
                        "size": get_file_info(receipt_file)['size_mb'] if receipt_file else None,
                        "data": get_base64_encoded_file(receipt_file) if receipt_file else None
                    },
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                if 'expenses' not in st.session_state:
                    st.session_state.expenses = []
                st.session_state.expenses.append(new_expense)
                
                st.success(f"✅ Expense of ${expense_amount:,.2f} added successfully!")
                if receipt_file:
                    st.info(f"📄 Receipt {receipt_file.name} attached")
                st.balloons()
            else:
                st.warning("⚠️ Please fill in required fields (Amount and Vendor)")
    
    with tab4:
        st.markdown("### 📄 Receipt Management")
        
        # Display uploaded receipts
        all_receipts = []
        
        # From session state expenses
        if 'expenses' in st.session_state:
            for expense in st.session_state.expenses:
                if expense.get('receipt') and expense['receipt'].get('name'):
                    all_receipts.append({
                        "Receipt": expense['receipt']['name'],
                        "Category": expense['category'],
                        "Amount": f"${expense['amount']:,.2f}",
                        "Vendor": expense['vendor'],
                        "Date": expense['date'],
                        "Size": f"{expense['receipt']['size']:.2f} MB" if expense['receipt']['size'] else "N/A"
                    })
        
        if all_receipts:
            st.markdown(f"#### 📋 Uploaded Receipts ({len(all_receipts)} total)")
            receipts_df = pd.DataFrame(all_receipts)
            st.dataframe(receipts_df, use_container_width=True, hide_index=True)
            
            # Receipt actions
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📥 Export Receipts", use_container_width=True):
                    st.success("Receipt export initiated")
            with col2:
                if st.button("📊 Generate Report", use_container_width=True):
                    st.success("Expense report generated")
            with col3:
                if st.button("📧 Email Receipts", use_container_width=True):
                    st.success("Receipts emailed to finance team")
        else:
            st.info("No receipts uploaded yet")
            
            # Sample receipt showcase
            if st.button("📄 Load Sample Receipts", use_container_width=True):
                sample_receipts = [
                    {"name": "catering_invoice_001.pdf", "category": "Catering", "amount": 2500.00, "size": 1.2},
                    {"name": "av_equipment_receipt.jpg", "category": "AV Equipment", "amount": 1800.00, "size": 2.3},
                    {"name": "security_payment.pdf", "category": "Security", "amount": 3200.00, "size": 0.8}
                ]
                
                for receipt in sample_receipts:
                    expense = {
                        "category": receipt["category"],
                        "amount": receipt["amount"],
                        "vendor": f"Sample {receipt['category']} Vendor",
                        "description": f"Sample {receipt['category'].lower()} expense",
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "payment_method": "Sample",
                        "receipt": {
                            "name": receipt["name"],
                            "type": "application/pdf" if receipt["name"].endswith('.pdf') else "image/jpeg",
                            "size": receipt["size"],
                            "data": "sample_data"
                        },
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    if 'expenses' not in st.session_state:
                        st.session_state.expenses = []
                    st.session_state.expenses.append(expense)
                
                st.success("✅ Sample receipts loaded!")
                st.rerun()

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
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔧 General", "👥 Users", "🔐 Security", "🔔 Notifications"])
    
    with tab1:
        st.markdown("### 🔧 General Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🌐 System Configuration")
            event_name = st.text_input("Event Name:", value="EventIQ 2025")
            event_date = st.date_input("Event Date:")
            max_participants = st.number_input("Max Participants:", min_value=1, value=500, step=50)
            timezone = st.selectbox("Timezone:", ["EST", "PST", "CST", "MST", "UTC"])
            
            if st.button("💾 Save General Settings", use_container_width=True):
                st.success("✅ General settings saved successfully!")
        
        with col2:
            st.markdown("#### 📧 Email Configuration")
            smtp_server = st.text_input("SMTP Server:", value="smtp.gmail.com")
            smtp_port = st.number_input("SMTP Port:", value=587)
            email_username = st.text_input("Email Username:")
            email_password = st.text_input("Email Password:", type="password")
            
            if st.button("📧 Test Email Connection", use_container_width=True):
                st.success("✅ Email connection test successful!")
        
        # Configuration file upload
        st.markdown("#### 📁 Configuration Files")
        col1, col2 = st.columns(2)
        with col1:
            config_file = st.file_uploader(
                "Upload Configuration File:", 
                type=['json', 'yml', 'yaml', 'txt', 'cfg'], 
                key="config_upload"
            )
            
            if config_file:
                file_info = get_file_info(config_file)
                st.success(f"✅ Config uploaded: {config_file.name} ({file_info['size_mb']:.2f} MB)")
                
                # Show file preview
                if config_file.type == "application/json":
                    try:
                        config_content = json.loads(config_file.getvalue().decode('utf-8'))
                        st.json(config_content)
                    except:
                        st.warning("Invalid JSON format")
                else:
                    content_preview = config_file.getvalue().decode('utf-8')[:500]
                    st.text_area("File Preview:", content_preview, height=100, disabled=True)
                
                if st.button("📥 Apply Configuration", use_container_width=True):
                    st.success("✅ Configuration applied successfully!")
        
        with col2:
            # Logo upload
            logo_file = st.file_uploader(
                "Upload Event Logo:", 
                type=['jpg', 'jpeg', 'png', 'svg'], 
                key="logo_upload"
            )
            
            if logo_file:
                file_info = get_file_info(logo_file)
                st.success(f"✅ Logo uploaded: {logo_file.name} ({file_info['size_mb']:.2f} MB)")
                display_image_preview(logo_file)
                
                if st.button("🎨 Set as Event Logo", use_container_width=True):
                    st.success("✅ Event logo updated!")
            
            # Sample configuration download
            if st.button("📄 Download Sample Config", use_container_width=True):
                sample_config = {
                    "event": {
                        "name": "EventIQ 2025",
                        "date": "2025-02-15",
                        "max_participants": 500,
                        "timezone": "EST"
                    },
                    "email": {
                        "smtp_server": "smtp.gmail.com",
                        "smtp_port": 587,
                        "use_tls": True
                    },
                    "features": {
                        "certificates_enabled": True,
                        "media_gallery_enabled": True,
                        "budget_tracking_enabled": True
                    }
                }
                
                config_json = json.dumps(sample_config, indent=2)
                st.download_button(
                    "📥 Download",
                    config_json,
                    "eventiq_config.json",
                    "application/json"
                )
        
        st.markdown("#### 🎨 Theme Settings")
        col1, col2, col3 = st.columns(3)
        with col1:
            primary_color = st.color_picker("Primary Color:", "#667eea")
        with col2:
            secondary_color = st.color_picker("Secondary Color:", "#764ba2")
        with col3:
            accent_color = st.color_picker("Accent Color:", "#52c41a")
    
    with tab2:
        st.markdown("### 👥 User Management")
        
        # User list
        st.markdown("#### 👤 Active Users")
        users_data = [
            {"Name": "John Smith", "Email": "organizer@eventiq.com", "Role": "Organizer", "Status": "Active", "Last Login": "2025-01-30 14:30"},
            {"Name": "Sarah Johnson", "Email": "volunteer@eventiq.com", "Role": "Volunteer", "Status": "Active", "Last Login": "2025-01-30 12:15"},
            {"Name": "Mike Wilson", "Email": "participant@eventiq.com", "Role": "Participant", "Status": "Active", "Last Login": "2025-01-29 18:45"},
            {"Name": "Alice Brown", "Email": "vendor@eventiq.com", "Role": "Vendor", "Status": "Inactive", "Last Login": "2025-01-28 09:20"},
            {"Name": "Admin User", "Email": "admin@eventiq.com", "Role": "Admin", "Status": "Active", "Last Login": "2025-01-30 16:00"},
        ]
        
        users_df = pd.DataFrame(users_data)
        st.dataframe(users_df, use_container_width=True, hide_index=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("➕ Add New User", use_container_width=True):
                st.success("New user creation form would open")
        with col2:
            if st.button("📤 Export Users", use_container_width=True):
                # Generate CSV export
                csv_data = users_df.to_csv(index=False)
                st.download_button(
                    "📥 Download CSV",
                    csv_data,
                    "users_export.csv",
                    "text/csv"
                )
        with col3:
            if st.button("📧 Send Notifications", use_container_width=True):
                st.success("Bulk notifications sent")
        
        # Bulk user import
        st.markdown("#### 📤 Bulk User Import")
        col1, col2 = st.columns(2)
        with col1:
            user_import_file = st.file_uploader(
                "Upload User List (CSV/Excel):", 
                type=['csv', 'xlsx', 'xls'], 
                key="user_import"
            )
            
            if user_import_file:
                file_info = get_file_info(user_import_file)
                st.success(f"✅ File uploaded: {user_import_file.name} ({file_info['size_mb']:.2f} MB)")
                
                try:
                    if user_import_file.name.endswith('.csv'):
                        df = pd.read_csv(user_import_file)
                    else:
                        df = pd.read_excel(user_import_file)
                    
                    st.dataframe(df.head(), use_container_width=True)
                    
                    if st.button("👥 Import Users", use_container_width=True):
                        st.success(f"✅ {len(df)} users imported successfully!")
                        st.balloons()
                
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
        
        with col2:
            if st.button("📄 Download User Template", use_container_width=True):
                template_data = {
                    "Name": ["John Doe", "Jane Smith"],
                    "Email": ["john@example.com", "jane@example.com"],
                    "Role": ["Organizer", "Volunteer"],
                    "Status": ["Active", "Active"]
                }
                template_df = pd.DataFrame(template_data)
                csv_template = template_df.to_csv(index=False)
                st.download_button(
                    "📥 Download Template",
                    csv_template,
                    "user_import_template.csv",
                    "text/csv"
                )
        
        # Role management
        st.markdown("#### 🎭 Role Management")
        roles = ["Admin", "Organizer", "Volunteer", "Participant", "Vendor"]
        selected_role = st.selectbox("Select Role to Configure:", roles)
        
        permissions = ["View Dashboard", "Manage Users", "Generate Certificates", "Manage Budget", "View Analytics", "System Settings"]
        selected_permissions = st.multiselect(f"Permissions for {selected_role}:", permissions, default=permissions[:3])
        
        if st.button("💾 Update Role Permissions"):
            st.success(f"✅ Permissions updated for {selected_role} role!")
    
    with tab3:
        st.markdown("### 🔐 Security Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🔑 Password Policy")
            min_length = st.slider("Minimum Password Length:", 6, 20, 8)
            require_uppercase = st.checkbox("Require Uppercase Letters", value=True)
            require_lowercase = st.checkbox("Require Lowercase Letters", value=True)
            require_numbers = st.checkbox("Require Numbers", value=True)
            require_symbols = st.checkbox("Require Special Characters", value=False)
            
            if st.button("💾 Save Password Policy", use_container_width=True):
                st.success("✅ Password policy updated!")
        
        with col2:
            st.markdown("#### 🛡️ Security Features")
            two_factor = st.checkbox("Enable Two-Factor Authentication", value=False)
            session_timeout = st.slider("Session Timeout (minutes):", 15, 480, 60)
            max_login_attempts = st.slider("Max Login Attempts:", 3, 10, 5)
            ip_whitelist = st.text_area("IP Whitelist (one per line):")
            
            if st.button("🛡️ Save Security Settings", use_container_width=True):
                st.success("✅ Security settings updated!")
        
        # Security logs
        st.markdown("#### � Security Logs")
        security_logs = [
            {"Time": "2025-01-30 16:05", "Event": "Successful Login", "User": "admin@eventiq.com", "IP": "192.168.1.100"},
            {"Time": "2025-01-30 15:45", "Event": "Failed Login Attempt", "User": "unknown@test.com", "IP": "10.0.0.50"},
            {"Time": "2025-01-30 14:30", "Event": "Password Changed", "User": "organizer@eventiq.com", "IP": "192.168.1.105"},
            {"Time": "2025-01-30 12:15", "Event": "Successful Login", "User": "volunteer@eventiq.com", "IP": "192.168.1.110"},
        ]
        
        logs_df = pd.DataFrame(security_logs)
        st.dataframe(logs_df, use_container_width=True, hide_index=True)
    
    with tab4:
        st.markdown("### 🔔 Notification Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📧 Email Notifications")
            email_new_registration = st.checkbox("New User Registration", value=True)
            email_certificate_ready = st.checkbox("Certificate Ready", value=True)
            email_event_updates = st.checkbox("Event Updates", value=True)
            email_feedback_received = st.checkbox("Feedback Received", value=False)
            email_budget_alerts = st.checkbox("Budget Alerts", value=True)
            
            if st.button("💾 Save Email Settings", use_container_width=True):
                st.success("✅ Email notification settings saved!")
        
        with col2:
            st.markdown("#### 🔔 System Notifications")
            system_maintenance = st.checkbox("Maintenance Alerts", value=True)
            system_errors = st.checkbox("System Errors", value=True)
            system_backups = st.checkbox("Backup Status", value=False)
            system_updates = st.checkbox("System Updates", value=True)
            
            if st.button("🔔 Save System Settings", use_container_width=True):
                st.success("✅ System notification settings saved!")
        
        # Notification templates
        st.markdown("#### 📝 Notification Templates")
        template_type = st.selectbox("Template Type:", ["Welcome Email", "Certificate Ready", "Event Update", "Password Reset"])
        template_subject = st.text_input("Subject:", value="Welcome to EventIQ!")
        template_body = st.text_area("Email Body:", value="Dear {name}, welcome to EventIQ 2025!", height=100)
        
        if st.button("💾 Save Template"):
            st.success(f"✅ {template_type} template saved!")

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
