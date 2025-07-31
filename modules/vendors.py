"""
Vendors Module for EventIQ Management System
Team Member: [Vendor Management Team]
"""

from .utils import *

def show_vendors_page():
    """Enhanced vendor management page"""
    st.markdown("## 🏭 Vendor Management")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Vendor Directory", "➕ Add Vendor", "📊 Analytics", "💰 Payments", "📧 Communications"])
    
    with tab1:
        show_vendor_directory()
    
    with tab2:
        show_add_vendor()
    
    with tab3:
        show_vendor_analytics()
    
    with tab4:
        show_payment_management()
    
    with tab5:
        show_vendor_communications()

def show_vendor_directory():
    """Display vendor directory with search and filters"""
    st.markdown("### 📋 Vendor Directory")
    
    # Filter and search options
    col1, col2, col3 = st.columns(3)
    with col1:
        search_term = st.text_input("🔍 Search vendors:")
    with col2:
        service_filter = st.selectbox("Filter by Service:", ["All", "Catering", "AV Equipment", "Security", "Cleaning", "Transportation", "Decoration", "Photography"])
    with col3:
        status_filter = st.selectbox("Filter by Status:", ["All", "Active", "Pending", "Inactive", "Cancelled"])
    
    # Get vendor data
    vendor_data = get_vendor_data()
    df = pd.DataFrame(vendor_data)
    
    # Apply filters
    df = apply_vendor_filters(df, search_term, service_filter, status_filter)
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Vendor actions
    show_vendor_actions()
    
    # Individual vendor management
    show_individual_vendor_management(vendor_data)

def show_add_vendor():
    """Add new vendor interface"""
    st.markdown("### ➕ Add New Vendor")
    
    col1, col2 = st.columns(2)
    with col1:
        vendor_info = show_basic_vendor_form()
    
    with col2:
        contract_info, documents = show_vendor_documents_form()
    
    show_vendor_save_button(vendor_info, contract_info, documents)

def show_vendor_analytics():
    """Display vendor analytics and charts"""
    st.markdown("### 📊 Vendor Analytics")
    
    # Key metrics
    show_vendor_metrics()
    
    # Charts
    show_vendor_charts()
    
    # Payment analysis
    show_payment_analysis()

def show_payment_management():
    """Payment management interface"""
    st.markdown("### 💰 Payment Management")
    
    # Payment overview
    show_payment_overview()
    
    # Payment tracking
    show_payment_tracking()
    
    # Payment actions
    show_payment_actions()
    
    # Individual payment processing
    show_individual_payment_processing()

def show_vendor_communications():
    """Vendor communications interface"""
    st.markdown("### 📧 Vendor Communications")
    
    tab5_1, tab5_2, tab5_3 = st.tabs(["📧 Send Messages", "📋 Message History", "📝 Templates"])
    
    with tab5_1:
        show_send_messages()
    
    with tab5_2:
        show_message_history()
    
    with tab5_3:
        show_message_templates()

