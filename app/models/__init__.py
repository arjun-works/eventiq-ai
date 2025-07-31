"""
Models Package

This package contains all SQLAlchemy models for the EventIQ system.
"""

# Import all models to ensure they are registered with SQLAlchemy
from .user import User, UserRole
from .volunteer import Volunteer, VolunteerAttendance, VolunteerRole
from .participant import Participant, ParticipantBoothVisit, ParticipantStats
from .budget import BudgetEstimate, Expense, BudgetSummary, BudgetCategory, BudgetStatus
from .booth import Booth, BoothFootfall, BoothStats
from .vendor import Vendor, VendorInteraction, VendorAsset, VendorStatus, InteractionType
from .workflow import WorkflowRequest, WorkflowApproval, WorkflowTemplate, WorkflowHistory, WorkflowStatus, ApprovalAction
from .feedback import Feedback, FeedbackCategory, FeedbackSummary, FeedbackType, SentimentScore
from .certificate import Certificate, CertificateTemplate, CertificateBatch, CertificateStatus, CertificateType
from .media import Media, MediaCollection, MediaCollectionItem, MediaDownloadLog, MediaType, MediaStatus
from .admin import SystemIssue, AdminLog, SystemMetrics, EventOverview, AIAssistantLog, IssueStatus, IssuePriority, IssueSource

__all__ = [
    # User models
    "User", "UserRole",
    
    # Volunteer models
    "Volunteer", "VolunteerAttendance", "VolunteerRole",
    
    # Participant models
    "Participant", "ParticipantBoothVisit", "ParticipantStats",
    
    # Budget models
    "BudgetEstimate", "Expense", "BudgetSummary", "BudgetCategory", "BudgetStatus",
    
    # Booth models
    "Booth", "BoothFootfall", "BoothStats",
    
    # Vendor models
    "Vendor", "VendorInteraction", "VendorAsset", "VendorStatus", "InteractionType",
    
    # Workflow models
    "WorkflowRequest", "WorkflowApproval", "WorkflowTemplate", "WorkflowHistory", 
    "WorkflowStatus", "ApprovalAction",
    
    # Feedback models
    "Feedback", "FeedbackCategory", "FeedbackSummary", "FeedbackType", "SentimentScore",
    
    # Certificate models
    "Certificate", "CertificateTemplate", "CertificateBatch", "CertificateStatus", "CertificateType",
    
    # Media models
    "Media", "MediaCollection", "MediaCollectionItem", "MediaDownloadLog", "MediaType", "MediaStatus",
    
    # Admin models
    "SystemIssue", "AdminLog", "SystemMetrics", "EventOverview", "AIAssistantLog",
    "IssueStatus", "IssuePriority", "IssueSource"
]
