"""
Data Models for EventIQ Management System
Type-safe data structures for all modules
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime
from modules.constants import UserRole, VolunteerStatus, BoothStatus, WorkflowStatus, FeedbackType

@dataclass
class User:
    """User model"""
    id: Optional[str] = None
    name: str = ""
    email: str = ""
    phone: str = ""
    role: UserRole = UserRole.PARTICIPANT
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    is_active: bool = True
    profile_image: Optional[str] = None

@dataclass
class Event:
    """Event model"""
    id: Optional[str] = None
    name: str = ""
    description: str = ""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    venue: str = ""
    max_participants: int = 0
    registration_fee: float = 0.0
    organizer_id: Optional[str] = None
    is_active: bool = True

@dataclass
class Volunteer:
    """Volunteer model"""
    id: Optional[str] = None
    user_id: str = ""
    name: str = ""
    email: str = ""
    phone: str = ""
    role: str = ""
    skills: str = ""
    availability: List[str] = None
    emergency_contact: str = ""
    t_shirt_size: str = ""
    dietary_restrictions: str = ""
    status: VolunteerStatus = VolunteerStatus.ACTIVE
    hours_worked: int = 0
    rating: float = 0.0
    resume_path: Optional[str] = None
    id_document_path: Optional[str] = None
    
    def __post_init__(self):
        if self.availability is None:
            self.availability = []

@dataclass
class Participant:
    """Participant model"""
    id: Optional[str] = None
    user_id: str = ""
    name: str = ""
    email: str = ""
    phone: str = ""
    organization: str = ""
    job_title: str = ""
    dietary_restrictions: str = ""
    accessibility_needs: str = ""
    emergency_contact: str = ""
    registration_date: Optional[datetime] = None
    payment_status: str = "pending"
    profile_image: Optional[str] = None

@dataclass
class Vendor:
    """Vendor model"""
    id: Optional[str] = None
    company_name: str = ""
    contact_person: str = ""
    email: str = ""
    phone: str = ""
    business_type: str = ""
    description: str = ""
    website: str = ""
    address: str = ""
    booth_id: Optional[str] = None
    contract_value: float = 0.0
    payment_status: str = "pending"
    documents: List[str] = None
    
    def __post_init__(self):
        if self.documents is None:
            self.documents = []

@dataclass
class Booth:
    """Booth model"""
    id: str = ""
    section: str = ""
    size: str = ""
    status: BoothStatus = BoothStatus.AVAILABLE
    vendor_id: Optional[str] = None
    price: float = 0.0
    has_power: bool = False
    has_wifi: bool = False
    special_features: List[str] = None
    layout_plan: Optional[str] = None
    
    def __post_init__(self):
        if self.special_features is None:
            self.special_features = []

@dataclass
class Certificate:
    """Certificate model"""
    id: Optional[str] = None
    recipient_name: str = ""
    recipient_email: str = ""
    certificate_type: str = ""
    event_name: str = ""
    issue_date: Optional[datetime] = None
    certificate_path: Optional[str] = None
    template_used: str = ""
    is_downloaded: bool = False

@dataclass
class WorkflowStep:
    """Workflow step model"""
    step_number: int = 0
    name: str = ""
    description: str = ""
    assignee: str = ""
    estimated_hours: int = 0
    is_completed: bool = False
    completed_date: Optional[datetime] = None

@dataclass
class Workflow:
    """Workflow model"""
    id: Optional[str] = None
    name: str = ""
    description: str = ""
    category: str = ""
    priority: str = "medium"
    status: WorkflowStatus = WorkflowStatus.ACTIVE
    assigned_to: str = ""
    created_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    progress_percentage: int = 0
    steps: List[WorkflowStep] = None
    attachments: List[str] = None
    
    def __post_init__(self):
        if self.steps is None:
            self.steps = []
        if self.attachments is None:
            self.attachments = []

@dataclass
class Feedback:
    """Feedback model"""
    id: Optional[str] = None
    feedback_type: FeedbackType = FeedbackType.EVENT_OVERALL
    respondent_name: str = ""
    respondent_email: str = ""
    organization: str = ""
    overall_rating: int = 0
    venue_rating: int = 0
    content_rating: int = 0
    organization_rating: int = 0
    value_rating: int = 0
    comments: str = ""
    suggestions: str = ""
    would_recommend: str = ""
    would_attend_again: str = ""
    submit_date: Optional[datetime] = None
    is_anonymous: bool = False
    attachments: List[str] = None
    
    def __post_init__(self):
        if self.attachments is None:
            self.attachments = []

@dataclass
class BudgetItem:
    """Budget item model"""
    id: Optional[str] = None
    category: str = ""
    item_name: str = ""
    description: str = ""
    budgeted_amount: float = 0.0
    actual_amount: float = 0.0
    vendor: str = ""
    payment_date: Optional[datetime] = None
    receipt_path: Optional[str] = None
    status: str = "planned"

@dataclass
class MediaItem:
    """Media item model"""
    id: Optional[str] = None
    file_name: str = ""
    file_path: str = ""
    file_type: str = ""
    file_size: int = 0
    upload_date: Optional[datetime] = None
    uploader_name: str = ""
    description: str = ""
    tags: List[str] = None
    is_featured: bool = False
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

@dataclass
class AnalyticsData:
    """Analytics data model"""
    metric_name: str = ""
    metric_value: Any = None
    metric_type: str = "counter"  # counter, gauge, histogram
    timestamp: Optional[datetime] = None
    dimensions: Dict[str, str] = None
    
    def __post_init__(self):
        if self.dimensions is None:
            self.dimensions = {}

@dataclass
class FileUpload:
    """File upload model"""
    file_name: str = ""
    file_path: str = ""
    file_size: int = 0
    file_type: str = ""
    upload_date: Optional[datetime] = None
    uploader: str = ""
    module: str = ""
    category: str = ""
    is_valid: bool = True
    error_message: str = ""

# Factory functions for creating model instances
def create_event(name: str, description: str, venue: str) -> Event:
    """Create a new event instance with required fields"""
    return Event(
        name=name,
        description=description,
        venue=venue,
        start_date=datetime.now(),
        end_date=datetime.now(),
        is_active=True
    )

def create_volunteer(name: str, email: str, role: str) -> Volunteer:
    """Create a new volunteer instance with required fields"""
    return Volunteer(
        name=name,
        email=email,
        role=role,
        status=VolunteerStatus.ACTIVE
    )

def create_participant(name: str, email: str) -> Participant:
    """Create a new participant instance with required fields"""
    return Participant(
        name=name,
        email=email,
        registration_date=datetime.now()
    )

def create_vendor(company_name: str, contact_person: str, email: str) -> Vendor:
    """Create a new vendor instance with required fields"""
    return Vendor(
        company_name=company_name,
        contact_person=contact_person,
        email=email
    )

def create_booth(booth_id: str, section: str, size: str, price: float) -> Booth:
    """Create a new booth instance with required fields"""
    return Booth(
        id=booth_id,
        section=section,
        size=size,
        price=price
    )

def create_workflow(name: str, description: str, assigned_to: str) -> Workflow:
    """Create a new workflow instance with required fields"""
    return Workflow(
        name=name,
        description=description,
        assigned_to=assigned_to,
        created_date=datetime.now()
    )

def create_feedback(feedback_type: FeedbackType) -> Feedback:
    """Create a new feedback instance with specified type"""
    return Feedback(
        feedback_type=feedback_type,
        submit_date=datetime.now()
    )
