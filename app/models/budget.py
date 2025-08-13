"""
Budget and Finance Models

This module defines models for budget estimation, expense tracking, and financial management.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Numeric, Enum as SQLEnum
from sqlalchemy.sql import func
from decimal import Decimal
from enum import Enum

from app.core.database import Base


class BudgetCategory(str, Enum):
    """Budget category enumeration"""
    FOOD = "food"
    BANNERS = "banners"
    TRANSPORT = "transport"
    EQUIPMENT = "equipment"
    VENUE = "venue"
    MARKETING = "marketing"
    STAFF = "staff"
    UTILITIES = "utilities"
    SECURITY = "security"
    MISCELLANEOUS = "miscellaneous"


class BudgetStatus(str, Enum):
    """Budget status enumeration"""
    DRAFT = "draft"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class BudgetEstimate(Base):
    """Budget estimation for different categories"""
    
    __tablename__ = "budget_estimates"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(SQLEnum(BudgetCategory), nullable=False)
    
    # Budget details
    item_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    estimated_cost = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    
    # Vendor information
    preferred_vendor = Column(String(255), nullable=True)
    vendor_contact = Column(String(255), nullable=True)
    quote_reference = Column(String(100), nullable=True)
    
    # Status and approval
    status = Column(SQLEnum(BudgetStatus), default=BudgetStatus.DRAFT, nullable=False)
    is_approved = Column(Boolean, default=False, nullable=False)
    approved_by = Column(String(255), nullable=True)
    approval_date = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    def __repr__(self):
        return f"<BudgetEstimate(id={self.id}, category='{self.category}', item='{self.item_name}', cost={self.estimated_cost})>"


class Expense(Base):
    """Actual expenses and bills for budget items"""
    
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    budget_estimate_id = Column(Integer, nullable=True)  # Link to budget estimate if exists
    category = Column(SQLEnum(BudgetCategory), nullable=False)
    
    # Expense details
    vendor_name = Column(String(255), nullable=False)
    item_description = Column(Text, nullable=False)
    actual_cost = Column(Numeric(10, 2), nullable=False)
    quantity_purchased = Column(Integer, default=1, nullable=False)
    unit_cost = Column(Numeric(10, 2), nullable=False)
    
    # Payment information
    payment_method = Column(String(50), nullable=True)  # cash, card, transfer, etc.
    invoice_number = Column(String(100), nullable=True)
    receipt_number = Column(String(100), nullable=True)
    payment_date = Column(DateTime(timezone=True), nullable=True)
    
    # Variance tracking
    estimated_cost = Column(Numeric(10, 2), nullable=True)  # For comparison
    variance_amount = Column(Numeric(10, 2), nullable=True)  # Actual - Estimated
    variance_percentage = Column(Numeric(5, 2), nullable=True)  # Variance as percentage
    is_high_variance = Column(Boolean, default=False, nullable=False)  # Auto-flagged if >20%
    
    # Status and approval
    is_approved = Column(Boolean, default=False, nullable=False)
    approved_by = Column(String(255), nullable=True)
    approval_date = Column(DateTime(timezone=True), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    def __repr__(self):
        return f"<Expense(id={self.id}, vendor='{self.vendor_name}', cost={self.actual_cost}, variance={self.variance_percentage}%)>"


class BudgetSummary(Base):
    """Aggregate budget summary and analytics"""
    
    __tablename__ = "budget_summary"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Summary by category
    category = Column(SQLEnum(BudgetCategory), nullable=False)
    total_estimated = Column(Numeric(10, 2), default=0, nullable=False)
    total_actual = Column(Numeric(10, 2), default=0, nullable=False)
    total_variance = Column(Numeric(10, 2), default=0, nullable=False)
    variance_percentage = Column(Numeric(5, 2), default=0, nullable=False)
    
    # Item counts
    estimated_items_count = Column(Integer, default=0, nullable=False)
    actual_expenses_count = Column(Integer, default=0, nullable=False)
    high_variance_items = Column(Integer, default=0, nullable=False)
    
    # Status tracking
    items_pending_approval = Column(Integer, default=0, nullable=False)
    items_approved = Column(Integer, default=0, nullable=False)
    
    # Date range for summary
    summary_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_updated = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    def __repr__(self):
        return f"<BudgetSummary(category='{self.category}', estimated={self.total_estimated}, actual={self.total_actual})>"
