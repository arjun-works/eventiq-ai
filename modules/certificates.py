"""
Certificates Module for EventIQ Management System
Team Member: [Certificate Management Team]
"""

from .utils import *

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
        show_certificates_registry()
    
    with tab2:
        show_certificate_generation()
    
    with tab3:
        show_certificate_analytics()

def show_certificates_registry():
    """Display certificate registry"""
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
                    cert_content = generate_certificate_content(cert)
                    
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

def show_certificate_generation():
    """Show certificate generation interface"""
    st.markdown("### 🎓 Generate Certificates")
    
    col1, col2 = st.columns(2)
    with col1:
        show_individual_certificate_generation()
    
    with col2:
        show_bulk_certificate_generation()

def show_individual_certificate_generation():
    """Individual certificate generation"""
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
            cert_content = generate_certificate_content({
                'volunteer_name': selected_volunteer['full_name'],
                'total_hours': selected_volunteer['total_hours'],
                'volunteer_role': selected_volunteer.get('role', 'Volunteer'),
                'volunteer_id': vol_id
            })
            
            st.text_area("Certificate Content:", cert_content, height=200, disabled=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🎓 Generate Certificate", use_container_width=True):
                    st.success(f"Certificate generated for {selected_volunteer['full_name']}")
                    show_success_animation()
            
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

def show_bulk_certificate_generation():
    """Bulk certificate generation"""
    st.markdown("#### 🎓 Bulk Generation")
    st.info("Generate certificates for all eligible volunteers")
    
    if st.button("🎓 Generate All Certificates", use_container_width=True):
        result = make_api_request("/certificates/bulk-generate", method="POST")
        if result:
            st.success(f"✅ {result.get('message', 'Bulk certificates generated!')}")
            if "eligible_volunteers" in result:
                st.write(f"Generated for {len(result['eligible_volunteers'])} volunteers")

def show_certificate_analytics():
    """Display certificate analytics"""
    st.markdown("### 📊 Certificate Analytics")
    
    cert_stats = make_api_request("/certificates/stats")
    if cert_stats:
        # Charts and analytics
        col1, col2 = st.columns(2)
        
        with col1:
            show_certificate_eligibility_chart(cert_stats)
        
        with col2:
            show_hours_distribution_chart()

def show_certificate_eligibility_chart(cert_stats):
    """Show certificate eligibility pie chart"""
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

def show_hours_distribution_chart():
    """Show volunteer hours distribution histogram"""
    volunteers = make_api_request("/volunteers/")
    if volunteers and "volunteers" in volunteers:
        hours_data = [v['total_hours'] for v in volunteers["volunteers"]]
        fig = px.histogram(x=hours_data, title='Volunteer Hours Distribution', 
                         labels={'x': 'Hours', 'y': 'Number of Volunteers'})
        st.plotly_chart(fig, use_container_width=True)

def generate_certificate_content(cert):
    """Generate certificate content"""
    return f"""
CERTIFICATE OF APPRECIATION

This is to certify that

{cert['volunteer_name']}

has successfully completed {cert['total_hours']} hours of volunteer service
as a {cert.get('volunteer_role', 'Volunteer')} for EventIQ 2025.

We appreciate your dedication and commitment to making this event successful.

Date: {datetime.now().strftime("%B %d, %Y")}
Certificate ID: CERT-{cert.get('volunteer_id', '000'):03d}-{datetime.now().strftime("%Y%m")}

EventIQ Management Team
"""
