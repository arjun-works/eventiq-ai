#!/usr/bin/env python3
"""
EventIQ Demo Setup & Launcher
=============================

This script prepares and launches the EventIQ demo with all sample files
and features ready for demonstration.
"""

import os
import sys
import json
import webbrowser
from datetime import datetime

def create_demo_banner():
    """Create demo banner"""
    print("\n" + "="*70)
    print("🎉 EventIQ Demo Setup & Launcher 🎉".center(70))
    print("="*70)
    print(f"📅 Demo Date: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}")
    print("🎯 Preparing complete file upload demonstration...")
    print("="*70 + "\n")

def setup_sample_files():
    """Create all sample files for demo"""
    print("📁 Setting up sample files for demonstration...")
    
    # Create sample_uploads directory
    sample_dir = "sample_uploads"
    if not os.path.exists(sample_dir):
        os.makedirs(sample_dir)
        print(f"   ✅ Created {sample_dir}/ directory")
    
    # 1. Participant import CSV
    participant_csv = """name,email,phone,organization,industry,role,dietary_restrictions
John Doe,john@techcorp.com,+1-555-0001,Tech Corp,Technology,Software Developer,None
Jane Smith,jane@designstudio.com,+1-555-0002,Design Studio,Design,UI/UX Designer,Vegetarian
Mike Johnson,mike@startupx.com,+1-555-0003,StartupX,Technology,Product Manager,Gluten-free
Sarah Wilson,sarah@healthcare.com,+1-555-0004,Health Plus,Healthcare,Medical Director,None
David Brown,david@finance.com,+1-555-0005,Finance Pro,Finance,Financial Analyst,Vegan
Alice Cooper,alice@marketing.com,+1-555-0006,Marketing Inc,Marketing,Brand Manager,None
Robert Taylor,robert@consulting.com,+1-555-0007,Consulting Group,Consulting,Senior Consultant,Vegetarian
Lisa Anderson,lisa@education.com,+1-555-0008,EduTech,Education,Learning Specialist,None"""
    
    with open(f"{sample_dir}/participants_import.csv", "w") as f:
        f.write(participant_csv)
    print("   📄 Created participants_import.csv (8 participants)")
    
    # 2. System configuration JSON
    config_data = {
        "event": {
            "name": "EventIQ 2025 Demo",
            "date": "2025-08-15",
            "location": "Convention Center, New York",
            "max_participants": 500,
            "timezone": "EST",
            "duration_days": 3
        },
        "email": {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "use_tls": True,
            "from_email": "noreply@eventiq.com",
            "admin_email": "admin@eventiq.com"
        },
        "features": {
            "certificates_enabled": True,
            "media_gallery_enabled": True,
            "budget_tracking_enabled": True,
            "vendor_management_enabled": True,
            "analytics_enabled": True,
            "notifications_enabled": True
        },
        "limits": {
            "max_file_size_mb": 50,
            "max_attachments": 10,
            "session_timeout_minutes": 30
        },
        "ui": {
            "theme": "professional",
            "primary_color": "#667eea",
            "secondary_color": "#764ba2",
            "enable_animations": True
        }
    }
    
    with open(f"{sample_dir}/eventiq_config.json", "w") as f:
        json.dump(config_data, f, indent=2)
    print("   ⚙️ Created eventiq_config.json (system configuration)")
    
    # 3. Expense tracking CSV
    expenses_csv = """category,amount,vendor,description,date,payment_method,receipt_number
Catering,2500.00,Coffee Express,Opening ceremony catering,2025-07-30,Credit Card,RCP-001
AV Equipment,1800.00,Tech Solutions,Audio visual equipment rental,2025-07-29,Bank Transfer,RCP-002
Security,3200.00,Security Plus,Event security services 3 days,2025-07-28,Check,RCP-003
Decoration,1500.00,Decorative Dreams,Venue decoration and setup,2025-07-27,Credit Card,RCP-004
Transportation,800.00,City Transport,Shuttle services for attendees,2025-07-26,Cash,RCP-005
Marketing,1200.00,Print Pro,Event banners and signage,2025-07-25,Credit Card,RCP-006
Accommodation,5000.00,Grand Hotel,Speaker accommodation,2025-07-24,Bank Transfer,RCP-007
Technology,900.00,WiFi Solutions,Event WiFi and networking,2025-07-23,Credit Card,RCP-008"""
    
    with open(f"{sample_dir}/expense_tracking.csv", "w") as f:
        f.write(expenses_csv)
    print("   💰 Created expense_tracking.csv (8 expense records)")
    
    # 4. User import template
    users_csv = """name,email,role,department,phone,status
Admin User,admin@eventiq.com,Admin,IT,+1-555-1001,Active
John Organizer,john.organizer@eventiq.com,Organizer,Events,+1-555-1002,Active
Sarah Volunteer,sarah.volunteer@eventiq.com,Volunteer,Support,+1-555-1003,Active
Mike Vendor,mike@vendor.com,Vendor,External,+1-555-1004,Active
Lisa Participant,lisa@participant.com,Participant,External,+1-555-1005,Active"""
    
    with open(f"{sample_dir}/users_import.csv", "w") as f:
        f.write(users_csv)
    print("   👥 Created users_import.csv (5 user accounts)")
    
    # 5. Vendor information CSV
    vendors_csv = """name,email,phone,service,contract_amount,status,setup_date
Coffee Express,coffee@express.com,+1-555-2001,Catering,2500.00,Active,2025-07-30
Tech Solutions,info@techsol.com,+1-555-2002,AV Equipment,1800.00,Active,2025-07-29
Security Plus,ops@secplus.com,+1-555-2003,Security,3200.00,Pending,2025-07-28
Decorative Dreams,hello@decdreams.com,+1-555-2004,Decoration,1500.00,Active,2025-07-27
Print Pro Marketing,contact@printpro.com,+1-555-2005,Marketing,1200.00,Active,2025-07-26"""
    
    with open(f"{sample_dir}/vendors_list.csv", "w") as f:
        f.write(vendors_csv)
    print("   🏭 Created vendors_list.csv (5 vendor records)")
    
    print(f"\n✅ All sample files created in '{sample_dir}/' directory\n")

