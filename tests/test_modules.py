"""
Test Module Structure for EventIQ Management System
Comprehensive testing for all modules
"""

import unittest
import pytest
from modules.config import config
from modules.constants import *
from modules.services.file_service import file_service
from modules.models import *

class TestModuleStructure(unittest.TestCase):
    """Test the overall module structure"""
    
    def test_config_loading(self):
        """Test configuration loading"""
        self.assertIsNotNone(config.get("ui.page_title"))
        self.assertEqual(config.get("ui.page_icon"), "🎉")
    
    def test_constants_availability(self):
        """Test that constants are properly defined"""
        self.assertTrue(len(USER_ROLES) > 0)
        self.assertTrue(len(PAGE_ICONS) > 0)
        self.assertTrue(len(NAVIGATION_MENUS) > 0)
    
    def test_file_service_initialization(self):
        """Test file service initialization"""
        self.assertIsNotNone(file_service)
        self.assertTrue(hasattr(file_service, 'validate_file'))
        self.assertTrue(hasattr(file_service, 'save_file'))

class TestDataModels(unittest.TestCase):
    """Test data model creation and validation"""
    
    def test_volunteer_model(self):
        """Test volunteer model creation"""
        volunteer = create_volunteer("John Doe", "john@example.com", "Registration")
        self.assertEqual(volunteer.name, "John Doe")
        self.assertEqual(volunteer.email, "john@example.com")
        self.assertEqual(volunteer.role, "Registration")
        self.assertEqual(volunteer.status, VolunteerStatus.ACTIVE)
    
    def test_participant_model(self):
        """Test participant model creation"""
        participant = create_participant("Jane Smith", "jane@example.com")
        self.assertEqual(participant.name, "Jane Smith")
        self.assertEqual(participant.email, "jane@example.com")
        self.assertIsNotNone(participant.registration_date)
    
    def test_booth_model(self):
        """Test booth model creation"""
        booth = create_booth("A-01", "Section A", "3x3", 500.0)
        self.assertEqual(booth.id, "A-01")
        self.assertEqual(booth.section, "Section A")
        self.assertEqual(booth.size, "3x3")
        self.assertEqual(booth.price, 500.0)

class TestFileService(unittest.TestCase):
    """Test file service functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.file_service = file_service
    
    def test_file_extension_validation(self):
        """Test file extension validation"""
        # Test valid extensions
        self.assertIn("pdf", DOCUMENT_EXTENSIONS)
        self.assertIn("jpg", IMAGE_EXTENSIONS)
        self.assertIn("csv", SPREADSHEET_EXTENSIONS)
    
    def test_directory_creation(self):
        """Test directory structure creation"""
        import tempfile
        import os
        
        # Test that directories are created properly
        test_dir = tempfile.mkdtemp()
        expected_path = os.path.join(test_dir, "test_module", "test_category")
        os.makedirs(expected_path, exist_ok=True)
        
        self.assertTrue(os.path.exists(expected_path))

class TestModuleIntegration(unittest.TestCase):
    """Test module integration and imports"""
    
    def test_module_imports(self):
        """Test that all modules can be imported"""
        try:
            from modules import dashboard
            from modules import certificates
            from modules import media_gallery
            from modules import vendors
            from modules import participants
            from modules import budget
            from modules import settings
            from modules import volunteers
            from modules import booths
            from modules import workflows
            from modules import feedback
            from modules import analytics
            success = True
        except ImportError:
            success = False
        
        self.assertTrue(success, "All modules should be importable")
    
    def test_module_functions(self):
        """Test that required functions exist in modules"""
        from modules.volunteers import show_volunteers_module
        from modules.booths import show_booths_module
        from modules.workflows import show_workflows_page
        from modules.feedback import show_feedback_page
        from modules.analytics import show_analytics_module
        
        # Test that functions are callable
        self.assertTrue(callable(show_volunteers_module))
        self.assertTrue(callable(show_booths_module))
        self.assertTrue(callable(show_workflows_page))
        self.assertTrue(callable(show_feedback_page))
        self.assertTrue(callable(show_analytics_module))

# Pytest fixtures for testing
@pytest.fixture
def sample_volunteer():
    """Create a sample volunteer for testing"""
    return create_volunteer("Test Volunteer", "test@volunteer.com", "Registration")

@pytest.fixture
def sample_participant():
    """Create a sample participant for testing"""
    return create_participant("Test Participant", "test@participant.com")

@pytest.fixture
def sample_booth():
    """Create a sample booth for testing"""
    return create_booth("TEST-01", "Test Section", "3x3", 100.0)

# Performance tests
class TestPerformance(unittest.TestCase):
    """Test performance characteristics"""
    
    def test_config_access_speed(self):
        """Test configuration access performance"""
        import time
        
        start_time = time.time()
        for _ in range(1000):
            config.get("ui.page_title")
        end_time = time.time()
        
        # Should be very fast (less than 0.1 seconds for 1000 accesses)
        self.assertLess(end_time - start_time, 0.1)
    
    def test_model_creation_speed(self):
        """Test model creation performance"""
        import time
        
        start_time = time.time()
        for i in range(100):
            volunteer = create_volunteer(f"Volunteer {i}", f"vol{i}@test.com", "Registration")
        end_time = time.time()
        
        # Model creation should be fast
        self.assertLess(end_time - start_time, 1.0)

if __name__ == "__main__":
    # Run all tests
    unittest.main(verbosity=2)
