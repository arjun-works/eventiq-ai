"""
Booth and Footfall Tracking Models

This module defines models for booth management and visitor tracking.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Booth(Base):
    """Booth information and configuration"""
    
    __tablename__ = "booths"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    booth_number = Column(String(50), unique=True, nullable=False)
    
    # Location and layout
    location_description = Column(Text, nullable=True)
    floor_level = Column(String(20), nullable=True)
    coordinates_x = Column(Integer, nullable=True)  # For mapping
    coordinates_y = Column(Integer, nullable=True)  # For mapping
    size_sqft = Column(Integer, nullable=True)
    
    # Booth details
    category = Column(String(100), nullable=True)  # Technology, Food, Education, etc.
    description = Column(Text, nullable=True)
    organizer_name = Column(String(255), nullable=True)
    organizer_contact = Column(String(255), nullable=True)
    
    # Capacity and timing
    max_capacity = Column(Integer, nullable=True)
    estimated_visit_duration = Column(Integer, nullable=True)  # In minutes
    operating_hours_start = Column(String(10), nullable=True)  # HH:MM format
    operating_hours_end = Column(String(10), nullable=True)  # HH:MM format
    
    # Features and requirements
    features = Column(JSON, nullable=True)  # List of features/amenities
    requirements = Column(JSON, nullable=True)  # Setup requirements
    special_instructions = Column(Text, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    setup_completed = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    footfall_data = relationship("BoothFootfall", back_populates="booth")
    
    def __repr__(self):
        return f"<Booth(id={self.id}, number='{self.booth_number}', name='{self.name}')>"


class BoothFootfall(Base):
    """IoT-simulated footfall data for booths"""
    
    __tablename__ = "booth_footfall"
    
    id = Column(Integer, primary_key=True, index=True)
    booth_id = Column(Integer, ForeignKey("booths.id"), nullable=False)
    
    # Footfall metrics
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    visitor_count = Column(Integer, default=0, nullable=False)
    entry_count = Column(Integer, default=0, nullable=False)
    exit_count = Column(Integer, default=0, nullable=False)
    current_occupancy = Column(Integer, default=0, nullable=False)
    
    # Time-based grouping
    hour_of_day = Column(Integer, nullable=False)  # 0-23
    day_of_week = Column(Integer, nullable=False)  # 0-6 (Monday=0)
    time_slot = Column(String(20), nullable=True)  # morning, afternoon, evening
    
    # IoT sensor data (simulated)
    sensor_id = Column(String(50), nullable=True)
    raw_data = Column(JSON, nullable=True)  # Raw sensor readings
    data_quality = Column(String(20), default="good", nullable=False)  # good, fair, poor
    
    # Analytics-ready fields
    peak_period = Column(Boolean, default=False, nullable=False)
    crowd_density = Column(String(20), nullable=True)  # low, medium, high, very_high
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    booth = relationship("Booth", back_populates="footfall_data")
    
    def __repr__(self):
        return f"<BoothFootfall(booth_id={self.booth_id}, timestamp={self.timestamp}, count={self.visitor_count})>"


class BoothStats(Base):
    """Aggregated booth statistics and analytics"""
    
    __tablename__ = "booth_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    booth_id = Column(Integer, ForeignKey("booths.id"), nullable=False)
    
    # Date range for statistics
    stats_date = Column(DateTime(timezone=True), nullable=False)
    
    # Daily aggregates
    total_visitors = Column(Integer, default=0, nullable=False)
    unique_visitors = Column(Integer, default=0, nullable=False)
    return_visitors = Column(Integer, default=0, nullable=False)
    average_visit_duration = Column(Integer, default=0, nullable=False)  # Minutes
    
    # Peak metrics
    peak_hour = Column(Integer, nullable=True)  # Hour with most visitors
    peak_occupancy = Column(Integer, default=0, nullable=False)
    peak_timestamp = Column(DateTime(timezone=True), nullable=True)
    
    # Engagement metrics
    total_interactions = Column(Integer, default=0, nullable=False)
    average_rating = Column(Integer, nullable=True)  # From participant feedback
    recommendation_rate = Column(Integer, default=0, nullable=False)  # Percentage
    
    # Operational metrics
    uptime_percentage = Column(Integer, default=100, nullable=False)
    technical_issues = Column(Integer, default=0, nullable=False)
    staff_efficiency_score = Column(Integer, nullable=True)  # 1-100
    
    # Rankings and comparisons
    popularity_rank = Column(Integer, nullable=True)  # Rank among all booths
    category_rank = Column(Integer, nullable=True)  # Rank within category
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    booth = relationship("Booth", backref="daily_stats")
    
    def __repr__(self):
        return f"<BoothStats(booth_id={self.booth_id}, date={self.stats_date}, visitors={self.total_visitors})>"
