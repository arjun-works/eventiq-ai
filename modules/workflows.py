"""
Workflows Management Module for EventIQ Management System
Team Member: [Workflows Team]
"""

from .utils import *

def show_workflows_page():
    """Workflows management interface"""
    st.markdown("## 🔄 Workflow Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔄 Active Workflows", "➕ Create Workflow", "📊 Analytics", "📄 Templates"])
    
    with tab1:
        st.markdown("### 🔄 Active Workflows")
        
        # Filter and search
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Filter by Status:", ["All", "Active", "Completed", "Paused", "Failed"])
        with col2:
            priority_filter = st.selectbox("Filter by Priority:", ["All", "High", "Medium", "Low"])
        with col3:
            search_workflow = st.text_input("🔍 Search workflows:", placeholder="Enter workflow name...")
        
        workflows = [
            {"Name": "Vendor Onboarding", "Status": "Active", "Progress": "75%", "Priority": "High", "Next Step": "Document Review", "Assigned": "John Doe"},
            {"Name": "Volunteer Training", "Status": "Completed", "Progress": "100%", "Priority": "Medium", "Next Step": "N/A", "Assigned": "Sarah Smith"},
            {"Name": "Equipment Setup", "Status": "In Progress", "Progress": "45%", "Priority": "High", "Next Step": "Testing Phase", "Assigned": "Mike Wilson"},
            {"Name": "Catering Coordination", "Status": "Active", "Progress": "60%", "Priority": "Medium", "Next Step": "Menu Approval", "Assigned": "Alice Brown"},
            {"Name": "Security Briefing", "Status": "Paused", "Progress": "30%", "Priority": "High", "Next Step": "Schedule Meeting", "Assigned": "Tom Davis"},
        ]
        
        # Apply filters
        filtered_workflows = workflows
        if status_filter != "All":
            filtered_workflows = [w for w in filtered_workflows if w["Status"] == status_filter]
        if priority_filter != "All":
            filtered_workflows = [w for w in filtered_workflows if w["Priority"] == priority_filter]
        if search_workflow:
            filtered_workflows = [w for w in filtered_workflows if search_workflow.lower() in w["Name"].lower()]
        
        for workflow in filtered_workflows:
            with st.expander(f"🔄 {workflow['Name']} - {workflow['Status']} ({workflow['Priority']} Priority)"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Progress:** {workflow['Progress']}")
                    st.write(f"**Next Step:** {workflow['Next Step']}")
                    st.write(f"**Assigned to:** {workflow['Assigned']}")
                
                with col2:
                    st.write(f"**Priority:** {workflow['Priority']}")
                    st.write(f"**Status:** {workflow['Status']}")
                    
                    # Progress bar
                    progress_val = int(workflow['Progress'].replace('%', ''))
                    st.progress(progress_val / 100)
                
                with col3:
                    if st.button(f"📋 View Details", key=f"workflow_details_{workflow['Name']}"):
                        st.success(f"Opening {workflow['Name']} details")
                    if st.button(f"✏️ Edit", key=f"workflow_edit_{workflow['Name']}"):
                        st.info(f"Editing {workflow['Name']}")
                    if st.button(f"▶️ Advance", key=f"workflow_advance_{workflow['Name']}"):
                        st.success(f"Advanced {workflow['Name']} to next step")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("🔄 Refresh All", use_container_width=True):
                st.success("All workflows refreshed!")
        with col2:
            if st.button("📧 Send Updates", use_container_width=True):
                st.success("Progress updates sent!")
        with col3:
            if st.button("📊 Generate Report", use_container_width=True):
                st.success("Workflow report generated!")
        with col4:
            if st.button("⚠️ Check Overdue", use_container_width=True):
                st.warning("2 workflows are overdue!")
    
    with tab2:
        st.markdown("### ➕ Create New Workflow")
        
        with st.form("create_workflow"):
            col1, col2 = st.columns(2)
            with col1:
                workflow_name = st.text_input("Workflow Name:*")
                workflow_description = st.text_area("Description:*")
                priority = st.selectbox("Priority:", ["Low", "Medium", "High", "Critical"])
                assigned_to = st.selectbox("Assign to:", ["John Doe", "Sarah Smith", "Mike Wilson", "Alice Brown", "Tom Davis"])
                due_date = st.date_input("Due Date:")
            
            with col2:
                category = st.selectbox("Category:", ["Event Setup", "Vendor Management", "Staff Coordination", "Technical", "Marketing", "Other"])
                dependencies = st.multiselect("Dependencies:", ["Vendor Onboarding", "Equipment Setup", "Volunteer Training", "Security Briefing"])
                approval_required = st.checkbox("Requires Approval")
                notifications = st.multiselect("Notify:", ["Email", "SMS", "In-App", "Slack"])
                estimated_hours = st.number_input("Estimated Hours:", min_value=1, max_value=1000, value=8)
            
            # Workflow steps
            st.markdown("#### 📋 Workflow Steps")
            num_steps = st.number_input("Number of Steps:", min_value=1, max_value=20, value=3)
            
            steps = []
            for i in range(num_steps):
                step_col1, step_col2, step_col3 = st.columns(3)
                with step_col1:
                    step_name = st.text_input(f"Step {i+1} Name:", key=f"step_name_{i}")
                with step_col2:
                    step_assignee = st.selectbox(f"Assignee:", ["John Doe", "Sarah Smith", "Mike Wilson", "Alice Brown", "Tom Davis"], key=f"step_assignee_{i}")
                with step_col3:
                    step_duration = st.number_input(f"Duration (hours):", min_value=1, max_value=100, value=2, key=f"step_duration_{i}")
                
                if step_name:
                    steps.append({"name": step_name, "assignee": step_assignee, "duration": step_duration})
            
            # File attachments
            st.markdown("#### 📄 Attachments")
            col1, col2 = st.columns(2)
            with col1:
                workflow_template = st.file_uploader("Workflow Template", type=['pdf', 'doc', 'docx', 'xlsx'])
                if workflow_template:
                    st.success(f"✅ Template uploaded: {workflow_template.name}")
            
            with col2:
                reference_docs = st.file_uploader("Reference Documents", type=['pdf', 'doc', 'docx'], accept_multiple_files=True)
                if reference_docs:
                    st.success(f"✅ {len(reference_docs)} reference documents uploaded")
            
            submitted = st.form_submit_button("🔄 Create Workflow", use_container_width=True)
            
            if submitted:
                if workflow_name and workflow_description and len(steps) > 0:
                    # Save uploaded files
                    if workflow_template:
                        save_uploaded_file(workflow_template, f"workflows/templates/{workflow_name}_{workflow_template.name}")
                    
                    if reference_docs:
                        for doc in reference_docs:
                            save_uploaded_file(doc, f"workflows/references/{workflow_name}_{doc.name}")
                    
                    st.success(f"✅ Workflow '{workflow_name}' created successfully!")
                    st.info(f"📧 Notification sent to {assigned_to}")
                    show_success_animation()
                else:
                    st.error("❌ Please fill in all required fields and add at least one step")
    
    with tab3:
        st.markdown("### 📊 Workflow Analytics")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🔄 Active Workflows", "8", delta="2")
        with col2:
            st.metric("✅ Completed This Month", "15", delta="3")
        with col3:
            st.metric("⏰ Avg Completion Time", "3.2 days", delta="-0.5")
        with col4:
            st.metric("📈 Success Rate", "94%", delta="2%")
        
        # Charts
        col1, col2 = st.columns(2)
        with col1:
            # Workflow status distribution
            statuses = ["Active", "Completed", "Paused", "Failed"]
            counts = [8, 15, 2, 1]
            fig = px.pie(values=counts, names=statuses, title="Workflow Status Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Completion trends
            months = ["Nov", "Dec", "Jan"]
            completed = [12, 18, 15]
            fig = px.line(x=months, y=completed, title="Workflow Completion Trends")
            st.plotly_chart(fig, use_container_width=True)
        
        # Performance by category
        st.markdown("#### 📈 Performance by Category")
        category_data = [
            {"Category": "Event Setup", "Total": 5, "Completed": 4, "Success Rate": "80%", "Avg Duration": "2.5 days"},
            {"Category": "Vendor Management", "Total": 8, "Completed": 7, "Success Rate": "87%", "Avg Duration": "3.1 days"},
            {"Category": "Staff Coordination", "Total": 6, "Completed": 6, "Success Rate": "100%", "Avg Duration": "1.8 days"},
            {"Category": "Technical", "Total": 4, "Completed": 3, "Success Rate": "75%", "Avg Duration": "4.2 days"},
        ]
        df_category = pd.DataFrame(category_data)
        st.dataframe(df_category, use_container_width=True, hide_index=True)
        
        # Team performance
        st.markdown("#### 👥 Team Performance")
        team_data = [
            {"Team Member": "John Doe", "Active Workflows": 3, "Completed": 12, "Success Rate": "95%"},
            {"Team Member": "Sarah Smith", "Active Workflows": 2, "Completed": 8, "Success Rate": "100%"},
            {"Team Member": "Mike Wilson", "Active Workflows": 2, "Completed": 6, "Success Rate": "85%"},
            {"Team Member": "Alice Brown", "Active Workflows": 1, "Completed": 5, "Success Rate": "90%"},
        ]
        df_team = pd.DataFrame(team_data)
        st.dataframe(df_team, use_container_width=True, hide_index=True)
    
    with tab4:
        st.markdown("### 📄 Workflow Templates & Documentation")
        
        # Template upload section
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📋 Upload Workflow Templates")
            template_file = st.file_uploader("Workflow Template", type=['pdf', 'doc', 'docx', 'xlsx', 'json'])
            if template_file:
                saved_path = save_uploaded_file(template_file, f"workflows/templates/{template_file.name}")
                st.success(f"✅ Template uploaded!")
                
                file_info = get_file_info(saved_path)
                st.info(f"📄 File: {file_info['name']} | Size: {file_info['size']}")
        
        with col2:
            st.markdown("#### 📚 Upload Process Documentation")
            process_doc = st.file_uploader("Process Documentation", type=['pdf', 'doc', 'docx'])
            if process_doc:
                saved_path = save_uploaded_file(process_doc, f"workflows/documentation/{process_doc.name}")
                st.success(f"✅ Documentation uploaded!")
                
                file_info = get_file_info(saved_path)
                st.info(f"📄 File: {file_info['name']} | Size: {file_info['size']}")
        
        # Standard operating procedures
        st.markdown("#### 📖 Standard Operating Procedures (SOPs)")
        sop_file = st.file_uploader("Upload SOP Documents", type=['pdf', 'doc', 'docx'], accept_multiple_files=True)
        if sop_file:
            for doc in sop_file:
                saved_path = save_uploaded_file(doc, f"workflows/sops/{doc.name}")
            st.success(f"✅ {len(sop_file)} SOP documents uploaded!")
        
        # Template library
        st.markdown("#### 📚 Template Library")
        templates_data = [
            {"Template": "Vendor Onboarding", "Category": "Vendor Management", "Last Updated": "2025-01-20", "Usage": "15 times"},
            {"Template": "Event Setup Checklist", "Category": "Event Setup", "Last Updated": "2025-01-18", "Usage": "8 times"},
            {"Template": "Security Protocol", "Category": "Security", "Last Updated": "2025-01-15", "Usage": "5 times"},
            {"Template": "Equipment Testing", "Category": "Technical", "Last Updated": "2025-01-10", "Usage": "12 times"},
        ]
        df_templates = pd.DataFrame(templates_data)
        st.dataframe(df_templates, use_container_width=True, hide_index=True)
        
        # Workflow automation
        st.markdown("#### 🤖 Workflow Automation")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Auto-assign Tasks", use_container_width=True):
                st.success("Tasks auto-assigned based on availability!")
        with col2:
            if st.button("📧 Schedule Reminders", use_container_width=True):
                st.success("Automated reminders scheduled!")
        with col3:
            if st.button("📊 Generate SLA Report", use_container_width=True):
                st.success("SLA compliance report generated!")
