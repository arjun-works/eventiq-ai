"""
Legacy Additional Modules File - Now Separated
===============================================

This file previously contained 5 modules that have now been separated into individual files:

1. Volunteers Module -> modules/volunteers.py
2. Booths Module -> modules/booths.py  
3. Workflows Module -> modules/workflows.py
4. Feedback Module -> modules/feedback.py
5. Analytics Module -> modules/analytics.py

Each module is now maintained by its respective team for better collaboration.

This file is kept for reference and can be removed once all teams 
have transitioned to the new modular structure.
"""

# Import the separated modules for backward compatibility
from .volunteers import show_volunteers_module
from .booths import show_booths_module
from .workflows import show_workflows_page
from .feedback import show_feedback_page
from .analytics import show_analytics_module

# Re-export all functions for backward compatibility
__all__ = [
    'show_volunteers_module',
    'show_booths_module', 
    'show_workflows_page',
    'show_feedback_page',
    'show_analytics_module'
]
