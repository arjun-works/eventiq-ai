"""
Volunteer Management Models

This module defines models for volunteer registration, attendance, and management.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from typing import Dict, List

from app.core.database import Base


class Volunteer(Base):
    """Volunteer registration and profile model"""
    
    __tablename__ = "volunteers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Volunteer-specific information
    skills = Column(JSON, nullable=True)  # List of skills
    available_time_slots = Column(JSON, nullable=True)  # Available time slots
    preferred_roles = Column(JSON, nullable=True)  # Preferred volunteer roles
    experience_level = Column(String(50), nullable=True)  # Beginner, Intermediate, Expert
    emergency_contact = Column(String(255), nullable=True)
    emergency_phone = Column(String(20), nullable=True)
    
    # Assignment information
    assigned_booth = Column(String(100), nullable=True)
    assigned_role = Column(String(100), nullable=True)
    assignment_type = Column(String(20), default="manual")  # manual, auto
    
    # Status
    is_approved = Column(Boolean, default=False, nullable=False)
    is_checked_in = Column(Boolean, default=False, nullable=False)
    total_hours = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    user = relationship("User", backref="volunteer_profile")
    attendance_records = relationship("VolunteerAttendance", back_populates="volunteer")
    
    def __repr__(self):
        return f"<Volunteer(id={self.id}, user_id={self.user_id}, role='{self.assigned_role}')>"


class VolunteerAttendance(Base):
    """Volunteer attendance tracking with QR code check-in/out"""
    
    __tablename__ = "volunteer_attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    volunteer_id = Column(Integer, ForeignKey("volunteers.id"), nullable=False)
    
    # Check-in/out information
    check_in_time = Column(DateTime(timezone=True), nullable=True)
    check_out_time = Column(DateTime(timezone=True), nullable=True)
    qr_code = Column(String(255), unique=True, nullable=False)  # Unique QR code for session
    
    # Location and shift information
    booth_assigned = Column(String(100), nullable=True)
    shift_date = Column(DateTime(timezone=True), nullable=False)
    planned_duration = Column(Integer, nullable=True)  # Planned duration in minutes
    actual_duration = Column(Integer, nullable=True)  # Actual duration in minutes
    
    # Status and notes
    status = Column(String(20), default="scheduled")  # scheduled, active, completed, no_show
    notes = Column(Text, nullable=True)
    supervisor_notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    volunteer = relationship("Volunteer", back_populates="attendance_records")
    
    def __repr__(self):
        return f"<VolunteerAttendance(id={self.id}, volunteer_id={self.volunteer_id}, status='{self.status}')>"


class VolunteerRole(Base):
    """Available volunteer roles and their requirements"""
    
    __tablename__ = "volunteer_roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    required_skills = Column(JSON, nullable=True)  # Required skills for this role
    min_experience_level = Column(String(50), nullable=True)
    max_volunteers_needed = Column(Integer, nullable=True)
    current_volunteers_assigned = Column(Integer, default=0, nullable=False)
    
    # Role configuration
    requires_training = Column(Boolean, default=False, nullable=False)
    is_leadership_role = Column(Boolean, default=False, nullable=False)
    time_commitment_hours = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    def __repr__(self):
        return f"<VolunteerRole(id={self.id}, name='{self.name}', assigned={self.current_volunteers_assigned})>"