def get_vendor_data():
    """Get enhanced vendor data"""
    return [
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

def apply_vendor_filters(df, search_term, service_filter, status_filter):
    """Apply filters to vendor dataframe"""
    if search_term:
        df = df[df['Name'].str.contains(search_term, case=False) | 
               df['Service'].str.contains(search_term, case=False)]
    if service_filter != "All":
        df = df[df['Service'] == service_filter]
    if status_filter != "All":
        df = df[df['Status'] == status_filter]
    return df

def show_vendor_actions():
    """Display vendor action buttons"""
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

def show_individual_vendor_management(vendor_data):
    """Individual vendor management interface"""
    st.markdown("#### 👤 Individual Vendor Management")
    selected_vendor = st.selectbox("Select Vendor:", [v["Name"] for v in vendor_data])
    
    vendor_info = next(v for v in vendor_data if v["Name"] == selected_vendor)
    
    # Display vendor details
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
    
    # Action buttons
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

def show_basic_vendor_form():
    """Basic vendor information form"""
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
    
    return {
        'name': vendor_name,
        'email': vendor_email,
        'phone': vendor_phone,
        'website': vendor_website,
        'address': vendor_address,
        'service': vendor_service,
        'description': service_description,
        'materials': materials_brought
    }

def show_vendor_documents_form():
    """Vendor documents and contract form"""
    st.markdown("#### 💰 Contract Information")
    contract_amount = st.number_input("Contract Amount ($):", min_value=0.0, step=100.0)
    payment_terms = st.selectbox("Payment Terms:", ["Net 30", "Net 15", "Upon Completion", "50% Advance", "Payment on Delivery"])
    booth_required = st.checkbox("Booth Space Required")
    preferred_booth = ""
    if booth_required:
        preferred_booth = st.text_input("Preferred Booth Location:")
    
    st.markdown("#### 📄 Documentation")
    documents = {}
    
    # Insurance file upload
    insurance_file = st.file_uploader("Insurance Certificate:", type=['pdf', 'jpg', 'png'], key="vendor_insurance")
    if insurance_file:
        file_info = get_file_info(insurance_file)
        st.success(f"✅ {insurance_file.name} ({file_info['size_mb']:.2f} MB)")
        documents['insurance'] = insurance_file
        if st.button("📋 Preview Insurance", key="preview_insurance"):
            st.info(f"Insurance file: {insurance_file.name} - Ready for processing")
    
    # License file upload
    license_file = st.file_uploader("Business License:", type=['pdf', 'jpg', 'png'], key="vendor_license")
    if license_file:
        file_info = get_file_info(license_file)
        st.success(f"✅ {license_file.name} ({file_info['size_mb']:.2f} MB)")
        documents['license'] = license_file
        if st.button("📋 Preview License", key="preview_license"):
            st.info(f"License file: {license_file.name} - Ready for processing")
    
    # Contract file upload
    contract_file = st.file_uploader("Signed Contract:", type=['pdf'], key="vendor_contract")
    if contract_file:
        file_info = get_file_info(contract_file)
        st.success(f"✅ {contract_file.name} ({file_info['size_mb']:.2f} MB)")
        documents['contract'] = contract_file
        if st.button("📋 Preview Contract", key="preview_contract"):
            st.info(f"Contract file: {contract_file.name} - Ready for processing")
    
    # Sample documents
    show_sample_document_buttons()
    
    st.markdown("#### ⚙️ Additional Information")
    special_requirements = st.text_area("Special Requirements:")
    setup_time = st.selectbox("Setup Time Required:", ["1 hour", "2 hours", "4 hours", "Full day", "Multiple days"])
    emergency_contact = st.text_input("Emergency Contact:")
    
    contract_info = {
        'amount': contract_amount,
        'terms': payment_terms,
        'booth_required': booth_required,
        'preferred_booth': preferred_booth,
        'special_requirements': special_requirements,
        'setup_time': setup_time,
        'emergency_contact': emergency_contact
    }
    
    return contract_info, documents

def show_sample_document_buttons():
    """Show sample document loading buttons"""
    st.markdown("#### 📁 Sample Documents")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Load Sample Insurance", key="sample_insurance"):
            st.session_state.sample_insurance = {
                "name": "sample_insurance_certificate.pdf",
                "type": "application/pdf",
                "size": "1.2 MB",
                "status": "Uploaded"
            }
            st.success("✅ Sample insurance certificate loaded!")
    
    with col2:
        if st.button("📄 Load Sample License", key="sample_license"):
            st.session_state.sample_license = {
                "name": "sample_business_license.pdf", 
                "type": "application/pdf",
                "size": "0.8 MB",
                "status": "Uploaded"
            }
            st.success("✅ Sample business license loaded!")

def show_vendor_save_button(vendor_info, contract_info, documents):
    """Show save vendor button and handle saving"""
    if st.button("💾 Add Vendor", use_container_width=True):
        if vendor_info['name'] and vendor_info['email']:
            # Process uploaded documents
            vendor_documents = {}
            for doc_type, doc_file in documents.items():
                if doc_file:
                    vendor_documents[doc_type] = {
                        "name": doc_file.name,
                        "type": doc_file.type,
                        "size": get_file_info(doc_file)['size_mb'],
                        "data": get_base64_encoded_file(doc_file)
                    }
            
            # Store vendor information
            save_new_vendor(vendor_info, contract_info, vendor_documents)
        else:
            st.warning("⚠️ Please fill in required fields (Name and Email)")

def save_new_vendor(vendor_info, contract_info, vendor_documents):
    """Save new vendor to session state"""
    new_vendor = {
        **vendor_info,
        **contract_info,
        "documents": vendor_documents,
        "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    if 'vendors' not in st.session_state:
        st.session_state.vendors = []
    st.session_state.vendors.append(new_vendor)
    
    st.success(f"✅ Vendor '{vendor_info['name']}' added successfully!")
    show_success_animation()
    
    # Show summary of uploaded documents
    if vendor_documents:
        st.markdown("#### 📄 Documents Uploaded:")
        for doc_type, doc_info in vendor_documents.items():
            st.info(f"✅ {doc_type.title()}: {doc_info['name']} ({doc_info['size']:.2f} MB)")

def show_vendor_metrics():
    """Display vendor key metrics"""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🏭 Total Vendors", "15")
    with col2:
        st.metric("✅ Active Vendors", "12")
    with col3:
        st.metric("💰 Total Contracts", "$25,800")
    with col4:
        st.metric("⭐ Avg. Rating", "4.4")

def show_vendor_charts():
    """Display vendor analytics charts"""
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

def show_payment_analysis():
    """Display payment status analysis"""
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

def show_payment_overview():
    """Display payment overview metrics"""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Total Payable", "$25,800")
    with col2:
        st.metric("✅ Paid", "$18,100")
    with col3:
        st.metric("⏳ Pending", "$5,200")
    with col4:
        st.metric("🚨 Overdue", "$2,500")

def show_payment_tracking():
    """Display payment tracking table"""
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

def show_payment_actions():
    """Display payment action buttons"""
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

def show_individual_payment_processing():
    """Individual payment processing interface"""
    st.markdown("#### 🏦 Individual Payment Processing")
    payment_data = [
        {"Vendor": "Tech Solutions", "Status": "Pending"},
        {"Vendor": "Security Plus", "Status": "Not Sent"}
    ]
    
    col1, col2 = st.columns(2)
    with col1:
        payment_vendor = st.selectbox("Select Vendor for Payment:", [p["Vendor"] for p in payment_data])
        payment_amount = st.number_input("Payment Amount ($):", min_value=0.0, step=100.0, value=1800.0)
        payment_method = st.selectbox("Payment Method:", ["Bank Transfer", "Check", "Wire Transfer", "Credit Card", "Cash"])
    
    with col2:
        payment_reference = st.text_input("Payment Reference/Note:")
        payment_date = st.date_input("Payment Date:")
        
        if st.button("💰 Process Payment", use_container_width=True):
            st.success(f"✅ Payment of ${payment_amount:,.0f} processed for {payment_vendor}")

def show_send_messages():
    """Send messages interface"""
    st.markdown("#### 📧 Send New Message")
    
    col1, col2 = st.columns(2)
    with col1:
        message_type = st.radio("Message Type:", ["Individual", "Bulk", "Group"])
        recipients = get_message_recipients(message_type)
        message_priority = st.selectbox("Priority:", ["Normal", "High", "Urgent"])
    
    with col2:
        message_subject = st.text_input("Subject:")
        message_body = st.text_area("Message:", height=150)
        
        # Handle attachments
        handle_message_attachments()
        
        # Scheduling
        schedule_send = st.checkbox("Schedule for later")
        send_date, send_time = None, None
        if schedule_send:
            send_date = st.date_input("Send Date:")
            send_time = st.time_input("Send Time:")
        
        # Send button
        handle_send_message(message_subject, message_body, recipients, message_priority, schedule_send, send_date, send_time)

def get_message_recipients(message_type):
    """Get message recipients based on type"""
    vendor_data = get_vendor_data()
    
    if message_type == "Individual":
        return st.multiselect("Select Vendor:", [v["Name"] for v in vendor_data])
    elif message_type == "Bulk":
        st.write("Message will be sent to all vendors")
        return "All Vendors"
    else:
        service_group = st.selectbox("Select Service Group:", ["Catering", "AV Equipment", "Security", "Cleaning", "Decoration"])
        return f"All {service_group} vendors"

def handle_message_attachments():
    """Handle message attachments"""
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
    
    return attachments

def handle_send_message(message_subject, message_body, recipients, message_priority, schedule_send, send_date, send_time):
    """Handle sending message"""
    if st.button("📤 Send Message", use_container_width=True):
        if message_subject and message_body:
            # Store message and show success
            store_vendor_message(message_subject, message_body, recipients, message_priority, schedule_send, send_date, send_time)
        else:
            st.warning("⚠️ Please fill in subject and message")

def store_vendor_message(message_subject, message_body, recipients, message_priority, schedule_send, send_date, send_time):
    """Store vendor message in session state"""
    # Get attachments from session state if available
    attachments = st.session_state.get('comm_attachments', [])
    processed_attachments = []
    
    if attachments:
        for attachment in attachments:
            processed_attachments.append({
                "name": attachment.name,
                "type": attachment.type,
                "size": get_file_info(attachment)['size_mb'],
                "data": get_base64_encoded_file(attachment)
            })
    
    # Store message
    if 'vendor_messages' not in st.session_state:
        st.session_state.vendor_messages = []
    
    new_message = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "recipients": recipients,
        "subject": message_subject,
        "body": message_body,
        "priority": message_priority,
        "attachments": processed_attachments,
        "scheduled": schedule_send,
        "send_date": send_date.strftime("%Y-%m-%d") if schedule_send and send_date else None,
        "send_time": send_time.strftime("%H:%M") if schedule_send and send_time else None
    }
    st.session_state.vendor_messages.append(new_message)
    
    st.success(f"✅ Message sent successfully!")
    if processed_attachments:
        total_size = sum(att['size'] for att in processed_attachments)
        st.info(f"📎 {len(processed_attachments)} attachment(s) included ({total_size:.2f} MB total)")
    if schedule_send:
        st.info(f"⏰ Scheduled for {send_date} at {send_time}")

def show_message_history():
    """Display communication history"""
    st.markdown("#### 📋 Communication History")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        vendor_data = get_vendor_data()
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

def show_message_templates():
    """Display message templates management"""
    st.markdown("#### 📝 Message Templates")
    
    # Template management
    col1, col2 = st.columns(2)
    with col1:
        template_category = st.selectbox("Template Category:", [
            "Welcome", "Contract", "Payment", "Setup Instructions", 
            "Reminders", "Thank You", "Emergency", "General Updates"
        ])
        
        templates = get_message_templates()
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

def get_message_templates():
    """Get predefined message templates"""
    return {
        "Welcome": "Welcome to EventIQ 2025! We're excited to have you as our vendor partner.",
        "Contract": "Please find attached your vendor contract for EventIQ 2025. Please review and return signed copy.",
        "Payment": "This is a reminder that your payment of {amount} is due on {date}.",
        "Setup Instructions": "Please find attached your booth setup instructions for EventIQ 2025.",
        "Reminders": "Reminder: {event} is scheduled for {date} at {time}.",
        "Thank You": "Thank you for your excellent service at EventIQ 2025!",
        "Emergency": "URGENT: Please contact event coordination immediately regarding {issue}.",
        "General Updates": "EventIQ 2025 Update: {message}"
    }
