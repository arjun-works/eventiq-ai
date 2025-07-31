#!/usr/bin/env python3
"""
EventIQ Team Readiness Checker
Verifies that the repository is ready for 10-member team collaboration
"""

import os
import sys
import subprocess
from pathlib import Path

def check_git_status():
    """Check if Git is initialized and configured"""
    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository is initialized")
            return True
        else:
            print("❌ Git repository not initialized")
            print("   Run: git init")
            return False
    except FileNotFoundError:
        print("❌ Git not found - please install Git")
        return False

def check_branches():
    """Check if develop branch exists"""
    try:
        result = subprocess.run(['git', 'branch', '-a'], capture_output=True, text=True)
        branches = result.stdout
        if 'develop' in branches:
            print("✅ Develop branch exists")
            return True
        else:
            print("❌ Develop branch missing")
            print("   Run: git checkout -b develop && git push -u origin develop")
            return False
    except:
        print("❌ Cannot check branches")
        return False

def check_modules():
    """Check if all required modules exist"""
    required_modules = [
        'dashboard.py', 'event_setup.py', 'budget.py', 'participants.py',
        'media_gallery.py', 'vendors.py', 'certificates.py', 'analytics.py',
        'settings.py', 'workflows.py', 'feedback.py', 'config.py',
        'constants.py', 'utils.py'
    ]
    
    modules_dir = Path('modules')
    if not modules_dir.exists():
        print("❌ Modules directory missing")
        return False
    
    missing_modules = []
    for module in required_modules:
        if not (modules_dir / module).exists():
            missing_modules.append(module)
    
    if missing_modules:
        print(f"❌ Missing modules: {', '.join(missing_modules)}")
        return False
    else:
        print("✅ All required modules present")
        return True

def check_frontend():
    """Check if main frontend file exists"""
    if Path('enhanced_frontend.py').exists():
        print("✅ Main frontend file exists")
        return True
    else:
        print("❌ enhanced_frontend.py missing")
        return False

def check_gitignore():
    """Check if .gitignore exists with proper entries"""
    gitignore_path = Path('.gitignore')
    if gitignore_path.exists():
        content = gitignore_path.read_text()
        required_entries = ['__pycache__/', '*.pyc', '.env', 'venv/', 'uploads/']
        missing = [entry for entry in required_entries if entry not in content]
        
        if missing:
            print(f"⚠️  .gitignore missing entries: {', '.join(missing)}")
            return False
        else:
            print("✅ .gitignore properly configured")
            return True
    else:
        print("❌ .gitignore missing")
        return False

def check_requirements():
    """Check if requirements.txt exists"""
    if Path('requirements.txt').exists():
        print("✅ requirements.txt exists")
        return True
    else:
        print("❌ requirements.txt missing")
        return False

def check_documentation():
    """Check if team documentation exists"""
    docs = ['TEAM_COLLABORATION_GUIDE.md', 'README.md']
    missing_docs = [doc for doc in docs if not Path(doc).exists()]
    
    if missing_docs:
        print(f"⚠️  Missing documentation: {', '.join(missing_docs)}")
        return False
    else:
        print("✅ Team documentation present")
        return True

def main():
    """Run all checks"""
    print("🔍 EventIQ Team Readiness Check")
    print("=" * 40)
    
    checks = [
        check_git_status,
        check_branches,
        check_modules,
        check_frontend,
        check_gitignore,
        check_requirements,
        check_documentation
    ]
    
    results = []
    for check in checks:
        results.append(check())
        print()
    
    passed = sum(results)
    total = len(results)
    
    print("=" * 40)
    print(f"📊 Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 Repository is ready for team collaboration!")
        print("\n🚀 Next steps for team members:")
        print("1. Clone the repository")
        print("2. Run setup script: scripts/team_git_setup.bat")
        print("3. Start working on assigned modules")
        print("4. Follow the daily workflow in GIT_WORKFLOW_CHEATSHEET.md")
        return True
    else:
        print("❌ Repository needs setup before team collaboration")
        print("\n🔧 Fix the issues above, then run this script again")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
