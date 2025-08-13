"""
Feedback Collection Models

This module defines models for participant and volunteer feedback with AI sentiment analysis.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum

from app.core.database import Base


class FeedbackType(str, Enum):
    """Feedback type enumeration"""
    PARTICIPANT = "participant"
    VOLUNTEER = "volunteer"
    ORGANIZER = "organizer"
    VENDOR = "vendor"


class SentimentScore(str, Enum):
    """Sentiment analysis score enumeration"""
    VERY_POSITIVE = "very_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very_negative"


class Feedback(Base):
    """Main feedback collection table"""
    
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Feedback source
    feedback_type = Column(SQLEnum(FeedbackType), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Optional for anonymous feedback
    
    # Feedback content
    overall_rating = Column(Integer, nullable=False)  # 1-5 scale
    title = Column(String(255), nullable=True)
    detailed_feedback = Column(Text, nullable=False)
    
    # Specific ratings
    event_organization_rating = Column(Integer, nullable=True)  # 1-5 scale
    venue_rating = Column(Integer, nullable=True)  # 1-5 scale
    staff_helpfulness_rating = Column(Integer, nullable=True)  # 1-5 scale
    value_for_time_rating = Column(Integer, nullable=True)  # 1-5 scale
    
    # Additional context
    booth_visited = Column(String(255), nullable=True)
    session_attended = Column(String(255), nullable=True)
    improvement_suggestions = Column(Text, nullable=True)
    would_recommend = Column(Boolean, nullable=True)
    would_attend_again = Column(Boolean, nullable=True)
    
    # AI Sentiment Analysis
    sentiment_score = Column(SQLEnum(SentimentScore), nullable=True)
    sentiment_confidence = Column(Integer, nullable=True)  # 0-100 confidence percentage
    ai_processed = Column(Boolean, default=False, nullable=False)
    ai_processing_date = Column(DateTime(timezone=True), nullable=True)
    
    # Key phrases and topics (AI extracted)
    key_phrases = Column(Text, nullable=True)  # JSON string of key phrases
    topics_mentioned = Column(Text, nullable=True)  # JSON string of topics
    emotion_analysis = Column(Text, nullable=True)  # JSON string of emotions detected
    
    # Metadata
    submission_method = Column(String(50), nullable=True)  # web_form, mobile_app, paper
    is_anonymous = Column(Boolean, default=False, nullable=False)
    contact_for_followup = Column(Boolean, default=False, nullable=False)
    
    # Status and follow-up
    is_reviewed = Column(Boolean, default=False, nullable=False)
    requires_action = Column(Boolean, default=False, nullable=False)
    action_taken = Column(Text, nullable=True)
    reviewed_by = Column(String(255), nullable=True)
    review_date = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    user = relationship("User", backref="feedback_given")
    
    def __repr__(self):
        return f"<Feedback(id={self.id}, type='{self.feedback_type}', rating={self.overall_rating}, sentiment='{self.sentiment_score}')>"


class FeedbackCategory(Base):
    """Feedback categorization for better analysis"""
    
    __tablename__ = "feedback_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    feedback_id = Column(Integer, ForeignKey("feedback.id"), nullable=False)
    
    # Category information
    category_name = Column(String(100), nullable=False)  # venue, food, staff, organization, etc.
    subcategory = Column(String(100), nullable=True)  # More specific categorization
    confidence_score = Column(Integer, nullable=True)  # AI confidence in categorization
    
    # Auto-assigned vs manual
    is_auto_assigned = Column(Boolean, default=True, nullable=False)
    assigned_by = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    feedback = relationship("Feedback", backref="categories")
    
    def __repr__(self):
        return f"<FeedbackCategory(feedback_id={self.feedback_id}, category='{self.category_name}')>"


class FeedbackSummary(Base):
    """Aggregated feedback statistics and insights"""
    
    __tablename__ = "feedback_summary"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Summary period
    summary_date = Column(DateTime(timezone=True), nullable=False)
    feedback_type = Column(SQLEnum(FeedbackType), nullable=False)
    
    # Response metrics
    total_responses = Column(Integer, default=0, nullable=False)
    response_rate = Column(Integer, nullable=True)  # Percentage
    average_rating = Column(Integer, nullable=True)  # Average overall rating
    
    # Rating distribution
    rating_1_count = Column(Integer, default=0, nullable=False)
    rating_2_count = Column(Integer, default=0, nullable=False)
    rating_3_count = Column(Integer, default=0, nullable=False)
    rating_4_count = Column(Integer, default=0, nullable=False)
    rating_5_count = Column(Integer, default=0, nullable=False)
    
    # Sentiment distribution
    very_positive_count = Column(Integer, default=0, nullable=False)
    positive_count = Column(Integer, default=0, nullable=False)
    neutral_count = Column(Integer, default=0, nullable=False)
    negative_count = Column(Integer, default=0, nullable=False)
    very_negative_count = Column(Integer, default=0, nullable=False)
    
    # Engagement metrics
    would_recommend_percentage = Column(Integer, nullable=True)
    would_attend_again_percentage = Column(Integer, nullable=True)
    contact_for_followup_count = Column(Integer, default=0, nullable=False)
    
    # Top issues and praise
    most_mentioned_issues = Column(Text, nullable=True)  # JSON string
    most_mentioned_positives = Column(Text, nullable=True)  # JSON string
    trending_topics = Column(Text, nullable=True)  # JSON string
    
    # Action items
    requires_immediate_attention = Column(Integer, default=0, nullable=False)
    actionable_feedback_count = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    def __repr__(self):
        return f"<FeedbackSummary(date={self.summary_date}, type='{self.feedback_type}', total={self.total_responses})>"
