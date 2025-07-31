"""
EventIQ Streamlit Frontend

Main Streamlit application for the EventIQ event management system.
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from typing import Dict, Any, Optional

# Page configuration
st.set_page_config(
    page_title="EventIQ - Event Management System",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API base URL
API_BASE_URL = "http://localhost:8000/api/v1"

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'access_token' not in st.session_state:
    st.session_state.access_token = None


def authenticate_user(email: str, password: str) -> bool:
    """Authenticate user with the API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            data={"username": email, "password": password}
        )
        if response.status_code == 200:
            token_data = response.json()
            st.session_state.access_token = token_data["access_token"]
            
            # Get user info
            headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
            user_response = requests.get(f"{API_BASE_URL}/auth/me", headers=headers)
            if user_response.status_code == 200:
                st.session_state.user_data = user_response.json()
                st.session_state.authenticated = True
                return True
        return False
    except Exception as e:
        st.error(f"Authentication error: {e}")
        return False


def logout():
    """Logout user"""
    st.session_state.authenticated = False
    st.session_state.user_data = None
    st.session_state.access_token = None
    st.rerun()


def get_headers() -> Dict[str, str]:
    """Get headers with authentication token"""
    return {"Authorization": f"Bearer {st.session_state.access_token}"}


def login_page():
    """Display login page"""
    st.title("🎪 EventIQ - Event Management System")
    st.markdown("### Welcome to EventIQ")
    st.markdown("Your comprehensive AI-powered event management platform")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("#### Sign In")
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit_button = st.form_submit_button("Sign In", type="primary", use_container_width=True)
            
            if submit_button:
                if email and password:
                    with st.spinner("Authenticating..."):
                        if authenticate_user(email, password):
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Invalid credentials. Please try again.")
                else:
                    st.error("Please enter both email and password.")
        
        st.markdown("---")
        st.markdown("#### Demo Credentials")
        demo_creds = [
            ("Admin", "admin@eventiq.com", "admin123"),
            ("Organizer", "organizer@eventiq.com", "organizer123"),
            ("Volunteer", "volunteer1@example.com", "volunteer123"),
            ("Participant", "participant1@example.com", "participant123")
        ]
        
        for role, email, password in demo_creds:
            if st.button(f"Login as {role}", key=f"demo_{role.lower()}", use_container_width=True):
                if authenticate_user(email, password):
                    st.success(f"Logged in as {role}!")
                    st.rerun()


