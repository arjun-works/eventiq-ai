# 🚀 Streamlit Cloud Deployment Guide for EventIQ

## 📋 **Prerequisites**
1. ✅ GitHub repository with EventIQ code
2. ✅ All team members added as collaborators
3. ✅ Streamlit Cloud account
4. ✅ Repository is public or you have Streamlit Cloud Pro

---

## 🌐 **Step-by-Step Streamlit Cloud Deployment**

### **Step 1: Prepare Repository for Deployment**

#### **A. Essential Files (Already Created)**
```
eventiq-ai/
├── app.py                    # ✅ Entry point for Streamlit Cloud
├── requirements.txt          # ✅ Python dependencies
├── .streamlit/
│   ├── config.toml          # ✅ Streamlit configuration
│   └── secrets.toml         # ✅ Secrets template (DON'T commit)
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # ✅ GitHub Actions pipeline
└── README.md                # ✅ Updated with deployment info
```

#### **B. Update .gitignore for Deployment**
```bash
# Add to .gitignore
.streamlit/secrets.toml
*.pyc
__pycache__/
.env
venv/
uploads/
*.log
.DS_Store
Thumbs.db
```

### **Step 2: Push to GitHub**
```bash
# Add all deployment files
git add app.py .streamlit/config.toml .github/workflows/ci-cd.yml README.md
git commit -m "Add Streamlit Cloud deployment configuration"
git push origin main
```

### **Step 3: Deploy to Streamlit Cloud**

#### **A. Connect to Streamlit Cloud**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub account
3. Click **"New app"**

#### **B. Configure Deployment**
1. **Repository**: Select `your-username/eventiq-ai`
2. **Branch**: `main`
3. **Main file path**: `app.py`
4. **App URL** (optional): `eventiq-ai` (creates: eventiq-ai.streamlit.app)

#### **C. Advanced Settings**
```
Python version: 3.9
Requirements file: requirements.txt
```

### **Step 4: Configure Secrets (If Needed)**
1. In Streamlit Cloud dashboard, go to **"Manage app"**
2. Click **"Secrets"** tab
3. Add secrets in TOML format:
```toml
[general]
DATABASE_URL = "sqlite:///eventiq.db"
DEBUG = false
ENVIRONMENT = "production"

[email]
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your-email@company.com"
SMTP_PASSWORD = "your-app-password"

[security]
SECRET_KEY = "your-production-secret-key"
```

### **Step 5: Test Deployment**
1. Wait for deployment to complete (2-5 minutes)
2. Access your app at: `https://eventiq-ai.streamlit.app`
3. Test all modules and functionality
4. Check logs for any errors

---

## 🔄 **Continuous Deployment Setup**

### **Automatic Deployment**
- ✅ **Trigger**: Push to `main` branch
- ✅ **Process**: Streamlit Cloud automatically redeploys
- ✅ **Testing**: GitHub Actions run tests before deployment
- ✅ **Notifications**: Team gets notified of deployment status

### **Team Workflow for Deployment**
```bash
# Team member workflow
git checkout feature/your-module
# Make changes to your module
git add modules/your_module.py
git commit -m "Module: Add new feature"
git push origin feature/your-module

# Create PR to develop
# After review and merge to develop
# Team lead merges develop to main
# Automatic deployment to Streamlit Cloud
```

---

## 🛠️ **Production Configuration**

### **Environment Variables in Streamlit Cloud**
Set these in the Streamlit Cloud secrets:

```toml
[general]
ENVIRONMENT = "production"
DEBUG = false
MAX_FILE_SIZE_MB = 200

[database]
DATABASE_URL = "postgresql://user:pass@host:5432/eventiq"  # If using external DB

[file_storage]
UPLOAD_FOLDER = "/tmp/uploads"  # Streamlit Cloud uses /tmp for temporary files
MAX_UPLOAD_SIZE = 200  # MB

[features]
ENABLE_ANALYTICS = true
ENABLE_EMAIL = true
ENABLE_CERTIFICATES = true
```

### **Performance Optimization**
```python
# Add to app.py for production
import streamlit as st

# Configure for production
st.set_page_config(
    page_title="EventIQ - Corporate IT Events",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-username/eventiq-ai',
        'Report a bug': "https://github.com/your-username/eventiq-ai/issues",
        'About': "EventIQ - Corporate IT Event Management System"
    }
)

# Cache configuration for better performance
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_sample_data():
    # Load sample data
    pass
```

---

## 📊 **Monitoring & Maintenance**

### **Health Checks**
- ✅ **App Status**: Monitor at `https://eventiq-ai.streamlit.app`
- ✅ **GitHub Actions**: Check workflow status
- ✅ **Streamlit Logs**: Monitor in Streamlit Cloud dashboard
- ✅ **User Feedback**: Collect via feedback module

### **Update Process**
1. **Team Development**: Work in feature branches
2. **Integration**: Merge to `develop` branch
3. **Testing**: Full system testing
4. **Release**: Merge `develop` to `main`
5. **Deployment**: Automatic via Streamlit Cloud
6. **Verification**: Test live application

---

## 🚨 **Troubleshooting Common Issues**

### **Deployment Fails**
```bash
# Check requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements.txt"
git push origin main
```

### **Module Import Errors**
```python
# In app.py, ensure proper imports
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
```

### **File Upload Issues**
```python
# Use Streamlit's temp directory
import tempfile
UPLOAD_FOLDER = tempfile.gettempdir()
```

### **Memory Issues**
```python
# Add memory optimization
@st.cache_data(max_entries=100)
def process_large_file(file):
    # Process file with caching
    pass
```

---

## 🔗 **Useful Links**

- 🌐 **Live App**: https://eventiq-ai.streamlit.app
- 📚 **Streamlit Docs**: https://docs.streamlit.io/streamlit-cloud
- 🔧 **GitHub Repo**: https://github.com/your-username/eventiq-ai
- 📋 **Team Guide**: TEAM_COLLABORATION_GUIDE.md
- 📊 **Workflow**: GIT_WORKFLOW_CHEATSHEET.md

---

## 📞 **Support**

### **Deployment Issues**
1. Check Streamlit Cloud logs
2. Verify GitHub Actions status
3. Test locally: `streamlit run app.py`
4. Contact team lead for assistance

### **Team Collaboration**
1. Follow module assignments
2. Use feature branches
3. Create PRs for all changes
4. Test before merging to main

---

**🎉 Your EventIQ application is now live on Streamlit Cloud with automatic deployment! 🚀**

**Live URL**: `https://eventiq-ai.streamlit.app`

Every push to the `main` branch will automatically update your live application!
