"""
Feedback Management Module for EventIQ Management System
Team Member: [Feedback Team]
"""

from .utils import *

def show_feedback_page():
    """Feedback management interface"""
    st.markdown("## 📝 Feedback Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Collect Feedback", "📋 View Responses", "📊 Analytics", "📄 Reports"])
    
    with tab1:
        st.markdown("### 📝 Event Feedback Form")
        
        # Feedback type selection
        feedback_type = st.selectbox("Feedback Type:", ["Event Overall", "Session Specific", "Vendor Feedback", "Volunteer Feedback", "Venue Feedback"])
        
        with st.form("feedback_form"):
            if feedback_type == "Event Overall":
                col1, col2 = st.columns(2)
                with col1:
                    overall_rating = st.slider("Overall Event Rating:", 1, 5, 4)
                    venue_rating = st.slider("Venue Rating:", 1, 5, 4)
                    content_rating = st.slider("Content Quality:", 1, 5, 4)
                    organization_rating = st.slider("Organization Rating:", 1, 5, 4)
                
                with col2:
                    value_rating = st.slider("Value for Money:", 1, 5, 4)
                    networking_rating = st.slider("Networking Opportunities:", 1, 5, 4)
                    recommend = st.selectbox("Would you recommend this event?", ["Yes", "No", "Maybe"])
                    attend_again = st.selectbox("Would you attend again?", ["Definitely", "Probably", "Maybe", "Probably Not", "Definitely Not"])
            
            elif feedback_type == "Session Specific":
                col1, col2 = st.columns(2)
                with col1:
                    session_name = st.selectbox("Session:", ["Opening Keynote", "Tech Workshop A", "Panel Discussion", "Networking Lunch", "Closing Ceremony"])
                    session_rating = st.slider("Session Rating:", 1, 5, 4)
                    speaker_rating = st.slider("Speaker/Presenter Rating:", 1, 5, 4)
                
                with col2:
                    content_relevance = st.slider("Content Relevance:", 1, 5, 4)
                    session_length = st.selectbox("Session Length:", ["Too Short", "Just Right", "Too Long"])
                    technical_quality = st.slider("Technical Quality (A/V, etc.):", 1, 5, 4)
            
            # Common fields for all feedback types
            st.markdown("### 💭 Additional Comments")
            col1, col2 = st.columns(2)
            with col1:
                what_liked = st.text_area("What did you like most?")
                improvements = st.text_area("What could be improved?")
            
            with col2:
                additional_comments = st.text_area("Additional Comments:")
                future_topics = st.text_area("Suggested topics for future events:")
            
            # Contact information (optional)
            st.markdown("### 👤 Contact Information (Optional)")
            col1, col2, col3 = st.columns(3)
            with col1:
                respondent_name = st.text_input("Name:")
                email = st.text_input("Email:")
            with col2:
                organization = st.text_input("Organization:")
                role = st.text_input("Job Title/Role:")
            with col3:
                contact_permission = st.checkbox("Allow follow-up contact")
                anonymous = st.checkbox("Submit anonymously")
            
            # File uploads for feedback
            st.markdown("### 📄 Attachments (Optional)")
            col1, col2 = st.columns(2)
            with col1:
                feedback_images = st.file_uploader("Upload Images", type=['jpg', 'png', 'gif'], accept_multiple_files=True)
                if feedback_images:
                    st.success(f"✅ {len(feedback_images)} images uploaded")
                    for img in feedback_images:
                        display_image_preview(img)
            
            with col2:
                feedback_docs = st.file_uploader("Upload Documents", type=['pdf', 'doc', 'docx', 'txt'], accept_multiple_files=True)
                if feedback_docs:
                    st.success(f"✅ {len(feedback_docs)} documents uploaded")
            
            submitted = st.form_submit_button("📝 Submit Feedback", use_container_width=True)
            
            if submitted:
                # Save uploaded files
                if feedback_images:
                    for img in feedback_images:
                        save_uploaded_file(img, f"feedback/images/{feedback_type}_{img.name}")
                
                if feedback_docs:
                    for doc in feedback_docs:
                        save_uploaded_file(doc, f"feedback/documents/{feedback_type}_{doc.name}")
                
                st.success("Thank you for your feedback! 🎉")
                show_success_animation()
                
                # Show confirmation details
                st.info(f"📧 Confirmation sent to: {email if email else 'Anonymous submission'}")
    
    with tab2:
        st.markdown("### 📋 Feedback Responses")
        
        # Filter and search options
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            type_filter = st.selectbox("Filter by Type:", ["All", "Event Overall", "Session Specific", "Vendor Feedback", "Volunteer Feedback"])
        with col2:
            rating_filter = st.selectbox("Filter by Rating:", ["All", "5 Stars", "4 Stars", "3 Stars", "2 Stars", "1 Star"])
        with col3:
            date_filter = st.selectbox("Filter by Date:", ["All", "Today", "This Week", "This Month"])
        with col4:
            search_feedback = st.text_input("🔍 Search feedback:", placeholder="Enter keywords...")
        
        feedback_data = [
            {
                "Date": "2025-01-30", "Time": "14:30", "Type": "Event Overall", "Rating": 4.5, 
                "Respondent": "John Smith", "Organization": "Tech Corp", "Comments": "Great event organization! Very well coordinated.",
                "Attachments": "Yes"
            },
            {
                "Date": "2025-01-30", "Time": "15:45", "Type": "Session Specific", "Rating": 4.2, 
                "Respondent": "Sarah Johnson", "Organization": "StartupXYZ", "Comments": "Excellent speakers, learned a lot from the tech workshop.",
                "Attachments": "No"
            },
            {
                "Date": "2025-01-29", "Time": "16:20", "Type": "Venue Feedback", "Rating": 4.8, 
                "Respondent": "Mike Wilson", "Organization": "Event Solutions", "Comments": "Perfect venue with excellent facilities and setup.",
                "Attachments": "Yes"
            },
            {
                "Date": "2025-01-29", "Time": "11:15", "Type": "Volunteer Feedback", "Rating": 4.0, 
                "Respondent": "Alice Brown", "Organization": "Community Vol", "Comments": "Well organized volunteer program, clear instructions.",
                "Attachments": "No"
            },
            {
                "Date": "2025-01-28", "Time": "17:30", "Type": "Event Overall", "Rating": 3.8, 
                "Respondent": "Anonymous", "Organization": "N/A", "Comments": "Good event but could improve catering options.",
                "Attachments": "No"
            },
        ]
        
        df = pd.DataFrame(feedback_data)
        
        # Apply filters
        if type_filter != "All":
            df = df[df['Type'] == type_filter]
        if rating_filter != "All":
            rating_val = int(rating_filter.split()[0])
            df = df[df['Rating'] >= rating_val]
        if search_feedback:
            df = df[df['Comments'].str.contains(search_feedback, case=False, na=False)]
        
        # Display feedback with expandable details
        for index, row in df.iterrows():
            with st.expander(f"📝 {row['Type']} - {row['Rating']}⭐ ({row['Date']} {row['Time']})"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Respondent:** {row['Respondent']}")
                    st.write(f"**Organization:** {row['Organization']}")
                    st.write(f"**Rating:** {row['Rating']}⭐")
                
                with col2:
                    st.write(f"**Type:** {row['Type']}")
                    st.write(f"**Date:** {row['Date']} at {row['Time']}")
                    st.write(f"**Attachments:** {row['Attachments']}")
                
                with col3:
                    if st.button(f"📧 Respond", key=f"respond_{index}"):
                        st.success("Response email template opened")
                    if st.button(f"🏷️ Tag", key=f"tag_{index}"):
                        st.info("Feedback tagged for follow-up")
                
                st.markdown("**Comments:**")
                st.write(row['Comments'])
                
                if row['Attachments'] == "Yes":
                    st.markdown("**📎 Attachments:**")
                    st.info("Attachment viewer would display here")
        
        # Bulk actions
        st.markdown("### ⚡ Bulk Actions")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📧 Send Thank You", use_container_width=True):
                st.success("Thank you emails sent to all respondents!")
        with col2:
            if st.button("📊 Export to CSV", use_container_width=True):
                st.success("Feedback data exported to CSV!")
        with col3:
            if st.button("🏷️ Tag Priority", use_container_width=True):
                st.info("Low-rated feedback tagged as priority!")
        with col4:
            if st.button("📈 Generate Summary", use_container_width=True):
                st.success("Feedback summary generated!")
    
    with tab3:
        st.markdown("### 📊 Feedback Analytics")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📝 Total Responses", "127", delta="23")
        with col2:
            st.metric("⭐ Average Rating", "4.3", delta="0.2")
        with col3:
            st.metric("👍 Satisfaction Rate", "89%", delta="5%")
        with col4:
            st.metric("📈 Response Rate", "68%", delta="8%")
        
        # Charts
        col1, col2 = st.columns(2)
        with col1:
            # Rating distribution
            ratings = ["1 Star", "2 Stars", "3 Stars", "4 Stars", "5 Stars"]
            counts = [3, 8, 25, 45, 46]
            fig = px.bar(x=ratings, y=counts, title="Rating Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Feedback by type
            types = ["Event Overall", "Session Specific", "Venue", "Volunteer", "Vendor"]
            type_counts = [45, 35, 20, 15, 12]
            fig = px.pie(values=type_counts, names=types, title="Feedback by Type")
            st.plotly_chart(fig, use_container_width=True)
        
        # Sentiment analysis
        st.markdown("#### 💭 Sentiment Analysis")
        col1, col2 = st.columns(2)
        with col1:
            sentiments = ["Very Positive", "Positive", "Neutral", "Negative", "Very Negative"]
            sentiment_counts = [42, 38, 28, 15, 4]
            fig = px.bar(x=sentiments, y=sentiment_counts, title="Feedback Sentiment")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Response trends over time
            days = ["Day 1", "Day 2", "Day 3", "Post-Event"]
            responses = [45, 38, 32, 12]
            fig = px.line(x=days, y=responses, title="Response Trends")
            st.plotly_chart(fig, use_container_width=True)
        
        # Top comments/keywords
        st.markdown("#### 🔍 Most Mentioned Keywords")
        keywords_data = [
            {"Keyword": "Excellent", "Frequency": 45, "Context": "Event Organization"},
            {"Keyword": "Well Organized", "Frequency": 38, "Context": "Overall Experience"},
            {"Keyword": "Great Speakers", "Frequency": 32, "Context": "Content Quality"},
            {"Keyword": "Perfect Venue", "Frequency": 28, "Context": "Venue & Facilities"},
            {"Keyword": "Improve Catering", "Frequency": 15, "Context": "Food & Beverage"},
        ]
        df_keywords = pd.DataFrame(keywords_data)
        st.dataframe(df_keywords, use_container_width=True, hide_index=True)
    
    with tab4:
        st.markdown("### 📄 Feedback Reports & Documentation")
        
        # Report generation
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📊 Generate Reports")
            report_type = st.selectbox("Select Report Type:", [
                "Overall Feedback Summary",
                "Session-wise Analysis", 
                "Venue Feedback Report",
                "Volunteer Performance Report",
                "Vendor Feedback Analysis",
                "Improvement Recommendations"
            ])
            
            date_range = st.selectbox("Date Range:", ["All Time", "Last 7 Days", "Last 30 Days", "Event Period Only"])
            
            if st.button("📊 Generate Report", use_container_width=True):
                st.success(f"{report_type} generated successfully!")
                
                # Simulate report download
                st.download_button(
                    label="📥 Download Report",
                    data=f"Sample {report_type} report content",
                    file_name=f"feedback_report_{report_type.lower().replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )
        
        with col2:
            st.markdown("#### 📋 Upload Feedback Templates")
            template_file = st.file_uploader("Feedback Form Template", type=['pdf', 'doc', 'docx', 'html'])
            if template_file:
                saved_path = save_uploaded_file(template_file, f"feedback/templates/{template_file.name}")
                st.success(f"✅ Template uploaded!")
                
                file_info = get_file_info(saved_path)
                st.info(f"📄 File: {file_info['name']} | Size: {file_info['size']}")
        
        # Survey configuration
        st.markdown("#### ⚙️ Survey Configuration")
        col1, col2, col3 = st.columns(3)
        with col1:
            survey_config = st.file_uploader("Survey Configuration", type=['json', 'yaml', 'xml'])
            if survey_config:
                saved_path = save_uploaded_file(survey_config, f"feedback/config/{survey_config.name}")
                st.success("✅ Configuration uploaded!")
        
        with col2:
            email_templates = st.file_uploader("Email Templates", type=['html', 'txt'], accept_multiple_files=True)
            if email_templates:
                for template in email_templates:
                    save_uploaded_file(template, f"feedback/email_templates/{template.name}")
                st.success(f"✅ {len(email_templates)} email templates uploaded!")
        
        with col3:
            analytics_config = st.file_uploader("Analytics Configuration", type=['json', 'yaml'])
            if analytics_config:
                saved_path = save_uploaded_file(analytics_config, f"feedback/analytics/{analytics_config.name}")
                st.success("✅ Analytics config uploaded!")
        
        # Automated reports
        st.markdown("#### 🤖 Automated Reporting")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📧 Schedule Daily Reports", use_container_width=True):
                st.success("Daily feedback reports scheduled!")
        with col2:
            if st.button("📊 Setup Real-time Dashboard", use_container_width=True):
                st.success("Real-time feedback dashboard configured!")
        with col3:
            if st.button("🚨 Configure Alerts", use_container_width=True):
                st.success("Low rating alerts configured!")
