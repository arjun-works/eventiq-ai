"""
EventIQ Development Team Collaboration Guide
==========================================

This guide explains how 10 team members can collaborate effectively on the EventIQ 
codebase using Git, with each member working on separate modules independently.

## � **10-Member Team Git Workflow Strategy**

### **Team Structure & Module Assignment**

Your EventIQ system is perfectly designed for team collaboration with **14 independent modules**. Here's the recommended team assignment:

| Team Member | Primary Module(s) | Git Branch Pattern | Responsibilities |
|-------------|-------------------|-------------------|------------------|
| **Member 1** | `dashboard.py` | `feature/dashboard-*` | Main dashboard & real-time metrics |
| **Member 2** | `event_setup.py` | `feature/event-setup-*` | Corporate IT event management |
| **Member 3** | `budget.py` | `feature/budget-*` | Financial management & analytics |
| **Member 4** | `participants.py` | `feature/participants-*` | Participant management & bulk import |
| **Member 5** | `media_gallery.py` | `feature/media-*` | File uploads & media processing |
| **Member 6** | `vendors.py` | `feature/vendors-*` | Vendor management & contracts |
| **Member 7** | `certificates.py` | `feature/certificates-*` | Certificate generation & downloads |
| **Member 8** | `analytics.py` | `feature/analytics-*` | Data visualization & reporting |
| **Member 9** | `settings.py` + `config.py` | `feature/config-*` | System configuration & security |
| **Member 10** | `workflows.py` + `feedback.py` | `feature/workflows-*` | Process automation & feedback |

### **Additional Modules for Cross-Team Support:**
- `volunteers.py`, `booths.py`, `constants.py`, `utils.py` - Shared responsibilities

---

## 🌿 **Git Branching Strategy**

### **Main Branch Structure:**
```
main (production-ready)
├── develop (integration branch)
├── feature/dashboard-enhancements
├── feature/budget-analytics
├── feature/media-upload-improvements
├── feature/participant-bulk-import
├── hotfix/urgent-bug-fixes
└── release/v2.0.0
```

### **Branch Naming Convention:**
- **Feature branches:** `feature/module-name-description`
  - `feature/dashboard-realtime-metrics`
  - `feature/budget-expense-tracking` 
  - `feature/media-gallery-video-support`
- **Bug fixes:** `bugfix/module-name-issue`
- **Hotfixes:** `hotfix/critical-issue-description`
- **Releases:** `release/v1.2.0`

---

## 🚀 **Step-by-Step Collaboration Workflow**

### **1. Initial Repository Setup (Team Lead)**

```bash
# Initialize Git repository (if not already done)
cd eventiq-ai
git init
git remote add origin <your-repository-url>

# Create initial commit
git add .
git commit -m "Initial EventIQ modular architecture with 14 modules"
git push -u origin main

# Create develop branch
git checkout -b develop
git push -u origin develop
```

### **2. Team Member Setup (Each Developer)**

Each team member should follow these steps:

```bash
# Clone the repository
git clone <repository-url>
cd eventiq-ai

# Set up local development
git checkout develop
git pull origin develop

# Create personal feature branch
git checkout -b feature/dashboard-enhancements  # Replace with your module
git push -u origin feature/dashboard-enhancements
```

### **3. Daily Development Workflow**

#### **A. Start Working on Your Module**
```bash
# Switch to your feature branch
git checkout feature/your-module-name

# Pull latest changes from develop
git pull origin develop

# Start working on your assigned module
# Edit: modules/dashboard.py (or your assigned module)
```

#### **B. Making Changes & Commits**
```bash
# Check what you've changed
git status
git diff

# Stage only your module files
git add modules/dashboard.py  # Your assigned module
git add modules/utils.py      # Only if you modified shared utilities

# Commit with descriptive message
git commit -m "Dashboard: Add real-time metrics for corporate IT events

- Added live participant count updates
- Implemented budget utilization charts  
- Added corporate IT event type filtering
- Fixed dashboard loading performance issue
- Updated dashboard for corporate meeting types"
```

#### **C. Regular Sync with Team (IMPORTANT)**
```bash
# Daily sync with develop branch (recommended: morning and evening)
git checkout develop
git pull origin develop

# Switch back to your branch
git checkout feature/your-module-name

# Merge latest changes from develop
git merge develop

# If conflicts occur, resolve them in your IDE
# Then commit the merge
git commit -m "Merge latest develop changes"

# Push your updates
git push origin feature/your-module-name
```

---

## 🔥 **Conflict Resolution Strategy**

### **Common Conflict Scenarios & Solutions:**

#### **1. Multiple people editing the same module (AVOID THIS)**
```bash
# Prevention: Stick to your assigned module!
# If unavoidable conflict occurs:

git status  # Shows merge conflicts

# Open conflicted file in your IDE
# Look for conflict markers:
<<<<<<< HEAD
# Your changes
=======
# Other person's changes  
>>>>>>> feature/other-branch

# Resolve manually, communicate with team member, then:
git add modules/dashboard.py
git commit -m "Resolved merge conflict in dashboard module"
```

#### **2. Shared utility functions conflicts**
```bash
# When multiple people modify modules/utils.py
# BEST PRACTICE: Coordinate via team chat BEFORE modifying shared files

# If conflict occurs:
# 1. Communicate with the other developer immediately
# 2. Merge both changes if compatible
# 3. Test thoroughly after resolution
```

#### **3. Configuration file conflicts**
```bash
# For modules/config.py or modules/constants.py changes
# COORDINATION REQUIRED:
# 1. Post in team chat before modifying
# 2. Make changes in coordination with config team member
# 3. Test integration after merge
```

### 🏠 Dashboard Team (dashboard.py)
**Responsibility:** Role-based dashboard displays
**Files to edit:** `modules/dashboard.py`
**Key functions:**
- `show_role_dashboard()` - Main dashboard function
- Role-specific views for organizer, volunteer, participant, vendor, admin
- Quick action buttons and metrics display

**Team collaboration notes:**
- Independent module - safe to edit without affecting others
- Can add new dashboard widgets and metrics
- Coordinate with API team for new data requirements

### 🎓 Certificate Team (certificates.py)
**Responsibility:** Certificate generation and management
**Files to edit:** `modules/certificates.py`
**Key functions:**
- `show_certificates_page()` - Main certificate interface
- Individual and bulk certificate generation
- Certificate registry and analytics
- Real PDF generation and downloads

**Team collaboration notes:**
- Independent module with file upload capabilities
- Can enhance certificate templates and generation logic
- Test file uploads thoroughly

### 📸 Media Team (media_gallery.py)
**Responsibility:** Media uploads, gallery, and live streaming
**Files to edit:** `modules/media_gallery.py`
**Key functions:**
- `show_media_gallery_page()` - Main media interface
- Multi-file upload handling
- Image/video preview and gallery display
- Live streaming integration

**Team collaboration notes:**
- Handles multiple file formats
- Focus on user experience for media uploads
- Test with various file sizes and formats

### 🏭 Vendor Team (vendors.py)
**Responsibility:** Vendor management and communications
**Files to edit:** `modules/vendors.py`
**Key functions:**
- `show_vendors_page()` - Main vendor interface
- Vendor directory and profiles
- Document uploads and management
- Payment tracking and communications

**Team collaboration notes:**
- Complex workflow with multiple file types
- Focus on vendor portal user experience
- Coordinate with budget team for payment integration

### 👥 Participants Team (participants.py)
**Responsibility:** Participant management and registration
**Files to edit:** `modules/participants.py`
**Key functions:**
- `show_participants_module()` - Main participant interface
- Individual participant addition
- Bulk CSV import functionality
- Participant analytics and reporting

**Team collaboration notes:**
- Heavy focus on data import/export
- Ensure CSV processing is robust
- Test bulk operations thoroughly

### 💰 Budget Team (budget.py)
**Responsibility:** Financial management and expense tracking
**Files to edit:** `modules/budget.py`
**Key functions:**
- `show_budget_module()` - Main budget interface
- Expense tracking with receipt uploads
- Financial reporting and analytics
- Budget allocation and monitoring

**Team collaboration notes:**
- Sensitive financial data handling
- Focus on accuracy and validation
- Coordinate with vendor team for payment integration

### ⚙️ Settings Team (settings.py)
**Responsibility:** System configuration and user management
**Files to edit:** `modules/settings.py`
**Key functions:**
- `show_settings_page()` - Main settings interface
- User management and roles
- System configuration
- Security settings and notifications

**Team collaboration notes:**
- Critical system functionality
- Changes affect all users
- Test thoroughly in different roles
- Coordinate with core team for utility functions

### 🤝 Volunteers Team (volunteers.py)
**Responsibility:** Volunteer management and coordination
**Files to edit:** `modules/volunteers.py`
**Key functions:**
- `show_volunteers_module()` - Main volunteers interface
- Volunteer registration and management
- Training tracking and document management
- Performance analytics and scheduling

**Team collaboration notes:**
- Independent module with comprehensive volunteer lifecycle
- Focus on training workflows and document management
- Test file uploads for training materials and forms

### 🏢 Booths Team (booths.py)
**Responsibility:** Exhibition booth management and layout
**Files to edit:** `modules/booths.py`
**Key functions:**
- `show_booths_module()` - Main booth interface
- Floor plan management and booth reservations
- Vendor booth assignments and documentation
- Revenue tracking and utilization analytics

**Team collaboration notes:**
- Complex spatial management with file uploads
- Focus on floor plan visualizations and booth layouts
- Coordinate with vendor team for booth assignments

### 🔄 Workflows Team (workflows.py)
**Responsibility:** Business process automation and management
**Files to edit:** `modules/workflows.py`
**Key functions:**
- `show_workflows_page()` - Main workflow interface
- Workflow creation and step management
- Process automation and SOP documentation
- Team performance and completion tracking

**Team collaboration notes:**
- Critical for operational efficiency
- Focus on workflow templates and automation
- Coordinate with all teams for process integration

### 📝 Feedback Team (feedback.py)
**Responsibility:** Feedback collection and analysis
**Files to edit:** `modules/feedback.py`
**Key functions:**
- `show_feedback_page()` - Main feedback interface
- Multi-type feedback forms and collection
- Response analysis and sentiment tracking
- Report generation and automated surveys

**Team collaboration notes:**
- Important for continuous improvement
- Focus on user experience and data analysis
- Test various feedback types and file attachments

### 📊 Analytics Team (analytics.py)
**Responsibility:** Data analytics and business intelligence
**Files to edit:** `modules/analytics.py`
**Key functions:**
- `show_analytics_module()` - Main analytics interface
- Real-time dashboards and reporting
- Data export and integration capabilities
- Predictive analytics and ML insights

**Team collaboration notes:**
- Cross-functional data requirements
- Focus on data visualization and insights
- Coordinate with all teams for data integration

## 🚀 Getting Started

### 1. Clone and Setup
```bash
git clone <repository>
cd eventiq-ai
pip install -r requirements.txt
```

### 2. Choose Your Module
Pick your assigned module from the team structure above.

### 3. Run the Application
```bash
streamlit run main_modular.py
```

### 4. Development Workflow
```bash
# Create feature branch
git checkout -b feature/your-module-enhancement

# Edit your assigned module file
# Test your changes
streamlit run main_modular.py

# Commit your changes
git add modules/your_module.py
git commit -m "Enhancement: your feature description"

# Push and create pull request
git push origin feature/your-module-enhancement
```

## 🔄 Team Collaboration Rules

### ✅ DO:
- Edit only your assigned module file
- Test your changes thoroughly
- Add comments for complex logic
- Update this guide if you add new functions
- Communicate with other teams for shared dependencies

### ❌ DON'T:
- Edit other teams' module files without permission
- Make breaking changes to utils.py without team discussion
- Commit directly to main branch
- Remove existing functionality without team approval

### 📋 Code Standards:
- Follow existing function naming conventions
- Add docstrings for new functions
- Use type hints where possible
- Keep file upload functionality consistent
- Test with actual files, not just dummy data

## 🧪 Testing Your Module

### 1. Functionality Testing
- Test all buttons and forms in your module
- Upload actual files (images, PDFs, CSVs)
- Test with different user roles
- Verify data persistence across sessions

### 2. Integration Testing
- Ensure your module works with shared utilities
- Test navigation to/from other modules
- Verify API calls work correctly

### 3. Error Handling
- Test with invalid file formats
- Test with oversized files
- Test network connection issues
- Ensure graceful error messages

## 🔗 Inter-Module Communication

### Session State Variables:
- `st.session_state.logged_in` - Login status
- `st.session_state.user_role` - Current user role
- `st.session_state.user_email` - User email
- `st.session_state.uploaded_files` - Global file storage

### Shared Functions (from utils.py):
- `save_uploaded_file()` - Standard file upload
- `get_file_info()` - File metadata
- `make_api_request()` - API communication
- `display_success/error_message()` - Consistent messaging

## 📞 Support & Communication

### Team Channels:
- **Core Team:** Utility functions and shared resources
- **Frontend Teams:** Individual module development
- **API Team:** Backend services and data models
- **DevOps Team:** Deployment and infrastructure

### When to Coordinate:
- Adding new shared utilities
- Changing API endpoints
- Adding new user roles
- Modifying file upload workflows
- Database schema changes

## 🚀 Deployment

### Development Environment:
```bash
streamlit run main_modular.py
```

### Production Deployment:
- Merge approved pull requests to main
- Deploy via Docker or direct server deployment
- Monitor logs for any integration issues

---

## 🔧 **Essential Git Commands for 10-Member Team**

### **Daily Commands for Each Developer**
```bash
# Morning routine
git checkout feature/your-module-name
git pull origin develop                    # Get latest team changes
git merge develop                         # Merge team updates
git push origin feature/your-module-name  # Push merged changes

# Working routine
git add modules/your-module.py            # Stage your changes
git commit -m "Module: Description of what you did"
git push origin feature/your-module-name  # Save to remote

# Evening routine
git pull origin develop                   # Get end-of-day updates
git merge develop                        # Stay in sync
```

### **Weekly Integration Process**
```bash
# Every Friday - Integration Day
# 1. Create Pull Request from your feature branch to develop
# 2. Get 2 code reviews from team members  
# 3. Merge after approval
# 4. Test full system integration
# 5. Plan next week's work
```

### **Emergency Hotfix Process**
```bash
# For critical bugs affecting production
git checkout main
git checkout -b hotfix/critical-bug-name
# Make minimal fix
git add modules/affected-module.py
git commit -m "Hotfix: Brief description of fix"
# Get immediate review and merge to main AND develop
```

---

## 📋 **Team Coordination Rules**

### **Module Ownership (STRICTLY FOLLOW)**
- **Member 1:** `dashboard.py` only
- **Member 2:** `event_setup.py` only  
- **Member 3:** `budget.py` only
- **Member 4:** `participants.py` only
- **Member 5:** `media_gallery.py` only
- **Member 6:** `vendors.py` only
- **Member 7:** `certificates.py` only
- **Member 8:** `analytics.py` only
- **Member 9:** `settings.py` + `config.py`
- **Member 10:** `workflows.py` + `feedback.py`

### **Shared Files (COORDINATION REQUIRED)**
- `modules/utils.py` - Notify team before changes
- `modules/constants.py` - Team discussion required
- `enhanced_frontend.py` - Senior developer only

### **Conflict Prevention**
1. **Stick to your assigned module**
2. **Communicate before touching shared files**
3. **Pull from develop twice daily**
4. **Test your changes before pushing**
5. **Use descriptive commit messages**

---

## 🚨 **Quick Problem Resolution**

### **"I have merge conflicts!"**
```bash
git status                           # See conflicted files
# Open conflicted files in your IDE
# Look for <<<<<<< HEAD markers
# Choose correct version or merge both
git add modules/conflicted-file.py  # After resolving
git commit -m "Resolved merge conflict"
```

### **"My branch is behind develop!"**
```bash
git checkout develop
git pull origin develop
git checkout feature/your-branch
git merge develop
git push origin feature/your-branch
```

### **"I accidentally modified someone else's module!"**
```bash
git checkout -- modules/other-module.py  # Discard changes
# Or coordinate with that team member
```

---

**🎉 Success Formula: Your Module + Good Git Habits + Team Communication = Amazing EventIQ! 🎉**

**Remember:** Focus on making YOUR module the best it can be while respecting your teammates' work!

Happy Coding! 🚀
