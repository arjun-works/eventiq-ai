# Entry point for Streamlit Cloud deployment
# This file imports and runs the main EventIQ application

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run the main application
from enhanced_frontend import main

if __name__ == "__main__":
    main()
