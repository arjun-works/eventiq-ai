"""
Budget Module for EventIQ Management System
Team Member: [Budget Management Team]
"""

from .utils import *

def show_budget_module():
    """Budget management interface"""
    st.markdown("## 💰 Budget & Expense Management")
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "⚙️ Budget Setup", "📊 Budget Overview", "📋 Expenses", 
        "➕ Add Expense", "📄 Receipts", "📈 Analytics"
    ])
    
    with tab1:
        show_budget_setup()
    
    with tab2:
        show_budget_overview()
    
    with tab3:
        show_expenses_list()
    
    with tab4:
        show_add_expense()
    
    with tab5:
        show_receipts_management()
    
    with tab6:
        show_budget_analytics()

def show_budget_setup():
    """Budget setup and configuration interface"""
    st.markdown("### ⚙️ Budget Setup & Configuration")
    
    # Event budget configuration
    with st.form("budget_setup_form"):
        st.markdown("#### 🎯 Event Budget Configuration")
        
        col1, col2 = st.columns(2)
        with col1:
            event_name = st.text_input("Event Name:*", value="Tech Conference 2025")
            total_budget = st.number_input("Total Event Budget ($):*", min_value=1000, value=50000, step=1000)
            currency = st.selectbox("Currency:", ["USD", "EUR", "GBP", "INR", "CAD", "AUD"])
            budget_year = st.selectbox("Budget Year:", ["2025", "2024", "2026"])
            
        with col2:
            expected_attendees = st.number_input("Expected Attendees:", min_value=10, value=300, step=10)
            budget_per_person = st.number_input("Budget per Person ($):", value=total_budget/300 if total_budget else 0, disabled=True)
            contingency_percent = st.slider("Contingency Reserve (%):", 5, 25, 10)
            approval_required = st.checkbox("Require approval for expenses over $1000", value=True)
        
        # Category budget allocation
        st.markdown("#### 📊 Category Budget Allocation")
        
        # Pre-defined categories with suggested percentages
        categories = {
            "Venue & Technology Infrastructure": 30,
            "Catering & Refreshments": 20,
            "Speakers & Expert Fees": 15,
            "AV Equipment & IT Setup": 12,
            "Marketing & Communications": 8,
            "Staff & Security": 6,
            "Materials & Documentation": 4,
            "Transportation & Accommodation": 3,
            "Insurance & Contingency": 2
        }
        
        col1, col2, col3 = st.columns(3)
        allocated_budgets = {}
        
        for i, (category, suggested_percent) in enumerate(categories.items()):
            col_index = i % 3
            with [col1, col2, col3][col_index]:
                percent = st.slider(f"{category} (%):", 0, 50, suggested_percent, key=f"budget_{category}")
                amount = total_budget * percent / 100
                allocated_budgets[category] = {
                    "percentage": percent,
                    "amount": amount
                }
                st.caption(f"${amount:,.2f}")
        
        # Total allocation check
        total_allocated = sum([cat["percentage"] for cat in allocated_budgets.values()])
        if total_allocated != 100:
            st.warning(f"⚠️ Total allocation: {total_allocated}% (should be 100%)")
        else:
            st.success("✅ Budget allocation is balanced!")
        
        # Additional settings
        st.markdown("#### ⚙️ Additional Settings")
        col1, col2 = st.columns(2)
        with col1:
            budget_manager = st.text_input("Budget Manager:", value="Finance Team")
            notification_email = st.text_input("Notification Email:", value="finance@eventiq.com")
        with col2:
            auto_categorize = st.checkbox("Auto-categorize expenses", value=True)
            expense_approval_workflow = st.checkbox("Enable expense approval workflow", value=True)
        
        # Submit budget setup
        if st.form_submit_button("💾 Save Budget Configuration", use_container_width=True):
            # Store budget configuration in session state
            budget_config = {
                "event_name": event_name,
                "total_budget": total_budget,
                "currency": currency,
                "budget_year": budget_year,
                "expected_attendees": expected_attendees,
                "contingency_percent": contingency_percent,
                "categories": allocated_budgets,
                "settings": {
                    "approval_required": approval_required,
                    "budget_manager": budget_manager,
                    "notification_email": notification_email,
                    "auto_categorize": auto_categorize,
                    "expense_approval_workflow": expense_approval_workflow
                }
            }
            
            st.session_state.budget_config = budget_config
            st.success("✅ Budget configuration saved successfully!")
            show_success_animation()
            
            # Display summary
            st.markdown("#### 📋 Budget Summary")
            st.info(f"""
            **Event:** {event_name}  
            **Total Budget:** ${total_budget:,} {currency}  
            **Per Person:** ${total_budget/expected_attendees:.2f}  
            **Contingency:** ${total_budget * contingency_percent / 100:,.2f} ({contingency_percent}%)
            """)
    
    # Import/Export budget templates
    st.markdown("#### 📁 Budget Templates")
    col1, col2, col3 = st.columns(3)
    with col1:
        template_file = st.file_uploader("📥 Import Budget Template", type=['xlsx', 'csv', 'json'])
        if template_file:
            st.success(f"✅ Template uploaded: {template_file.name}")
    
    with col2:
        if st.button("📊 Export Current Budget", use_container_width=True):
            st.success("Budget template exported!")
    
    with col3:
        if st.button("🔄 Reset to Default", use_container_width=True):
            st.info("Budget reset to default configuration")

