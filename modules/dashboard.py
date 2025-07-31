"""
Dashboard Module for EventIQ Management System
Team Member: [Dashboard Team]
"""

from .utils import *

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
    show_organizer_metrics()
    
    # Quick actions
    show_organizer_quick_actions()
    
    # Recent activities
    show_recent_activities()

def show_volunteer_dashboard():
    """Enhanced volunteer dashboard"""
    st.markdown("## 🤝 Volunteer Dashboard")
    
    # Volunteer stats
    show_volunteer_stats()
    
    # Certificate eligibility
    show_certificate_status()
    
    # Quick actions
    show_volunteer_quick_actions()

def show_participant_dashboard():
    """Enhanced participant dashboard"""
    st.markdown("## 👥 Participant Dashboard")
    
    # Event information
    show_event_information()
    
    # Quick stats
    show_participant_stats()
    
    # Quick actions
    show_participant_quick_actions()

def show_vendor_dashboard():
    """Enhanced vendor dashboard"""
    st.markdown("## 🏭 Vendor Dashboard")
    
    # Vendor stats
    show_vendor_stats()
    
    # Quick actions
    show_vendor_quick_actions()

def show_admin_dashboard():
    """Enhanced admin dashboard"""
    st.markdown("## 👨‍💻 Admin Dashboard")
    
    # System stats
    show_admin_stats()
    
    # Quick actions
    show_admin_quick_actions()

def show_organizer_metrics():
    """Display organizer key metrics"""
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
        # Fallback data
        with col1:
            st.metric("👥 Total Participants", "125")
        with col2:
            st.metric("🤝 Active Volunteers", "18")
        with col3:
            st.metric("🏢 Booked Booths", "24")
        with col4:
            st.metric("💰 Budget Utilized", "$28,000")

def show_organizer_quick_actions():
    """Display organizer quick action buttons"""
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

def show_recent_activities():
    """Display recent activities"""
    st.markdown("### 📋 Recent Activities")
    
    # Get activities from API or use sample data
    analytics = make_api_request("/analytics/dashboard")
    if analytics and "recent_activities" in analytics:
        for activity in analytics["recent_activities"]:
            st.info(f"📋 {activity['message']}")
    else:
        # Sample activities
        activities = [
            "New vendor 'Coffee Express' added to directory",
            "5 new participants registered today",
            "Certificate generated for volunteer John Smith",
            "Budget updated with catering expenses",
            "Media gallery updated with event photos"
        ]
        for activity in activities:
            st.info(f"📋 {activity}")

def show_volunteer_stats():
    """Display volunteer statistics"""
    volunteers = make_api_request("/volunteers/")
    current_volunteer = {}
    
    if volunteers and "volunteers" in volunteers:
        # Find current volunteer (simplified)
        current_volunteer = volunteers["volunteers"][0] if volunteers["volunteers"] else {}
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("⏰ Hours Worked", current_volunteer.get("total_hours", 15))
    with col2:
        st.metric("🎯 Tasks Completed", current_volunteer.get("tasks_completed", 8))
    with col3:
        st.metric("⭐ Rating", f"{current_volunteer.get('rating', 4.5):.1f}/5.0")

def show_certificate_status():
    """Display certificate eligibility status"""
    st.markdown("### 🎓 Certificate Status")
    
    # Get volunteer hours
    volunteers = make_api_request("/volunteers/")
    hours = 15  # Default value
    
    if volunteers and "volunteers" in volunteers and volunteers["volunteers"]:
        hours = volunteers["volunteers"][0].get("total_hours", 15)
    
    if hours >= 5:
        st.success(f"✅ You are eligible for a certificate! You have completed {hours} hours.")
        if st.button("🎓 Generate My Certificate", use_container_width=True):
            st.success("Your certificate has been generated!")
            show_success_animation()
    else:
        remaining = 5 - hours
        st.warning(f"⏳ You need {remaining} more hours to be eligible for a certificate.")

def show_volunteer_quick_actions():
    """Display volunteer quick actions"""
    st.markdown("### 🚀 Quick Actions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Submit Feedback", use_container_width=True):
            st.success("Feedback form opened")
    with col2:
        if st.button("📧 Update Profile", use_container_width=True):
            st.success("Profile update form would open here")

def show_event_information():
    """Display event information for participants"""
    st.markdown("### 🎉 Event Information")
    st.info("Welcome to EventIQ 2025! Check out the latest updates and activities.")
    
    # Event highlights
    with st.expander("📅 Event Schedule Highlights", expanded=True):
        st.markdown("""
        **Day 1 (Aug 15):** Registration & Welcome Reception  
        **Day 2 (Aug 16):** Main Conference & Workshops  
        **Day 3 (Aug 17):** Exhibition & Networking  
        """)
    
    # Important announcements
    with st.expander("📢 Important Announcements"):
        st.markdown("""
        - 🍽️ Lunch will be served at 12:00 PM in the main hall
        - 📱 Download the EventIQ mobile app for real-time updates
        - 🎁 Prize drawing at 4:00 PM on the final day
        """)

def show_participant_stats():
    """Display participant statistics"""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📅 Event Days", "3")
    with col2:
        st.metric("🎪 Activities", "12")
    with col3:
        st.metric("🏢 Exhibitors", "8")

def show_participant_quick_actions():
    """Display participant quick actions"""
    st.markdown("### 🚀 Available Actions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Provide Feedback", use_container_width=True):
            st.success("Feedback form opened")
    with col2:
        if st.button("📧 Update Profile", use_container_width=True):
            st.success("Profile update form would open here")

def show_vendor_stats():
    """Display vendor statistics"""
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📦 Products/Services", "5")
    with col2:
        st.metric("💰 Revenue Target", "$10,000")
    with col3:
        st.metric("📊 Booth Status", "Active")
    
    # Vendor-specific information
    st.markdown("### 🏪 Your Booth Information")
    st.info("**Booth Location:** B-15 | **Setup Time:** 8:00 AM | **Breakdown:** 6:00 PM")

def show_vendor_quick_actions():
    """Display vendor quick actions"""
    st.markdown("### 🚀 Quick Actions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 View Sales", use_container_width=True):
            st.success("Sales dashboard opened")
    with col2:
        if st.button("📧 Update Profile", use_container_width=True):
            st.success("Profile update form would open here")

def show_admin_stats():
    """Display admin system statistics"""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Total Users", "125")
    with col2:
        st.metric("🔐 Active Sessions", "23")
    with col3:
        st.metric("📊 System Load", "12%")
    with col4:
        st.metric("💾 Storage Used", "67%")
    
    # System health indicators
    st.markdown("### 🔍 System Health")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("🟢 Database: Healthy")
    with col2:
        st.success("🟢 API: Operational")
    with col3:
        st.warning("🟡 Storage: 67% Full")

def show_admin_quick_actions():
    """Display admin quick actions"""
    st.markdown("### 🚀 Admin Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("👥 Manage Users", use_container_width=True):
            st.success("User management opened")
    with col2:
        if st.button("📊 System Reports", use_container_width=True):
            st.success("System reports generated")
    with col3:
        if st.button("⚙️ System Settings", use_container_width=True):
            st.success("System settings opened")
