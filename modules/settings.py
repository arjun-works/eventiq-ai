"""
Settings Module for EventIQ Management System
Team Member: [Settings & Configuration Team]
"""

from .utils import *

def show_settings_page():
    """System settings page"""
    st.markdown("## ⚙️ System Settings")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔧 General", "👥 Users", "🔐 Security", "🔔 Notifications"])
    
    with tab1:
        show_general_settings()
    
    with tab2:
        show_user_management()
    
    with tab3:
        show_security_settings()
    
    with tab4:
        show_notification_settings()

def show_general_settings():
    """Display general system settings"""
    st.markdown("### 🔧 General Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        show_system_configuration()
    
    with col2:
        show_email_configuration()
    
    show_configuration_files()
    show_theme_settings()

def show_system_configuration():
    """System configuration form"""
    st.markdown("#### 🌐 System Configuration")
    event_name = st.text_input("Event Name:", value="EventIQ 2025")
    event_date = st.date_input("Event Date:")
    max_participants = st.number_input("Max Participants:", min_value=1, value=500, step=50)
    timezone = st.selectbox("Timezone:", ["EST", "PST", "CST", "MST", "UTC"])
    
    if st.button("💾 Save General Settings", use_container_width=True):
        st.success("✅ General settings saved successfully!")

def show_email_configuration():
    """Email configuration form"""
    st.markdown("#### 📧 Email Configuration")
    smtp_server = st.text_input("SMTP Server:", value="smtp.gmail.com")
    smtp_port = st.number_input("SMTP Port:", value=587)
    email_username = st.text_input("Email Username:")
    email_password = st.text_input("Email Password:", type="password")
    
    if st.button("📧 Test Email Connection", use_container_width=True):
        st.success("✅ Email connection test successful!")

def show_configuration_files():
    """Configuration file upload and management"""
    st.markdown("#### 📁 Configuration Files")
    col1, col2 = st.columns(2)
    
    with col1:
        show_config_upload()
    
    with col2:
        show_logo_upload()

def show_config_upload():
    """Configuration file upload interface"""
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

def show_logo_upload():
    """Event logo upload interface"""
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
        sample_config = get_sample_config()
        config_json = json.dumps(sample_config, indent=2)
        st.download_button(
            "📥 Download",
            config_json,
            "eventiq_config.json",
            "application/json"
        )

def show_theme_settings():
    """Theme customization settings"""
    st.markdown("#### 🎨 Theme Settings")
    col1, col2, col3 = st.columns(3)
    with col1:
        primary_color = st.color_picker("Primary Color:", "#667eea")
    with col2:
        secondary_color = st.color_picker("Secondary Color:", "#764ba2")
    with col3:
        accent_color = st.color_picker("Accent Color:", "#52c41a")

def show_user_management():
    """User management interface"""
    st.markdown("### 👥 User Management")
    
    # User list
    show_active_users()
    
    # User actions
    show_user_actions()
    
    # Bulk user import
    show_bulk_user_import()
    
    # Role management
    show_role_management()

def show_active_users():
    """Display active users list"""
    st.markdown("#### 👤 Active Users")
    users_data = get_users_data()
    users_df = pd.DataFrame(users_data)
    st.dataframe(users_df, use_container_width=True, hide_index=True)

def show_user_actions():
    """User management action buttons"""
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("➕ Add New User", use_container_width=True):
            st.success("New user creation form would open")
    with col2:
        if st.button("📤 Export Users", use_container_width=True):
            # Generate CSV export
            users_df = pd.DataFrame(get_users_data())
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

def show_bulk_user_import():
    """Bulk user import interface"""
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
                    show_success_animation()
            
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
    
    with col2:
        if st.button("📄 Download User Template", use_container_width=True):
            template_data = get_user_template_data()
            template_df = pd.DataFrame(template_data)
            csv_template = template_df.to_csv(index=False)
            st.download_button(
                "📥 Download Template",
                csv_template,
                "user_import_template.csv",
                "text/csv"
            )

def show_role_management():
    """Role and permissions management"""
    st.markdown("#### 🎭 Role Management")
    roles = ["Admin", "Organizer", "Volunteer", "Participant", "Vendor"]
    selected_role = st.selectbox("Select Role to Configure:", roles)
    
    permissions = ["View Dashboard", "Manage Users", "Generate Certificates", "Manage Budget", "View Analytics", "System Settings"]
    selected_permissions = st.multiselect(f"Permissions for {selected_role}:", permissions, default=permissions[:3])
    
    if st.button("💾 Update Role Permissions"):
        st.success(f"✅ Permissions updated for {selected_role} role!")

def show_security_settings():
    """Security settings interface"""
    st.markdown("### 🔐 Security Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        show_password_policy()
    
    with col2:
        show_security_features()
    
    show_security_logs()

def show_password_policy():
    """Password policy configuration"""
    st.markdown("#### 🔑 Password Policy")
    min_length = st.slider("Minimum Password Length:", 6, 20, 8)
    require_uppercase = st.checkbox("Require Uppercase Letters", value=True)
    require_lowercase = st.checkbox("Require Lowercase Letters", value=True)
    require_numbers = st.checkbox("Require Numbers", value=True)
    require_symbols = st.checkbox("Require Special Characters", value=False)
    
    if st.button("💾 Save Password Policy", use_container_width=True):
        st.success("✅ Password policy updated!")

def show_security_features():
    """Security features configuration"""
    st.markdown("#### 🛡️ Security Features")
    two_factor = st.checkbox("Enable Two-Factor Authentication", value=False)
    session_timeout = st.slider("Session Timeout (minutes):", 15, 480, 60)
    max_login_attempts = st.slider("Max Login Attempts:", 3, 10, 5)
    ip_whitelist = st.text_area("IP Whitelist (one per line):")
    
    if st.button("🛡️ Save Security Settings", use_container_width=True):
        st.success("✅ Security settings updated!")

def show_security_logs():
    """Display security logs"""
    st.markdown("#### 📊 Security Logs")
    security_logs = get_security_logs()
    logs_df = pd.DataFrame(security_logs)
    st.dataframe(logs_df, use_container_width=True, hide_index=True)

def show_notification_settings():
    """Notification settings interface"""
    st.markdown("### 🔔 Notification Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        show_email_notifications()
    
    with col2:
        show_system_notifications()
    
    show_notification_templates()

def show_email_notifications():
    """Email notification settings"""
    st.markdown("#### 📧 Email Notifications")
    email_new_registration = st.checkbox("New User Registration", value=True)
    email_certificate_ready = st.checkbox("Certificate Ready", value=True)
    email_event_updates = st.checkbox("Event Updates", value=True)
    email_feedback_received = st.checkbox("Feedback Received", value=False)
    email_budget_alerts = st.checkbox("Budget Alerts", value=True)
    
    if st.button("💾 Save Email Settings", use_container_width=True):
        st.success("✅ Email notification settings saved!")

def show_system_notifications():
    """System notification settings"""
    st.markdown("#### 🔔 System Notifications")
    system_maintenance = st.checkbox("Maintenance Alerts", value=True)
    system_errors = st.checkbox("System Errors", value=True)
    system_backups = st.checkbox("Backup Status", value=False)
    system_updates = st.checkbox("System Updates", value=True)
    
    if st.button("🔔 Save System Settings", use_container_width=True):
        st.success("✅ System notification settings saved!")

def show_notification_templates():
    """Notification templates management"""
    st.markdown("#### 📝 Notification Templates")
    template_type = st.selectbox("Template Type:", ["Welcome Email", "Certificate Ready", "Event Update", "Password Reset"])
    template_subject = st.text_input("Subject:", value="Welcome to EventIQ!")
    template_body = st.text_area("Email Body:", value="Dear {name}, welcome to EventIQ 2025!", height=100)
    
    if st.button("💾 Save Template"):
        st.success(f"✅ {template_type} template saved!")

# Helper functions for settings module
def get_sample_config():
    """Get sample configuration data"""
    return {
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

def get_users_data():
    """Get sample users data"""
    return [
        {"Name": "John Smith", "Email": "organizer@eventiq.com", "Role": "Organizer", "Status": "Active", "Last Login": "2025-01-30 14:30"},
        {"Name": "Sarah Johnson", "Email": "volunteer@eventiq.com", "Role": "Volunteer", "Status": "Active", "Last Login": "2025-01-30 12:15"},
        {"Name": "Mike Wilson", "Email": "participant@eventiq.com", "Role": "Participant", "Status": "Active", "Last Login": "2025-01-29 18:45"},
        {"Name": "Alice Brown", "Email": "vendor@eventiq.com", "Role": "Vendor", "Status": "Inactive", "Last Login": "2025-01-28 09:20"},
        {"Name": "Admin User", "Email": "admin@eventiq.com", "Role": "Admin", "Status": "Active", "Last Login": "2025-01-30 16:00"},
    ]

def get_user_template_data():
    """Get user import template data"""
    return {
        "Name": ["John Doe", "Jane Smith"],
        "Email": ["john@example.com", "jane@example.com"],
        "Role": ["Organizer", "Volunteer"],
        "Status": ["Active", "Active"]
    }

def get_security_logs():
    """Get sample security logs"""
    return [
        {"Time": "2025-01-30 16:05", "Event": "Successful Login", "User": "admin@eventiq.com", "IP": "192.168.1.100"},
        {"Time": "2025-01-30 15:45", "Event": "Failed Login Attempt", "User": "unknown@test.com", "IP": "10.0.0.50"},
        {"Time": "2025-01-30 14:30", "Event": "Password Changed", "User": "organizer@eventiq.com", "IP": "192.168.1.105"},
        {"Time": "2025-01-30 12:15", "Event": "Successful Login", "User": "volunteer@eventiq.com", "IP": "192.168.1.110"},
    ]