def show_budget_analytics():
    """Advanced budget analytics and reporting"""
    st.markdown("### 📈 Budget Analytics & Insights")
    
    # Analytics overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Budget Utilization", "56%", delta="8%")
    with col2:
        st.metric("📊 Forecast Accuracy", "92%", delta="3%")
    with col3:
        st.metric("⚠️ Over-Budget Categories", "2", delta="-1")
    with col4:
        st.metric("💡 Cost Savings", "$3,200", delta="$800")
    
    # Advanced charts
    col1, col2 = st.columns(2)
    with col1:
        # Spending trend over time
        st.markdown("#### 📈 Spending Trend")
        months = ["Jan", "Feb", "Mar", "Apr", "May"]
        planned = [5000, 8000, 12000, 15000, 18000]
        actual = [4800, 8200, 11500, 16000, 17200]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=planned, mode='lines+markers', name='Planned', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=months, y=actual, mode='lines+markers', name='Actual', line=dict(color='red')))
        fig.update_layout(title="Budget vs Actual Spending", xaxis_title="Month", yaxis_title="Amount ($)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Category performance
        st.markdown("#### 🎯 Category Performance")
        categories = ["Venue", "Catering", "AV Tech", "Marketing", "Security"]
        budget_utilization = [85, 72, 105, 45, 90]  # Percentages
        
        fig = go.Figure(data=go.Bar(
            x=categories,
            y=budget_utilization,
            marker_color=['red' if x > 100 else 'orange' if x > 80 else 'green' for x in budget_utilization]
        ))
        fig.update_layout(title="Budget Utilization by Category (%)", yaxis_title="Utilization %")
        fig.add_hline(y=100, line_dash="dash", line_color="red", annotation_text="Budget Limit")
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed analytics
    tab1, tab2, tab3 = st.tabs(["🔍 Variance Analysis", "📊 Forecasting", "💡 Recommendations"])
    
    with tab1:
        st.markdown("#### 🔍 Budget Variance Analysis")
        variance_data = [
            {"Category": "Venue & Facilities", "Budgeted": "$12,500", "Actual": "$11,800", "Variance": "-$700", "% Variance": "-5.6%"},
            {"Category": "Catering & F&B", "Budgeted": "$10,000", "Actual": "$10,800", "Variance": "+$800", "% Variance": "+8.0%"},
            {"Category": "AV Equipment", "Budgeted": "$6,000", "Actual": "$6,300", "Variance": "+$300", "% Variance": "+5.0%"},
            {"Category": "Marketing", "Budgeted": "$5,000", "Actual": "$3,200", "Variance": "-$1,800", "% Variance": "-36.0%"},
        ]
        df_variance = pd.DataFrame(variance_data)
        st.dataframe(df_variance, use_container_width=True, hide_index=True)
    
    with tab2:
        st.markdown("#### 📊 Budget Forecasting")
        st.info("💡 Based on current spending patterns, you're projected to be 3% under budget by event completion.")
        
        forecast_data = [
            {"Metric": "Projected Total Spend", "Current": "$28,000", "Projected": "$48,500", "Budget": "$50,000"},
            {"Metric": "Expected Savings", "Current": "-", "Projected": "$1,500", "Budget": "-"},
            {"Metric": "Risk Categories", "Current": "2", "Projected": "1", "Budget": "0"},
        ]
        df_forecast = pd.DataFrame(forecast_data)
        st.dataframe(df_forecast, use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("#### 💡 AI-Powered Recommendations")
        
        recommendations = [
            {
                "Priority": "🔴 High",
                "Category": "Catering",
                "Issue": "8% over budget",
                "Recommendation": "Negotiate with vendor for volume discount or adjust menu options",
                "Potential Savings": "$600"
            },
            {
                "Priority": "🟡 Medium", 
                "Category": "Marketing",
                "Issue": "Significantly under budget",
                "Recommendation": "Increase social media advertising to boost attendance",
                "Potential Impact": "+50 attendees"
            },
            {
                "Priority": "🟢 Low",
                "Category": "AV Equipment",
                "Issue": "Slightly over budget",
                "Recommendation": "Consider renting instead of purchasing for future events",
                "Potential Savings": "$200"
            }
        ]
        
        for rec in recommendations:
            with st.expander(f"{rec['Priority']} {rec['Category']} - {rec['Issue']}"):
                st.write(f"**Recommendation:** {rec['Recommendation']}")
                if 'Potential Savings' in rec:
                    st.success(f"💰 Potential Savings: {rec['Potential Savings']}")
                if 'Potential Impact' in rec:
                    st.info(f"📈 Potential Impact: {rec['Potential Impact']}")
    
    # Export analytics
    st.markdown("#### 📥 Export Analytics")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Export Variance Report", use_container_width=True):
            st.success("Variance analysis exported!")
    with col2:
        if st.button("📈 Export Forecast", use_container_width=True):
            st.success("Budget forecast exported!")
    with col3:
        if st.button("💡 Export Recommendations", use_container_width=True):
            st.success("Recommendations report exported!")

def show_budget_overview():
    """Display budget overview and charts"""
    st.markdown("### 📊 Budget Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Total Budget", "$50,000")
    with col2:
        st.metric("💸 Spent", "$28,000")
    with col3:
        st.metric("💵 Remaining", "$22,000")
    with col4:
        st.metric("📊 Utilization", "56%")
    
    # Budget breakdown charts
    col1, col2 = st.columns(2)
    with col1:
        # Spending by category
        categories = {"Catering": 8000, "AV Equipment": 5000, "Security": 6000, "Decoration": 4000, "Marketing": 3000, "Other": 2000}
        fig = px.pie(values=list(categories.values()), names=list(categories.keys()),
                    title="Spending by Category")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Budget vs Actual
        budget_data = {
            "Category": list(categories.keys()),
            "Budgeted": [10000, 6000, 7000, 5000, 4000, 3000],
            "Actual": list(categories.values())
        }
        df = pd.DataFrame(budget_data)
        fig = px.bar(df, x="Category", y=["Budgeted", "Actual"], 
                    title="Budget vs Actual Spending", barmode="group")
        st.plotly_chart(fig, use_container_width=True)

def show_expenses_list():
    """Display expenses list with filters"""
    st.markdown("### 📋 Expense Tracking")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        category_filter = st.selectbox("Filter by Category:", ["All", "Catering", "AV Equipment", "Security", "Decoration", "Marketing"])
    with col2:
        date_from = st.date_input("From Date:")
    with col3:
        date_to = st.date_input("To Date:")
    
    # Sample expenses data
    expenses_data = get_sample_expenses_data()
    df = pd.DataFrame(expenses_data)
    
    # Apply filters
    if category_filter != "All":
        df = df[df['Category'] == category_filter]
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Export options
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Generate Report", use_container_width=True):
            st.success("Expense report generated!")
    with col2:
        if st.button("📧 Email to Finance", use_container_width=True):
            st.success("Report emailed to finance team!")
    with col3:
        if st.button("📥 Export CSV", use_container_width=True):
            st.success("Data exported to CSV!")

def show_add_expense():
    """Add new expense with receipt upload"""
    st.markdown("### ➕ Add New Expense")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 💰 Expense Details")
        category = st.selectbox("Category:", ["Catering", "AV Equipment", "Security", "Decoration", "Marketing", "Transportation", "Other"])
        amount = st.number_input("Amount ($):", min_value=0.0, step=10.0)
        vendor = st.text_input("Vendor/Supplier:")
        description = st.text_area("Description:")
        expense_date = st.date_input("Expense Date:")
        payment_method = st.selectbox("Payment Method:", ["Credit Card", "Bank Transfer", "Check", "Cash"])
    
    with col2:
        st.markdown("#### 📄 Receipt Upload")
        receipt_file = st.file_uploader("Upload Receipt:", type=['jpg', 'jpeg', 'png', 'pdf'])
        
        if receipt_file:
            file_info = get_file_info(receipt_file)
            st.success(f"✅ Receipt uploaded: {receipt_file.name} ({file_info['size_mb']:.2f} MB)")
            
            # Show image preview if it's an image
            if receipt_file.type.startswith('image/'):
                display_image_preview(receipt_file)
            else:
                st.info(f"📄 PDF Receipt: {receipt_file.name}")
        
        # Sample receipt upload
        if st.button("📄 Upload Sample Receipt", use_container_width=True):
            st.session_state.sample_receipt = {
                "name": "sample_receipt.jpg",
                "type": "image/jpeg",
                "size": "1.2 MB"
            }
            st.success("✅ Sample receipt uploaded!")
        
        receipt_number = st.text_input("Receipt Number:")
        notes = st.text_area("Additional Notes:")
    
    if st.button("💾 Add Expense", use_container_width=True):
        if category and amount > 0 and vendor:
            # Store expense data
            expense_data = {
                "category": category,
                "amount": amount,
                "vendor": vendor,
                "description": description,
                "date": expense_date.strftime("%Y-%m-%d"),
                "payment_method": payment_method,
                "receipt_number": receipt_number,
                "notes": notes,
                "has_receipt": receipt_file is not None,
                "receipt_name": receipt_file.name if receipt_file else None
            }
            
            # Store in session state
            if 'expenses' not in st.session_state:
                st.session_state.expenses = []
            st.session_state.expenses.append(expense_data)
            
            st.success(f"✅ Expense of ${amount:,.2f} added successfully!")
            if receipt_file:
                st.info(f"📄 Receipt '{receipt_file.name}' attached")
            show_success_animation()
        else:
            st.warning("⚠️ Please fill in required fields")

def show_receipts_management():
    """Receipt management interface"""
    st.markdown("### 📄 Receipt Management")
    
    # Receipt overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📄 Total Receipts", "28")
    with col2:
        st.metric("✅ Verified", "24")
    with col3:
        st.metric("⏳ Pending", "3")
    with col4:
        st.metric("❌ Missing", "1")
    
    # Receipt list
    st.markdown("#### 📋 Receipt List")
    receipt_data = [
        {"Expense": "Catering Services", "Vendor": "Coffee Express", "Amount": "$2,500", "Receipt": "receipt_001.pdf", "Status": "Verified"},
        {"Expense": "AV Equipment", "Vendor": "Tech Solutions", "Amount": "$1,800", "Receipt": "receipt_002.jpg", "Status": "Verified"},
        {"Expense": "Security Services", "Vendor": "Security Plus", "Amount": "$3,200", "Receipt": "receipt_003.pdf", "Status": "Pending"},
        {"Expense": "Decoration", "Vendor": "Decorative Dreams", "Amount": "$1,500", "Receipt": "receipt_004.jpg", "Status": "Verified"},
    ]
    
    for receipt in receipt_data:
        with st.expander(f"📄 {receipt['Expense']} - {receipt['Amount']}"):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(f"**Vendor:** {receipt['Vendor']}")
                st.write(f"**Amount:** {receipt['Amount']}")
            with col2:
                st.write(f"**Receipt:** {receipt['Receipt']}")
                st.write(f"**Status:** {receipt['Status']}")
            with col3:
                if st.button(f"👁️ View", key=f"view_{receipt['Expense']}"):
                    st.success(f"Opening {receipt['Receipt']}")
            with col4:
                if st.button(f"📥 Download", key=f"download_{receipt['Expense']}"):
                    st.success(f"Downloading {receipt['Receipt']}")

def get_sample_expenses_data():
    """Get sample expenses data"""
    return [
        {"Category": "Catering", "Amount": "$2,500", "Vendor": "Coffee Express", "Date": "2025-01-30", "Status": "Paid", "Receipt": "Yes"},
        {"Category": "AV Equipment", "Amount": "$1,800", "Vendor": "Tech Solutions", "Date": "2025-01-29", "Status": "Pending", "Receipt": "Yes"},
        {"Category": "Security", "Amount": "$3,200", "Vendor": "Security Plus", "Date": "2025-01-28", "Status": "Approved", "Receipt": "No"},
        {"Category": "Decoration", "Amount": "$1,500", "Vendor": "Decorative Dreams", "Date": "2025-01-27", "Status": "Paid", "Receipt": "Yes"},
        {"Category": "Marketing", "Amount": "$1,200", "Vendor": "Print Pro", "Date": "2025-01-26", "Status": "Paid", "Receipt": "Yes"},
    ]
