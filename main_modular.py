"""
EventIQ Management System - Modular Main Application
Team-based development with separate modules for each navigation section
"""

import streamlit as st
import sys
import os

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

# Import all modules
from modules.utils import *
from modules.dashboard import show_role_dashboard
from modules.event_setup import show_event_setup_module
from modules.certificates import show_certificates_page
from modules.media_gallery import show_media_gallery_page
from modules.vendors import show_vendors_page
from modules.participants import show_participants_module
from modules.budget import show_budget_module
from modules.settings import show_settings_page
from modules.volunteers import show_volunteers_module
from modules.booths import show_booths_module
from modules.workflows import show_workflows_page
from modules.feedback import show_feedback_page
from modules.analytics import show_analytics_module

# Page Configuration
st.set_page_config(
    page_title="EventIQ Management System",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="expanded"
)

def show_login_page():
    """Enhanced login page with demo accounts"""
    st.markdown("""
    <div style="text-align: center; padding: 50px 0;">
        <h1>🎉 EventIQ Management System</h1>
        <h3>Comprehensive Event Management Platform</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login")
        
        with st.form("login_form"):
            email = st.text_input("📧 Email:", value="organizer@eventiq.com")
            password = st.text_input("🔑 Password:", type="password", value="organizer123")
            login_submitted = st.form_submit_button("🚪 Login", use_container_width=True)
            
            if login_submitted:
                # Demo authentication logic
                demo_accounts = {
                    "organizer@eventiq.com": {"password": "organizer123", "role": "organizer", "name": "Event Organizer"},
                    "volunteer@eventiq.com": {"password": "volunteer123", "role": "volunteer", "name": "Volunteer User"},
                    "participant@eventiq.com": {"password": "participant123", "role": "participant", "name": "Participant User"},
                    "vendor@eventiq.com": {"password": "vendor123", "role": "vendor", "name": "Vendor User"},
                    "admin@eventiq.com": {"password": "admin123", "role": "admin", "name": "System Admin"}
                }
                
                if email in demo_accounts and demo_accounts[email]["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.session_state.user_role = demo_accounts[email]["role"]
                    st.session_state.user_name = demo_accounts[email]["name"]
                    
                    # Initialize session state for file uploads
                    if 'uploaded_media' not in st.session_state:
                        st.session_state.uploaded_media = []
                    
                    st.success(f"✅ Welcome, {demo_accounts[email]['name']}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
        
        # Demo accounts section
        st.markdown("---")
        st.markdown("### 🎯 Demo Accounts")
        
        demo_info = [
            ("👨‍💼 Event Organizer", "organizer@eventiq.com", "organizer123", "Full system access"),
            ("🤝 Volunteer", "volunteer@eventiq.com", "volunteer123", "Certificates & Feedback"),
            ("👥 Participant", "participant@eventiq.com", "participant123", "Basic access"),
            ("🏭 Vendor", "vendor@eventiq.com", "vendor123", "Vendor portal"),
            ("👨‍💻 Admin", "admin@eventiq.com", "admin123", "System administration")
        ]
        
        for role, demo_email, demo_pass, access in demo_info:
            with st.expander(f"{role} - {access}"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.code(f"Email: {demo_email}")
                with col_b:
                    st.code(f"Password: {demo_pass}")

def show_dashboard():
    """Main dashboard with navigation"""
    user_role = st.session_state.get('user_role', 'participant')
    user_email = st.session_state.get('user_email', '')
    user_name = st.session_state.get('user_name', '')
    
    # Header with logout
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.markdown(f"### 🎉 EventIQ Dashboard - {user_name}")
    with col2:
        st.markdown(f"👤 {user_email}")
    with col3:
        if st.button("🚪 Logout"):
            # Clear session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        st.markdown("---")
        
        # Role-based navigation menu
        if user_role == "organizer":
            navigation_options = [
                "🏠 Dashboard",
                "� Event Setup",
                "�🎓 Certificates", 
                "📸 Media Gallery",
                "🏭 Vendors",
                "👥 Participants",
                "🤝 Volunteers",
                "💰 Budget",
                "🏢 Booths",
                "🔄 Workflows",
                "📝 Feedback",
                "📊 Analytics",
                "⚙️ Settings"
            ]
        elif user_role == "volunteer":
            navigation_options = [
                "🏠 Dashboard",
                "🎓 My Certificates",
                "📝 Feedback",
                "⚙️ Profile"
            ]
        elif user_role == "participant":
            navigation_options = [
                "🏠 Dashboard",
                "📝 Feedback",
                "⚙️ Profile"
            ]
        elif user_role == "vendor":
            navigation_options = [
                "🏠 Dashboard",
                "🏭 Vendor Portal",
                "⚙️ Profile"
            ]
        elif user_role == "admin":
            navigation_options = [
                "🏠 Dashboard",
                "👥 User Management",
                "📊 System Analytics",
                "⚙️ System Settings"
            ]
        else:
            navigation_options = [
                "🏠 Dashboard",
                "⚙️ Profile"
            ]
        
        page = st.selectbox("🧭 Navigate to:", navigation_options)
        
        # Team member info
        st.markdown("---")
        st.markdown("### 👥 Development Team")
        team_modules = {
            "🏠 Dashboard": "Dashboard Team",
            "� Event Setup": "Event Setup Team",
            "�🎓 Certificates": "Certificate Team", 
            "📸 Media Gallery": "Media Team",
            "🏭 Vendors": "Vendor Team",
            "👥 Participants": "Participants Team",
            "💰 Budget": "Budget Team",
            "⚙️ Settings": "Settings Team",
            "🤝 Volunteers": "Volunteers Team",
            "🏢 Booths": "Booths Team",
            "🔄 Workflows": "Workflows Team",
            "📝 Feedback": "Feedback Team",
            "📊 Analytics": "Analytics Team"
        }
        
        current_module = team_modules.get(page, "Core Team")
        st.info(f"**Current Module:** {current_module}")
    
    # Page routing to respective modules
    route_to_page(page, user_role)

def route_to_page(page, user_role):
    """Route to the appropriate page/module"""
    try:
        if page == "🏠 Dashboard":
            show_role_dashboard(user_role)
        elif page == "� Event Setup":
            show_event_setup_module()
        elif page == "�🎓 Certificates" or page == "🎓 My Certificates":
            show_certificates_page()
        elif page == "📸 Media Gallery":
            show_media_gallery_page()
        elif page == "🏭 Vendors" or page == "🏭 Vendor Portal":
            show_vendors_page()
        elif page == "👥 Participants":
            show_participants_module()
        elif page == "🤝 Volunteers":
            show_volunteers_module()
        elif page == "💰 Budget":
            show_budget_module()
        elif page == "🏢 Booths":
            show_booths_module()
        elif page == "🔄 Workflows":
            show_workflows_page()
        elif page == "📝 Feedback":
            show_feedback_page()
        elif page == "📊 Analytics" or page == "📊 System Analytics":
            show_analytics_module()
        elif page == "⚙️ Settings" or page == "⚙️ Profile" or page == "⚙️ System Settings":
            show_settings_page()
        elif page == "👥 User Management":
            show_settings_page()  # Redirect to settings for user management
        else:
            st.error(f"Page '{page}' not found!")
            
    except Exception as e:
        st.error(f"Error loading module: {str(e)}")
        st.info("Please check if all module files are properly configured.")

def main():
    """Main application entry point"""
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
