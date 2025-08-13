"""
Vendor and Asset Management Models

This module defines models for vendor information, interactions, and asset tracking.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, Enum as SQLEnum
from sqlalchemy.sql import func
from enum import Enum

from app.core.database import Base


class VendorStatus(str, Enum):
    """Vendor status enumeration"""
    PENDING = "pending"
    APPROVED = "approved"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    BLACKLISTED = "blacklisted"


class InteractionType(str, Enum):
    """Vendor interaction type enumeration"""
    INITIAL_CONTACT = "initial_contact"
    QUOTE_REQUEST = "quote_request"
    QUOTE_RECEIVED = "quote_received"
    NEGOTIATION = "negotiation"
    CONTRACT_SIGNED = "contract_signed"
    DELIVERY = "delivery"
    PAYMENT = "payment"
    FOLLOW_UP = "follow_up"
    COMPLAINT = "complaint"
    RESOLUTION = "resolution"


class Vendor(Base):
    """Vendor information and profile"""
    
    __tablename__ = "vendors"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic information
    name = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=True)
    contact_person = Column(String(255), nullable=True)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    
    # Address and location
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    zip_code = Column(String(20), nullable=True)
    country = Column(String(100), nullable=True)
    
    # Business details
    business_type = Column(String(100), nullable=True)
    services_offered = Column(JSON, nullable=True)  # List of services
    specializations = Column(JSON, nullable=True)  # Areas of expertise
    years_in_business = Column(Integer, nullable=True)
    
    # Event-specific information
    purpose = Column(String(255), nullable=True)  # Purpose for this event
    materials_brought = Column(JSON, nullable=True)  # List of materials/equipment
    setup_requirements = Column(Text, nullable=True)
    special_instructions = Column(Text, nullable=True)
    
    # Financial information
    payment_terms = Column(String(100), nullable=True)
    credit_limit = Column(Integer, nullable=True)
    tax_id = Column(String(50), nullable=True)
    
    # Status and ratings
    status = Column(SQLEnum(VendorStatus), default=VendorStatus.PENDING, nullable=False)
    rating = Column(Integer, nullable=True)  # 1-5 scale
    reliability_score = Column(Integer, nullable=True)  # 1-100
    is_preferred = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    last_contact_date = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Vendor(id={self.id}, name='{self.name}', status='{self.status}')>"


class VendorInteraction(Base):
    """CRM-like vendor interaction tracking"""
    
    __tablename__ = "vendor_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, nullable=False)  # Foreign key to vendors
    
    # Interaction details
    interaction_type = Column(SQLEnum(InteractionType), nullable=False)
    subject = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Communication details
    communication_method = Column(String(50), nullable=True)  # email, phone, in_person
    initiated_by = Column(String(255), nullable=True)  # Who started the interaction
    contact_person = Column(String(255), nullable=True)  # Vendor contact person
    
    # Follow-up and status
    follow_up_required = Column(Boolean, default=False, nullable=False)
    follow_up_date = Column(DateTime(timezone=True), nullable=True)
    priority = Column(String(20), default="medium", nullable=False)  # low, medium, high, urgent
    status = Column(String(50), default="open", nullable=False)  # open, in_progress, closed
    
    # Outcomes and results
    outcome = Column(Text, nullable=True)
    action_items = Column(JSON, nullable=True)  # List of action items
    attachments = Column(JSON, nullable=True)  # List of file paths/URLs
    
    # Financial impact
    estimated_value = Column(Integer, nullable=True)
    actual_value = Column(Integer, nullable=True)
    
    # Timestamps
    interaction_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    def __repr__(self):
        return f"<VendorInteraction(id={self.id}, vendor_id={self.vendor_id}, type='{self.interaction_type}')>"


class VendorAsset(Base):
    """Assets and materials provided by vendors"""
    
    __tablename__ = "vendor_assets"
    
    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, nullable=False)  # Foreign key to vendors
    
    # Asset information
    asset_name = Column(String(255), nullable=False)
    asset_type = Column(String(100), nullable=True)  # equipment, material, service
    description = Column(Text, nullable=True)
    model_number = Column(String(100), nullable=True)
    serial_number = Column(String(100), nullable=True)
    
    # Quantity and specifications
    quantity = Column(Integer, default=1, nullable=False)
    unit_of_measure = Column(String(50), nullable=True)
    specifications = Column(JSON, nullable=True)  # Technical specifications
    
    # Location and status
    current_location = Column(String(255), nullable=True)
    condition = Column(String(50), nullable=True)  # excellent, good, fair, poor
    status = Column(String(50), default="available", nullable=False)  # available, in_use, maintenance, retired
    
    # Dates and tracking
    delivery_date = Column(DateTime(timezone=True), nullable=True)
    pickup_date = Column(DateTime(timezone=True), nullable=True)
    last_inspection_date = Column(DateTime(timezone=True), nullable=True)
    
    # Value and insurance
    purchase_value = Column(Integer, nullable=True)
    current_value = Column(Integer, nullable=True)
    is_insured = Column(Boolean, default=False, nullable=False)
    insurance_value = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    def __repr__(self):
        return f"<VendorAsset(id={self.id}, name='{self.asset_name}', vendor_id={self.vendor_id})>"