def create_demo_checklist():
    """Create a demo checklist file"""
    checklist = """# 🎯 EventIQ Demo Checklist

## Pre-Demo Setup
- [ ] Sample files created in sample_uploads/
- [ ] Application started on localhost:8501
- [ ] Browser opened to demo page
- [ ] Demo accounts ready

## Demo Flow Checklist

### 1. Login & Dashboard (2 min)
- [ ] Show login page with demo accounts
- [ ] Login as Event Organizer
- [ ] Tour dashboard with live metrics
- [ ] Show role-based navigation

### 2. Media Gallery Upload (3 min)
- [ ] Navigate to Media Gallery
- [ ] Upload actual photo/video files
- [ ] Show real-time preview and metadata
- [ ] Save files and view in gallery
- [ ] Demonstrate filtering and search

### 3. Participant Bulk Import (2 min)
- [ ] Go to Participants → Bulk Import
- [ ] Upload participants_import.csv
- [ ] Show file preview and import
- [ ] View imported participants
- [ ] Show analytics updates

### 4. Expense Receipt Upload (2 min)
- [ ] Navigate to Budget → Add Expense
- [ ] Fill expense details
- [ ] Upload receipt image/PDF
- [ ] Save and view in receipts
- [ ] Show expense tracking

### 5. Vendor Document Management (2 min)
- [ ] Go to Vendors → Add Vendor
- [ ] Fill vendor information
- [ ] Upload insurance/license/contract
- [ ] Save vendor with documents
- [ ] Show document management

### 6. Certificate Generation (1 min)
- [ ] Navigate to Certificates
- [ ] Generate certificate for volunteer
- [ ] Download actual certificate file
- [ ] Show certificate preview

### 7. Settings & Configuration (1 min)
- [ ] Go to Settings
- [ ] Upload eventiq_config.json
- [ ] Upload event logo
- [ ] Show bulk user import
- [ ] Download templates

### 8. Role Demonstration (1 min)
- [ ] Logout and login as Volunteer
- [ ] Show limited access
- [ ] Login as Participant
- [ ] Show restricted features

## Key Points to Emphasize
- ✅ Real file uploads and processing
- ✅ Professional enterprise UI/UX
- ✅ Comprehensive event management
- ✅ Role-based access control
- ✅ Bulk operations and efficiency
- ✅ Production-ready architecture

## Demo Success Metrics
- [ ] File uploads working in all modules
- [ ] Previews and metadata displayed
- [ ] Downloads functioning properly
- [ ] Role-based access demonstrated
- [ ] Professional presentation completed

Total Demo Time: ~15 minutes
File Upload Demos: 6+ modules
User Roles Shown: 3+ different levels
"""
    
    with open("DEMO_CHECKLIST.md", "w") as f:
        f.write(checklist)
    print("📋 Created DEMO_CHECKLIST.md for presentation guide")

