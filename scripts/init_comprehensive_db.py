"""
Enhanced Database Initialization Script

This script creates comprehensive sample data for all EventIQ modules
to enable full system testing and demonstration.
"""

import asyncio
import hashlib
from datetime import datetime, timedelta
from decimal import Decimal

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models import Base
from app.models.user import User
from app.models.volunteer import Volunteer, VolunteerRole, VolunteerAttendance
from app.models.participant import Participant, ParticipantRegistration, RegistrationStatus
from app.models.budget import Budget, BudgetCategory, Expense, ExpenseStatus
from app.models.booth import Booth, BoothAssignment, BoothStatus, BoothType


def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


async def init_database():
    """Initialize database with comprehensive sample data"""
    
    # Create async engine
    engine = create_async_engine(
        "sqlite+aiosqlite:///./eventiq.db",
        echo=True
    )
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    # Create async session
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        print("🎯 Creating sample users...")
        
        # Create admin user
        admin = User(
            email="admin@eventiq.com",
            password_hash=hash_password("admin123"),
            full_name="Event Administrator",
            role="admin",
            phone="+1-555-0101",
            is_verified=True
        )
        session.add(admin)
        
        # Create organizer users
        organizer1 = User(
            email="organizer@eventiq.com",
            password_hash=hash_password("organizer123"),
            full_name="Event Organizer",
            role="organizer",
            phone="+1-555-0102",
            is_verified=True
        )
        session.add(organizer1)
        
        organizer2 = User(
            email="sarah.manager@eventiq.com",
            password_hash=hash_password("organizer123"),
            full_name="Sarah Event Manager",
            role="organizer",
            phone="+1-555-0103",
            is_verified=True
        )
        session.add(organizer2)
        
        # Create volunteer users
        volunteer_user = User(
            email="volunteer@eventiq.com",
            password_hash=hash_password("volunteer123"),
            full_name="Event Volunteer",
            role="volunteer",
            phone="+1-555-0201",
            is_verified=True
        )
        session.add(volunteer_user)
        
        # Additional volunteer users
        volunteer_users = []
        for i in range(2, 6):
            vol_user = User(
                email=f"volunteer{i}@eventiq.com",
                password_hash=hash_password("volunteer123"),
                full_name=f"Volunteer {i}",
                role="volunteer",
                phone=f"+1-555-020{i}",
                is_verified=True
            )
            session.add(vol_user)
            volunteer_users.append(vol_user)
        
        # Create participant users
        participant_user = User(
            email="participant@eventiq.com",
            password_hash=hash_password("participant123"),
            full_name="Event Participant",
            role="participant",
            phone="+1-555-0301",
            is_verified=True
        )
        session.add(participant_user)
        
        # Additional participant users
        participant_users = []
        for i in range(2, 11):
            part_user = User(
                email=f"participant{i}@eventiq.com",
                password_hash=hash_password("participant123"),
                full_name=f"Participant {i}",
                role="participant",
                phone=f"+1-555-030{i}",
                is_verified=True
            )
            session.add(part_user)
            participant_users.append(part_user)
        
        await session.commit()
        print("✅ Users created successfully!")
        
        print("🎯 Creating volunteer profiles...")
        
        # Create volunteer profile for main volunteer
        volunteer = Volunteer(
            user_id=volunteer_user.id,
            volunteer_role=VolunteerRole.COORDINATOR,
            skills="Event Management, Public Speaking, Leadership",
            availability="Full-time during event days",
            emergency_contact="Jane Doe - +1-555-9999",
            t_shirt_size="L",
            dietary_restrictions="Vegetarian",
            special_requirements=None
        )
        session.add(volunteer)
        
        # Create profiles for additional volunteers
        volunteer_roles = [VolunteerRole.USHER, VolunteerRole.TECHNICAL, VolunteerRole.REGISTRATION, VolunteerRole.GENERAL]
        volunteer_profiles = []
        
        for i, vol_user in enumerate(volunteer_users):
            vol_profile = Volunteer(
                user_id=vol_user.id,
                volunteer_role=volunteer_roles[i % len(volunteer_roles)],
                skills=f"Skills for volunteer {i+2}",
                availability="Part-time",
                emergency_contact=f"Emergency contact {i+2} - +1-555-888{i}",
                t_shirt_size=["S", "M", "L", "XL"][i % 4],
                dietary_restrictions=["None", "Vegetarian", "Vegan", "Gluten-free"][i % 4] if i % 2 == 0 else None
            )
            session.add(vol_profile)
            volunteer_profiles.append(vol_profile)
        
        await session.commit()
        print("✅ Volunteer profiles created!")
        
        print("🎯 Creating participant profiles...")
        
        # Create participant profile for main participant
        participant = Participant(
            user_id=participant_user.id,
            organization="Tech Solutions Inc.",
            job_title="Software Engineer",
            industry="Technology",
            interests="AI, Machine Learning, Web Development",
            dietary_restrictions="No nuts",
            accessibility_needs=None,
            emergency_contact="John Smith - +1-555-8888",
            t_shirt_size="M",
            linkedin_profile="https://linkedin.com/in/eventparticipant",
            how_did_you_hear="Social Media"
        )
        session.add(participant)
        
        # Create profiles for additional participants
        organizations = ["TechCorp", "Innovation Labs", "Digital Solutions", "Future Systems", "Smart Analytics"]
        industries = ["Technology", "Finance", "Healthcare", "Education", "Manufacturing"]
        job_titles = ["Developer", "Analyst", "Manager", "Consultant", "Designer"]
        
        participant_profiles = []
        for i, part_user in enumerate(participant_users):
            part_profile = Participant(
                user_id=part_user.id,
                organization=organizations[i % len(organizations)],
                job_title=job_titles[i % len(job_titles)],
                industry=industries[i % len(industries)],
                interests=f"Professional interests for participant {i+2}",
                emergency_contact=f"Emergency contact {i+2} - +1-555-777{i}",
                t_shirt_size=["S", "M", "L", "XL"][i % 4],
                linkedin_profile=f"https://linkedin.com/in/participant{i+2}",
                how_did_you_hear=["Website", "Email", "Social Media", "Word of mouth"][i % 4]
            )
            session.add(part_profile)
            participant_profiles.append(part_profile)
        
        await session.commit()
        print("✅ Participant profiles created!")
        
        print("🎯 Creating budget and financial data...")
        
        # Create event budget
        budget = Budget(
            event_name="TechCon 2024",
            total_budget=Decimal("50000.00"),
            description="Main budget for TechCon 2024 conference",
            created_by=organizer1.id
        )
        session.add(budget)
        await session.commit()
        
        # Create budget categories
        categories_data = [
            ("Venue", Decimal("15000.00"), "Conference venue rental and setup"),
            ("Catering", Decimal("12000.00"), "Food and beverages for attendees"),
            ("Technology", Decimal("8000.00"), "AV equipment, WiFi, streaming"),
            ("Marketing", Decimal("5000.00"), "Promotional materials and advertising"),
            ("Speakers", Decimal("7000.00"), "Speaker fees and travel expenses"),
            ("Materials", Decimal("3000.00"), "Swag, badges, and printed materials")
        ]
        
        categories = []
        for name, amount, desc in categories_data:
            category = BudgetCategory(
                budget_id=budget.id,
                name=name,
                allocated_amount=amount,
                description=desc
            )
            session.add(category)
            categories.append(category)
            
            # Update budget allocated amount
            budget.allocated_amount += amount
        
        await session.commit()
        print("✅ Budget categories created!")
        
        # Create sample expenses
        expenses_data = [
            (0, "Grand Conference Center", "Venue rental for 3 days", Decimal("14500.00"), ExpenseStatus.APPROVED),
            (1, "Premier Catering Co.", "Opening day lunch", Decimal("2800.00"), ExpenseStatus.APPROVED),
            (1, "Coffee Express", "Coffee service", Decimal("1200.00"), ExpenseStatus.PENDING),
            (2, "Tech Solutions AV", "Sound system rental", Decimal("3500.00"), ExpenseStatus.APPROVED),
            (3, "Digital Marketing Inc.", "Social media campaign", Decimal("2200.00"), ExpenseStatus.PENDING),
            (4, "Dr. Jane Speaker", "Keynote speaker fee", Decimal("5000.00"), ExpenseStatus.APPROVED)
        ]
        
        for cat_idx, vendor, desc, amount, status in expenses_data:
            expense = Expense(
                category_id=categories[cat_idx].id,
                vendor_name=vendor,
                description=desc,
                amount=amount,
                status=status,
                submitted_by=organizer1.id,
                notes=f"Expense for {desc.lower()}"
            )
            
            if status == ExpenseStatus.APPROVED:
                expense.approved_by = admin.id
                expense.approved_at = datetime.now() - timedelta(days=1)
                # Update category spent amount
                categories[cat_idx].spent_amount += amount
                budget.spent_amount += amount
            
            session.add(expense)
        
        await session.commit()
        print("✅ Sample expenses created!")
        
        print("🎯 Creating booth and venue data...")
        
        # Create booths
        booth_data = [
            ("A-01", BoothType.STANDARD, "Main Hall - Section A", "10x10 ft", "Power, WiFi, Table, 2 Chairs", 100.0, 800.0),
            ("A-02", BoothType.PREMIUM, "Main Hall - Section A", "15x15 ft", "Power, WiFi, Premium Setup, Storage", 150.0, 1200.0),
            ("B-01", BoothType.STANDARD, "Main Hall - Section B", "10x10 ft", "Power, WiFi, Table, 2 Chairs", 100.0, 800.0),
            ("B-02", BoothType.STANDARD, "Main Hall - Section B", "10x10 ft", "Power, WiFi, Table, 2 Chairs", 100.0, 800.0),
            ("C-01", BoothType.FOOD, "Food Court Area", "12x12 ft", "Power, Water, Sink, Ventilation", 120.0, 1000.0),
            ("VIP-01", BoothType.VIP, "VIP Section", "20x20 ft", "Full Setup, Private Area, Catering", 300.0, 2500.0)
        ]
        
        booths = []
        for number, booth_type, location, size, amenities, hourly, daily in booth_data:
            booth = Booth(
                booth_number=number,
                booth_type=booth_type,
                location=location,
                size=size,
                amenities=amenities,
                hourly_rate=hourly,
                daily_rate=daily,
                status=BoothStatus.AVAILABLE,
                description=f"Booth {number} in {location}"
            )
            session.add(booth)
            booths.append(booth)
        
        await session.commit()
        print("✅ Booths created!")
        
        # Create booth assignments
        assignment_data = [
            (0, "TechCorp Solutions", datetime.now() + timedelta(days=1), datetime.now() + timedelta(days=3), 2400.0, True),
            (1, "Innovation Labs", datetime.now() + timedelta(days=1), datetime.now() + timedelta(days=3), 3600.0, True),
            (4, "Gourmet Food Truck", datetime.now() + timedelta(days=1), datetime.now() + timedelta(days=3), 3000.0, False),
            (5, "Premium Sponsor Corp", datetime.now() + timedelta(days=1), datetime.now() + timedelta(days=3), 7500.0, True)
        ]
        
        for booth_idx, vendor, start, end, cost, confirmed in assignment_data:
            assignment = BoothAssignment(
                booth_id=booths[booth_idx].id,
                vendor_name=vendor,
                start_time=start,
                end_time=end,
                total_cost=cost,
                contact_person=f"Contact for {vendor}",
                contact_phone=f"+1-555-{1000 + booth_idx * 111}",
                assigned_by=organizer1.id,
                is_confirmed=confirmed,
                notes=f"Assignment for booth {booths[booth_idx].booth_number}"
            )
            session.add(assignment)
            
            # Update booth status
            if confirmed:
                booths[booth_idx].status = BoothStatus.RESERVED
        
        await session.commit()
        print("✅ Booth assignments created!")
        
        print("🎯 Creating participant registrations...")
        
        # Create event registrations for participants
        events = ["TechCon 2024", "AI Workshop", "Networking Session", "Innovation Panel"]
        
        # Register main participant for all events
        for event in events:
            registration = ParticipantRegistration(
                participant_id=participant.id,
                event_name=event,
                registration_status=RegistrationStatus.CONFIRMED,
                confirmation_date=datetime.now() - timedelta(days=2),
                notes=f"Registration for {event}"
            )
            session.add(registration)
        
        # Register other participants for random events
        import random
        for i, profile in enumerate(participant_profiles[:5]):  # Register first 5 additional participants
            num_events = random.randint(1, 3)
            selected_events = random.sample(events, num_events)
            
            for event in selected_events:
                status = random.choice([RegistrationStatus.PENDING, RegistrationStatus.CONFIRMED])
                registration = ParticipantRegistration(
                    participant_id=profile.id,
                    event_name=event,
                    registration_status=status,
                    confirmation_date=datetime.now() - timedelta(days=1) if status == RegistrationStatus.CONFIRMED else None,
                    notes=f"Registration for {event} by {profile.user_id}"
                )
                session.add(registration)
        
        await session.commit()
        print("✅ Participant registrations created!")
        
        print("🎯 Creating volunteer attendance records...")
        
        # Create attendance records for volunteers
        base_time = datetime.now() - timedelta(days=1)
        
        # Main volunteer attendance
        attendance1 = VolunteerAttendance(
            volunteer_id=volunteer.id,
            check_in_time=base_time.replace(hour=8, minute=0),
            check_out_time=base_time.replace(hour=17, minute=30),
            hours_worked=9.5,
            check_in_location="Main Entrance",
            check_out_location="Main Entrance",
            notes="Full day coordination duties"
        )
        session.add(attendance1)
        
        # Update volunteer total hours
        volunteer.total_hours += int(attendance1.hours_worked)
        
        # Additional volunteer attendance
        for i, vol_profile in enumerate(volunteer_profiles[:3]):
            check_in = base_time.replace(hour=9, minute=0) + timedelta(minutes=i*15)
            check_out = base_time.replace(hour=16, minute=0) + timedelta(minutes=i*10)
            hours = (check_out - check_in).total_seconds() / 3600
            
            attendance = VolunteerAttendance(
                volunteer_id=vol_profile.id,
                check_in_time=check_in,
                check_out_time=check_out,
                hours_worked=round(hours, 2),
                check_in_location="Volunteer Check-in",
                check_out_location="Volunteer Check-in",
                notes=f"Volunteer duties for {vol_profile.volunteer_role.value}"
            )
            session.add(attendance)
            
            # Update volunteer total hours
            vol_profile.total_hours += int(hours)
        
        await session.commit()
        print("✅ Volunteer attendance records created!")
        
        print("\n🎉 Database initialization completed successfully!")
        print("\n📊 Summary of created data:")
        print(f"   👥 Users: {len([admin, organizer1, organizer2, volunteer_user] + volunteer_users + [participant_user] + participant_users)}")
        print(f"   🤝 Volunteers: {len([volunteer] + volunteer_profiles)}")
        print(f"   🎯 Participants: {len([participant] + participant_profiles)}")
        print(f"   💰 Budgets: 1 with {len(categories)} categories")
        print(f"   🏢 Booths: {len(booths)} with {len(assignment_data)} assignments")
        print(f"   📝 Registrations: Multiple event registrations")
        print(f"   ⏰ Attendance: Multiple volunteer attendance records")
        
        print("\n🔑 Login Credentials:")
        print("   Admin: admin@eventiq.com / admin123")
        print("   Organizer: organizer@eventiq.com / organizer123")
        print("   Volunteer: volunteer@eventiq.com / volunteer123")
        print("   Participant: participant@eventiq.com / participant123")
        
    await engine.dispose()


if __name__ == "__main__":
    print("🚀 Initializing EventIQ Database with comprehensive sample data...")
    asyncio.run(init_database())
