"""
Certificate Generation Models

This module defines models for generating and managing volunteer certificates.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum

from app.core.database import Base


class CertificateStatus(str, Enum):
    """Certificate status enumeration"""
    DRAFT = "draft"
    GENERATED = "generated"
    SENT = "sent"
    DOWNLOADED = "downloaded"
    REVOKED = "revoked"


class CertificateType(str, Enum):
    """Certificate type enumeration"""
    VOLUNTEER_COMPLETION = "volunteer_completion"
    VOLUNTEER_APPRECIATION = "volunteer_appreciation"
    PARTICIPANT_COMPLETION = "participant_completion"
    ORGANIZER_RECOGNITION = "organizer_recognition"
    VENDOR_PARTNERSHIP = "vendor_partnership"


class Certificate(Base):
    """Certificate generation and management"""
    
    __tablename__ = "certificates"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Certificate details
    certificate_number = Column(String(50), unique=True, nullable=False)
    certificate_type = Column(SQLEnum(CertificateType), nullable=False)
    title = Column(String(255), nullable=False)
    
    # Recipient information
    recipient_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_name = Column(String(255), nullable=False)
    recipient_email = Column(String(255), nullable=False)
    
    # Achievement details
    achievement_description = Column(Text, nullable=False)
    hours_volunteered = Column(Integer, nullable=True)  # For volunteer certificates
    booth_assigned = Column(String(255), nullable=True)  # For volunteer certificates
    role_performed = Column(String(255), nullable=True)  # Role during event
    event_dates = Column(String(100), nullable=True)  # Event duration
    
    # Certificate content
    custom_message = Column(Text, nullable=True)
    skills_demonstrated = Column(String(500), nullable=True)  # List of skills
    additional_recognitions = Column(Text, nullable=True)
    
    # Template and design
    template_used = Column(String(100), nullable=False, default="default")
    logo_url = Column(String(500), nullable=True)
    signature_name = Column(String(255), nullable=True)
    signature_title = Column(String(255), nullable=True)
    
    # File information
    pdf_file_path = Column(String(500), nullable=True)
    pdf_file_size = Column(Integer, nullable=True)  # File size in bytes
    download_url = Column(String(500), nullable=True)
    
    # Status and tracking
    status = Column(SQLEnum(CertificateStatus), default=CertificateStatus.DRAFT, nullable=False)
    generation_date = Column(DateTime(timezone=True), nullable=True)
    sent_date = Column(DateTime(timezone=True), nullable=True)
    download_count = Column(Integer, default=0, nullable=False)
    last_downloaded = Column(DateTime(timezone=True), nullable=True)
    
    # Verification
    verification_code = Column(String(100), unique=True, nullable=False)
    is_verified = Column(Boolean, default=True, nullable=False)
    verification_url = Column(String(500), nullable=True)
    
    # Email delivery
    email_sent = Column(Boolean, default=False, nullable=False)
    email_delivery_attempts = Column(Integer, default=0, nullable=False)
    last_email_attempt = Column(DateTime(timezone=True), nullable=True)
    email_error_message = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    recipient = relationship("User", backref="certificates_received")
    
    def __repr__(self):
        return f"<Certificate(id={self.id}, number='{self.certificate_number}', recipient='{self.recipient_name}')>"


class CertificateTemplate(Base):
    """Certificate templates for different types of certificates"""
    
    __tablename__ = "certificate_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Template details
    name = Column(String(255), nullable=False)
    certificate_type = Column(SQLEnum(CertificateType), nullable=False)
    description = Column(Text, nullable=True)
    
    # Template files
    html_template_path = Column(String(500), nullable=False)
    css_file_path = Column(String(500), nullable=True)
    preview_image_path = Column(String(500), nullable=True)
    
    # Template configuration
    default_title = Column(String(255), nullable=True)
    default_message = Column(Text, nullable=True)
    required_fields = Column(String(500), nullable=True)  # JSON list of required fields
    optional_fields = Column(String(500), nullable=True)  # JSON list of optional fields
    
    # Design settings
    page_size = Column(String(20), default="A4", nullable=False)  # A4, Letter, etc.
    orientation = Column(String(20), default="landscape", nullable=False)  # portrait, landscape
    background_color = Column(String(20), nullable=True)
    font_family = Column(String(100), nullable=True)
    
    # Usage and status
    is_active = Column(Boolean, default=True, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    times_used = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    def __repr__(self):
        return f"<CertificateTemplate(id={self.id}, name='{self.name}', type='{self.certificate_type}')>"


class CertificateBatch(Base):
    """Batch processing for multiple certificate generation"""
    
    __tablename__ = "certificate_batches"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Batch details
    batch_name = Column(String(255), nullable=False)
    certificate_type = Column(SQLEnum(CertificateType), nullable=False)
    template_used = Column(String(100), nullable=False)
    
    # Processing status
    total_certificates = Column(Integer, default=0, nullable=False)
    processed_count = Column(Integer, default=0, nullable=False)
    successful_count = Column(Integer, default=0, nullable=False)
    failed_count = Column(Integer, default=0, nullable=False)
    
    # Batch configuration
    auto_send_email = Column(Boolean, default=False, nullable=False)
    include_verification = Column(Boolean, default=True, nullable=False)
    custom_message = Column(Text, nullable=True)
    
    # Processing info
    started_by = Column(String(255), nullable=False)
    processing_started = Column(DateTime(timezone=True), nullable=True)
    processing_completed = Column(DateTime(timezone=True), nullable=True)
    estimated_completion = Column(DateTime(timezone=True), nullable=True)
    
    # Error handling
    error_log = Column(Text, nullable=True)
    retry_failed = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    def __repr__(self):
        return f"<CertificateBatch(id={self.id}, name='{self.batch_name}', total={self.total_certificates})>"
