#!/usr/bin/env python3
"""
EventIQ Demo Script
===================

This script demonstrates all the enhanced file upload features 
in the EventIQ management system.
"""

import os
import sys
import time
import subprocess
from datetime import datetime

def print_banner():
    """Print the EventIQ demo banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║                    🎉 EventIQ Demo 2025 🎉                   ║
    ║                                                              ║
    ║              Professional Event Management System            ║
    ║                   with File Upload Features                  ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)
    print(f"📅 Demo Date: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}")
    print("🚀 Starting EventIQ demonstration...\n")

def check_requirements():
    """Check if required packages are installed"""
    print("🔍 Checking system requirements...")
    
    required_packages = [
        'streamlit',
        'pandas',
        'plotly',
        'requests',
        'pillow'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"   ❌ {package} (missing)")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("📦 Installing missing packages...")
        
        for package in missing_packages:
            package_name = package
            if package == 'pillow':
                package_name = 'Pillow'
            
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])
                print(f"   ✅ Installed {package}")
            except subprocess.CalledProcessError:
                print(f"   ❌ Failed to install {package}")
    
    print("\n✅ System requirements check complete!\n")

def demo_features():
    """Demonstrate key features"""
    print("🎯 EventIQ Key Features Demo:")
    print("=" * 50)
    
    features = [
        {
            "icon": "📸",
            "name": "Media Gallery",
            "description": "Upload photos, videos, and documents with preview functionality"
        },
        {
            "icon": "🏭",
            "name": "Vendor Management",
            "description": "Upload contracts, licenses, and insurance documents"
        },
        {
            "icon": "👥",
            "name": "Participant Management",
            "description": "Bulk import participants from CSV/Excel files"
        },
        {
            "icon": "💰",
            "name": "Budget Tracking",
            "description": "Upload expense receipts and financial documents"
        },
        {
            "icon": "🎓",
            "name": "Certificate System",
            "description": "Generate and download volunteer certificates"
        },
        {
            "icon": "⚙️",
            "name": "System Settings",
            "description": "Upload configuration files and system logos"
        },
        {
            "icon": "📧",
            "name": "Communications",
            "description": "Send emails with file attachments"
        },
        {
            "icon": "📊",
            "name": "Analytics Dashboard",
            "description": "Real-time data visualization and reporting"
        }
    ]
    
    for i, feature in enumerate(features, 1):
        print(f"{i:2d}. {feature['icon']} {feature['name']}")
        print(f"     {feature['description']}")
        time.sleep(0.5)
    
    print("\n" + "=" * 50)

def create_sample_files():
    """Create sample files for demonstration"""
    print("📁 Creating sample files for demo...")
    
    # Create uploads directory
    uploads_dir = "sample_uploads"
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    
    # Create sample CSV for participant import
    sample_csv = f"""name,email,phone,organization,industry,role,dietary_restrictions
John Doe,john@techcorp.com,+1-555-0001,Tech Corp,Technology,Developer,None
Jane Smith,jane@designstudio.com,+1-555-0002,Design Studio,Design,Designer,Vegetarian
Mike Johnson,mike@startupx.com,+1-555-0003,StartupX,Technology,Manager,Gluten-free
Sarah Wilson,sarah@healthcare.com,+1-555-0004,Health Plus,Healthcare,Director,None
David Brown,david@finance.com,+1-555-0005,Finance Pro,Finance,Analyst,Vegan"""
    
    with open(f"{uploads_dir}/sample_participants.csv", "w") as f:
        f.write(sample_csv)
    
    # Create sample configuration file
    import json
    sample_config = {
        "event": {
            "name": "EventIQ 2025 Demo",
            "date": "2025-08-15",
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
    
    with open(f"{uploads_dir}/sample_config.json", "w") as f:
        json.dump(sample_config, f, indent=2)
    
    # Create sample expense report
    sample_expenses = f"""category,amount,vendor,description,date,payment_method
Catering,2500.00,Coffee Express,Event catering services,2025-07-30,Credit Card
AV Equipment,1800.00,Tech Solutions,Audio visual equipment rental,2025-07-29,Bank Transfer
Security,3200.00,Security Plus,Event security services,2025-07-28,Check
Decoration,1500.00,Decorative Dreams,Event decoration and setup,2025-07-27,Credit Card
Transportation,800.00,City Transport,Shuttle services for attendees,2025-07-26,Cash"""
    
    with open(f"{uploads_dir}/sample_expenses.csv", "w") as f:
        f.write(sample_expenses)
    
    print(f"   ✅ Created sample files in '{uploads_dir}/' directory")
    print(f"   📄 sample_participants.csv - Participant data for bulk import")
    print(f"   ⚙️ sample_config.json - System configuration file")
    print(f"   💰 sample_expenses.csv - Expense tracking data")
    print()

def start_application():
    """Start the Streamlit application"""
    print("🚀 Starting EventIQ Application...")
    print("🌐 The application will open in your default web browser")
    print("📝 Use the following demo credentials:")
    print()
    
    credentials = [
        ("👨‍💼 Event Organizer", "organizer@eventiq.com", "organizer123"),
        ("🤝 Volunteer", "volunteer@eventiq.com", "volunteer123"),
        ("👥 Participant", "participant@eventiq.com", "participant123"),
        ("🏭 Vendor", "vendor@eventiq.com", "vendor123"),
        ("👨‍💻 Admin", "admin@eventiq.com", "admin123")
    ]
    
    for role, email, password in credentials:
        print(f"   {role}")
        print(f"   📧 Email: {email}")
        print(f"   🔑 Password: {password}")
        print()
    
    print("🎯 Demo Workflow:")
    print("1. Login with any demo account")
    print("2. Navigate to different modules using the sidebar")
    print("3. Try uploading the sample files we created")
    print("4. Test the file upload features in each module")
    print("5. Download generated certificates and reports")
    print()
    
    print("⚡ Starting application in 3 seconds...")
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    try:
        # Start Streamlit application
        os.system("streamlit run enhanced_frontend.py --server.port 8501 --server.headless false")
    except KeyboardInterrupt:
        print("\n👋 Demo ended by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("💡 Try running manually: streamlit run enhanced_frontend.py")

def main():
    """Main demo function"""
    print_banner()
    check_requirements()
    demo_features()
    create_sample_files()
    
    print("🎬 Ready to start the demo!")
    response = input("Press Enter to launch EventIQ application (or 'q' to quit): ")
    
    if response.lower() != 'q':
        start_application()
    else:
        print("👋 Demo cancelled. Run this script again when ready!")

if __name__ == "__main__":
    main()
