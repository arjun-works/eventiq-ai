#!/usr/bin/env python3
"""
Install dependencies with SSL workaround
"""
import subprocess
import sys
import ssl

def install_packages():
    """Install required packages with SSL workaround"""
    # Disable SSL verification (not recommended for production)
    ssl._create_default_https_context = ssl._create_unverified_context
    
    packages = [
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "python-multipart==0.0.6",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "sqlalchemy==2.0.23",
        "streamlit==1.28.2"
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "--trusted-host", "pypi.org",
                "--trusted-host", "pypi.python.org", 
                "--trusted-host", "files.pythonhosted.org",
                "--disable-pip-version-check",
                package
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"✓ Successfully installed {package}")
            else:
                print(f"✗ Failed to install {package}: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"✗ Timeout installing {package}")
        except Exception as e:
            print(f"✗ Error installing {package}: {e}")
    
    print("\nInstallation complete!")

if __name__ == "__main__":
    install_packages()
