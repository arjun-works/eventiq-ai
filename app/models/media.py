"""
Media and Photo Management Models

This module defines models for handling event photos, media uploads, and metadata.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum

from app.core.database import Base


class MediaType(str, Enum):
    """Media type enumeration"""
    PHOTO = "photo"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"


class MediaStatus(str, Enum):
    """Media status enumeration"""
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    APPROVED = "approved"
    REJECTED = "rejected"
    ARCHIVED = "archived"


class Media(Base):
    """Media files uploaded by volunteers and participants"""
    
    __tablename__ = "media"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # File information
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)  # Size in bytes
    file_extension = Column(String(10), nullable=False)
    mime_type = Column(String(100), nullable=False)
    
    # Media details
    media_type = Column(SQLEnum(MediaType), nullable=False)
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    alt_text = Column(String(255), nullable=True)  # For accessibility
    
    # Upload information
    uploaded_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    uploaded_by_name = Column(String(255), nullable=False)
    upload_source = Column(String(50), nullable=True)  # web, mobile_app, direct
    
    # Location and context
    booth_location = Column(String(255), nullable=True)
    event_area = Column(String(255), nullable=True)
    coordinates_latitude = Column(String(20), nullable=True)
    coordinates_longitude = Column(String(20), nullable=True)
    
    # Timestamp metadata
    photo_taken_timestamp = Column(DateTime(timezone=True), nullable=True)
    upload_timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Camera/device metadata
    camera_make = Column(String(100), nullable=True)
    camera_model = Column(String(100), nullable=True)
    device_info = Column(Text, nullable=True)  # JSON string with device details
    
    # Image-specific metadata (for photos)
    image_width = Column(Integer, nullable=True)
    image_height = Column(Integer, nullable=True)
    resolution_dpi = Column(Integer, nullable=True)
    color_space = Column(String(20), nullable=True)
    has_flash = Column(Boolean, nullable=True)
    iso_speed = Column(Integer, nullable=True)
    exposure_time = Column(String(20), nullable=True)
    focal_length = Column(String(20), nullable=True)
    
    # Content moderation and approval
    status = Column(SQLEnum(MediaStatus), default=MediaStatus.UPLOADED, nullable=False)
    moderation_notes = Column(Text, nullable=True)
    approved_by = Column(String(255), nullable=True)
    approval_date = Column(DateTime(timezone=True), nullable=True)
    
    # Usage and permissions
    is_public = Column(Boolean, default=True, nullable=False)
    allow_commercial_use = Column(Boolean, default=False, nullable=False)
    copyright_holder = Column(String(255), nullable=True)
    usage_rights = Column(String(100), nullable=True)
    
    # Social and engagement
    view_count = Column(Integer, default=0, nullable=False)
    download_count = Column(Integer, default=0, nullable=False)
    like_count = Column(Integer, default=0, nullable=False)
    
    # Processing and thumbnails
    has_thumbnail = Column(Boolean, default=False, nullable=False)
    thumbnail_path = Column(String(500), nullable=True)
    processed_versions = Column(Text, nullable=True)  # JSON list of processed versions
    
    # Tags and categorization
    tags = Column(String(500), nullable=True)  # Comma-separated tags
    auto_generated_tags = Column(String(500), nullable=True)  # AI-generated tags
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    uploader = relationship("User", backref="uploaded_media")
    
    def __repr__(self):
        return f"<Media(id={self.id}, filename='{self.filename}', type='{self.media_type}', status='{self.status}')>"


class MediaCollection(Base):
    """Collections or albums of related media"""
    
    __tablename__ = "media_collections"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Collection details
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    collection_type = Column(String(50), nullable=True)  # booth, event_day, highlights, etc.
    
    # Collection metadata
    created_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_public = Column(Boolean, default=True, nullable=False)
    is_featured = Column(Boolean, default=False, nullable=False)
    
    # Statistics
    media_count = Column(Integer, default=0, nullable=False)
    total_views = Column(Integer, default=0, nullable=False)
    
    # Cover image
    cover_media_id = Column(Integer, nullable=True)  # ID of media to use as cover
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    creator = relationship("User", backref="created_collections")
    
    def __repr__(self):
        return f"<MediaCollection(id={self.id}, name='{self.name}', count={self.media_count})>"


class MediaCollectionItem(Base):
    """Items within media collections"""
    
    __tablename__ = "media_collection_items"
    
    id = Column(Integer, primary_key=True, index=True)
    collection_id = Column(Integer, ForeignKey("media_collections.id"), nullable=False)
    media_id = Column(Integer, ForeignKey("media.id"), nullable=False)
    
    # Item details
    order_index = Column(Integer, nullable=True)  # For ordering within collection
    caption = Column(Text, nullable=True)  # Custom caption for this item in collection
    
    # Timestamps
    added_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    collection = relationship("MediaCollection", backref="items")
    media_item = relationship("Media", backref="in_collections")
    
    def __repr__(self):
        return f"<MediaCollectionItem(collection_id={self.collection_id}, media_id={self.media_id})>"


class MediaDownloadLog(Base):
    """Track media downloads for analytics"""
    
    __tablename__ = "media_download_log"
    
    id = Column(Integer, primary_key=True, index=True)
    media_id = Column(Integer, ForeignKey("media.id"), nullable=False)
    
    # Download details
    downloaded_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Null for anonymous
    download_type = Column(String(20), nullable=False)  # original, thumbnail, processed
    
    # Request information
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    referrer = Column(String(500), nullable=True)
    
    # Download metadata
    file_size_bytes = Column(Integer, nullable=True)
    download_successful = Column(Boolean, default=True, nullable=False)
    
    # Timestamp
    download_timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    media_item = relationship("Media", backref="download_history")
    downloader = relationship("User", backref="media_downloads")
    
    def __repr__(self):
        return f"<MediaDownloadLog(id={self.id}, media_id={self.media_id}, timestamp={self.download_timestamp})>"
