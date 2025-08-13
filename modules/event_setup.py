"""
EventIQ Event Setup Module
Comprehensive event configuration and management system
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
from modules.config import config
from modules.constants import EventStatus, UserRole
from modules.models import Event, create_event
from modules.services.file_service import FileService
from modules.utils import show_success_animation

def show_event_setup_module():
    """Main event setup interface for corporate IT events"""
    st.markdown("# 🎯 Corporate IT Event Setup & Management")
    st.markdown("### Comprehensive event management for corporate IT companies")
    
    # Event setup tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🆕 New Corporate Event", 
        "📋 Corporate Templates", 
        "🎯 Event Details", 
        "⚙️ Advanced Settings", 
        "📊 Event Dashboard"
    ])
    
    with tab1:
        show_new_event_setup()
    
    with tab2:
        show_event_templates()
    
    with tab3:
        show_event_details()
    
    with tab4:
        show_advanced_settings()
    
    with tab5:
        show_event_dashboard()

def show_new_event_setup():
    """Create new corporate IT event with comprehensive setup"""
    st.markdown("### 🆕 Create New Corporate IT Event")
    
    # Event type selection
    st.markdown("#### 💼 Corporate IT Event Types")
    event_types = {
        "Tech Conference": {
            "icon": "🏢", 
            "description": "Technology conferences, seminars, product launches",
            "typical_duration": "1-3 days",
            "common_features": ["Keynote Speakers", "Tech Demos", "Networking", "Digital Certificates", "Live Streaming"]
        },
        "Corporate Meeting": {
            "icon": "🤝", 
            "description": "Board meetings, quarterly reviews, team meetings",
            "typical_duration": "Half day - 2 days",
            "common_features": ["AV Equipment", "Presentation Tools", "Video Conferencing", "Digital Minutes"]
        },
        "Team Building": {
            "icon": "👥", 
            "description": "Team building activities, corporate retreats, workshops",
            "typical_duration": "1-2 days",
            "common_features": ["Activities", "Team Challenges", "Catering", "Photography", "Feedback Systems"]
        },
        "Training Workshop": {
            "icon": "�", 
            "description": "Technical training, skill development, certification programs",
            "typical_duration": "1-5 days",
            "common_features": ["Training Materials", "Certifications", "Assessments", "Virtual Labs", "Resources"]
        },
        "Product Launch": {
            "icon": "🚀", 
            "description": "Software releases, product announcements, demo events",
            "typical_duration": "Half day - 1 day",
            "common_features": ["Product Demos", "Press Kit", "Media Coverage", "Client Presentations"]
        },
        "Hackathon": {
            "icon": "💻", 
            "description": "Coding competitions, innovation challenges, tech contests",
            "typical_duration": "1-3 days",
            "common_features": ["Development Environment", "Mentors", "Judging Panel", "Prizes", "Tech Support"]
        },
        "Client Meeting": {
            "icon": "�", 
            "description": "Client presentations, project reviews, stakeholder meetings",
            "typical_duration": "Half day - 1 day",
            "common_features": ["Presentation Setup", "Client Materials", "Refreshments", "Follow-up Actions"]
        },
        "Awards Ceremony": {
            "icon": "🏆", 
            "description": "Employee recognition, achievement awards, company celebrations",
            "typical_duration": "Half day",
            "common_features": ["Awards", "Recognition Certificates", "Photography", "Entertainment", "Catering"]
        },
        "Webinar": {
            "icon": "🌐", 
            "description": "Online seminars, virtual presentations, remote training",
            "typical_duration": "1-4 hours",
            "common_features": ["Streaming Platform", "Interactive Chat", "Recording", "Registration System"]
        }
    }
    
    # Display event type cards
    cols = st.columns(3)
    selected_event_type = None
    
    for i, (event_type, details) in enumerate(event_types.items()):
        with cols[i % 3]:
            if st.button(
                f"{details['icon']} {event_type}", 
                key=f"event_type_{event_type}",
                use_container_width=True
            ):
                selected_event_type = event_type
                st.session_state.selected_event_type = event_type
            
            st.caption(details['description'])
            st.caption(f"⏱️ {details['typical_duration']}")
    
    # Show event type details if selected
    if 'selected_event_type' in st.session_state:
        selected_type = st.session_state.selected_event_type
        details = event_types[selected_type]
        
        st.markdown(f"### {details['icon']} {selected_type} Event Setup")
        
        # Event basic information form
        with st.form("event_setup_form"):
            st.markdown("#### 📝 Basic Information")
            
            col1, col2 = st.columns(2)
            with col1:
                event_name = st.text_input("Event Name:*", placeholder="Enter event name")
                event_description = st.text_area("Description:", placeholder="Brief description of the event")
                organizer_name = st.text_input("Organizer Name:*", placeholder="Event organizer")
                organizer_email = st.text_input("Contact Email:*", placeholder="contact@example.com")
                
            with col2:
                start_date = st.date_input("Start Date:*", value=datetime.now().date())
                end_date = st.date_input("End Date:*", value=datetime.now().date() + timedelta(days=1))
                start_time = st.time_input("Start Time:*")
                end_time = st.time_input("End Time:*")
            
            # Event capacity and location
            st.markdown("#### 📍 Location & Capacity")
            col1, col2 = st.columns(2)
            with col1:
                venue_type = st.selectbox("Venue Type:", [
                    "Physical Location", "Virtual Event", "Hybrid Event"
                ])
                if venue_type in ["Physical Location", "Hybrid Event"]:
                    venue_name = st.text_input("Venue Name:", placeholder="Event venue")
                    venue_address = st.text_area("Venue Address:", placeholder="Full address")
                
            with col2:
                expected_attendees = st.number_input("Expected Attendees:", min_value=1, value=100)
                max_capacity = st.number_input("Maximum Capacity:", min_value=1, value=expected_attendees)
                registration_required = st.checkbox("Registration Required", value=True)
                paid_event = st.checkbox("Paid Event", value=False)
                
                if paid_event:
                    ticket_price = st.number_input("Ticket Price ($):", min_value=0.0, value=0.0)
            
            # Budget setup integration
            st.markdown("#### 💰 Budget Configuration")
            col1, col2 = st.columns(2)
            with col1:
                total_budget = st.number_input("Total Budget ($):", min_value=0, value=10000)
                currency = st.selectbox("Currency:", ["USD", "EUR", "GBP", "INR", "CAD", "AUD"])
            with col2:
                budget_per_person = total_budget / expected_attendees if expected_attendees > 0 else 0
                st.number_input("Budget per Person ($):", value=budget_per_person, disabled=True)
                contingency = st.slider("Contingency Reserve (%):", 5, 25, 10)
            
            # Event-specific features based on type
            st.markdown(f"#### ⚡ {selected_type}-Specific Features")
            features = details['common_features']
            
            selected_features = {}
            if len(features) > 1:
                cols = st.columns(min(len(features), 4))
                for i, feature in enumerate(features):
                    with cols[i % len(cols)]:
                        selected_features[feature] = st.checkbox(feature, value=True)
            
            # Submit form
            if st.form_submit_button("🚀 Create Event", use_container_width=True):
                if event_name and organizer_name and organizer_email:
                    # Create event configuration
                    event_config = {
                        "type": selected_type,
                        "name": event_name,
                        "description": event_description,
                        "organizer": {
                            "name": organizer_name,
                            "email": organizer_email
                        },
                        "schedule": {
                            "start_date": start_date.isoformat(),
                            "end_date": end_date.isoformat(),
                            "start_time": start_time.strftime("%H:%M"),
                            "end_time": end_time.strftime("%H:%M")
                        },
                        "venue": {
                            "type": venue_type,
                            "name": venue_name if venue_type != "Virtual Event" else "Virtual",
                            "address": venue_address if venue_type != "Virtual Event" else "Online"
                        },
                        "capacity": {
                            "expected": expected_attendees,
                            "maximum": max_capacity,
                            "registration_required": registration_required
                        },
                        "budget": {
                            "total": total_budget,
                            "currency": currency,
                            "per_person": budget_per_person,
                            "contingency": contingency
                        },
                        "features": selected_features,
                        "pricing": {
                            "paid_event": paid_event,
                            "ticket_price": ticket_price if paid_event else 0
                        },
                        "created_at": datetime.now().isoformat(),
                        "status": "Draft"
                    }
                    
                    # Store in session state
                    st.session_state.current_event = event_config
                    st.session_state.event_created = True
                    st.success("✅ Event created successfully!")
                    
                else:
                    st.error("Please fill in all required fields (marked with *)")
        
        # Show next steps outside the form if event was created
        if st.session_state.get("event_created", False):
            st.info("""
            🎉 **Event Created Successfully!**
            
            **Next Steps:**
            1. Configure detailed settings in Advanced Settings tab
            2. Set up budget allocation in Budget module
            3. Add team members and assign roles
            4. Create event timeline and milestones
            5. Launch event registration
            """)
            
            # Option to continue with setup (outside form)
            if st.button("➡️ Continue with Advanced Setup", use_container_width=True):
                st.session_state.active_tab = "advanced_settings"
                st.session_state.event_created = False  # Reset the flag
                st.rerun()

def show_event_templates():
    """Pre-built corporate IT event templates for quick setup"""
    st.markdown("### 📋 Corporate IT Event Templates")
    st.markdown("Choose from pre-built templates designed for corporate IT company events")
    
    templates = {
        "Annual Tech Conference 2025": {
            "type": "Tech Conference",
            "description": "3-day technology conference with keynote speakers, tech demos, and networking",
            "duration": "3 days",
            "expected_attendees": 500,
            "budget": 150000,
            "features": ["Keynote Speakers", "Tech Demo Booths", "Networking Sessions", "Digital Certificates", "Live Streaming", "Mobile App"]
        },
        "Quarterly Board Meeting": {
            "type": "Corporate Meeting", 
            "description": "Quarterly business review with board members and executives",
            "duration": "1 day",
            "expected_attendees": 25,
            "budget": 15000,
            "features": ["Board Presentation", "Financial Review", "Executive Dining", "Secure Video Conferencing", "Digital Minutes"]
        },
        "Software Development Training": {
            "type": "Training Workshop",
            "description": "5-day intensive training on latest development technologies and best practices",
            "duration": "5 days",
            "expected_attendees": 50,
            "budget": 35000,
            "features": ["Hands-on Labs", "Expert Trainers", "Certification Exams", "Training Materials", "Virtual Environment Access"]
        },
        "Product Launch Event": {
            "type": "Product Launch",
            "description": "New software product launch with client demos and media coverage",
            "duration": "1 day", 
            "expected_attendees": 200,
            "budget": 75000,
            "features": ["Product Demonstrations", "Press Conference", "Client Presentations", "Media Kit", "Live Demo Environment"]
        },
        "Innovation Hackathon": {
            "type": "Hackathon",
            "description": "48-hour coding competition for developing innovative solutions",
            "duration": "2 days",
            "expected_attendees": 100,
            "budget": 50000,
            "features": ["Development Workstations", "Mentorship", "Judging Panel", "Prize Distribution", "24/7 Tech Support"]
        },
        "Employee Recognition Awards": {
            "type": "Awards Ceremony",
            "description": "Annual employee recognition ceremony celebrating achievements",
            "duration": "1 evening",
            "expected_attendees": 300,
            "budget": 40000,
            "features": ["Awards Presentation", "Achievement Certificates", "Professional Photography", "Gala Dinner", "Entertainment"]
        },
        "Client Webinar Series": {
            "type": "Webinar",
            "description": "Monthly webinar series for client education and product updates",
            "duration": "2 hours",
            "expected_attendees": 1000,
            "budget": 8000,
            "features": ["HD Streaming", "Interactive Q&A", "Recording & Replay", "Registration Management", "Follow-up Materials"]
        },
        "Team Building Workshop": {
            "type": "Team Building",
            "description": "Department team building activities and skill development workshop",
            "duration": "1 day",
            "expected_attendees": 75,
            "budget": 25000,
            "features": ["Team Activities", "Leadership Workshops", "Outdoor Challenges", "Team Lunch", "Feedback Sessions"]
        }
    }
    
    # Display templates in cards
    cols = st.columns(2)
    for i, (template_name, template_data) in enumerate(templates.items()):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"#### {template_data['type']} Template")
                st.markdown(f"**{template_name}**")
                st.markdown(template_data['description'])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.caption(f"⏱️ Duration: {template_data['duration']}")
                    st.caption(f"👥 Attendees: {template_data['expected_attendees']}")
                with col2:
                    st.caption(f"💰 Budget: ${template_data['budget']:,}")
                
                # Features
                st.markdown("**Features:**")
                for feature in template_data['features'][:3]:
                    st.markdown(f"• {feature}")
                if len(template_data['features']) > 3:
                    st.caption(f"+ {len(template_data['features']) - 3} more features")
                
                if st.button(f"Use {template_name} Template", key=f"template_{template_name}", use_container_width=True):
                    st.session_state.selected_template = template_data
                    st.session_state.template_name = template_name
                    st.success(f"✅ Template '{template_name}' selected!")
                    
                st.markdown("---")
    
    # Custom template creation
    st.markdown("### 🛠️ Create Custom Template")
    with st.expander("➕ Create Your Own Template"):
        with st.form("custom_template"):
            template_name = st.text_input("Template Name:")
            template_description = st.text_area("Description:")
            template_type = st.selectbox("Event Type:", ["Conference", "Wedding", "Corporate Meeting", "Festival", "Trade Show", "Sports Event", "Educational", "Charity/Fundraising"])
            
            col1, col2 = st.columns(2)
            with col1:
                default_duration = st.text_input("Default Duration:", value="1 day")
                default_attendees = st.number_input("Default Attendees:", value=100)
            with col2:
                default_budget = st.number_input("Default Budget ($):", value=10000)
                
            if st.form_submit_button("💾 Save Template"):
                st.success("Custom template saved!")

def show_event_details():
    """Detailed event configuration and management"""
    st.markdown("### 🎯 Event Details & Configuration")
    
    if 'current_event' not in st.session_state:
        st.warning("⚠️ No event selected. Please create an event first.")
        return
    
    event = st.session_state.current_event
    
    # Event overview
    st.markdown(f"## {event['name']}")
    st.markdown(f"**Type:** {event['type']} | **Status:** {event['status']}")
    
    # Editable event details
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Basic Info", "📅 Schedule", "👥 Team & Roles", "📊 Progress"])
    
    with tab1:
        show_basic_info_editor(event)
    
    with tab2:
        show_schedule_manager(event)
    
    with tab3:
        show_team_management(event)
    
    with tab4:
        show_progress_tracker(event)

def show_basic_info_editor(event):
    """Edit basic event information"""
    st.markdown("#### 📝 Edit Basic Information")
    
    with st.form("edit_basic_info"):
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("Event Name:", value=event['name'])
            new_description = st.text_area("Description:", value=event.get('description', ''))
            new_organizer = st.text_input("Organizer:", value=event['organizer']['name'])
            
        with col2:
            new_email = st.text_input("Contact Email:", value=event['organizer']['email'])
            new_expected = st.number_input("Expected Attendees:", value=event['capacity']['expected'])
            new_max = st.number_input("Max Capacity:", value=event['capacity']['maximum'])
        
        if st.form_submit_button("💾 Update Basic Info"):
            # Update event in session state
            st.session_state.current_event.update({
                'name': new_name,
                'description': new_description,
                'organizer': {'name': new_organizer, 'email': new_email},
                'capacity': {'expected': new_expected, 'maximum': new_max, 'registration_required': event['capacity']['registration_required']}
            })
            st.success("✅ Basic information updated!")

def show_schedule_manager(event):
    """Manage event schedule and timeline"""
    st.markdown("#### 📅 Schedule Management")
    
    # Current schedule
    schedule = event['schedule']
    st.info(f"""
    **Current Schedule:**  
    📅 **Dates:** {schedule['start_date']} to {schedule['end_date']}  
    ⏰ **Time:** {schedule['start_time']} - {schedule['end_time']}
    """)
    
    # Schedule editor
    with st.form("schedule_editor"):
        col1, col2 = st.columns(2)
        with col1:
            new_start_date = st.date_input("Start Date:", value=datetime.fromisoformat(schedule['start_date']).date())
            new_start_time = st.time_input("Start Time:", value=datetime.strptime(schedule['start_time'], "%H:%M").time())
        with col2:
            new_end_date = st.date_input("End Date:", value=datetime.fromisoformat(schedule['end_date']).date())
            new_end_time = st.time_input("End Time:", value=datetime.strptime(schedule['end_time'], "%H:%M").time())
        
        if st.form_submit_button("🔄 Update Schedule"):
            st.session_state.current_event['schedule'].update({
                'start_date': new_start_date.isoformat(),
                'end_date': new_end_date.isoformat(),
                'start_time': new_start_time.strftime("%H:%M"),
                'end_time': new_end_time.strftime("%H:%M")
            })
            st.success("✅ Schedule updated!")
    
    # Timeline management
    st.markdown("#### ⏰ Event Timeline")
    
    if 'timeline' not in st.session_state.current_event:
        st.session_state.current_event['timeline'] = []
    
    # Add timeline item
    with st.expander("➕ Add Timeline Item"):
        with st.form("add_timeline"):
            col1, col2 = st.columns(2)
            with col1:
                timeline_date = st.date_input("Date:")
                timeline_time = st.time_input("Time:")
            with col2:
                timeline_title = st.text_input("Title:")
                timeline_description = st.text_area("Description:")
            
            if st.form_submit_button("➕ Add to Timeline"):
                timeline_item = {
                    "date": timeline_date.isoformat(),
                    "time": timeline_time.strftime("%H:%M"),
                    "title": timeline_title,
                    "description": timeline_description
                }
                st.session_state.current_event['timeline'].append(timeline_item)
                st.success("Timeline item added!")
    
    # Display current timeline
    if st.session_state.current_event['timeline']:
        st.markdown("**Current Timeline:**")
        for i, item in enumerate(st.session_state.current_event['timeline']):
            with st.container():
                col1, col2, col3 = st.columns([2, 4, 1])
                with col1:
                    st.text(f"{item['date']} {item['time']}")
                with col2:
                    st.markdown(f"**{item['title']}**")
                    st.caption(item['description'])
                with col3:
                    if st.button("🗑️", key=f"delete_timeline_{i}"):
                        st.session_state.current_event['timeline'].pop(i)
                        st.rerun()

def show_team_management(event):
    """Manage event team and role assignments"""
    st.markdown("#### 👥 Team & Role Management")
    
    # Initialize team if not exists
    if 'team' not in st.session_state.current_event:
        st.session_state.current_event['team'] = []
    
    # Available roles based on event type
    roles_by_type = {
        "Tech Conference": ["Event Manager", "Technical Coordinator", "Speaker Liaison", "IT Support", "Marketing Manager", "Registration Coordinator"],
        "Corporate Meeting": ["Meeting Facilitator", "IT Support", "Executive Assistant", "Catering Coordinator", "Security Officer"],
        "Team Building": ["Team Building Facilitator", "HR Coordinator", "Activity Coordinator", "Photographer", "Logistics Manager"],
        "Training Workshop": ["Training Coordinator", "Subject Matter Expert", "IT Lab Manager", "Assessment Coordinator", "Technical Support"],
        "Product Launch": ["Product Manager", "Demo Coordinator", "Marketing Lead", "Press Relations", "Technical Support", "Client Relations"],
        "Hackathon": ["Hackathon Director", "Technical Mentor", "Judge Coordinator", "DevOps Support", "Catering Manager", "Prize Coordinator"],
        "Client Meeting": ["Account Manager", "Technical Lead", "Presentation Coordinator", "Client Relations", "IT Support"],
        "Awards Ceremony": ["Event Coordinator", "HR Manager", "AV Technician", "Photography Team", "Catering Manager", "Awards Coordinator"],
        "Webinar": ["Webinar Host", "Technical Producer", "Content Manager", "Registration Coordinator", "Technical Support"],
        "Custom": ["Event Manager", "Project Coordinator", "Technical Lead", "Marketing Manager", "Logistics Coordinator", "Support Staff"]
    }
    
    available_roles = roles_by_type.get(event['type'], roles_by_type["Custom"])
    
    # Add team member
    with st.expander("➕ Add Team Member"):
        with st.form("add_team_member"):
            col1, col2 = st.columns(2)
            with col1:
                member_name = st.text_input("Name:")
                member_email = st.text_input("Email:")
            with col2:
                member_role = st.selectbox("Role:", available_roles)
                member_department = st.text_input("Department:")
            
            member_permissions = st.multiselect("Permissions:", [
                "View All", "Edit Event Details", "Manage Budget", "Manage Team", 
                "Manage Participants", "Generate Reports", "Admin Access"
            ])
            
            if st.form_submit_button("➕ Add Team Member"):
                team_member = {
                    "name": member_name,
                    "email": member_email,
                    "role": member_role,
                    "department": member_department,
                    "permissions": member_permissions,
                    "added_date": datetime.now().isoformat()
                }
                st.session_state.current_event['team'].append(team_member)
                st.success(f"Team member {member_name} added!")
    
    # Display current team
    if st.session_state.current_event['team']:
        st.markdown("**Current Team:**")
        team_df = pd.DataFrame(st.session_state.current_event['team'])
        st.dataframe(team_df[['name', 'role', 'email', 'department']], use_container_width=True, hide_index=True)
    else:
        st.info("No team members added yet.")

def show_progress_tracker(event):
    """Track event preparation progress"""
    st.markdown("#### 📊 Event Progress Tracker")
    
    # Progress categories
    progress_categories = {
        "Planning & Approval": ["Event Concept & Objectives", "Budget Approval", "Venue Booking", "Date Confirmation", "Management Sign-off"],
        "Technology Setup": ["IT Infrastructure", "AV Equipment", "Network Setup", "Security Systems", "Backup Solutions"],
        "Content & Speakers": ["Speaker Confirmation", "Presentation Materials", "Technical Requirements", "Demo Environment", "Content Review"],
        "Marketing & Registration": ["Marketing Plan", "Registration System", "Internal Communications", "External Promotion", "Attendee Management"],
        "Final Preparations": ["Rehearsals & Testing", "Final Headcount", "Emergency Protocols", "Day-of Coordination", "Post-Event Follow-up Plan"]
    }
    
    # Initialize progress if not exists
    if 'progress' not in st.session_state.current_event:
        st.session_state.current_event['progress'] = {}
        for category, tasks in progress_categories.items():
            st.session_state.current_event['progress'][category] = {task: False for task in tasks}
    
    # Display progress
    total_tasks = sum(len(tasks) for tasks in progress_categories.values())
    completed_tasks = sum(
        sum(st.session_state.current_event['progress'][cat].values()) 
        for cat in progress_categories.keys()
    )
    
    progress_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    
    st.metric("Overall Progress", f"{progress_percentage:.1f}%", f"{completed_tasks}/{total_tasks} tasks")
    st.progress(progress_percentage / 100)
    
    # Category progress
    for category, tasks in progress_categories.items():
        with st.expander(f"{category} ({sum(st.session_state.current_event['progress'][category].values())}/{len(tasks)} completed)"):
            for task in tasks:
                current_status = st.session_state.current_event['progress'][category].get(task, False)
                new_status = st.checkbox(task, value=current_status, key=f"progress_{category}_{task}")
                if new_status != current_status:
                    st.session_state.current_event['progress'][category][task] = new_status
                    st.rerun()

def show_advanced_settings():
    """Advanced event configuration options"""
    st.markdown("### ⚙️ Advanced Event Settings")
    
    if 'current_event' not in st.session_state:
        st.warning("⚠️ No event selected. Please create an event first.")
        return
    
    event = st.session_state.current_event
    
    # Advanced settings tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔧 Configuration", "🔒 Security", "📧 Notifications", "🔌 Integrations"])
    
    with tab1:
        show_configuration_settings(event)
    
    with tab2:
        show_security_settings(event)
    
    with tab3:
        show_notification_settings(event)
    
    with tab4:
        show_integration_settings(event)

def show_configuration_settings(event):
    """Event configuration settings"""
    st.markdown("#### 🔧 Event Configuration")
    
    # Registration settings
    st.markdown("**Registration Settings**")
    col1, col2 = st.columns(2)
    with col1:
        registration_open = st.checkbox("Registration Open", value=True)
        early_bird_discount = st.checkbox("Early Bird Discount", value=False)
        if early_bird_discount:
            early_bird_date = st.date_input("Early Bird Deadline:")
            early_bird_percent = st.slider("Early Bird Discount (%):", 5, 50, 20)
    
    with col2:
        waitlist_enabled = st.checkbox("Enable Waitlist", value=True)
        confirmation_required = st.checkbox("Require Confirmation", value=True)
        custom_fields = st.text_area("Custom Registration Fields (one per line):")
    
    # Event features
    st.markdown("**Event Features**")
    feature_cols = st.columns(3)
    features = [
        "Live Streaming", "Recording", "Q&A Sessions", "Networking", 
        "Mobile App", "Check-in System", "Feedback Collection", 
        "Certificate Generation", "Photo Gallery"
    ]
    
    selected_features = {}
    for i, feature in enumerate(features):
        with feature_cols[i % 3]:
            selected_features[feature] = st.checkbox(feature, key=f"feature_{feature}")
    
    # Accessibility options
    st.markdown("**Accessibility Options**")
    col1, col2 = st.columns(2)
    with col1:
        accessibility_features = st.multiselect("Accessibility Features:", [
            "Sign Language Interpretation", "Closed Captions", "Wheelchair Access",
            "Audio Description", "Large Print Materials", "Braille Materials"
        ])
    with col2:
        dietary_options = st.multiselect("Dietary Options:", [
            "Vegetarian", "Vegan", "Gluten-Free", "Kosher", "Halal", "Nut-Free"
        ])

def show_security_settings(event):
    """Security and privacy settings"""
    st.markdown("#### 🔒 Security & Privacy Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Access Control**")
        require_login = st.checkbox("Require Login for Registration", value=True)
        email_verification = st.checkbox("Email Verification Required", value=True)
        admin_approval = st.checkbox("Admin Approval for Registration", value=False)
        
        st.markdown("**Data Privacy**")
        gdpr_compliance = st.checkbox("GDPR Compliance Mode", value=True)
        data_retention_days = st.number_input("Data Retention (days):", min_value=30, value=365)
        
    with col2:
        st.markdown("**Security Measures**")
        two_factor_auth = st.checkbox("Two-Factor Authentication", value=False)
        session_timeout = st.number_input("Session Timeout (minutes):", min_value=15, value=60)
        max_login_attempts = st.number_input("Max Login Attempts:", min_value=3, value=5)
        
        st.markdown("**Content Security**")
        content_moderation = st.checkbox("Content Moderation", value=True)
        spam_protection = st.checkbox("Spam Protection", value=True)

def show_notification_settings(event):
    """Notification and communication settings"""
    st.markdown("#### 📧 Notification Settings")
    
    # Email notifications
    st.markdown("**Email Notifications**")
    col1, col2 = st.columns(2)
    with col1:
        registration_confirmation = st.checkbox("Registration Confirmation", value=True)
        event_reminders = st.checkbox("Event Reminders", value=True)
        if event_reminders:
            reminder_days = st.multiselect("Send Reminders:", ["7 days before", "3 days before", "1 day before", "2 hours before"])
        
    with col2:
        update_notifications = st.checkbox("Event Update Notifications", value=True)
        feedback_requests = st.checkbox("Post-Event Feedback Requests", value=True)
        newsletter_signup = st.checkbox("Newsletter Signup Option", value=False)
    
    # Communication channels
    st.markdown("**Communication Channels**")
    communication_channels = st.multiselect("Enable Communication Channels:", [
        "Email", "SMS", "Push Notifications", "In-App Messages", "Slack Integration", "WhatsApp"
    ])
    
    # Custom notification templates
    st.markdown("**Custom Email Templates**")
    with st.expander("Customize Email Templates"):
        template_type = st.selectbox("Template Type:", [
            "Registration Confirmation", "Event Reminder", "Event Updates", "Feedback Request"
        ])
        
        template_subject = st.text_input("Email Subject:", value=f"[{event['name']}] ")
        template_body = st.text_area("Email Body:", height=200, 
                                   value="Dear {{participant_name}},\n\nThank you for registering for {{event_name}}.\n\nBest regards,\nEvent Team")
        
        if st.button("💾 Save Template"):
            st.success("Email template saved!")

def show_integration_settings(event):
    """Third-party integrations"""
    st.markdown("#### 🔌 Third-Party Integrations")
    
    # Popular integrations for corporate IT events
    integrations = {
        "Microsoft Teams": {"icon": "📹", "description": "Enterprise video conferencing and collaboration", "status": "Available"},
        "Zoom": {"icon": "🎥", "description": "Video conferencing for hybrid and virtual events", "status": "Available"},
        "Salesforce": {"icon": "☁️", "description": "CRM integration for lead management and attendee tracking", "status": "Available"},
        "Office 365": {"icon": "📧", "description": "Email integration and document collaboration", "status": "Connected"},
        "Slack": {"icon": "�", "description": "Team communication and event notifications", "status": "Available"},
        "Azure Active Directory": {"icon": "�", "description": "Single sign-on and user authentication", "status": "Available"},
        "ServiceNow": {"icon": "🎯", "description": "IT service management and workflow automation", "status": "Available"},
        "Jira": {"icon": "📋", "description": "Project management and issue tracking", "status": "Available"},
        "Power BI": {"icon": "📊", "description": "Business intelligence and analytics dashboards", "status": "Available"},
        "SharePoint": {"icon": "📁", "description": "Document management and collaboration platform", "status": "Available"}
    }
    
    cols = st.columns(2)
    for i, (integration, details) in enumerate(integrations.items()):
        with cols[i % 2]:
            with st.container():
                col1, col2, col3 = st.columns([1, 3, 1])
                with col1:
                    st.markdown(f"### {details['icon']}")
                with col2:
                    st.markdown(f"**{integration}**")
                    st.caption(details['description'])
                with col3:
                    if details['status'] == "Connected":
                        st.success("✅ Connected")
                    else:
                        if st.button("Connect", key=f"connect_{integration}"):
                            st.success(f"Connected to {integration}!")
                
                st.markdown("---")
    
    # Custom integrations
    st.markdown("#### 🛠️ Custom Integrations")
    with st.expander("Add Custom Integration"):
        custom_name = st.text_input("Integration Name:")
        custom_url = st.text_input("Webhook URL:")
        custom_auth = st.text_input("API Key/Token:", type="password")
        
        if st.button("🔗 Add Integration"):
            st.success("Custom integration added!")

def show_event_dashboard():
    """Event overview dashboard"""
    st.markdown("### 📊 Event Dashboard")
    
    if 'current_event' not in st.session_state:
        st.warning("⚠️ No event selected. Please create an event first.")
        return
    
    event = st.session_state.current_event
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📅 Days Until Event", "45", delta="-1")
    with col2:
        registrations = 127
        capacity = event['capacity']['expected']
        st.metric("👥 Registrations", f"{registrations}/{capacity}", delta="+12")
    with col3:
        budget_used = 28000
        total_budget = event['budget']['total']
        st.metric("💰 Budget Used", f"${budget_used:,}", delta=f"{(budget_used/total_budget)*100:.1f}%")
    with col4:
        st.metric("📋 Tasks Complete", "68%", delta="+5%")
    
    # Charts
    col1, col2 = st.columns(2)
    with col1:
        # Registration trend
        st.markdown("#### 📈 Registration Trend")
        days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"]
        registrations = [15, 28, 45, 67, 89]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=days, y=registrations, mode='lines+markers', name='Registrations'))
        fig.update_layout(title="Daily Registration Count", xaxis_title="Days", yaxis_title="Cumulative Registrations")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Budget breakdown
        st.markdown("#### 💰 Budget Breakdown")
        categories = ["Venue", "Catering", "AV Tech", "Marketing", "Staff"]
        budgets = [12000, 8000, 6000, 4000, 3000]
        
        fig = go.Figure(data=go.Pie(labels=categories, values=budgets))
        fig.update_layout(title="Budget Allocation by Category")
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity
    st.markdown("#### 📝 Recent Activity")
    activities = [
        {"time": "2 hours ago", "activity": "New registration: John Smith", "type": "registration"},
        {"time": "5 hours ago", "activity": "Budget updated by Finance Team", "type": "budget"},
        {"time": "1 day ago", "activity": "Venue contract signed", "type": "contract"},
        {"time": "2 days ago", "activity": "Speaker confirmed: Dr. Jane Doe", "type": "speaker"},
        {"time": "3 days ago", "activity": "Marketing campaign launched", "type": "marketing"}
    ]
    
    for activity in activities:
        icon = {"registration": "👥", "budget": "💰", "contract": "📋", "speaker": "🎤", "marketing": "📢"}.get(activity['type'], "📝")
        st.markdown(f"{icon} **{activity['time']}** - {activity['activity']}")
    
    # Quick actions
    st.markdown("#### ⚡ Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📧 Send Update", use_container_width=True):
            st.success("Update email sent to all participants!")
    with col2:
        if st.button("📊 Generate Report", use_container_width=True):
            st.success("Event report generated!")
    with col3:
        if st.button("💾 Export Data", use_container_width=True):
            st.success("Event data exported!")
    with col4:
        if st.button("🔄 Backup Event", use_container_width=True):
            st.success("Event backed up successfully!")
