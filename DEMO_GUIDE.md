# 🎉 EventIQ Demo Guide

Welcome to the EventIQ Management System demonstration! This guide will walk you through all the enhanced file upload features we've implemented.

## 🚀 Quick Start

### Option 1: Run Demo Script
```bash
python demo.py
```

### Option 2: Manual Start
```bash
streamlit run enhanced_frontend.py
```

## 🔐 Demo Accounts

| Role | Email | Password | Access Level |
|------|-------|----------|--------------|
| 👨‍💼 Event Organizer | organizer@eventiq.com | organizer123 | Full Access |
| 🤝 Volunteer | volunteer@eventiq.com | volunteer123 | Limited Access |
| 👥 Participant | participant@eventiq.com | participant123 | Basic Access |
| 🏭 Vendor | vendor@eventiq.com | vendor123 | Vendor Portal |
| 👨‍💻 Admin | admin@eventiq.com | admin123 | System Admin |

## 📋 Demo Checklist

### 1. 📸 Media Gallery Module
- [ ] Upload photos (JPG, PNG)
- [ ] Upload videos (MP4, AVI)
- [ ] Upload documents (PDF, DOC)
- [ ] View image previews
- [ ] Test sample file loading
- [ ] Filter media by type/location
- [ ] Download media files

**Demo Steps:**
1. Navigate to "Media Gallery" from sidebar
2. Go to "Upload" tab
3. Upload sample images/videos
4. Add metadata (location, photographer, tags)
5. Save and view in gallery
6. Test filtering and downloading

### 2. 🏭 Vendor Management Module
- [ ] Add new vendor with documents
- [ ] Upload insurance certificates
- [ ] Upload business licenses
- [ ] Upload signed contracts
- [ ] Send communications with attachments
- [ ] Process payments with receipts

**Demo Steps:**
1. Navigate to "Vendors" module
2. Go to "Add Vendor" tab
3. Fill vendor information
4. Upload insurance, license, and contract files
5. Save vendor
6. Test communication with attachments

### 3. 👥 Participant Management Module
- [ ] Bulk import participants from CSV
- [ ] Upload participant photos
- [ ] Download import templates
- [ ] View import statistics
- [ ] Export participant data

**Demo Steps:**
1. Navigate to "Participants" module
2. Go to "Bulk Import" tab
3. Download sample CSV template
4. Upload the sample_participants.csv file
5. Preview and import data
6. Add individual participant with photo

### 4. 💰 Budget & Finance Module
- [ ] Add expenses with receipt uploads
- [ ] Upload expense receipts (JPG, PDF)
- [ ] View receipt management
- [ ] Generate expense reports
- [ ] Track spending by category

**Demo Steps:**
1. Navigate to "Budget" module
2. Go to "Add Expense" tab
3. Enter expense details
4. Upload receipt image/PDF
5. Save expense
6. View in receipts management

### 5. 🎓 Certificate System
- [ ] Generate individual certificates
- [ ] Download certificates as files
- [ ] Preview certificate content
- [ ] Bulk certificate generation

**Demo Steps:**
1. Navigate to "Certificates" module
2. Go to "Generate" tab
3. Select eligible volunteer
4. Preview certificate
5. Generate and download

### 6. ⚙️ Settings & Configuration
- [ ] Upload configuration files (JSON, YAML)
- [ ] Upload event logos
- [ ] Bulk import users from CSV
- [ ] Download templates

**Demo Steps:**
1. Navigate to "Settings" module
2. Upload sample_config.json file
3. Upload event logo image
4. Test user bulk import
5. Download configuration templates

### 7. 📧 Communication Features
- [ ] Send emails with attachments
- [ ] Upload multiple file attachments
- [ ] Preview attached files
- [ ] Schedule email delivery

**Demo Steps:**
1. Go to Vendor Communications
2. Compose new message
3. Add multiple attachments
4. Preview attachments
5. Send or schedule message

## 🎯 Key Features to Highlight

### File Upload Capabilities
- **Multiple Formats**: Images, videos, documents, spreadsheets
- **Real Processing**: Files are actually processed and stored
- **Preview Functionality**: Image previews, file info display
- **Size Management**: File size calculation and limits
- **Metadata Extraction**: Automatic file information

### User Experience
- **Drag & Drop**: Modern file upload interface
- **Progress Indicators**: Visual feedback during upload
- **Error Handling**: Proper validation and error messages
- **Mobile Responsive**: Works on all device sizes
- **Sample Data**: Built-in sample files for testing

### Enterprise Features
- **Bulk Operations**: Mass import/export capabilities
- **Template Downloads**: Standardized data formats
- **File Management**: Organized storage and retrieval
- **Security**: File type validation and size limits
- **Audit Trail**: Upload tracking and metadata

## 📊 Demo Scenarios

### Scenario 1: Event Setup
1. Login as Event Organizer
2. Upload event logo in Settings
3. Bulk import participants
4. Add vendors with documentation
5. Set up media gallery

### Scenario 2: During Event
1. Upload event photos/videos
2. Track expenses with receipts
3. Monitor participant check-ins
4. Send vendor communications

### Scenario 3: Post Event
1. Generate volunteer certificates
2. Create expense reports
3. Export all data
4. Send follow-up communications

## 🔧 Technical Highlights

### File Processing
```python
# Real file upload with metadata
file_info = get_file_info(uploaded_file)
file_data = get_base64_encoded_file(uploaded_file)
display_image_preview(uploaded_file)
```

### Session State Management
```python
# Persistent file storage
st.session_state.uploaded_media.append({
    "name": file.name,
    "data": file_data,
    "metadata": file_info
})
```

### Download Functionality
```python
# Generate downloadable content
st.download_button(
    label="📥 Download",
    data=content,
    file_name="certificate.txt",
    mime="text/plain"
)
```

## 🎬 Demo Script

1. **Introduction** (2 min)
   - Show login page with demo accounts
   - Explain role-based access

2. **Core Features** (5 min)
   - Navigate through all modules
   - Show file upload interfaces
   - Demonstrate real-time processing

3. **File Upload Demo** (8 min)
   - Upload files in each module
   - Show previews and metadata
   - Test download functionality

4. **Bulk Operations** (3 min)
   - Demonstrate CSV imports
   - Show template downloads
   - Bulk certificate generation

5. **Advanced Features** (2 min)
   - Communication attachments
   - Configuration uploads
   - System management

## 🏆 Success Metrics

After the demo, users should understand:
- ✅ How to upload files in each module
- ✅ File processing capabilities
- ✅ Data import/export functionality
- ✅ Professional UI/UX design
- ✅ Enterprise-grade features

## 🎯 Next Steps

1. **Production Deployment**
   - Set up proper file storage (AWS S3, etc.)
   - Configure database persistence
   - Add user authentication system

2. **Enhanced Features**
   - File encryption and security
   - Advanced file processing (OCR, etc.)
   - Integration with external services

3. **Scaling**
   - Load balancing for file uploads
   - CDN for media delivery
   - Backup and disaster recovery

---

## 📞 Support

For questions or issues during the demo:
- Check the error console in the browser
- Verify file types are supported
- Ensure file sizes are reasonable
- Try refreshing the application if needed

**Enjoy the EventIQ Demo! 🎉**
