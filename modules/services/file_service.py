"""
File Service for EventIQ Management System
Centralized file handling and validation
"""

import os
import uuid
import mimetypes
from datetime import datetime
from typing import Optional, Dict, Any, List
from modules.config import config
from modules.constants import *
from modules.models import FileUpload

class FileService:
    """Service for handling file operations"""
    
    def __init__(self):
        self.upload_base_dir = config.get("file_upload.upload_directory", "uploads")
        self.max_file_size = config.get("file_upload.max_file_size_mb", 10) * 1024 * 1024
        
    def validate_file(self, file, category: str = "document") -> Dict[str, Any]:
        """
        Validate uploaded file
        Returns: dict with validation results
        """
        validation_result = {
            "is_valid": True,
            "errors": [],
            "file_info": {}
        }
        
        if not file:
            validation_result["is_valid"] = False
            validation_result["errors"].append("No file provided")
            return validation_result
        
        # Check file size
        if hasattr(file, 'size') and file.size > self.max_file_size:
            validation_result["is_valid"] = False
            validation_result["errors"].append(f"File size ({file.size} bytes) exceeds maximum allowed size ({self.max_file_size} bytes)")
        
        # Check file type
        file_extension = file.name.split('.')[-1].lower() if '.' in file.name else ""
        allowed_extensions = self._get_allowed_extensions(category)
        
        if file_extension not in allowed_extensions:
            validation_result["is_valid"] = False
            validation_result["errors"].append(f"File type '{file_extension}' not allowed for category '{category}'")
        
        # Get file info
        validation_result["file_info"] = {
            "name": file.name,
            "size": getattr(file, 'size', 0),
            "type": file.type if hasattr(file, 'type') else mimetypes.guess_type(file.name)[0],
            "extension": file_extension
        }
        
        return validation_result
    
    def save_file(self, file, module: str, category: str, custom_name: Optional[str] = None) -> FileUpload:
        """
        Save uploaded file to organized directory structure
        Returns: FileUpload model with file details
        """
        # Validate file first
        validation = self.validate_file(file, category)
        
        if not validation["is_valid"]:
            return FileUpload(
                file_name=file.name,
                is_valid=False,
                error_message="; ".join(validation["errors"])
            )
        
        # Generate unique filename
        file_extension = validation["file_info"]["extension"]
        unique_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if custom_name:
            safe_name = self._sanitize_filename(custom_name)
            filename = f"{timestamp}_{safe_name}_{unique_id}.{file_extension}"
        else:
            safe_name = self._sanitize_filename(file.name.rsplit('.', 1)[0])
            filename = f"{timestamp}_{safe_name}_{unique_id}.{file_extension}"
        
        # Create directory structure
        save_dir = os.path.join(self.upload_base_dir, module, category)
        os.makedirs(save_dir, exist_ok=True)
        
        # Save file
        file_path = os.path.join(save_dir, filename)
        
        try:
            with open(file_path, "wb") as f:
                if hasattr(file, 'read'):
                    f.write(file.read())
                else:
                    f.write(file.getvalue())
            
            return FileUpload(
                file_name=filename,
                file_path=file_path,
                file_size=validation["file_info"]["size"],
                file_type=validation["file_info"]["type"],
                upload_date=datetime.now(),
                module=module,
                category=category,
                is_valid=True
            )
            
        except Exception as e:
            return FileUpload(
                file_name=file.name,
                is_valid=False,
                error_message=f"Failed to save file: {str(e)}"
            )
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get information about a saved file"""
        if not os.path.exists(file_path):
            return {"exists": False, "error": "File not found"}
        
        file_stats = os.stat(file_path)
        return {
            "exists": True,
            "name": os.path.basename(file_path),
            "size": file_stats.st_size,
            "size_mb": round(file_stats.st_size / (1024 * 1024), 2),
            "created": datetime.fromtimestamp(file_stats.st_ctime),
            "modified": datetime.fromtimestamp(file_stats.st_mtime),
            "extension": os.path.splitext(file_path)[1][1:].lower()
        }
    
    def delete_file(self, file_path: str) -> bool:
        """Delete a file safely"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception:
            return False
    
    def list_files(self, module: str, category: str) -> List[Dict[str, Any]]:
        """List all files in a module category"""
        directory = os.path.join(self.upload_base_dir, module, category)
        files = []
        
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    file_info = self.get_file_info(file_path)
                    files.append(file_info)
        
        return files
    
    def cleanup_old_files(self, days_old: int = 30) -> int:
        """Clean up files older than specified days"""
        cleaned_count = 0
        cutoff_time = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
        
        for root, dirs, files in os.walk(self.upload_base_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.getmtime(file_path) < cutoff_time:
                    if self.delete_file(file_path):
                        cleaned_count += 1
        
        return cleaned_count
    
    def _get_allowed_extensions(self, category: str) -> List[str]:
        """Get allowed file extensions for category"""
        extension_map = {
            "image": IMAGE_EXTENSIONS,
            "document": DOCUMENT_EXTENSIONS,
            "spreadsheet": SPREADSHEET_EXTENSIONS,
            "presentation": PRESENTATION_EXTENSIONS,
            "archive": ARCHIVE_EXTENSIONS,
            "cad": CAD_EXTENSIONS,
            "video": VIDEO_EXTENSIONS,
            "audio": AUDIO_EXTENSIONS
        }
        
        return extension_map.get(category, DOCUMENT_EXTENSIONS)
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to remove invalid characters"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename[:50]  # Limit length

# Global file service instance
file_service = FileService()
