"""
Workflow and Approval Models

This module defines models for workflow management and approval processes.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, Enum as SQLEnum
from sqlalchemy.sql import func
from enum import Enum

from app.core.database import Base


class WorkflowStatus(str, Enum):
    """Workflow status enumeration"""
    SUBMITTED = "submitted"
    IN_REVIEW = "in_review"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"


class ApprovalAction(str, Enum):
    """Approval action enumeration"""
    APPROVE = "approve"
    REJECT = "reject"
    REQUEST_CHANGES = "request_changes"
    ESCALATE = "escalate"
    DELEGATE = "delegate"


class WorkflowRequest(Base):
    """Main workflow request for material approvals"""
    
    __tablename__ = "workflow_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Request details
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    request_type = Column(String(100), nullable=False)  # material_approval, security_clearance, etc.
    priority = Column(String(20), default="medium", nullable=False)  # low, medium, high, urgent
    
    # Requester information
    requester_name = Column(String(255), nullable=False)
    requester_email = Column(String(255), nullable=False)
    requester_department = Column(String(100), nullable=True)
    
    # Request content
    materials_requested = Column(JSON, nullable=True)  # List of materials/items
    justification = Column(Text, nullable=True)
    business_case = Column(Text, nullable=True)
    estimated_cost = Column(Integer, nullable=True)
    
    # Workflow configuration
    approval_levels_required = Column(Integer, default=1, nullable=False)
    current_approval_level = Column(Integer, default=0, nullable=False)
    auto_approval_eligible = Column(Boolean, default=False, nullable=False)
    
    # Status and tracking
    status = Column(SQLEnum(WorkflowStatus), default=WorkflowStatus.SUBMITTED, nullable=False)
    reference_number = Column(String(50), unique=True, nullable=False)
    
    # Dates and deadlines
    submission_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    target_completion_date = Column(DateTime(timezone=True), nullable=True)
    actual_completion_date = Column(DateTime(timezone=True), nullable=True)
    
    # External system integration
    external_system_id = Column(String(100), nullable=True)  # Pega case ID if available
    external_system_url = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    def __repr__(self):
        return f"<WorkflowRequest(id={self.id}, ref='{self.reference_number}', status='{self.status}')>"


class WorkflowApproval(Base):
    """Individual approval steps within a workflow"""
    
    __tablename__ = "workflow_approvals"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_request_id = Column(Integer, nullable=False)  # Foreign key to workflow_requests
    
    # Approval step details
    approval_level = Column(Integer, nullable=False)
    approver_name = Column(String(255), nullable=False)
    approver_email = Column(String(255), nullable=False)
    approver_role = Column(String(100), nullable=True)
    
    # Approval decision
    action = Column(SQLEnum(ApprovalAction), nullable=True)
    decision_date = Column(DateTime(timezone=True), nullable=True)
    comments = Column(Text, nullable=True)
    conditions = Column(Text, nullable=True)  # Any conditions for approval
    
    # Status and timing
    is_pending = Column(Boolean, default=True, nullable=False)
    is_delegated = Column(Boolean, default=False, nullable=False)
    delegated_to = Column(String(255), nullable=True)
    
    # Notification tracking
    notification_sent = Column(Boolean, default=False, nullable=False)
    notification_date = Column(DateTime(timezone=True), nullable=True)
    reminder_count = Column(Integer, default=0, nullable=False)
    last_reminder_date = Column(DateTime(timezone=True), nullable=True)
    
    # SLA tracking
    expected_response_date = Column(DateTime(timezone=True), nullable=True)
    is_overdue = Column(Boolean, default=False, nullable=False)
    escalation_triggered = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    def __repr__(self):
        return f"<WorkflowApproval(id={self.id}, level={self.approval_level}, approver='{self.approver_name}')>"


class WorkflowTemplate(Base):
    """Predefined workflow templates for different types of requests"""
    
    __tablename__ = "workflow_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Template details
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    request_type = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Workflow configuration
    approval_levels = Column(JSON, nullable=False)  # List of approval level configurations
    auto_approval_rules = Column(JSON, nullable=True)  # Rules for auto-approval
    sla_hours = Column(Integer, default=72, nullable=False)  # SLA in hours
    
    # Notification settings
    notification_template = Column(Text, nullable=True)
    reminder_intervals = Column(JSON, nullable=True)  # Reminder schedule
    escalation_rules = Column(JSON, nullable=True)  # Escalation configuration
    
    # Usage statistics
    times_used = Column(Integer, default=0, nullable=False)
    average_completion_time = Column(Integer, nullable=True)  # In hours
    approval_rate = Column(Integer, nullable=True)  # Percentage
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    def __repr__(self):
        return f"<WorkflowTemplate(id={self.id}, name='{self.name}', type='{self.request_type}')>"


class WorkflowHistory(Base):
    """Audit trail and history for workflow requests"""
    
    __tablename__ = "workflow_history"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_request_id = Column(Integer, nullable=False)  # Foreign key to workflow_requests
    
    # History entry details
    action = Column(String(100), nullable=False)  # status_change, comment_added, etc.
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    
    # Actor information
    actor_name = Column(String(255), nullable=False)
    actor_email = Column(String(255), nullable=False)
    actor_role = Column(String(100), nullable=True)
    
    # System information
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    
    # Timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<WorkflowHistory(id={self.id}, action='{self.action}', actor='{self.actor_name}')>"
