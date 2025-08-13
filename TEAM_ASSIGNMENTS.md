# 👥 EventIQ Team Module Assignments

## 🎯 **Module Assignments**

| Team Member | Module | Feature Branch | GitHub Username |
|-------------|--------|----------------|-----------------|
| **Member 1** | Certificates & Mail | `feature/certificates` | @member1_github |
| **Member 2** | Event Setup | `feature/event-setup` | @member2_github |
| **Member 3** | Settings | `feature/settings` | @member3_github |
| **Member 4** | Feedback & Analytics | `feature/feedback-analytics` | @member4_github |
| **Member 5** | Media Gallery | `feature/media-gallery` | @member5_github |
| **Member 6** | Vendors | `feature/vendors` | @member6_github |
| **Member 7** | Participants | `feature/participants` | @member7_github |
| **Member 8** | Booths | `feature/booths` | @member8_github |
| **Member 9** | Workflows | `feature/workflows` | @member9_github |
| **Member 10** | Budget | `feature/budget` | @member10_github |

## 🚀 **Getting Started Instructions**

### **For Each Team Member:**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/eventiq-ai.git
   cd eventiq-ai
   ```

2. **Switch to your assigned branch:**
   ```bash
   git fetch
   git checkout feature/your-module-name
   ```

3. **Set up development environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Start working on your module:**
   - Edit ONLY your assigned module file: `modules/your_module.py`
   - Test your changes: `streamlit run enhanced_frontend.py`

5. **Daily workflow:**
   ```bash
   # Make changes to your module
   git add modules/your_module.py
   git commit -m "ModuleName: Description of changes"
   git push origin feature/your-module-name
   ```

6. **Weekly integration:**
   - Create Pull Request from your feature branch to `develop`
   - Add description of what you built
   - Request review from team lead

## 🚫 **Important Rules**

1. **ONLY edit your assigned module file**
2. **Never edit other team members' modules**
3. **Don't modify core files** (`config.py`, `utils.py`, `constants.py`)
4. **Always work in your feature branch**
5. **All changes must go through Pull Requests**
6. **Get code review before merging**

## 📞 **Need Help?**
- Check `TEAM_COLLABORATION_GUIDE.md` for detailed workflow
- Ask in team chat for quick questions
- Contact team lead for module conflicts

---

**🎉 Let's build an amazing EventIQ system together! 🎉**