def dashboard_overview():
    """Main dashboard overview"""
    st.title("📊 EventIQ Dashboard")
    
    # User welcome message
    user_name = st.session_state.user_data.get("full_name", "User")
    user_role = st.session_state.user_data.get("role", "user")
    st.markdown(f"### Welcome back, {user_name}! ({user_role.title()})")
    
    # Key metrics cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📝 Total Participants",
            value="150",
            delta="12 today"
        )
    
    with col2:
        st.metric(
            label="🙋‍♀️ Active Volunteers",
            value="22",
            delta="2 checked in"
        )
    
    with col3:
        st.metric(
            label="🏪 Active Booths",
            value="12",
            delta="All operational"
        )
    
    with col4:
        st.metric(
            label="💰 Budget Status",
            value="$15,450",
            delta="3% over budget"
        )
    
    # Two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Registration Trends")
        
        # Sample data for registration trends
        dates = pd.date_range(start="2025-07-20", end="2025-07-30", freq="D")
        registrations = [5, 8, 12, 15, 20, 25, 28, 35, 42, 48, 50]
        
        df = pd.DataFrame({
            "Date": dates,
            "Registrations": registrations
        })
        
        fig = px.line(df, x="Date", y="Registrations", 
                     title="Daily Registration Count",
                     markers=True)
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Booth Popularity")
        
        # Sample booth data
        booth_data = {
            "Booth": ["AI & ML Showcase", "Startup Hub", "Sustainable Tech", "Robotics Demo", "VR Experience"],
            "Visitors": [85, 72, 65, 58, 45]
        }
        
        fig = px.bar(booth_data, x="Booth", y="Visitors",
                    title="Visitors per Booth",
                    color="Visitors",
                    color_continuous_scale="viridis")
        fig.update_layout(height=300, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity section
    st.subheader("🔔 Recent Activity")
    
    activities = [
        {"time": "2 minutes ago", "activity": "New participant registered: John Smith", "type": "registration"},
        {"time": "5 minutes ago", "activity": "Volunteer checked in at Registration Desk", "type": "volunteer"},
        {"time": "10 minutes ago", "activity": "Feedback submitted for AI Showcase booth", "type": "feedback"},
        {"time": "15 minutes ago", "activity": "Budget item approved: Catering Services", "type": "budget"},
        {"time": "20 minutes ago", "activity": "New vendor added: TechRent Solutions", "type": "vendor"}
    ]
    
    for activity in activities:
        icon = {"registration": "📝", "volunteer": "🙋‍♀️", "feedback": "💬", "budget": "💰", "vendor": "🏢"}.get(activity["type"], "📋")
        st.markdown(f"{icon} **{activity['time']}** - {activity['activity']}")


def sidebar_navigation():
    """Sidebar navigation"""
    st.sidebar.markdown(f"### Hello, {st.session_state.user_data.get('full_name', 'User')}!")
    st.sidebar.markdown(f"**Role:** {st.session_state.user_data.get('role', 'user').title()}")
    
    st.sidebar.markdown("---")
    
    # Navigation menu
    menu_items = {
        "📊 Dashboard": "dashboard",
        "📝 Participants": "participants", 
        "🙋‍♀️ Volunteers": "volunteers",
        "🏪 Booths": "booths",
        "💰 Budget": "budget",
        "🏢 Vendors": "vendors",
        "📋 Workflows": "workflows",
        "💬 Feedback": "feedback",
        "🏆 Certificates": "certificates",
        "📸 Media": "media",
        "📈 Analytics": "analytics"
    }
    
    # Show admin menu for admin users
    if st.session_state.user_data.get('role') == 'admin':
        menu_items["⚙️ Admin"] = "admin"
    
    selected_page = st.sidebar.selectbox("Navigate to:", list(menu_items.keys()))
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        logout()
    
    return menu_items[selected_page]


def participants_page():
    """Participants management page"""
    st.title("📝 Participant Management")
    
    tab1, tab2, tab3 = st.tabs(["📋 Overview", "➕ Register New", "📊 Analytics"])
    
    with tab1:
        st.subheader("Registered Participants")
        
        # Sample participant data
        participants_data = {
            "Name": ["Carol Davis", "David Wilson", "Emma Johnson", "Frank Miller"],
            "Ticket": ["TK2025001", "TK2025002", "TK2025003", "TK2025004"],
            "Email": ["carol.davis@example.com", "david.wilson@example.com", "emma.johnson@example.com", "frank.miller@example.com"],
            "Status": ["Checked In", "Registered", "Checked In", "Registered"],
            "Registration Date": ["2025-07-20", "2025-07-21", "2025-07-22", "2025-07-23"]
        }
        
        df = pd.DataFrame(participants_data)
        st.dataframe(df, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 Export Participants", type="secondary"):
                st.success("Participant list exported successfully!")
        
        with col2:
            if st.button("📧 Send Notifications", type="secondary"):
                st.success("Notifications sent to all registered participants!")
    
    with tab2:
        st.subheader("Register New Participant")
        
        with st.form("participant_registration"):
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input("Full Name*")
                email = st.text_input("Email*")
                phone = st.text_input("Phone Number")
                organization = st.text_input("Organization")
            
            with col2:
                age_group = st.selectbox("Age Group", ["18-25", "26-35", "36-45", "46-55", "55+"])
                interests = st.multiselect("Interests", ["Technology", "Innovation", "Networking", "AI/ML", "Startups"])
                dietary_restrictions = st.multiselect("Dietary Restrictions", ["Vegetarian", "Vegan", "Gluten-free", "Halal", "Kosher"])
                accessibility_needs = st.text_area("Accessibility Needs")
            
            if st.form_submit_button("Register Participant", type="primary"):
                if full_name and email:
                    st.success(f"Participant {full_name} registered successfully!")
                    st.info(f"Ticket Number: TK{2025000 + len(participants_data['Name']) + 1}")
                else:
                    st.error("Please fill in all required fields.")
    
    with tab3:
        st.subheader("Participant Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Age group distribution
            age_data = {"Age Group": ["18-25", "26-35", "36-45", "46-55", "55+"], 
                       "Count": [45, 38, 32, 25, 10]}
            fig = px.pie(age_data, values="Count", names="Age Group", title="Age Group Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Registration source
            source_data = {"Source": ["Online", "Referral", "Walk-in", "Social Media"], 
                          "Count": [85, 35, 20, 10]}
            fig = px.bar(source_data, x="Source", y="Count", title="Registration Sources")
            st.plotly_chart(fig, use_container_width=True)


def volunteers_page():
    """Volunteers management page"""
    st.title("🙋‍♀️ Volunteer Management")
    
    tab1, tab2, tab3 = st.tabs(["👥 Active Volunteers", "📋 Attendance", "➕ Register New"])
    
    with tab1:
        st.subheader("Current Volunteers")
        
        volunteer_data = {
            "Name": ["Alice Johnson", "Bob Smith", "Charlie Brown", "Diana Ross"],
            "Role": ["Registration Assistant", "Technical Support", "Booth Guide", "Setup Crew"],
            "Booth": ["Registration Desk", "A1", "B2", "Main Hall"],
            "Hours": [8, 6, 4, 12],
            "Status": ["Checked In", "Checked In", "Break", "Checked Out"]
        }
        
        df = pd.DataFrame(volunteer_data)
        st.dataframe(df, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📊 Generate Report"):
                st.success("Volunteer report generated!")
        with col2:
            if st.button("🏆 Generate Certificates"):
                st.success("Certificates generated for all volunteers!")
        with col3:
            if st.button("📱 Send QR Codes"):
                st.success("QR codes sent to all volunteers!")
    
    with tab2:
        st.subheader("Attendance Tracking")
        
        # QR Code scanner simulation
        st.markdown("#### QR Code Check-in/Check-out")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📷 Scan QR Code", type="primary"):
                st.success("Volunteer checked in: Alice Johnson")
                st.info("Time: 09:15 AM | Booth: Registration Desk")
        
        with col2:
            manual_checkin = st.selectbox("Manual Check-in", ["Select Volunteer", "Alice Johnson", "Bob Smith", "Charlie Brown", "Diana Ross"])
            if st.button("✅ Manual Check-in"):
                if manual_checkin != "Select Volunteer":
                    st.success(f"{manual_checkin} checked in manually!")
    
    with tab3:
        st.subheader("Register New Volunteer")
        
        with st.form("volunteer_registration"):
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input("Full Name*")
                email = st.text_input("Email*")
                phone = st.text_input("Phone Number")
                emergency_contact = st.text_input("Emergency Contact")
            
            with col2:
                skills = st.multiselect("Skills", ["Communication", "Event Management", "Technical Support", "First Aid", "Photography"])
                experience = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Expert"])
                availability = st.multiselect("Available Time Slots", ["09:00-13:00", "13:00-17:00", "17:00-21:00"])
                preferred_roles = st.multiselect("Preferred Roles", ["Registration", "Technical Support", "Booth Guide", "Setup/Teardown"])
            
            if st.form_submit_button("Register Volunteer", type="primary"):
                if full_name and email:
                    st.success(f"Volunteer {full_name} registered successfully!")
                else:
                    st.error("Please fill in all required fields.")


def main():
    """Main application function"""
    if not st.session_state.authenticated:
        login_page()
    else:
        # Authenticated user interface
        page = sidebar_navigation()
        
        if page == "dashboard":
            dashboard_overview()
        elif page == "participants":
            participants_page()
        elif page == "volunteers":
            volunteers_page()
        else:
            st.title(f"🚧 {page.title()} Page")
            st.info("This page is under development. Check back soon!")
            st.markdown("### Available Features:")
            st.markdown("- Dashboard Overview ✅")
            st.markdown("- Participant Management ✅")
            st.markdown("- Volunteer Management ✅")
            st.markdown("- Other modules coming soon...")


if __name__ == "__main__":
    main()
