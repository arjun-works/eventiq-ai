"""
Participants Module for EventIQ Management System
Team Member: [Participants Management Team]
"""

from .utils import *

def show_participants_module():
    """Participants management interface"""
    st.markdown("## 👥 Participant Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Participants List", "➕ Add Participant", "📥 Bulk Import", "📊 Analytics"])
    
    with tab1:
        show_participants_list()
    
    with tab2:
        show_add_participant()
    
    with tab3:
        show_bulk_import()
    
    with tab4:
        show_participants_analytics()

def show_participants_list():
    """Display participants list with search and filters"""
    st.markdown("### 📋 Registered Participants")
    
    # Search and filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        search_term = st.text_input("🔍 Search participants:")
    with col2:
        organization_filter = st.selectbox("Filter by Organization:", ["All", "Tech Corp", "Design Studio", "StartupX"])
    with col3:
        status_filter = st.selectbox("Filter by Status:", ["All", "Registered", "Checked-in", "Cancelled"])
    
    # Sample participant data
    participants_data = get_sample_participants_data()
    df = pd.DataFrame(participants_data)
    
    # Apply filters
    if search_term:
        df = df[df['Name'].str.contains(search_term, case=False)]
    if organization_filter != "All":
        df = df[df['Organization'] == organization_filter]
    if status_filter != "All":
        df = df[df['Status'] == status_filter]
    
    st.dataframe(df, use_container_width=True, hide_index=True)

def show_add_participant():
    """Add individual participant interface"""
    st.markdown("### ➕ Add New Participant")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name:")
        email = st.text_input("Email:")
        phone = st.text_input("Phone:")
        organization = st.text_input("Organization:")
        industry = st.selectbox("Industry:", ["Technology", "Healthcare", "Finance", "Education", "Other"])
    
    with col2:
        role = st.text_input("Job Title/Role:")
        dietary_restrictions = st.text_area("Dietary Restrictions:")
        emergency_contact = st.text_input("Emergency Contact:")
        
        # Photo upload
        participant_photo = st.file_uploader("Profile Photo:", type=['jpg', 'jpeg', 'png'])
        if participant_photo:
            display_image_preview(participant_photo)
    
    if st.button("💾 Add Participant", use_container_width=True):
        if name and email:
            st.success(f"✅ Participant '{name}' added successfully!")
            show_success_animation()
        else:
            st.warning("⚠️ Please fill in required fields")

def show_bulk_import():
    """Bulk import participants from CSV"""
    st.markdown("### 📥 Bulk Import Participants")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📄 CSV Template")
        if st.button("📥 Download Sample CSV Template", use_container_width=True):
            csv_content = get_participants_csv_template()
            st.download_button(
                label="📥 Download Template",
                data=csv_content,
                file_name="participants_template.csv",
                mime="text/csv"
            )
    
    with col2:
        st.markdown("#### 📤 Upload CSV File")
        csv_file = st.file_uploader("Upload CSV/Excel file:", type=['csv', 'xlsx'])
        
        if csv_file:
            file_info = get_file_info(csv_file)
            st.success(f"✅ File selected: {csv_file.name} ({file_info['size_mb']:.2f} MB)")
            
            # Process and preview CSV
            if csv_file.type == 'text/csv':
                try:
                    df = pd.read_csv(csv_file)
                    st.markdown("##### 📋 Data Preview:")
                    st.dataframe(df.head(), use_container_width=True)
                    st.info(f"Found {len(df)} participants in the file")
                    
                    if st.button("📥 Import All Participants", use_container_width=True):
                        st.success(f"✅ Successfully imported {len(df)} participants!")
                        show_success_animation()
                except Exception as e:
                    st.error(f"Error processing CSV: {str(e)}")

def show_participants_analytics():
    """Display participants analytics"""
    st.markdown("### 📊 Participant Analytics")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Total Registered", "125")
    with col2:
        st.metric("✅ Checked-in", "98")
    with col3:
        st.metric("🏢 Organizations", "25")
    with col4:
        st.metric("🌍 Countries", "8")
    
    # Charts
    col1, col2 = st.columns(2)
    with col1:
        # Industry distribution
        industry_data = {"Technology": 45, "Healthcare": 25, "Finance": 20, "Education": 15, "Other": 20}
        fig = px.pie(values=list(industry_data.values()), names=list(industry_data.keys()),
                    title="Participants by Industry")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Registration over time
        dates = ["2025-01-28", "2025-01-29", "2025-01-30", "2025-01-31"]
        registrations = [15, 25, 35, 50]
        fig = px.line(x=dates, y=registrations, title="Registration Growth")
        st.plotly_chart(fig, use_container_width=True)

def get_sample_participants_data():
    """Get sample participants data"""
    return [
        {"Name": "John Doe", "Email": "john@techcorp.com", "Organization": "Tech Corp", "Industry": "Technology", "Status": "Registered"},
        {"Name": "Jane Smith", "Email": "jane@designstudio.com", "Organization": "Design Studio", "Industry": "Technology", "Status": "Checked-in"},
        {"Name": "Mike Johnson", "Email": "mike@startupx.com", "Organization": "StartupX", "Industry": "Technology", "Status": "Registered"},
        {"Name": "Sarah Wilson", "Email": "sarah@healthcare.com", "Organization": "Health Plus", "Industry": "Healthcare", "Status": "Checked-in"},
        {"Name": "David Brown", "Email": "david@finance.com", "Organization": "Finance Pro", "Industry": "Finance", "Status": "Registered"},
    ]

def get_participants_csv_template():
    """Get CSV template for participants import"""
    return """name,email,phone,organization,industry,role,dietary_restrictions
John Doe,john@example.com,+1-555-0001,Tech Corp,Technology,Software Developer,None
Jane Smith,jane@example.com,+1-555-0002,Design Studio,Design,UI/UX Designer,Vegetarian
Mike Johnson,mike@example.com,+1-555-0003,StartupX,Technology,Product Manager,Gluten-free"""