def display_demo_info():
    """Display demo information"""
    print("🎬 DEMO READY! Here's what you need to know:\n")
    
    print("🔐 DEMO ACCOUNTS:")
    accounts = [
        ("👨‍💼 Event Organizer", "organizer@eventiq.com", "organizer123", "Full Access"),
        ("🤝 Volunteer", "volunteer@eventiq.com", "volunteer123", "Certificates & Feedback"),
        ("👥 Participant", "participant@eventiq.com", "participant123", "Basic Access"),
        ("🏭 Vendor", "vendor@eventiq.com", "vendor123", "Vendor Portal"),
        ("👨‍💻 Admin", "admin@eventiq.com", "admin123", "System Admin")
    ]
    
    for role, email, password, access in accounts:
        print(f"   {role}")
        print(f"   📧 {email} | 🔑 {password}")
        print(f"   🎯 {access}\n")
    
    print("📁 SAMPLE FILES FOR UPLOAD:")
    files = [
        "📄 participants_import.csv - Bulk participant import (8 records)",
        "⚙️ eventiq_config.json - System configuration file",
        "💰 expense_tracking.csv - Expense data with receipts",
        "👥 users_import.csv - Bulk user import template",
        "🏭 vendors_list.csv - Vendor management data"
    ]
    
    for file_desc in files:
        print(f"   {file_desc}")
    
    print(f"\n📂 All files located in: {os.path.abspath('sample_uploads')}/")
    
    print(f"\n🌐 APPLICATION URL: http://localhost:8501")
    print(f"📊 Start with: streamlit run enhanced_frontend.py")
    
    print("\n🎯 DEMO FLOW:")
    flow = [
        "1. Login as Event Organizer",
        "2. Media Gallery → Upload photos/videos",
        "3. Participants → Bulk import CSV",
        "4. Budget → Upload expense receipts",
        "5. Vendors → Upload documents",
        "6. Certificates → Generate & download",
        "7. Settings → Configuration upload",
        "8. Role switching demonstration"
    ]
    
    for step in flow:
        print(f"   {step}")
    
    print("\n" + "="*70)

def launch_application():
    """Launch the Streamlit application"""
    print("🚀 Launching EventIQ Application...")
    
    try:
        # Try to open browser to the application
        webbrowser.open('http://localhost:8501')
        print("🌐 Browser opened to http://localhost:8501")
    except:
        print("🌐 Please open your browser to: http://localhost:8501")
    
    print("\n⚡ Starting Streamlit application...")
    print("💡 Use Ctrl+C to stop the application\n")
    
    # Start Streamlit
    os.system("streamlit run enhanced_frontend.py --server.port 8501")

def main():
    """Main demo setup function"""
    create_demo_banner()
    setup_sample_files()
    create_demo_checklist()
    display_demo_info()
    
    print("🎬 Ready to start the demo!")
    response = input("Press Enter to launch EventIQ application (or 'q' to quit): ")
    
    if response.lower() != 'q':
        launch_application()
    else:
        print("\n👋 Demo setup complete! Run 'streamlit run enhanced_frontend.py' when ready.")
        print("📋 Check DEMO_CHECKLIST.md for presentation guide.")

if __name__ == "__main__":
    main()
