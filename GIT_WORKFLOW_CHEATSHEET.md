# 📋 EventIQ Daily Git Workflow Cheat Sheet

## 🌅 **Morning Routine (5 minutes)**
```bash
# 1. Switch to your feature branch
git checkout feature/your-module-name

# 2. Get latest team changes
git pull origin develop

# 3. Merge team updates into your branch
git merge develop

# 4. Push the merged updates
git push origin feature/your-module-name

# 5. Start coding!
# Edit: modules/your-assigned-module.py
```

## 💻 **During Development**
```bash
# Save your work frequently
git add modules/your-module.py
git commit -m "Module: Brief description of what you did"
git push origin feature/your-module-name

# Example commit messages:
# "Dashboard: Added real-time participant counter"
# "Budget: Fixed expense calculation bug"
# "Media: Improved file upload validation"
```

## 🌆 **End of Day Routine (3 minutes)**
```bash
# 1. Save final changes
git add modules/your-module.py
git commit -m "Module: End of day - [what you accomplished]"

# 2. Get latest team changes
git pull origin develop
git merge develop

# 3. Push everything
git push origin feature/your-module-name
```

## 📅 **Weekly Integration (Fridays)**
```bash
# 1. Prepare for integration
git checkout feature/your-module-name
git pull origin develop
git merge develop

# 2. Test your module thoroughly
streamlit run enhanced_frontend.py
# Navigate to your module and test all features

# 3. Create Pull Request
# Go to GitHub/GitLab
# Create PR: feature/your-module-name → develop
# Add description of what you built this week
# Request 2 reviewers

# 4. After merge approval
# Your feature branch gets merged to develop
# Start new branch for next week's work
```

## 🚨 **Emergency Commands**

### **"Help! I have merge conflicts!"**
```bash
git status  # See which files have conflicts
# Open conflicted files in VS Code
# Look for <<<<<<< HEAD and >>>>>>> markers
# Choose the correct code or combine both
git add modules/conflicted-file.py
git commit -m "Resolved merge conflict in [module]"
```

### **"I accidentally changed someone else's module!"**
```bash
# Undo changes to other modules (BEFORE committing)
git checkout -- modules/other-persons-module.py
```

### **"My branch is way behind!"**
```bash
git checkout develop
git pull origin develop
git checkout feature/your-module-name
git merge develop
# Resolve any conflicts, then:
git push origin feature/your-module-name
```

### **"I need to fix a critical bug right now!"**
```bash
git checkout main
git checkout -b hotfix/critical-bug-description
# Make minimal fix
git add modules/your-module.py
git commit -m "Hotfix: Brief description"
# Get immediate review and merge
```

## ✅ **Success Checklist**

### **Daily Goals:**
- [ ] Pulled latest changes from develop
- [ ] Made progress on your assigned module
- [ ] Committed with descriptive messages
- [ ] Pushed changes to your feature branch
- [ ] Tested your module works correctly

### **Weekly Goals:**
- [ ] Module improvements completed
- [ ] All features tested thoroughly
- [ ] Pull request created with good description
- [ ] Code reviewed by teammates
- [ ] Merged to develop successfully

### **Module Quality Standards:**
- [ ] Your module loads without errors
- [ ] All buttons and features work
- [ ] File uploads work correctly (if applicable)
- [ ] UI looks professional and consistent
- [ ] Error handling works properly

## 🎯 **Module Assignments Reminder**

| Member | Module | Branch Pattern |
|--------|--------|---------------|
| Member 1 | `dashboard.py` | `feature/dashboard-*` |
| Member 2 | `event_setup.py` | `feature/event-setup-*` |
| Member 3 | `budget.py` | `feature/budget-*` |
| Member 4 | `participants.py` | `feature/participants-*` |
| Member 5 | `media_gallery.py` | `feature/media-*` |
| Member 6 | `vendors.py` | `feature/vendors-*` |
| Member 7 | `certificates.py` | `feature/certificates-*` |
| Member 8 | `analytics.py` | `feature/analytics-*` |
| Member 9 | `settings.py` + `config.py` | `feature/config-*` |
| Member 10 | `workflows.py` + `feedback.py` | `feature/workflows-*` |

## 🚫 **Never Do This:**
- ❌ Work directly on `main` or `develop` branch
- ❌ Force push (`git push --force`) to shared branches
- ❌ Modify another team member's module without coordination
- ❌ Commit temporary files, logs, or personal configs
- ❌ Delete other people's branches
- ❌ Merge your own pull requests without review

## 📞 **Need Help?**
1. **Check:** `TEAM_COLLABORATION_GUIDE.md` (full guide)
2. **Ask:** Team chat for quick questions
3. **Emergency:** Contact team lead directly

---

**🎉 Keep this cheat sheet handy! Simple daily habits = successful team collaboration! 🎉**
