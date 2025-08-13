"""
Constants and Enumerations for EventIQ Management System
Centralized definitions for consistent usage across all modules
"""

from enum import Enum
from typing import List, Dict

class UserRole(Enum):
    """User role enumeration"""
    ORGANIZER = "organizer"
    VOLUNTEER = "volunteer"
    PARTICIPANT = "participant"
    VENDOR = "vendor"
    ADMIN = "admin"

class EventStatus(Enum):
    """Event status enumeration"""
    PLANNING = "planning"
    REGISTRATION_OPEN = "registration_open"
    REGISTRATION_CLOSED = "registration_closed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class VolunteerStatus(Enum):
    """Volunteer status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_BREAK = "on_break"
    COMPLETED = "completed"

class BoothStatus(Enum):
    """Booth status enumeration"""
    AVAILABLE = "available"
    RESERVED = "reserved"
    OCCUPIED = "occupied"
    MAINTENANCE = "maintenance"

class WorkflowStatus(Enum):
    """Workflow status enumeration"""
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    FAILED = "failed"
    CANCELLED = "cancelled"

class FeedbackType(Enum):
    """Feedback type enumeration"""
    EVENT_OVERALL = "event_overall"
    SESSION_SPECIFIC = "session_specific"
    VENDOR_FEEDBACK = "vendor_feedback"
    VOLUNTEER_FEEDBACK = "volunteer_feedback"
    VENUE_FEEDBACK = "venue_feedback"

class Priority(Enum):
    """Priority level enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# File type constants
IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "gif", "bmp", "webp"]
DOCUMENT_EXTENSIONS = ["pdf", "doc", "docx", "txt", "rtf"]
SPREADSHEET_EXTENSIONS = ["csv", "xlsx", "xls"]
PRESENTATION_EXTENSIONS = ["ppt", "pptx"]
ARCHIVE_EXTENSIONS = ["zip", "rar", "7z"]
CAD_EXTENSIONS = ["dwg", "dxf"]
VIDEO_EXTENSIONS = ["mp4", "avi", "mov", "wmv", "flv"]
AUDIO_EXTENSIONS = ["mp3", "wav", "ogg", "m4a"]

# UI Constants
PAGE_ICONS = {
    "dashboard": "🏠",
    "event_setup": "🎯",
    "certificates": "🎓",
    "media_gallery": "📸",
    "vendors": "🏭",
    "participants": "👥",
    "budget": "💰",
    "settings": "⚙️",
    "volunteers": "🤝",
    "booths": "🏢",
    "workflows": "🔄",
    "feedback": "📝",
    "analytics": "📊"
}

# Navigation menu configurations
NAVIGATION_MENUS = {
    UserRole.ORGANIZER.value: [
        "🏠 Dashboard",
        "� Event Setup",
        "�🎓 Certificates", 
        "📸 Media Gallery",
        "🏭 Vendors",
        "👥 Participants",
        "🤝 Volunteers",
        "💰 Budget",
        "🏢 Booths",
        "🔄 Workflows",
        "📝 Feedback",
        "📊 Analytics",
        "⚙️ Settings"
    ],
    UserRole.VOLUNTEER.value: [
        "🏠 Dashboard",
        "🎓 My Certificates",
        "📝 Feedback",
        "⚙️ Profile"
    ],
    UserRole.PARTICIPANT.value: [
        "🏠 Dashboard",
        "📝 Feedback",
        "⚙️ Profile"
    ],
    UserRole.VENDOR.value: [
        "🏠 Dashboard",
        "🏭 Vendor Portal",
        "⚙️ Profile"
    ],
    UserRole.ADMIN.value: [
        "🏠 Dashboard",
        "👥 User Management",
        "📊 System Analytics",
        "⚙️ System Settings"
    ]
}

# Team assignments for modules
TEAM_ASSIGNMENTS = {
    "utils": "Core Team",
    "dashboard": "Dashboard Team",
    "event_setup": "Event Setup Team",
    "certificates": "Certificate Team",
    "media_gallery": "Media Team",
    "vendors": "Vendor Team",
    "participants": "Participants Team",
    "budget": "Budget Team",
    "settings": "Settings Team",
    "volunteers": "Volunteers Team",
    "booths": "Booths Team",
    "workflows": "Workflows Team",
    "feedback": "Feedback Team",
    "analytics": "Analytics Team"
}

