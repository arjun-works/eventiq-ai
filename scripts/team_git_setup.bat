@echo off
REM EventIQ Team Git Setup Script (Windows)
REM Run this script to set up your development environment

echo 🎉 EventIQ Team Git Setup
echo =========================

REM Get team member info
set /p developer_name="Enter your name: "
set /p module_name="Enter your module assignment (dashboard, budget, media, etc.): "

REM Configure Git
echo ⚙️ Configuring Git...
git config --global user.name "%developer_name%"
git config --global user.email "%developer_name%@company.com"
git config --global core.autocrlf true
git config --global init.defaultBranch main

REM Useful Git aliases
echo 🔧 Setting up Git aliases...
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
git config --global alias.lg "log --oneline --graph --all"

REM Set up development branch
echo 🌿 Setting up your feature branch...
set branch_name=feature/%module_name%-enhancements
git checkout develop
git pull origin develop
git checkout -b %branch_name%
git push -u origin %branch_name%

echo ✅ Setup complete!
echo.
echo 📋 Your development setup:
echo    Developer: %developer_name%
echo    Module: %module_name%
echo    Branch: %branch_name%
echo.
echo 🚀 Next steps:
echo 1. Start editing modules/%module_name%.py
echo 2. Test with: streamlit run enhanced_frontend.py
echo 3. Commit changes: git add modules/%module_name%.py ^&^& git commit -m "Module: Description"
echo 4. Push changes: git push origin %branch_name%
echo.
echo 📞 Need help? Check TEAM_COLLABORATION_GUIDE.md
echo.
echo Happy coding! 🎉

pause
