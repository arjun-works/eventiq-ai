"""
Volunteers Management Module for EventIQ Management System
Team Member: [Volunteers Team]
"""

from .utils import *

def show_volunteers_module():
    """Volunteers management interface"""
    st.markdown("## 🤝 Volunteer Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["👥 Volunteers List", "➕ Add Volunteer", "📊 Analytics", "📄 Documents"])
    
    with tab1:
        st.markdown("### 👥 Active Volunteers")
        
        # Search and filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("🔍 Search volunteers:", placeholder="Enter name or role...")
        with col2:
            role_filter = st.selectbox("Filter by role:", ["All", "Registration", "Information", "Security", "Setup", "Cleanup"])
        with col3:
            status_filter = st.selectbox("Filter by status:", ["All", "Active", "Inactive", "On Break"])
        
        volunteers_data = [
            {"Name": "John Smith", "Role": "Registration", "Hours": 15, "Rating": 4.5, "Status": "Active", "Contact": "john@email.com"},
            {"Name": "Sarah Johnson", "Role": "Information", "Hours": 12, "Rating": 4.8, "Status": "Active", "Contact": "sarah@email.com"},
            {"Name": "Mike Wilson", "Role": "Security", "Hours": 20, "Rating": 4.2, "Status": "Active", "Contact": "mike@email.com"},
            {"Name": "Alice Brown", "Role": "Setup", "Hours": 8, "Rating": 4.6, "Status": "Active", "Contact": "alice@email.com"},
            {"Name": "Tom Davis", "Role": "Cleanup", "Hours": 6, "Rating": 4.3, "Status": "On Break", "Contact": "tom@email.com"},
        ]
        
        df = pd.DataFrame(volunteers_data)
        
        # Apply filters
        if search_term:
            df = df[df['Name'].str.contains(search_term, case=False) | 
                   df['Role'].str.contains(search_term, case=False)]
        if role_filter != "All":
            df = df[df['Role'] == role_filter]
        if status_filter != "All":
            df = df[df['Status'] == status_filter]
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📧 Send Announcement", use_container_width=True):
                st.success("Announcement sent to all volunteers!")
        with col2:
            if st.button("📅 Schedule Meeting", use_container_width=True):
                st.success("Meeting scheduled successfully!")
        with col3:
            if st.button("📊 Export Data", use_container_width=True):
                st.success("Volunteer data exported!")
    
    with tab2:
        st.markdown("### ➕ Add New Volunteer")
        
        with st.form("volunteer_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name:*")
                email = st.text_input("Email:*")
                phone = st.text_input("Phone:*")
                role = st.selectbox("Primary Role:*", ["Registration", "Information", "Security", "Setup", "Cleanup", "General Support"])
                age = st.number_input("Age:", min_value=16, max_value=80, value=25)
            
            with col2:
                availability = st.multiselect("Availability:*", ["Day 1", "Day 2", "Day 3", "Pre-Event", "Post-Event"])
                skills = st.text_area("Skills & Experience:")
                emergency_contact = st.text_input("Emergency Contact:")
                t_shirt_size = st.selectbox("T-Shirt Size:", ["XS", "S", "M", "L", "XL", "XXL"])
                dietary_restrictions = st.text_input("Dietary Restrictions:")
            
            # File uploads
            st.markdown("### 📄 Documents")
            col1, col2 = st.columns(2)
            with col1:
                resume = st.file_uploader("📄 Resume/CV", type=['pdf', 'doc', 'docx'])
                if resume:
                    st.success(f"✅ Resume uploaded: {resume.name}")
            
            with col2:
                id_document = st.file_uploader("🆔 ID Document", type=['pdf', 'jpg', 'png'])
                if id_document:
                    st.success(f"✅ ID document uploaded: {id_document.name}")
            
            # Agreement checkbox
            agreement = st.checkbox("I agree to the volunteer terms and conditions*")
            
            submitted = st.form_submit_button("🤝 Register Volunteer", use_container_width=True)
            
            if submitted:
                if name and email and phone and role and availability and agreement:
                    # Save files if uploaded
                    if resume:
                        save_uploaded_file(resume, f"volunteers/resumes/{name}_{resume.name}")
                    if id_document:
                        save_uploaded_file(id_document, f"volunteers/ids/{name}_{id_document.name}")
                    
                    st.success(f"✅ Volunteer '{name}' registered successfully!")
                    show_success_animation()
                    
                    # Send welcome email simulation
                    st.info(f"📧 Welcome email sent to {email}")
                else:
                    st.error("❌ Please fill in all required fields (*) and accept the terms")
    
    with tab3:
        st.markdown("### 📊 Volunteer Analytics")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("👥 Total Volunteers", "23", delta="3")
        with col2:
            st.metric("⏰ Total Hours", "358", delta="45")
        with col3:
            st.metric("⭐ Avg Rating", "4.5", delta="0.1")
        with col4:
            st.metric("✅ Retention Rate", "89%", delta="5%")
        
        # Charts
        col1, col2 = st.columns(2)
        with col1:
            # Volunteers by role
            roles = ["Registration", "Information", "Security", "Setup", "Cleanup"]
            counts = [8, 6, 4, 3, 2]
            fig = px.pie(values=counts, names=roles, title="Volunteers by Role")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Hours distribution
            volunteers = ["John", "Sarah", "Mike", "Alice", "Tom"]
            hours = [15, 12, 20, 8, 6]
            fig = px.bar(x=volunteers, y=hours, title="Volunteer Hours")
            st.plotly_chart(fig, use_container_width=True)
        
        # Performance tracking
        st.markdown("### 📈 Performance Tracking")
        performance_data = [
            {"Volunteer": "John Smith", "Tasks Completed": 12, "Rating": 4.5, "Punctuality": "95%"},
            {"Volunteer": "Sarah Johnson", "Tasks Completed": 10, "Rating": 4.8, "Punctuality": "100%"},
            {"Volunteer": "Mike Wilson", "Tasks Completed": 15, "Rating": 4.2, "Punctuality": "90%"},
        ]
        df_performance = pd.DataFrame(performance_data)
        st.dataframe(df_performance, use_container_width=True, hide_index=True)
    
    with tab4:
        st.markdown("### 📄 Volunteer Documents & Training")
        
        # Document upload section
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📋 Upload Training Materials")
            training_doc = st.file_uploader("Training Manual", type=['pdf', 'doc', 'docx'])
            if training_doc:
                saved_path = save_uploaded_file(training_doc, f"volunteers/training/{training_doc.name}")
                st.success(f"✅ Training document uploaded!")
                
                # Display document info
                file_info = get_file_info(saved_path)
                display_file_info(file_info)
        
        with col2:
            st.markdown("#### 📝 Upload Forms & Templates")
            form_doc = st.file_uploader("Volunteer Forms", type=['pdf', 'doc', 'docx'])
            if form_doc:
                saved_path = save_uploaded_file(form_doc, f"volunteers/forms/{form_doc.name}")
                st.success(f"✅ Form uploaded!")
                
                file_info = get_file_info(saved_path)
                display_file_info(file_info)
        
        # Training completion tracking
        st.markdown("#### 🎓 Training Completion Status")
        training_data = [
            {"Volunteer": "John Smith", "Safety Training": "✅", "Role Training": "✅", "Emergency Procedures": "✅"},
            {"Volunteer": "Sarah Johnson", "Safety Training": "✅", "Role Training": "✅", "Emergency Procedures": "⏳"},
            {"Volunteer": "Mike Wilson", "Safety Training": "✅", "Role Training": "⏳", "Emergency Procedures": "❌"},
        ]
        df_training = pd.DataFrame(training_data)
        st.dataframe(df_training, use_container_width=True, hide_index=True)
        
        # Bulk actions
        st.markdown("#### ⚡ Bulk Actions")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📧 Send Training Reminder", use_container_width=True):
                st.success("Training reminders sent!")
        with col2:
            if st.button("📊 Generate Training Report", use_container_width=True):
                st.success("Training report generated!")
        with col3:
            if st.button("🎓 Mark Training Complete", use_container_width=True):
                st.success("Training marked as complete!")
