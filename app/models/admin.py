"""
Admin Dashboard and System Management Models

This module defines models for admin functionality, system monitoring, and issue tracking.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, Enum as SQLEnum
from sqlalchemy.sql import func
from enum import Enum

from app.core.database import Base


class IssueStatus(str, Enum):
    """Issue status enumeration"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    CANCELLED = "cancelled"


class IssuePriority(str, Enum):
    """Issue priority enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    URGENT = "urgent"


class IssueSource(str, Enum):
    """Issue source enumeration"""
    MANUAL = "manual"
    AUTO_DETECTED = "auto_detected"
    AI_DETECTED = "ai_detected"
    USER_REPORTED = "user_reported"
    SYSTEM_ALERT = "system_alert"


class SystemIssue(Base):
    """Issue tracking for event management system"""
    
    __tablename__ = "system_issues"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Issue details
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    issue_type = Column(String(100), nullable=False)  # technical, process, user_experience, etc.
    category = Column(String(100), nullable=True)  # More specific categorization
    
    # Severity and priority
    priority = Column(SQLEnum(IssuePriority), default=IssuePriority.MEDIUM, nullable=False)
    severity_score = Column(Integer, nullable=True)  # 1-10 scale
    impact_level = Column(String(50), nullable=True)  # low, medium, high, critical
    
    # Source and detection
    source = Column(SQLEnum(IssueSource), nullable=False)
    detected_by = Column(String(255), nullable=True)  # User/system that detected the issue
    detection_method = Column(String(100), nullable=True)  # How it was detected
    
    # Status and assignment
    status = Column(SQLEnum(IssueStatus), default=IssueStatus.OPEN, nullable=False)
    assigned_to = Column(String(255), nullable=True)
    assigned_team = Column(String(100), nullable=True)
    
    # Resolution details
    resolution_notes = Column(Text, nullable=True)
    root_cause = Column(Text, nullable=True)
    resolution_steps = Column(Text, nullable=True)  # JSON list of steps taken
    
    # Time tracking
    estimated_resolution_time = Column(Integer, nullable=True)  # Hours
    actual_resolution_time = Column(Integer, nullable=True)  # Hours
    first_response_time = Column(DateTime(timezone=True), nullable=True)
    resolution_date = Column(DateTime(timezone=True), nullable=True)
    
    # Impact assessment
    affected_users_count = Column(Integer, default=0, nullable=False)
    affected_modules = Column(JSON, nullable=True)  # List of affected system modules
    business_impact = Column(Text, nullable=True)
    
    # Follow-up and prevention
    requires_follow_up = Column(Boolean, default=False, nullable=False)
    prevention_measures = Column(Text, nullable=True)
    similar_issues_count = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    def __repr__(self):
        return f"<SystemIssue(id={self.id}, title='{self.title}', status='{self.status}', priority='{self.priority}')>"


class AdminLog(Base):
    """Admin activity logging for audit trail"""
    
    __tablename__ = "admin_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Admin and action details
    admin_user = Column(String(255), nullable=False)
    action = Column(String(255), nullable=False)
    target_type = Column(String(100), nullable=True)  # user, booth, vendor, etc.
    target_id = Column(String(50), nullable=True)  # ID of affected entity
    
    # Action details
    description = Column(Text, nullable=False)
    old_values = Column(JSON, nullable=True)  # Before values (for updates)
    new_values = Column(JSON, nullable=True)  # After values (for updates)
    
    # Context information
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    session_id = Column(String(100), nullable=True)
    
    # Success and error handling
    success = Column(Boolean, default=True, nullable=False)
    error_message = Column(Text, nullable=True)
    
    # Timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<AdminLog(id={self.id}, admin='{self.admin_user}', action='{self.action}')>"


class SystemMetrics(Base):
    """System performance and usage metrics"""
    
    __tablename__ = "system_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Metric details
    metric_name = Column(String(100), nullable=False)
    metric_category = Column(String(50), nullable=False)  # performance, usage, business, etc.
    metric_value = Column(Integer, nullable=False)
    metric_unit = Column(String(20), nullable=True)  # count, percentage, seconds, etc.
    
    # Time information
    measurement_timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    measurement_hour = Column(Integer, nullable=False)  # Hour of day (0-23)
    measurement_date = Column(DateTime(timezone=True), nullable=False)  # Date only
    
    # Additional context
    additional_data = Column(JSON, nullable=True)  # Any additional metric data
    
    def __repr__(self):
        return f"<SystemMetrics(metric='{self.metric_name}', value={self.metric_value}, timestamp={self.measurement_timestamp})>"


class EventOverview(Base):
    """High-level event statistics and overview"""
    
    __tablename__ = "event_overview"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Date for the overview
    overview_date = Column(DateTime(timezone=True), nullable=False)
    
    # Participant metrics
    total_registered_participants = Column(Integer, default=0, nullable=False)
    total_checked_in_participants = Column(Integer, default=0, nullable=False)
    participant_attendance_rate = Column(Integer, default=0, nullable=False)  # Percentage
    
    # Volunteer metrics
    total_registered_volunteers = Column(Integer, default=0, nullable=False)
    total_active_volunteers = Column(Integer, default=0, nullable=False)
    total_volunteer_hours = Column(Integer, default=0, nullable=False)
    
    # Booth metrics
    total_active_booths = Column(Integer, default=0, nullable=False)
    average_booth_visitors = Column(Integer, default=0, nullable=False)
    most_popular_booth = Column(String(255), nullable=True)
    
    # Budget metrics
    total_estimated_budget = Column(Integer, default=0, nullable=False)
    total_actual_expenses = Column(Integer, default=0, nullable=False)
    budget_variance_percentage = Column(Integer, default=0, nullable=False)
    
    # System health
    system_uptime_percentage = Column(Integer, default=100, nullable=False)
    total_system_issues = Column(Integer, default=0, nullable=False)
    resolved_issues_count = Column(Integer, default=0, nullable=False)
    
    # Engagement metrics
    total_feedback_responses = Column(Integer, default=0, nullable=False)
    average_satisfaction_score = Column(Integer, default=0, nullable=False)
    
    # Generated certificates
    certificates_generated = Column(Integer, default=0, nullable=False)
    certificates_sent = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    def __repr__(self):
        return f"<EventOverview(date={self.overview_date}, participants={self.total_registered_participants}, volunteers={self.total_registered_volunteers})>"


class AIAssistantLog(Base):
    """AI Assistant interaction logging"""
    
    __tablename__ = "ai_assistant_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # User and session info
    user_id = Column(Integer, nullable=True)  # Null for anonymous users
    session_id = Column(String(100), nullable=False)
    user_role = Column(String(50), nullable=True)
    
    # Query and response
    user_query = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    response_type = Column(String(50), nullable=True)  # answer, clarification, error, etc.
    
    # Processing metrics
    processing_time_ms = Column(Integer, nullable=True)
    tokens_used = Column(Integer, nullable=True)
    model_used = Column(String(100), nullable=True)
    
    # Context and intent
    query_intent = Column(String(100), nullable=True)  # Detected intent
    context_data = Column(JSON, nullable=True)  # Relevant context used
    confidence_score = Column(Integer, nullable=True)  # AI confidence in response
    
    # User feedback
    user_rating = Column(Integer, nullable=True)  # 1-5 scale
    was_helpful = Column(Boolean, nullable=True)
    follow_up_needed = Column(Boolean, default=False, nullable=False)
    
    # Error handling
    had_error = Column(Boolean, default=False, nullable=False)
    error_type = Column(String(100), nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<AIAssistantLog(id={self.id}, session='{self.session_id}', timestamp={self.timestamp})>"
