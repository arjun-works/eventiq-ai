"""
Database Initialization Script

This script initializes the database with sample data for development and testing.
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
from decimal import Decimal

# Add the parent directory to the path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import init_db, AsyncSessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.volunteer import Volunteer, VolunteerAttendance, VolunteerRole
from app.models.participant import Participant, ParticipantBoothVisit
from app.models.budget import BudgetEstimate, Expense, BudgetCategory, BudgetStatus
from app.models.booth import Booth, BoothFootfall
from app.models.vendor import Vendor, VendorInteraction, VendorAsset, VendorStatus, InteractionType
from app.models.workflow import WorkflowRequest, WorkflowApproval, WorkflowTemplate, WorkflowStatus
from app.models.feedback import Feedback, FeedbackType, SentimentScore
from app.models.certificate import Certificate, CertificateTemplate, CertificateStatus, CertificateType
from app.models.media import Media, MediaCollection, MediaType, MediaStatus
from app.models.admin import SystemIssue, EventOverview, IssueStatus, IssuePriority, IssueSource
import json


async def create_sample_users():
    """Create sample users"""
    async with AsyncSessionLocal() as db:
        users_data = [
            {
                "email": "admin@eventiq.com",
                "password": "admin123",
                "full_name": "System Administrator",
                "role": UserRole.ADMIN,
                "phone": "+1-555-0001",
                "organization": "EventIQ",
                "bio": "System administrator for EventIQ platform"
            },
            {
                "email": "organizer@eventiq.com", 
                "password": "organizer123",
                "full_name": "Event Organizer",
                "role": UserRole.ORGANIZER,
                "phone": "+1-555-0002",
                "organization": "Tech University",
                "bio": "Lead organizer for campus events"
            },
            {
                "email": "volunteer1@example.com",
                "password": "volunteer123",
                "full_name": "Alice Johnson",
                "role": UserRole.VOLUNTEER,
                "phone": "+1-555-0003",
                "organization": "Computer Science Club",
                "bio": "Passionate about technology and helping others"
            },
            {
                "email": "volunteer2@example.com",
                "password": "volunteer123",
                "full_name": "Bob Smith",
                "role": UserRole.VOLUNTEER,
                "phone": "+1-555-0004", 
                "organization": "Engineering Society",
                "bio": "Senior student with event management experience"
            },
            {
                "email": "participant1@example.com",
                "password": "participant123",
                "full_name": "Carol Davis",
                "role": UserRole.PARTICIPANT,
                "phone": "+1-555-0005",
                "organization": "Marketing Department",
                "bio": "Interested in AI and technology trends"
            },
            {
                "email": "participant2@example.com",
                "password": "participant123",
                "full_name": "David Wilson",
                "role": UserRole.PARTICIPANT,
                "phone": "+1-555-0006",
                "organization": "Business School",
                "bio": "MBA student focusing on innovation"
            }
        ]
        
        for user_data in users_data:
            existing_user = await db.execute(
                "SELECT id FROM users WHERE email = :email",
                {"email": user_data["email"]}
            )
            if not existing_user.fetchone():
                user = User(
                    email=user_data["email"],
                    hashed_password=get_password_hash(user_data["password"]),
                    full_name=user_data["full_name"],
                    role=user_data["role"],
                    phone=user_data["phone"],
                    organization=user_data["organization"],
                    bio=user_data["bio"],
                    is_active=True,
                    is_verified=True
                )
                db.add(user)
        
        await db.commit()
        print("✅ Sample users created")


async def create_sample_booths():
    """Create sample booths"""
    async with AsyncSessionLocal() as db:
        booths_data = [
            {
                "name": "AI & Machine Learning Showcase",
                "booth_number": "A1",
                "location_description": "Main Hall - North Wing",
                "floor_level": "Ground Floor",
                "coordinates_x": 100,
                "coordinates_y": 200,
                "size_sqft": 150,
                "category": "Technology",
                "description": "Explore the latest in AI and ML technologies",
                "organizer_name": "Dr. Sarah Chen",
                "organizer_contact": "s.chen@techuni.edu",
                "max_capacity": 25,
                "estimated_visit_duration": 20,
                "operating_hours_start": "09:00",
                "operating_hours_end": "17:00",
                "features": ["Interactive Demos", "VR Experience", "Expert Talks"],
                "requirements": ["Power Supply", "Internet", "Projector"]
            },
            {
                "name": "Startup Innovation Hub",
                "booth_number": "B2", 
                "location_description": "Main Hall - South Wing",
                "floor_level": "Ground Floor",
                "coordinates_x": 300,
                "coordinates_y": 150,
                "size_sqft": 200,
                "category": "Business",
                "description": "Meet innovative startups and entrepreneurs",
                "organizer_name": "Mark Thompson",
                "organizer_contact": "m.thompson@bizuni.edu",
                "max_capacity": 30,
                "estimated_visit_duration": 15,
                "operating_hours_start": "10:00",
                "operating_hours_end": "16:00",
                "features": ["Pitch Sessions", "Networking", "Investor Meetings"],
                "requirements": ["Sound System", "Internet", "Display Screens"]
            },
            {
                "name": "Sustainable Tech Solutions",
                "booth_number": "C3",
                "location_description": "Main Hall - East Wing", 
                "floor_level": "Ground Floor",
                "coordinates_x": 200,
                "coordinates_y": 300,
                "size_sqft": 120,
                "category": "Environment",
                "description": "Green technology and sustainability initiatives",
                "organizer_name": "Emma Green",
                "organizer_contact": "e.green@ecotech.org",
                "max_capacity": 20,
                "estimated_visit_duration": 25,
                "operating_hours_start": "09:30",
                "operating_hours_end": "17:30",
                "features": ["Eco Demos", "Sustainability Talks", "Green Products"],
                "requirements": ["Power Supply", "Water Access", "Recycling Bins"]
            }
        ]
        
        for booth_data in booths_data:
            booth = Booth(**booth_data)
            db.add(booth)
        
        await db.commit()
        print("✅ Sample booths created")


async def create_sample_volunteers():
    """Create sample volunteers"""
    async with AsyncSessionLocal() as db:
        # First get user IDs
        result = await db.execute("SELECT id, email FROM users WHERE role = 'volunteer'")
        volunteer_users = result.fetchall()
        
        for user in volunteer_users:
            volunteer = Volunteer(
                user_id=user[0],
                skills=["Communication", "Event Management", "Technical Support"],
                available_time_slots=["09:00-13:00", "13:00-17:00"],
                preferred_roles=["Registration Desk", "Technical Support"],
                experience_level="Intermediate",
                emergency_contact="Emergency Contact",
                emergency_phone="+1-555-9999",
                assigned_booth="A1" if user[1] == "volunteer1@example.com" else "B2",
                assigned_role="Registration Assistant",
                assignment_type="manual",
                is_approved=True,
                total_hours=8
            )
            db.add(volunteer)
        
        await db.commit()
        print("✅ Sample volunteers created")


async def create_sample_participants():
    """Create sample participants"""
    async with AsyncSessionLocal() as db:
        # Get participant user IDs
        result = await db.execute("SELECT id, email FROM users WHERE role = 'participant'")
        participant_users = result.fetchall()
        
        for i, user in enumerate(participant_users):
            participant = Participant(
                user_id=user[0],
                registration_date=datetime.now() - timedelta(days=10),
                registration_source="online",
                ticket_number=f"TK{2025000 + i + 1}",
                age_group="26-35",
                interests=["Technology", "Innovation", "Networking"],
                dietary_restrictions=["Vegetarian"] if i % 2 == 0 else [],
                preferred_booths=["A1", "B2", "C3"],
                preferred_time_slots=["10:00-12:00", "14:00-16:00"],
                notification_preferences=["email", "sms"],
                is_confirmed=True,
                has_attended=True,
                check_in_time=datetime.now() - timedelta(hours=6)
            )
            db.add(participant)
        
        await db.commit()
        print("✅ Sample participants created")


async def create_sample_budget():
    """Create sample budget data"""
    async with AsyncSessionLocal() as db:
        budget_data = [
            {
                "category": BudgetCategory.FOOD,
                "item_name": "Catering Services",
                "description": "Lunch and refreshments for 500 attendees",
                "estimated_cost": Decimal("5000.00"),
                "quantity": 1,
                "unit_price": Decimal("5000.00"),
                "preferred_vendor": "University Catering",
                "status": BudgetStatus.APPROVED,
                "is_approved": True
            },
            {
                "category": BudgetCategory.EQUIPMENT,
                "item_name": "Audio/Visual Equipment",
                "description": "Projectors, microphones, speakers for booths",
                "estimated_cost": Decimal("3000.00"),
                "quantity": 10,
                "unit_price": Decimal("300.00"),
                "preferred_vendor": "TechRent Solutions",
                "status": BudgetStatus.IN_PROGRESS
            },
            {
                "category": BudgetCategory.MARKETING,
                "item_name": "Promotional Materials",
                "description": "Banners, flyers, digital displays",
                "estimated_cost": Decimal("1500.00"),
                "quantity": 1,
                "unit_price": Decimal("1500.00"),
                "preferred_vendor": "PrintPro Marketing",
                "status": BudgetStatus.APPROVED,
                "is_approved": True
            }
        ]
        
        for item in budget_data:
            budget = BudgetEstimate(**item)
            db.add(budget)
        
        # Create corresponding expenses
        expenses_data = [
            {
                "category": BudgetCategory.FOOD,
                "vendor_name": "University Catering",
                "item_description": "Catering Services - Actual cost",
                "actual_cost": Decimal("5200.00"),
                "quantity_purchased": 1,
                "unit_cost": Decimal("5200.00"),
                "estimated_cost": Decimal("5000.00"),
                "variance_amount": Decimal("200.00"),
                "variance_percentage": Decimal("4.00"),
                "is_high_variance": False,
                "is_approved": True,
                "payment_method": "Bank Transfer"
            }
        ]
        
        for expense in expenses_data:
            expense_obj = Expense(**expense)
            db.add(expense_obj)
        
        await db.commit()
        print("✅ Sample budget data created")


async def create_sample_vendors():
    """Create sample vendors"""
    async with AsyncSessionLocal() as db:
        vendors_data = [
            {
                "name": "TechRent Solutions",
                "company_name": "TechRent Solutions Inc.",
                "contact_person": "Michael Rodriguez",
                "email": "contact@techrent.com",
                "phone": "+1-555-7001",
                "address": "123 Tech Street, Innovation City",
                "city": "Innovation City",
                "state": "CA",
                "business_type": "Equipment Rental",
                "services_offered": ["AV Equipment", "Technical Support", "Setup Services"],
                "purpose": "Provide audio/visual equipment for event booths",
                "materials_brought": ["Projectors", "Microphones", "Speakers", "Cables"],
                "status": VendorStatus.APPROVED,
                "rating": 5,
                "is_preferred": True
            },
            {
                "name": "PrintPro Marketing",
                "company_name": "PrintPro Marketing LLC",
                "contact_person": "Jennifer Lee",
                "email": "info@printpro.com",
                "phone": "+1-555-7002",
                "address": "456 Design Ave, Creative District",
                "city": "Creative District",
                "state": "NY",
                "business_type": "Marketing & Print Services",
                "services_offered": ["Digital Printing", "Banner Design", "Marketing Materials"],
                "purpose": "Provide promotional materials and signage",
                "materials_brought": ["Banners", "Flyers", "Digital Displays"],
                "status": VendorStatus.ACTIVE,
                "rating": 4
            }
        ]
        
        for vendor_data in vendors_data:
            vendor = Vendor(**vendor_data)
            db.add(vendor)
        
        await db.commit()
        print("✅ Sample vendors created")


async def create_sample_feedback():
    """Create sample feedback data"""
    async with AsyncSessionLocal() as db:
        # Get some user IDs
        result = await db.execute("SELECT id FROM users LIMIT 3")
        user_ids = [row[0] for row in result.fetchall()]
        
        feedback_data = [
            {
                "feedback_type": FeedbackType.PARTICIPANT,
                "user_id": user_ids[0] if user_ids else None,
                "overall_rating": 5,
                "title": "Excellent Event!",
                "detailed_feedback": "The AI showcase was absolutely amazing. Great organization and very informative sessions.",
                "event_organization_rating": 5,
                "venue_rating": 4,
                "staff_helpfulness_rating": 5,
                "booth_visited": "AI & Machine Learning Showcase",
                "would_recommend": True,
                "would_attend_again": True,
                "sentiment_score": SentimentScore.VERY_POSITIVE,
                "sentiment_confidence": 95,
                "ai_processed": True
            },
            {
                "feedback_type": FeedbackType.VOLUNTEER,
                "user_id": user_ids[1] if len(user_ids) > 1 else None,
                "overall_rating": 4,
                "title": "Good Experience with Minor Issues",
                "detailed_feedback": "Overall great event to volunteer for. Could use better communication about schedule changes.",
                "event_organization_rating": 4,
                "staff_helpfulness_rating": 4,
                "improvement_suggestions": "Better volunteer coordination and clearer instructions",
                "sentiment_score": SentimentScore.POSITIVE,
                "sentiment_confidence": 88,
                "ai_processed": True
            },
            {
                "feedback_type": FeedbackType.PARTICIPANT,
                "user_id": user_ids[2] if len(user_ids) > 2 else None,
                "overall_rating": 3,
                "title": "Average Experience",
                "detailed_feedback": "The event was okay but could have been better organized. Long waiting times at popular booths.",
                "event_organization_rating": 3,
                "venue_rating": 4,
                "improvement_suggestions": "Better crowd management and shorter wait times",
                "sentiment_score": SentimentScore.NEUTRAL,
                "sentiment_confidence": 82,
                "ai_processed": True
            }
        ]
        
        for feedback in feedback_data:
            feedback_obj = Feedback(**feedback)
            db.add(feedback_obj)
        
        await db.commit()
        print("✅ Sample feedback created")


async def create_sample_certificates():
    """Create sample certificates"""
    async with AsyncSessionLocal() as db:
        # Get volunteer user IDs
        result = await db.execute("SELECT id, full_name, email FROM users WHERE role = 'volunteer'")
        volunteers = result.fetchall()
        
        for i, volunteer in enumerate(volunteers):
            certificate = Certificate(
                certificate_number=f"CERT-2025-{1000 + i + 1}",
                certificate_type=CertificateType.VOLUNTEER_COMPLETION,
                title="Certificate of Volunteer Service",
                recipient_user_id=volunteer[0],
                recipient_name=volunteer[1],
                recipient_email=volunteer[2],
                achievement_description=f"Successfully completed volunteer service at TechFest 2025",
                hours_volunteered=8,
                booth_assigned="Registration Desk",
                role_performed="Registration Assistant",
                event_dates="March 15-16, 2025",
                template_used="default",
                verification_code=f"VERIFY-{1000 + i + 1}",
                status=CertificateStatus.GENERATED
            )
            db.add(certificate)
        
        await db.commit()
        print("✅ Sample certificates created")


async def create_sample_system_issues():
    """Create sample system issues"""
    async with AsyncSessionLocal() as db:
        issues_data = [
            {
                "title": "Slow Response Time on Registration Page",
                "description": "Users reporting slow loading times when submitting registration forms",
                "issue_type": "performance",
                "priority": IssuePriority.HIGH,
                "severity_score": 7,
                "source": IssueSource.USER_REPORTED,
                "detected_by": "Support Team",
                "status": IssueStatus.IN_PROGRESS,
                "assigned_to": "Tech Team",
                "affected_users_count": 45
            },
            {
                "title": "QR Code Scanner Not Working on Mobile",
                "description": "Mobile app QR code scanner failing to read volunteer check-in codes",
                "issue_type": "technical",
                "priority": IssuePriority.CRITICAL,
                "severity_score": 9,
                "source": IssueSource.AUTO_DETECTED,
                "status": IssueStatus.RESOLVED,
                "resolution_notes": "Updated QR code library and improved camera permissions",
                "affected_users_count": 12
            }
        ]
        
        for issue_data in issues_data:
            issue = SystemIssue(**issue_data)
            db.add(issue)
        
        await db.commit()
        print("✅ Sample system issues created")


async def create_sample_event_overview():
    """Create sample event overview data"""
    async with AsyncSessionLocal() as db:
        overview = EventOverview(
            overview_date=datetime.now().date(),
            total_registered_participants=150,
            total_checked_in_participants=135,
            participant_attendance_rate=90,
            total_registered_volunteers=25,
            total_active_volunteers=22,
            total_volunteer_hours=176,
            total_active_booths=12,
            average_booth_visitors=45,
            most_popular_booth="AI & Machine Learning Showcase",
            total_estimated_budget=15000,
            total_actual_expenses=15450,
            budget_variance_percentage=3,
            system_uptime_percentage=99,
            total_system_issues=5,
            resolved_issues_count=4,
            total_feedback_responses=87,
            average_satisfaction_score=4,
            certificates_generated=25,
            certificates_sent=22
        )
        db.add(overview)
        
        await db.commit()
        print("✅ Sample event overview created")


async def main():
    """Main function to initialize database with sample data"""
    print("🚀 Initializing EventIQ database with sample data...")
    
    try:
        # Initialize database tables
        await init_db()
        print("✅ Database tables initialized")
        
        # Create sample data
        await create_sample_users()
        await create_sample_booths()
        await create_sample_volunteers()
        await create_sample_participants()
        await create_sample_budget()
        await create_sample_vendors()
        await create_sample_feedback()
        await create_sample_certificates()
        await create_sample_system_issues()
        await create_sample_event_overview()
        
        print("\n🎉 Database initialization completed successfully!")
        print("\n📊 Sample Data Summary:")
        print("- 6 Users (1 Admin, 1 Organizer, 2 Volunteers, 2 Participants)")
        print("- 3 Event Booths")
        print("- 2 Volunteer Profiles")
        print("- 2 Participant Registrations")
        print("- 3 Budget Items + 1 Expense")
        print("- 2 Vendors")
        print("- 3 Feedback Entries")
        print("- 2 Certificates")
        print("- 2 System Issues")
        print("- 1 Event Overview")
        
        print("\n🔐 Login Credentials:")
        print("Admin: admin@eventiq.com / admin123")
        print("Organizer: organizer@eventiq.com / organizer123")
        print("Volunteer: volunteer1@example.com / volunteer123")
        print("Participant: participant1@example.com / participant123")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
