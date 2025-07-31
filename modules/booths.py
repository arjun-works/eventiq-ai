"""
Booths Management Module for EventIQ Management System
Team Member: [Booths Team]
"""

from .utils import *

def show_booths_module():
    """Booths management interface"""
    st.markdown("## 🏢 Booth Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🏢 Booth Layout", "📋 Reservations", "📊 Analytics", "📄 Documents"])
    
    with tab1:
        st.markdown("### 🏢 Exhibition Hall Layout")
        
        # Layout controls
        col1, col2, col3 = st.columns(3)
        with col1:
            hall_section = st.selectbox("Hall Section:", ["All", "Section A", "Section B", "Section C"])
        with col2:
            booth_status = st.selectbox("Filter by Status:", ["All", "Available", "Occupied", "Reserved", "Maintenance"])
        with col3:
            booth_size = st.selectbox("Filter by Size:", ["All", "3x3", "3x6", "6x6", "Custom"])
        
        booth_data = [
            {"Booth": "A-01", "Vendor": "Coffee Express", "Size": "3x3", "Status": "Occupied", "Power": "Yes", "WiFi": "Yes", "Price": "$500"},
            {"Booth": "A-02", "Vendor": "Tech Solutions", "Size": "3x6", "Status": "Occupied", "Power": "Yes", "WiFi": "Yes", "Price": "$800"},
            {"Booth": "A-03", "Vendor": "Available", "Size": "3x3", "Status": "Available", "Power": "Yes", "WiFi": "Yes", "Price": "$500"},
            {"Booth": "B-01", "Vendor": "Security Plus", "Size": "3x3", "Status": "Reserved", "Power": "No", "WiFi": "Yes", "Price": "$400"},
            {"Booth": "B-02", "Vendor": "Available", "Size": "6x6", "Status": "Available", "Power": "Yes", "WiFi": "Yes", "Price": "$1200"},
            {"Booth": "C-01", "Vendor": "Food Corner", "Size": "3x6", "Status": "Occupied", "Power": "Yes", "WiFi": "No", "Price": "$700"},
        ]
        
        df = pd.DataFrame(booth_data)
        
        # Apply filters
        if hall_section != "All":
            section_letter = hall_section.split(" ")[1]
            df = df[df['Booth'].str.startswith(section_letter)]
        if booth_status != "All":
            df = df[df['Status'] == booth_status]
        if booth_size != "All":
            df = df[df['Size'] == booth_size]
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Visual layout map
        st.markdown("### 🗺️ Interactive Booth Map")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Section A**")
            for i in range(1, 4):
                booth_id = f"A-{i:02d}"
                booth_info = df[df['Booth'] == booth_id]
                if not booth_info.empty:
                    status = booth_info.iloc[0]['Status']
                    color = "🟢" if status == "Available" else "🔴" if status == "Occupied" else "🟡"
                    st.write(f"{color} {booth_id}")
        
        with col2:
            st.markdown("**Section B**")
            for i in range(1, 4):
                booth_id = f"B-{i:02d}"
                booth_info = df[df['Booth'] == booth_id]
                if not booth_info.empty:
                    status = booth_info.iloc[0]['Status']
                    color = "🟢" if status == "Available" else "🔴" if status == "Occupied" else "🟡"
                    st.write(f"{color} {booth_id}")
        
        with col3:
            st.markdown("**Section C**")
            for i in range(1, 4):
                booth_id = f"C-{i:02d}"
                booth_info = df[df['Booth'] == booth_id]
                if not booth_info.empty:
                    status = booth_info.iloc[0]['Status']
                    color = "🟢" if status == "Available" else "🔴" if status == "Occupied" else "🟡"
                    st.write(f"{color} {booth_id}")
    
    with tab2:
        st.markdown("### 📋 Booth Reservations")
        
        # New reservation form
        with st.form("booth_reservation"):
            st.markdown("#### ➕ New Booth Reservation")
            col1, col2 = st.columns(2)
            with col1:
                booth_id = st.selectbox("Select Booth:", ["A-03", "B-02", "C-04", "C-05"])
                vendor_name = st.text_input("Vendor/Company Name:*")
                contact_person = st.text_input("Contact Person:*")
                email = st.text_input("Email:*")
                phone = st.text_input("Phone:*")
            
            with col2:
                booth_size_req = st.selectbox("Required Size:", ["3x3", "3x6", "6x6", "Custom"])
                power_required = st.checkbox("Power Required")
                wifi_required = st.checkbox("WiFi Required")
                special_requirements = st.text_area("Special Requirements:")
                setup_date = st.date_input("Setup Date:")
            
            # File uploads for reservation
            st.markdown("#### 📄 Required Documents")
            col1, col2 = st.columns(2)
            with col1:
                business_license = st.file_uploader("Business License*", type=['pdf', 'jpg', 'png'])
                if business_license:
                    st.success(f"✅ Business license uploaded: {business_license.name}")
            
            with col2:
                insurance_doc = st.file_uploader("Insurance Certificate*", type=['pdf', 'jpg', 'png'])
                if insurance_doc:
                    st.success(f"✅ Insurance document uploaded: {insurance_doc.name}")
            
            # Booth layout plan
            layout_plan = st.file_uploader("Booth Layout Plan (Optional)", type=['pdf', 'jpg', 'png', 'dwg'])
            if layout_plan:
                st.success(f"✅ Layout plan uploaded: {layout_plan.name}")
                if layout_plan.type.startswith('image/'):
                    display_image_preview(layout_plan)
            
            submitted = st.form_submit_button("📋 Submit Reservation", use_container_width=True)
            
            if submitted:
                if vendor_name and contact_person and email and phone and business_license and insurance_doc:
                    # Save uploaded files
                    if business_license:
                        save_uploaded_file(business_license, f"booths/licenses/{vendor_name}_{business_license.name}")
                    if insurance_doc:
                        save_uploaded_file(insurance_doc, f"booths/insurance/{vendor_name}_{insurance_doc.name}")
                    if layout_plan:
                        save_uploaded_file(layout_plan, f"booths/layouts/{vendor_name}_{layout_plan.name}")
                    
                    st.success(f"✅ Booth reservation submitted for {vendor_name}!")
                    show_success_animation()
                else:
                    st.error("❌ Please fill in all required fields and upload required documents")
        
        # Existing reservations
        st.markdown("#### 📋 Current Reservations")
        reservations_data = [
            {"Booth": "A-01", "Vendor": "Coffee Express", "Contact": "John Doe", "Status": "Confirmed", "Payment": "Paid"},
            {"Booth": "A-02", "Vendor": "Tech Solutions", "Contact": "Jane Smith", "Status": "Confirmed", "Payment": "Pending"},
            {"Booth": "B-01", "Vendor": "Security Plus", "Contact": "Mike Johnson", "Status": "Pending", "Payment": "Not Paid"},
        ]
        df_reservations = pd.DataFrame(reservations_data)
        st.dataframe(df_reservations, use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("### 📊 Booth Analytics")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🏢 Total Booths", "36", delta="6")
        with col2:
            st.metric("✅ Occupied", "24", delta="3")
        with col3:
            st.metric("💰 Revenue", "$32,400", delta="$4,200")
        with col4:
            st.metric("📈 Occupancy Rate", "67%", delta="8%")
        
        # Charts
        col1, col2 = st.columns(2)
        with col1:
            # Booth occupancy by section
            sections = ["Section A", "Section B", "Section C"]
            occupancy = [85, 60, 55]
            fig = px.bar(x=sections, y=occupancy, title="Occupancy Rate by Section (%)")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Revenue by booth size
            sizes = ["3x3", "3x6", "6x6"]
            revenue = [12000, 15000, 5400]
            fig = px.pie(values=revenue, names=sizes, title="Revenue by Booth Size")
            st.plotly_chart(fig, use_container_width=True)
        
        # Booth utilization over time
        st.markdown("#### 📈 Booth Booking Timeline")
        timeline_data = [
            {"Month": "Jan", "Bookings": 8, "Available": 28},
            {"Month": "Feb", "Bookings": 15, "Available": 21},
            {"Month": "Mar", "Bookings": 24, "Available": 12},
        ]
        df_timeline = pd.DataFrame(timeline_data)
        fig = px.line(df_timeline, x="Month", y=["Bookings", "Available"], title="Booking Trends")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### 📄 Booth Documents & Floor Plans")
        
        # Document upload section
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🗺️ Upload Floor Plans")
            floor_plan = st.file_uploader("Exhibition Hall Floor Plan", type=['pdf', 'jpg', 'png', 'dwg'])
            if floor_plan:
                saved_path = save_uploaded_file(floor_plan, f"booths/floor_plans/{floor_plan.name}")
                st.success(f"✅ Floor plan uploaded!")
                
                # Display image preview for supported formats
                if floor_plan.type.startswith('image/'):
                    display_image_preview(floor_plan)
                
                file_info = get_file_info(saved_path)
                st.info(f"📄 File: {file_info['name']} | Size: {file_info['size']}")
        
        with col2:
            st.markdown("#### 📋 Upload Guidelines")
            guidelines_doc = st.file_uploader("Booth Setup Guidelines", type=['pdf', 'doc', 'docx'])
            if guidelines_doc:
                saved_path = save_uploaded_file(guidelines_doc, f"booths/guidelines/{guidelines_doc.name}")
                st.success(f"✅ Guidelines uploaded!")
                
                file_info = get_file_info(saved_path)
                st.info(f"📄 File: {file_info['name']} | Size: {file_info['size']}")
        
        # Booth specifications upload
        st.markdown("#### ⚡ Technical Specifications")
        col1, col2 = st.columns(2)
        with col1:
            electrical_plan = st.file_uploader("Electrical Layout", type=['pdf', 'dwg', 'jpg', 'png'])
            if electrical_plan:
                saved_path = save_uploaded_file(electrical_plan, f"booths/electrical/{electrical_plan.name}")
                st.success("✅ Electrical layout uploaded!")
        
        with col2:
            network_plan = st.file_uploader("Network Layout", type=['pdf', 'dwg', 'jpg', 'png'])
            if network_plan:
                saved_path = save_uploaded_file(network_plan, f"booths/network/{network_plan.name}")
                st.success("✅ Network layout uploaded!")
        
        # Document management
        st.markdown("#### 📚 Document Library")
        documents_data = [
            {"Document": "Main Floor Plan", "Type": "Floor Plan", "Last Updated": "2025-01-25", "Status": "Current"},
            {"Document": "Setup Guidelines", "Type": "Guidelines", "Last Updated": "2025-01-20", "Status": "Current"},
            {"Document": "Electrical Layout", "Type": "Technical", "Last Updated": "2025-01-15", "Status": "Current"},
        ]
        df_docs = pd.DataFrame(documents_data)
        st.dataframe(df_docs, use_container_width=True, hide_index=True)
        
        # Quick actions
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📊 Generate Booth Report", use_container_width=True):
                st.success("Booth utilization report generated!")
        with col2:
            if st.button("📧 Send Layout to Vendors", use_container_width=True):
                st.success("Floor plans sent to all vendors!")
        with col3:
            if st.button("🔄 Update Availability", use_container_width=True):
                st.success("Booth availability updated!")