# Email templates
EMAIL_TEMPLATES = {
    "welcome_volunteer": {
        "subject": "Welcome to EventIQ - Volunteer Registration Confirmed",
        "template": "Thank you for registering as a volunteer for our event!"
    },
    "certificate_ready": {
        "subject": "Your EventIQ Certificate is Ready",
        "template": "Your participation certificate has been generated and is ready for download."
    },
    "vendor_approved": {
        "subject": "Vendor Application Approved - EventIQ",
        "template": "Congratulations! Your vendor application has been approved."
    },
    "feedback_reminder": {
        "subject": "We'd Love Your Feedback - EventIQ",
        "template": "Please take a moment to share your experience with us."
    }
}

# Status colors for UI
STATUS_COLORS = {
    "active": "#28a745",      # Green
    "inactive": "#6c757d",    # Gray
    "pending": "#ffc107",     # Yellow
    "completed": "#17a2b8",   # Blue
    "cancelled": "#dc3545",   # Red
    "high": "#dc3545",        # Red for high priority
    "medium": "#ffc107",      # Yellow for medium priority
    "low": "#28a745"          # Green for low priority
}

# Default values
DEFAULT_VALUES = {
    "pagination_size": 10,
    "session_timeout": 3600,  # 1 hour in seconds
    "max_file_size_mb": 10,
    "auto_refresh_interval": 30,  # seconds
    "chart_height": 400,
    "table_height": 300
}

# API endpoints
API_ENDPOINTS = {
    "auth": "/api/v1/auth",
    "users": "/api/v1/users",
    "events": "/api/v1/events",
    "certificates": "/api/v1/certificates",
    "vendors": "/api/v1/vendors",
    "participants": "/api/v1/participants",
    "volunteers": "/api/v1/volunteers",
    "booths": "/api/v1/booths",
    "workflows": "/api/v1/workflows",
    "feedback": "/api/v1/feedback",
    "analytics": "/api/v1/analytics",
    "media": "/api/v1/media",
    "budget": "/api/v1/budget"
}

# Validation rules
VALIDATION_RULES = {
    "email": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    "phone": r'^\+?1?\d{9,15}$',
    "password_min_length": 8,
    "name_min_length": 2,
    "name_max_length": 100
}

# Chart configurations
CHART_CONFIGS = {
    "default_colors": ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8'],
    "chart_height": 400,
    "font_family": "Arial, sans-serif",
    "font_size": 12
}

# Error messages
ERROR_MESSAGES = {
    "file_too_large": "File size exceeds the maximum allowed limit",
    "invalid_file_type": "File type is not supported",
    "required_field": "This field is required",
    "invalid_email": "Please enter a valid email address",
    "invalid_phone": "Please enter a valid phone number",
    "weak_password": "Password must be at least 8 characters long",
    "upload_failed": "File upload failed. Please try again",
    "network_error": "Network error. Please check your connection",
    "unauthorized": "You are not authorized to perform this action",
    "session_expired": "Your session has expired. Please log in again"
}

# Success messages
SUCCESS_MESSAGES = {
    "file_uploaded": "File uploaded successfully",
    "data_saved": "Data saved successfully",
    "email_sent": "Email sent successfully",
    "user_created": "User created successfully",
    "certificate_generated": "Certificate generated successfully",
    "workflow_completed": "Workflow completed successfully",
    "feedback_submitted": "Feedback submitted successfully"
}

# Module feature flags
FEATURE_FLAGS = {
    "enable_real_time_analytics": True,
    "enable_bulk_operations": True,
    "enable_file_compression": True,
    "enable_email_notifications": True,
    "enable_audit_logging": True,
    "enable_data_export": True,
    "enable_api_integration": True,
    "enable_mobile_responsive": True
}

def get_user_navigation(user_role: str) -> List[str]:
    """Get navigation menu for specific user role"""
    return NAVIGATION_MENUS.get(user_role, NAVIGATION_MENUS[UserRole.PARTICIPANT.value])

def get_team_for_module(module_name: str) -> str:
    """Get team assignment for a specific module"""
    return TEAM_ASSIGNMENTS.get(module_name, "General Team")

def get_status_color(status: str) -> str:
    """Get color code for a status"""
    return STATUS_COLORS.get(status.lower(), "#6c757d")

def is_feature_enabled(feature_name: str) -> bool:
    """Check if a feature is enabled"""
    return FEATURE_FLAGS.get(feature_name, False)
