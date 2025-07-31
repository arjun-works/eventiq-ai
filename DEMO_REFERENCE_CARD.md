# 🎯 EventIQ Demo Quick Reference Card

## 🚀 How to Start Demo

```bash
# Option 1: Use Demo Launcher (Recommended)
python demo_launcher.py

# Option 2: Direct Launch
streamlit run enhanced_frontend.py

# Option 3: Use Demo Script
python demo.py
```

## 🔐 Demo Login Accounts

| Role | Email | Password | Access Level |
|------|--------|----------|--------------|
| **Event Organizer** | organizer@eventiq.com | organizer123 | Full Access |
| **Volunteer** | volunteer@eventiq.com | volunteer123 | Certificates & Feedback |
| **Participant** | participant@eventiq.com | participant123 | Basic Access |
| **Vendor** | vendor@eventiq.com | vendor123 | Vendor Portal |
| **Admin** | admin@eventiq.com | admin123 | System Admin |

## 📁 Sample Files for Upload

All files created in `sample_uploads/` directory:

- **📄 participants_import.csv** - 8 participants for bulk import
- **⚙️ eventiq_config.json** - System configuration file
- **💰 expense_tracking.csv** - 8 expense records with receipts
- **👥 users_import.csv** - 5 user accounts template
- **🏭 vendors_list.csv** - 5 vendor records

## 🎬 15-Minute Demo Flow

### 1. Login & Dashboard (2 min)
- Show login with Event Organizer account
- Tour dashboard with live metrics
- Point out role-based navigation

### 2. Media Gallery - Real Uploads (3 min)
- Navigate to Media Gallery
- Upload actual image/video files
- Show real-time preview and metadata
- Demonstrate gallery features

### 3. Participant Bulk Import (2 min)
- Go to Participants → Bulk Import
- Upload `participants_import.csv`
- Show file preview and import process
- View imported data in participants list

### 4. Expense Receipt Upload (2 min)
- Navigate to Budget → Add Expense
- Fill expense form
- Upload receipt image/PDF
- Show expense tracking with attachments

### 5. Vendor Document Management (2 min)
- Go to Vendors → Add Vendor
- Upload insurance/license documents
- Show document management features
- View vendor with attachments

### 6. Certificate Generation (1 min)
- Navigate to Certificates
- Generate certificate for volunteer
- Download actual certificate file
- Show certificate preview

### 7. Settings Upload (1 min)
- Go to Settings
- Upload `eventiq_config.json`
- Show configuration import
- Upload logo and templates

### 8. Role Demonstration (2 min)
- Logout and login as Volunteer
- Show limited access permissions
- Login as Participant for restricted view
- Highlight role-based security

## 🎯 Key Demo Points

### File Upload Features
✅ **Real file processing** (not dummy data)  
✅ **Multiple file formats** (Images, PDFs, CSVs, JSON)  
✅ **File previews** with metadata display  
✅ **Bulk operations** for efficiency  
✅ **Download capabilities** for certificates/receipts  

### Professional Features
✅ **Role-based access control**  
✅ **Enterprise-grade UI/UX**  
✅ **Comprehensive event management**  
✅ **Real-time analytics and dashboards**  
✅ **Production-ready architecture**  

## 🔧 Quick Troubleshooting

**If app won't start:**
```bash
pip install streamlit pandas plotly pillow
```

**If files won't upload:**
- Check file size (max 50MB)
- Ensure supported formats
- Try refreshing browser

**If login fails:**
- Use exact credentials from reference card
- Check caps lock
- Try different role account

## 🌐 Application Info

- **URL:** http://localhost:8501
- **Port:** 8501 (default Streamlit)
- **Browser:** Any modern browser
- **Stop App:** Ctrl+C in terminal

## 📋 Demo Success Checklist

- [ ] All 6+ file upload modules demonstrated
- [ ] Real files uploaded and processed
- [ ] Role-based access shown
- [ ] Professional features highlighted
- [ ] Questions answered confidently

---

**Total Demo Time:** 15 minutes  
**File Upload Modules:** 6+ different areas  
**User Roles Shown:** 3+ different access levels  
**Sample Files:** 5 ready-to-use files  

**🎉 You're ready to showcase EventIQ's complete file upload capabilities!**
