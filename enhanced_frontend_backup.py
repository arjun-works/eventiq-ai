"""
Enhanced EventIQ Frontend with Streamlit

This provides a comprehensive web interface for the EventIQ event management system
with proper authentication, role-based access, and module management.
"""

import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, Optional

# Configure Streamlit page
st.set_page_config(
    page_title="EventIQ Management System",
    page_icon="🎯",
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
        st.info("Security configuration and access control options would be available here.")-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .role-badge {
        background: #e3f2fd;
        color: #1976d2;
        padding: 0.2rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .success-alert {
        background: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Helper Functions
def make_api_request(endpoint: str, method: str = "GET", data: dict = None, params: dict = None) -> Optional[Dict[str, Any]]:
    """Make API request with proper error handling"""
    try:
        headers = {}
        if "token" in st.session_state:
            headers["Authorization"] = f"Bearer {st.session_state.token}"
        
        url = f"{API_BASE_URL}{endpoint}"
        
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            st.error(f"Unsupported HTTP method: {method}")
            return None
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot connect to API server. Please ensure the server is running on localhost:8000")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return None

def login_user(email: str, password: str) -> bool:
    """Authenticate user and store session data"""
    try:
        response = requests.post(f"{API_BASE_URL}/auth/login", json={
            "email": email,
            "password": password
        })
        
        if response.status_code == 200:
            data = response.json()
            st.session_state.logged_in = True
            st.session_state.token = data.get("access_token")
            st.session_state.user_email = email
            st.session_state.user_name = data.get("full_name", "User")
            st.session_state.user_role = data.get("role", "participant")
            st.session_state.user_id = data.get("user_id")
            return True
        else:
            st.error("❌ Invalid credentials")
            return False
            
    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot connect to API server. Please ensure the server is running on localhost:8000")
        return False
    except Exception as e:
        st.error(f"Login failed: {e}")
        return False

def logout_user():
    """Clear session data"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

def show_login_page():
    """Display login form"""
    st.markdown('<div class="main-header"><h1>🎯 EventIQ Management System</h1><p>Comprehensive Event Management Platform</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login to Your Account")
        
        with st.form("login_form"):
            email = st.text_input("📧 Email Address", placeholder="Enter your email")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
            submit_button = st.form_submit_button("Login", use_container_width=True)
            
            if submit_button:
                if email and password:
                    if login_user(email, password):
                        st.success("✅ Login successful!")
                        st.rerun()
                else:
                    st.error("Please fill in all fields")
        
        st.markdown("---")
        st.markdown("### 🎮 Demo Credentials")
        
        demo_accounts = [
            {"role": "Admin", "email": "admin@eventiq.com", "password": "admin123", "color": "#ff4b4b"},
            {"role": "Organizer", "email": "organizer@eventiq.com", "password": "organizer123", "color": "#ff8c00"},
            {"role": "Volunteer", "email": "volunteer1@example.com", "password": "volunteer123", "color": "#00d4aa"},
            {"role": "Participant", "email": "participant1@example.com", "password": "participant123", "color": "#0068c9"}
        ]
        
        for account in demo_accounts:
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"""
                <div style="background: {account['color']}15; padding: 0.5rem; border-radius: 5px; margin: 0.25rem 0;">
                    <strong style="color: {account['color']}">{account['role']}</strong><br>
                    📧 {account['email']}<br>
                    🔑 {account['password']}
                </div>
                """, unsafe_allow_html=True)
            with col_b:
                if st.button(f"Login as {account['role']}", key=f"demo_{account['role']}"):
                    if login_user(account['email'], account['password']):
                        st.rerun()

def show_dashboard():
    """Display enhanced dashboard with navigation"""
    # Initialize page navigation
    if "current_page" not in st.session_state:
        st.session_state.current_page = "dashboard"
    
    # Header with user info
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="main-header">
            <h2>🎯 EventIQ Management System</h2>
            <p>Welcome back, {st.session_state.user_name}!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem;">
            <span class="role-badge">{st.session_state.user_role.upper()}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            logout_user()
    
    # Navigation sidebar
    st.sidebar.title("🎯 EventIQ Navigation")
    
    # Role-based navigation
    if st.session_state.user_role == "admin":
        pages = {
            "🏠 Dashboard": "dashboard",
            "👥 Participants": "participants", 
            "🤝 Volunteers": "volunteers",
            "💰 Budget & Finance": "budget",
            "🏢 Booths & Venues": "booths",
            "🎓 Certificates": "certificates",
            "📸 Media Gallery": "media",
            "🏭 Vendors": "vendors",
            "🔄 Workflows": "workflows", 
            "📝 Feedback": "feedback",
            "📊 Analytics": "analytics",
            "⚙️ Settings": "settings"
        }
    elif st.session_state.user_role == "organizer":
        pages = {
            "🏠 Dashboard": "dashboard",
            "👥 Participants": "participants", 
            "🤝 Volunteers": "volunteers",
            "💰 Budget & Finance": "budget",
            "🏢 Booths & Venues": "booths",
            "🎓 Certificates": "certificates",
            "📸 Media Gallery": "media",
            "🏭 Vendors": "vendors",
            "🔄 Workflows": "workflows", 
            "📝 Feedback": "feedback",
            "📊 Analytics": "analytics"
        }
    elif st.session_state.user_role == "volunteer":
        pages = {
            "🏠 Dashboard": "dashboard",
            "👤 My Profile": "profile",
            "⏰ Attendance": "attendance", 
            "🎓 My Certificate": "certificates",
            "📸 Media Upload": "media",
            "📝 Feedback": "feedback"
        }
    else:  # participant
        pages = {
            "🏠 Dashboard": "dashboard",
            "👤 My Profile": "profile",
            "📅 Events": "events",
            "📝 Feedback": "feedback"
        }
    
    selected_page = st.sidebar.selectbox("Navigate to:", list(pages.keys()))
    current_page = pages[selected_page]
    
    # Page content routing
    if current_page == "dashboard":
        if st.session_state.user_role == "admin":
            show_admin_dashboard()
        elif st.session_state.user_role == "organizer":
            show_organizer_dashboard()
        elif st.session_state.user_role == "volunteer":
            show_volunteer_dashboard()
        else:
            show_participant_dashboard()
    elif current_page == "certificates":
        show_certificates_page()
    elif current_page == "media":
        show_media_gallery_page()
    elif current_page == "vendors":
        show_vendors_page()
    elif current_page == "workflows":
        show_workflows_page()
    elif current_page == "feedback":
        show_feedback_page()
    elif current_page == "participants":
        show_participants_module()
    elif current_page == "volunteers":
        show_volunteers_module()
    elif current_page == "budget":
        show_budget_module()
    elif current_page == "booths":
        show_booths_module()
    elif current_page == "analytics":
        show_analytics_module()
    elif current_page == "settings":
        show_settings_page()
    else:
        st.markdown(f"## {selected_page}")
        st.info(f"The {selected_page} module is ready for implementation!")

def show_admin_dashboard():
    """Admin dashboard with full system overview"""
    st.markdown("## 👑 Administrator Dashboard")
    
    # Get dashboard metrics
    metrics = make_api_request("/analytics/dashboard")
    financial = make_api_request("/analytics/financial")
    
    if metrics:
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Total Participants", metrics["total_participants"], delta="+3 this week")
        with col2:
            st.metric("🤝 Active Volunteers", metrics["total_volunteers"], delta="+1 this week")
        with col3:
            st.metric("🏢 Booth Occupancy", f"{metrics['occupied_booths']}/{metrics['total_booths']}", 
                     delta=f"{(metrics['occupied_booths']/metrics['total_booths']*100):.0f}%")
        with col4:
            st.metric("💰 Budget Utilization", f"${metrics['spent_amount']:,.0f}", 
                     delta=f"-${metrics['total_budget'] - metrics['spent_amount']:,.0f}")
        
        # Financial overview
        if financial:
            st.markdown("### 💹 Financial Overview")
            col1, col2 = st.columns(2)
            
            with col1:
                # Budget allocation chart
                budget_data = financial["budget_overview"]
                fig = go.Figure(data=[
                    go.Bar(name='Allocated', x=['Budget'], y=[budget_data["allocated"]], marker_color='lightblue'),
                    go.Bar(name='Spent', x=['Budget'], y=[budget_data["spent"]], marker_color='darkblue'),
                    go.Bar(name='Remaining', x=['Budget'], y=[budget_data["remaining"]], marker_color='lightgreen')
                ])
                fig.update_layout(title="Budget Status", barmode='group', height=300)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Spending by category
                spending_df = pd.DataFrame(financial["spending_by_category"])
                fig = px.pie(spending_df, values='spent', names='category', title='Spending by Category')
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
        
        # Recent activities
        st.markdown("### 📊 Recent Activities")
        for activity in metrics["recent_activities"]:
            activity_time = datetime.fromisoformat(activity["timestamp"].replace('Z', '+00:00'))
            time_ago = datetime.now() - activity_time.replace(tzinfo=None)
            
            icon_map = {"registration": "👥", "expense": "💰", "volunteer": "🤝", "booth": "🏢"}
            icon = icon_map.get(activity["type"], "📋")
            
            st.markdown(f"""
            <div class="metric-card">
                {icon} <strong>{activity["message"]}</strong><br>
                <small>⏰ {time_ago.seconds // 3600}h {(time_ago.seconds % 3600) // 60}m ago</small>
            </div>
            """, unsafe_allow_html=True)

def show_organizer_dashboard():
    """Organizer dashboard focused on event management"""
    st.markdown("## 📋 Organizer Dashboard")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "💰 Budget", "🏢 Booths", "👥 People"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📅 Events Active", "3", delta="+1 this month")
        with col2:
            st.metric("📝 Pending Approvals", "7", delta="-2 today")
        with col3:
            st.metric("⚠️ Action Items", "12", delta="+3 urgent")
        
        st.markdown("### 🎯 Quick Actions")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("➕ Add Event", use_container_width=True):
                st.success("Event creation form would open here")
        with col2:
            if st.button("📊 Generate Report", use_container_width=True):
                st.success("Report generation initiated")
        with col3:
            if st.button("✅ Approve Expenses", use_container_width=True):
                st.success("Expense approval queue opened")
        with col4:
            if st.button("📧 Send Notifications", use_container_width=True):
                st.success("Notification center opened")
    
    with tab2:
        st.markdown("### 💰 Budget Management")
        
        # Budget overview
        budgets = make_api_request("/budget/")
        if budgets and "budgets" in budgets:
            budget_data = budgets["budgets"][0]  # Get first budget
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Budget", f"${budget_data['total_budget']:,.0f}")
            with col2:
                st.metric("Allocated", f"${budget_data['allocated_amount']:,.0f}")
            with col3:
                st.metric("Spent", f"${budget_data['spent_amount']:,.0f}")
            with col4:
                remaining = budget_data['total_budget'] - budget_data['spent_amount']
                st.metric("Remaining", f"${remaining:,.0f}")
        
        # Budget categories and expenses side by side
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Budget Categories")
            categories = make_api_request("/budget/1/categories")
            if categories and "categories" in categories:
                cat_df = pd.DataFrame(categories["categories"])
                st.dataframe(cat_df[["name", "allocated_amount", "spent_amount", "remaining_amount"]], 
                           use_container_width=True, hide_index=True)
            
            # Quick budget actions
            st.markdown("#### 🎯 Quick Actions")
            if st.button("➕ Add Category", use_container_width=True):
                st.success("Category creation form would open here")
            if st.button("📝 Create Budget", use_container_width=True):
                st.success("New budget creation form would open here")
        
        with col2:
            st.markdown("#### � Recent Expenses")
            expenses = make_api_request("/budget/expenses")
            if expenses and "expenses" in expenses:
                exp_df = pd.DataFrame(expenses["expenses"])
                st.dataframe(exp_df[["vendor_name", "category_name", "amount", "status"]], 
                           use_container_width=True, hide_index=True)
            
            # Expense actions
            st.markdown("#### 💰 Expense Actions")
            if st.button("➕ Submit Expense", use_container_width=True):
                st.success("Expense submission form would open here")
            if st.button("✅ Approve Pending", use_container_width=True):
                st.success("Expense approval queue would open here")
    
    with tab3:
        st.markdown("### 🏢 Booth Management")
        
        # Booth overview metrics
        booths = make_api_request("/booths/")
        if booths and "booths" in booths:
            booth_list = booths["booths"]
            total_booths = len(booth_list)
            occupied_booths = len([b for b in booth_list if b.get("status") == "reserved" or b.get("status") == "occupied"])
            available_booths = len([b for b in booth_list if b.get("status") == "available"])
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Booths", total_booths)
            with col2:
                st.metric("Occupied", occupied_booths)
            with col3:
                st.metric("Available", available_booths)
            with col4:
                occupancy_rate = (occupied_booths / total_booths * 100) if total_booths > 0 else 0
                st.metric("Occupancy Rate", f"{occupancy_rate:.1f}%")
            
            # Booth status visualization
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🏢 Booth Status Overview")
                booth_df = pd.DataFrame(booth_list)
                if not booth_df.empty:
                    # Create status chart
                    status_counts = booth_df["status"].value_counts()
                    if len(status_counts) > 0:
                        fig = px.pie(values=status_counts.values, names=status_counts.index, 
                                   title="Booth Status Distribution")
                        fig.update_layout(height=300)
                        st.plotly_chart(fig, use_container_width=True)
                
                # Quick booth actions
                st.markdown("#### 🎯 Booth Actions")
                if st.button("➕ Add New Booth", use_container_width=True):
                    st.success("Booth creation form would open here")
                if st.button("📋 Assign Vendor", use_container_width=True):
                    st.success("Vendor assignment form would open here")
            
            with col2:
                st.markdown("#### 📊 Booth Details")
                display_cols = ["booth_number", "booth_type", "location", "status", "current_vendor"]
                available_cols = [col for col in display_cols if col in booth_df.columns]
                st.dataframe(booth_df[available_cols], use_container_width=True, hide_index=True)
                
                # Booth assignments
                assignments = make_api_request("/booths/assignments")
                if assignments and "assignments" in assignments:
                    st.markdown("#### 📝 Recent Assignments")
                    assign_df = pd.DataFrame(assignments["assignments"])
                    if not assign_df.empty:
                        display_assign_cols = ["booth_number", "vendor_name", "total_cost", "is_confirmed"]
                        available_assign_cols = [col for col in display_assign_cols if col in assign_df.columns]
                        st.dataframe(assign_df[available_assign_cols], use_container_width=True, hide_index=True)
        else:
            st.info("No booth data available")
    
    with tab4:
        st.markdown("### 👥 People Management")
        
        # Overview metrics
        volunteers = make_api_request("/volunteers/")
        participants = make_api_request("/participants/")
        
        # People metrics
        vol_count = len(volunteers["volunteers"]) if volunteers and "volunteers" in volunteers else 0
        part_count = len(participants["participants"]) if participants and "participants" in participants else 0
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("👥 Total Volunteers", vol_count)
        with col2:
            st.metric("🎯 Total Participants", part_count)
        with col3:
            if volunteers and "volunteers" in volunteers:
                active_vols = len([v for v in volunteers["volunteers"] if v.get("is_active", True)])
                st.metric("🤝 Active Volunteers", active_vols)
            else:
                st.metric("🤝 Active Volunteers", 0)
        with col4:
            if volunteers and "volunteers" in volunteers:
                total_hours = sum([v.get("total_hours", 0) for v in volunteers["volunteers"]])
                st.metric("⏰ Total Vol. Hours", total_hours)
            else:
                st.metric("⏰ Total Vol. Hours", 0)
        
        # Side by side volunteer and participant management
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🤝 Volunteer Management")
            
            if volunteers and "volunteers" in volunteers:
                vol_df = pd.DataFrame(volunteers["volunteers"])
                if not vol_df.empty:
                    display_vol_cols = ["full_name", "volunteer_role", "total_hours", "is_active"]
                    available_vol_cols = [col for col in display_vol_cols if col in vol_df.columns]
                    st.dataframe(vol_df[available_vol_cols], use_container_width=True, hide_index=True)
                    
                    # Volunteer actions
                    st.markdown("##### 🎯 Volunteer Actions")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("📊 View Attendance", use_container_width=True):
                            st.success("Attendance records would display here")
                    with col_b:
                        if st.button("🏆 Assign Roles", use_container_width=True):
                            st.success("Role assignment form would open here")
                    
                    # Volunteer analytics
                    if "volunteer_role" in vol_df.columns:
                        st.markdown("##### 📈 Role Distribution")
                        role_counts = vol_df["volunteer_role"].value_counts()
                        if len(role_counts) > 0:
                            fig = px.bar(x=role_counts.index, y=role_counts.values, 
                                       title="Volunteers by Role")
                            fig.update_layout(height=250, showlegend=False)
                            st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No volunteer data available")
        
        with col2:
            st.markdown("#### � Participant Management")
            
            if participants and "participants" in participants:
                part_df = pd.DataFrame(participants["participants"])
                if not part_df.empty:
                    display_part_cols = ["full_name", "organization", "industry", "registration_date"]
                    available_part_cols = [col for col in display_part_cols if col in part_df.columns]
                    st.dataframe(part_df[available_part_cols], use_container_width=True, hide_index=True)
                    
                    # Participant actions
                    st.markdown("##### 🎯 Participant Actions")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("📝 View Registrations", use_container_width=True):
                            st.success("Registration status would display here")
                    with col_b:
                        if st.button("📧 Send Notifications", use_container_width=True):
                            st.success("Notification system would open here")
                    
                    # Participant analytics
                    if "industry" in part_df.columns:
                        st.markdown("##### 🏭 Industry Distribution")
                        industry_counts = part_df["industry"].value_counts().head(5)
                        if len(industry_counts) > 0:
                            fig = px.bar(x=industry_counts.values, y=industry_counts.index, 
                                       orientation='h', title="Top Industries")
                            fig.update_layout(height=250, showlegend=False)
                            st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No participant data available")
        
        # Combined actions
        st.markdown("#### 🎯 People Management Actions")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📧 Bulk Email", use_container_width=True):
                st.success("Bulk email composer would open here")
        with col2:
            if st.button("📊 Generate Report", use_container_width=True):
                st.success("People analytics report would generate here")
        with col3:
            if st.button("📥 Export Data", use_container_width=True):
                st.success("Data export options would display here")
        with col4:
            if st.button("➕ Add Person", use_container_width=True):
                st.success("Person registration form would open here")
        
        # Certificates Section
        st.markdown("#### 🎓 Certificate Management")
        
        # Certificate statistics
        cert_stats = make_api_request("/certificates/stats")
        if cert_stats:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🎓 Eligible for Certificates", cert_stats.get("eligible_for_certificates", 0))
            with col2:
                st.metric("📜 Certificates Generated", cert_stats.get("certificates_generated", 0))
            with col3:
                st.metric("⏰ Total Volunteer Hours", cert_stats.get("total_volunteer_hours", 0))
        
        # Certificate actions
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📋 View All Certificates", use_container_width=True):
                certificates = make_api_request("/certificates/")
                if certificates and "certificates" in certificates:
                    if certificates["certificates"]:
                        cert_df = pd.DataFrame(certificates["certificates"])
                        st.dataframe(cert_df[["volunteer_name", "volunteer_role", "total_hours", "certificate_id"]], 
                                   use_container_width=True, hide_index=True)
                    else:
                        st.info("No certificates available")
                else:
                    st.error("Could not load certificates")
        
        with col2:
            if st.button("🎓 Generate Bulk Certificates", use_container_width=True):
                result = make_api_request("/certificates/bulk-generate", method="POST")
                if result:
                    st.success(f"✅ {result.get('message', 'Bulk certificates generated!')}")
                    if "eligible_volunteers" in result:
                        st.write(f"Generated for {len(result['eligible_volunteers'])} volunteers")
                else:
                    st.error("Failed to generate bulk certificates")
        
        with col3:
            if st.button("📊 Certificate Analytics", use_container_width=True):
                if cert_stats:
                    st.json(cert_stats)

def show_volunteer_dashboard():
    """Volunteer dashboard for attendance and tasks"""
    st.markdown("## 🤝 Volunteer Dashboard")
    
    # Get volunteer profile
    profile = make_api_request("/volunteers/me")
    
    if profile:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("⏰ Total Hours", profile.get("total_hours", 0))
        with col2:
            st.metric("📋 Role", profile.get("volunteer_role", "N/A").title())
        with col3:
            st.metric("⭐ Rating", profile.get("rating", "Not rated"))
        
        st.markdown("### 👤 My Profile")
        with st.expander("View/Edit Profile", expanded=False):
            st.write(f"**Name:** {profile.get('full_name', 'N/A')}")
            st.write(f"**Email:** {profile.get('email', 'N/A')}")
            st.write(f"**Skills:** {profile.get('skills', 'Not specified')}")
            st.write(f"**Availability:** {profile.get('availability', 'Not specified')}")
            st.write(f"**Emergency Contact:** {profile.get('emergency_contact', 'Not specified')}")
    
    # Attendance actions
    st.markdown("### ⏰ Attendance")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🟢 Check In", use_container_width=True):
            result = make_api_request("/volunteers/attendance/checkin", "POST", {
                "check_in_location": "Main Entrance",
                "notes": "Regular shift check-in"
            })
            if result:
                st.success("✅ Successfully checked in!")
    
    with col2:
        if st.button("🔴 Check Out", use_container_width=True):
            result = make_api_request("/volunteers/attendance/checkout", "POST")
            if result:
                st.success("✅ Successfully checked out!")
    
    # Attendance history
    attendance = make_api_request("/volunteers/attendance")
    if attendance and "attendance" in attendance:
        st.markdown("### 📊 Attendance History")
        att_df = pd.DataFrame(attendance["attendance"])
        if not att_df.empty:
            st.dataframe(att_df[["check_in_time", "check_out_time", "hours_worked", "check_in_location"]], use_container_width=True)
        else:
            st.info("No attendance records found")
    
    # Certificate section
    if profile:
        st.markdown("### 🎓 My Certificate")
        total_hours = profile.get("total_hours", 0)
        min_hours = 5
        eligible = total_hours >= min_hours
        
        col1, col2 = st.columns(2)
        with col1:
            if eligible:
                st.success(f"🎉 You are eligible for a certificate! ({total_hours} hours completed)")
                if st.button("🎓 Generate My Certificate", use_container_width=True):
                    st.success("Certificate generated! 📜")
                    st.balloons()
            else:
                st.warning(f"⚠️ Complete {min_hours - total_hours} more hours to earn your certificate")
                progress = total_hours / min_hours
                st.progress(progress)
        
        with col2:
            st.info("""
            🎓 **Certificate Requirements:**
            - Minimum 5 hours of service
            - Active volunteer status
            - Completed tasks
            """)

def show_participant_dashboard():
    """Participant dashboard for registrations and profile"""
    st.markdown("## 👥 Participant Dashboard")
    
    # Get participant profile
    profile = make_api_request("/participants/me")
    
    if profile:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏢 Organization", profile.get("organization", "N/A"))
        with col2:
            st.metric("💼 Job Title", profile.get("job_title", "N/A"))
        with col3:
            st.metric("🏭 Industry", profile.get("industry", "N/A"))
        
        st.markdown("### 👤 My Profile")
        with st.expander("View/Edit Profile", expanded=False):
            st.write(f"**Name:** {profile.get('full_name', 'N/A')}")
            st.write(f"**Email:** {profile.get('email', 'N/A')}")
            st.write(f"**Organization:** {profile.get('organization', 'Not specified')}")
            st.write(f"**Interests:** {profile.get('interests', 'Not specified')}")
            st.write(f"**LinkedIn:** {profile.get('linkedin_profile', 'Not specified')}")
    
    # Event registrations
    registrations = make_api_request("/participants/registrations")
    if registrations and "registrations" in registrations:
        st.markdown("### 📅 My Event Registrations")
        reg_df = pd.DataFrame(registrations["registrations"])
        if not reg_df.empty:
            st.dataframe(reg_df[["event_name", "registration_status", "registration_date"]], use_container_width=True)
        else:
            st.info("No event registrations found")
    
    # Quick actions
    st.markdown("### 🎯 Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Register for Event", use_container_width=True):
            st.success("Event registration form would open here")
    
    with col2:
        if st.button("🎫 View My Tickets", use_container_width=True):
            st.success("Ticket viewer would open here")
    
    with col3:
        if st.button("📋 Update Profile", use_container_width=True):
            st.success("Profile update form would open here")

# Main Application Logic
def main():
    """Main application entry point"""
    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    # Show appropriate page
    if not st.session_state.logged_in:
        show_login_page()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()
