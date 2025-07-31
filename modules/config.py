"""
Configuration Management Module for EventIQ Management System
Centralized configuration for all modules
"""

import os
from typing import Dict, Any
import json

class EventIQConfig:
    """Centralized configuration management"""
    
    def __init__(self):
        self.config = self._load_default_config()
        self._load_environment_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration settings"""
        return {
            # File Upload Settings
            "file_upload": {
                "max_file_size_mb": 10,
                "allowed_image_types": ["jpg", "jpeg", "png", "gif"],
                "allowed_document_types": ["pdf", "doc", "docx", "txt"],
                "allowed_spreadsheet_types": ["csv", "xlsx", "xls"],
                "upload_directory": "uploads"
            },
            
            # UI Settings
            "ui": {
                "page_title": "EventIQ Management System",
                "page_icon": "🎉",
                "layout": "wide",
                "sidebar_state": "expanded",
                "theme": "light"
            },
            
            # Module Settings
            "modules": {
                "certificates": {
                    "enabled": True,
                    "max_bulk_generation": 100
                },
                "media_gallery": {
                    "enabled": True,
                    "max_images_per_upload": 10
                },
                "vendors": {
                    "enabled": True,
                    "require_documents": True
                },
                "participants": {
                    "enabled": True,
                    "max_bulk_import": 1000
                },
                "budget": {
                    "enabled": True,
                    "currency": "USD"
                },
                "volunteers": {
                    "enabled": True,
                    "require_background_check": False
                },
                "booths": {
                    "enabled": True,
                    "default_booth_size": "3x3"
                },
                "workflows": {
                    "enabled": True,
                    "max_workflow_steps": 20
                },
                "feedback": {
                    "enabled": True,
                    "allow_anonymous": True
                },
                "analytics": {
                    "enabled": True,
                    "real_time_refresh": 30
                }
            },
            
            # Security Settings
            "security": {
                "session_timeout_minutes": 60,
                "require_email_verification": True,
                "password_min_length": 8
            },
            
            # API Settings
            "api": {
                "base_url": "http://localhost:8000",
                "timeout_seconds": 30,
                "retry_attempts": 3
            },
            
            # Demo Settings
            "demo": {
                "enabled": True,
                "auto_populate_data": True,
                "demo_accounts": {
                    "organizer@eventiq.com": {
                        "password": "organizer123",
                        "role": "organizer",
                        "name": "Event Organizer"
                    },
                    "volunteer@eventiq.com": {
                        "password": "volunteer123",
                        "role": "volunteer",
                        "name": "Volunteer User"
                    },
                    "participant@eventiq.com": {
                        "password": "participant123",
                        "role": "participant",
                        "name": "Participant User"
                    },
                    "vendor@eventiq.com": {
                        "password": "vendor123",
                        "role": "vendor",
                        "name": "Vendor User"
                    },
                    "admin@eventiq.com": {
                        "password": "admin123",
                        "role": "admin",
                        "name": "System Admin"
                    }
                }
            }
        }
    
    def _load_environment_config(self):
        """Load configuration from environment variables"""
        # Override with environment variables if they exist
        if os.getenv("EVENTIQ_API_URL"):
            self.config["api"]["base_url"] = os.getenv("EVENTIQ_API_URL")
        
        if os.getenv("EVENTIQ_UPLOAD_DIR"):
            self.config["file_upload"]["upload_directory"] = os.getenv("EVENTIQ_UPLOAD_DIR")
        
        if os.getenv("EVENTIQ_MAX_FILE_SIZE"):
            self.config["file_upload"]["max_file_size_mb"] = int(os.getenv("EVENTIQ_MAX_FILE_SIZE"))
    
    def get(self, key_path: str, default=None) -> Any:
        """
        Get configuration value using dot notation
        Example: config.get("file_upload.max_file_size_mb")
        """
        keys = key_path.split(".")
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any):
        """
        Set configuration value using dot notation
        Example: config.set("file_upload.max_file_size_mb", 20)
        """
        keys = key_path.split(".")
        target = self.config
        
        for key in keys[:-1]:
            if key not in target:
                target[key] = {}
            target = target[key]
        
        target[keys[-1]] = value
    
    def is_module_enabled(self, module_name: str) -> bool:
        """Check if a module is enabled"""
        return self.get(f"modules.{module_name}.enabled", True)
    
    def get_demo_accounts(self) -> Dict[str, Dict[str, str]]:
        """Get demo accounts configuration"""
        return self.get("demo.demo_accounts", {})
    
    def get_file_upload_config(self) -> Dict[str, Any]:
        """Get file upload configuration"""
        return self.get("file_upload", {})
    
    def save_config(self, file_path: str = "config/eventiq_config.json"):
        """Save current configuration to file"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def load_config(self, file_path: str = "config/eventiq_config.json"):
        """Load configuration from file"""
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                file_config = json.load(f)
                self._merge_config(self.config, file_config)
    
    def _merge_config(self, base: dict, override: dict):
        """Recursively merge configuration dictionaries"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value

# Global configuration instance
config = EventIQConfig()

# Configuration validation functions
def validate_file_type(file_name: str, category: str) -> bool:
    """Validate if file type is allowed for the given category"""
    allowed_types = []
    
    if category == "image":
        allowed_types = config.get("file_upload.allowed_image_types", [])
    elif category == "document":
        allowed_types = config.get("file_upload.allowed_document_types", [])
    elif category == "spreadsheet":
        allowed_types = config.get("file_upload.allowed_spreadsheet_types", [])
    
    file_extension = file_name.split('.')[-1].lower()
    return file_extension in allowed_types

def validate_file_size(file_size_bytes: int) -> bool:
    """Validate if file size is within allowed limits"""
    max_size_mb = config.get("file_upload.max_file_size_mb", 10)
    max_size_bytes = max_size_mb * 1024 * 1024
    return file_size_bytes <= max_size_bytes

def get_upload_directory() -> str:
    """Get the configured upload directory"""
    return config.get("file_upload.upload_directory", "uploads")
