"""
Participant Management Models

This module defines models for participant registration and tracking.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Participant(Base):
    """Participant registration and profile model"""
    
    __tablename__ = "participants"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Registration information
    registration_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    registration_source = Column(String(50), nullable=True)  # online, offline, referral
    ticket_number = Column(String(50), unique=True, nullable=False)
    
    # Participant details
    age_group = Column(String(20), nullable=True)  # 18-25, 26-35, etc.
    interests = Column(JSON, nullable=True)  # List of interests
    dietary_restrictions = Column(JSON, nullable=True)  # List of dietary restrictions
    accessibility_needs = Column(Text, nullable=True)
    
    # Event preferences
    preferred_booths = Column(JSON, nullable=True)  # List of preferred booth IDs
    preferred_time_slots = Column(JSON, nullable=True)  # Preferred attendance times
    notification_preferences = Column(JSON, nullable=True)  # Email, SMS, etc.
    
    # Status
    is_confirmed = Column(Boolean, default=False, nullable=False)
    has_attended = Column(Boolean, default=False, nullable=False)
    check_in_time = Column(DateTime(timezone=True), nullable=True)
    check_out_time = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    user = relationship("User", backref="participant_profile")
    booth_visits = relationship("ParticipantBoothVisit", back_populates="participant")
    
    def __repr__(self):
        return f"<Participant(id={self.id}, ticket='{self.ticket_number}', confirmed={self.is_confirmed})>"


class ParticipantBoothVisit(Base):
    """Track participant visits to different booths"""
    
    __tablename__ = "participant_booth_visits"
    
    id = Column(Integer, primary_key=True, index=True)
    participant_id = Column(Integer, ForeignKey("participants.id"), nullable=False)
    booth_id = Column(Integer, ForeignKey("booths.id"), nullable=False)
    
    # Visit information
    visit_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    duration_minutes = Column(Integer, nullable=True)
    interaction_type = Column(String(50), nullable=True)  # demo, consultation, information
    
    # Feedback and rating
    rating = Column(Integer, nullable=True)  # 1-5 scale
    feedback = Column(Text, nullable=True)
    would_recommend = Column(Boolean, nullable=True)
    
    # Status
    completed = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    participant = relationship("Participant", back_populates="booth_visits")
    booth = relationship("Booth", backref="participant_visits")
    
    def __repr__(self):
        return f"<ParticipantBoothVisit(id={self.id}, participant_id={self.participant_id}, booth_id={self.booth_id})>"


class ParticipantStats(Base):
    """Aggregate statistics for participants"""
    
    __tablename__ = "participant_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Daily stats
    date = Column(DateTime(timezone=True), nullable=False)
    total_registered = Column(Integer, default=0, nullable=False)
    total_confirmed = Column(Integer, default=0, nullable=False)
    total_attended = Column(Integer, default=0, nullable=False)
    total_no_shows = Column(Integer, default=0, nullable=False)
    
    # Demographics
    age_group_breakdown = Column(JSON, nullable=True)  # Distribution by age group
    registration_source_breakdown = Column(JSON, nullable=True)  # Distribution by source
    
    # Engagement metrics
    average_booth_visits = Column(Integer, default=0, nullable=False)
    average_duration_minutes = Column(Integer, default=0, nullable=False)
    peak_attendance_hour = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    def __repr__(self):
        return f"<ParticipantStats(date={self.date}, registered={self.total_registered}, attended={self.total_attended})>"
