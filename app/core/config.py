"""
Core Configuration Module

This module handles all application configuration using environment variables.
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    PROJECT_NAME: str = "EventIQ"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-super-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Environment
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str = "sqlite:///./eventiq.db"
    
    # AI/ML API Keys
    OPENAI_API_KEY: Optional[str] = None
    HUGGINGFACE_API_KEY: Optional[str] = None
    OPENROUTER_API_KEY: Optional[str] = None
    
    # Email Configuration
    SENDGRID_API_KEY: Optional[str] = None
    FROM_EMAIL: str = "noreply@eventiq.com"
    
    # External Integrations
    SALESFORCE_CLIENT_ID: Optional[str] = None
    SALESFORCE_CLIENT_SECRET: Optional[str] = None
    SALESFORCE_USERNAME: Optional[str] = None
    SALESFORCE_PASSWORD: Optional[str] = None
    SALESFORCE_SECURITY_TOKEN: Optional[str] = None
    
    PEGA_API_URL: Optional[str] = None
    PEGA_API_KEY: Optional[str] = None
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # File Upload Settings
    MAX_FILE_SIZE: int = 10485760  # 10MB
    UPLOAD_FOLDER: str = "./uploads"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/eventiq.log"
    
    # Frontend Settings
    STREAMLIT_SERVER_PORT: int = 8501
    STREAMLIT_SERVER_ADDRESS: str = "localhost"
    
    # QR Code Settings
    QR_CODE_SIZE: int = 10
    QR_CODE_BORDER: int = 4
    
    # Certificate Settings
    CERTIFICATE_TEMPLATE_PATH: str = "templates/certificate_template.html"
    CERTIFICATE_OUTPUT_PATH: str = "certificates/"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()

# Ensure required directories exist
os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(settings.CERTIFICATE_OUTPUT_PATH, exist_ok=True)
os.makedirs("logs", exist_ok=True)
