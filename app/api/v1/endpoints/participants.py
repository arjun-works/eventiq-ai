"""
Participants API Endpoints

This module handles participant registration, profile management,
and event participation tracking.
"""

from typing import List, Optional
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_user, get_current_active_user
from app.models.user import User
from app.models.participant import Participant, ParticipantRegistration, RegistrationStatus

router = APIRouter()

# Pydantic schemas for request/response
class ParticipantCreate(BaseModel):
    organization: Optional[str] = None
    job_title: Optional[str] = None
    industry: Optional[str] = None
    interests: Optional[str] = None
    dietary_restrictions: Optional[str] = None
    accessibility_needs: Optional[str] = None
    emergency_contact: Optional[str] = None
    t_shirt_size: Optional[str] = None
    linkedin_profile: Optional[str] = None
    how_did_you_hear: Optional[str] = None

class ParticipantUpdate(BaseModel):
    organization: Optional[str] = None
    job_title: Optional[str] = None
    industry: Optional[str] = None
    interests: Optional[str] = None
    dietary_restrictions: Optional[str] = None
    accessibility_needs: Optional[str] = None
    emergency_contact: Optional[str] = None
    t_shirt_size: Optional[str] = None
    linkedin_profile: Optional[str] = None
    how_did_you_hear: Optional[str] = None

class ParticipantResponse(BaseModel):
    id: int
    user_id: int
    organization: Optional[str]
    job_title: Optional[str]
    industry: Optional[str]
    interests: Optional[str]
    dietary_restrictions: Optional[str]
    accessibility_needs: Optional[str]
    emergency_contact: Optional[str]
    t_shirt_size: Optional[str]
    linkedin_profile: Optional[str]
    how_did_you_hear: Optional[str]
    registration_date: datetime
    is_active: bool
    
    # User details
    full_name: str
    email: str
    phone: Optional[str]

class RegistrationCreate(BaseModel):
    event_name: str
    notes: Optional[str] = None

class RegistrationResponse(BaseModel):
    id: int
    participant_id: int
    event_name: str
    registration_status: RegistrationStatus
    registration_date: datetime
    confirmation_date: Optional[datetime]
    notes: Optional[str]
    
    # Participant details
    participant_name: str
    participant_email: str

class RegistrationUpdate(BaseModel):
    registration_status: RegistrationStatus
    notes: Optional[str] = None


@router.post("/", response_model=ParticipantResponse)
async def create_participant_profile(
    participant_data: ParticipantCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> ParticipantResponse:
    """
    Create participant profile for current user
    """
    # Check if user already has a participant profile
    result = await db.execute(
        select(Participant).where(Participant.user_id == current_user.id)
    )
    existing_participant = result.scalar_one_or_none()
    
    if existing_participant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has a participant profile"
        )
    
    # Create new participant record
    participant = Participant(
        user_id=current_user.id,
        organization=participant_data.organization,
        job_title=participant_data.job_title,
        industry=participant_data.industry,
        interests=participant_data.interests,
        dietary_restrictions=participant_data.dietary_restrictions,
        accessibility_needs=participant_data.accessibility_needs,
        emergency_contact=participant_data.emergency_contact,
        t_shirt_size=participant_data.t_shirt_size,
        linkedin_profile=participant_data.linkedin_profile,
        how_did_you_hear=participant_data.how_did_you_hear
    )
    
    db.add(participant)
    await db.commit()
    await db.refresh(participant)
    
    return ParticipantResponse(
        id=participant.id,
        user_id=participant.user_id,
        organization=participant.organization,
        job_title=participant.job_title,
        industry=participant.industry,
        interests=participant.interests,
        dietary_restrictions=participant.dietary_restrictions,
        accessibility_needs=participant.accessibility_needs,
        emergency_contact=participant.emergency_contact,
        t_shirt_size=participant.t_shirt_size,
        linkedin_profile=participant.linkedin_profile,
        how_did_you_hear=participant.how_did_you_hear,
        registration_date=participant.registration_date,
        is_active=participant.is_active,
        full_name=current_user.full_name,
        email=current_user.email,
        phone=current_user.phone
    )


@router.get("/", response_model=List[ParticipantResponse])
async def get_participants(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    industry: Optional[str] = Query(None),
    organization: Optional[str] = Query(None),
    active_only: bool = Query(True),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[ParticipantResponse]:
    """
    Get list of participants (admin/organizer only)
    """
    if current_user.role not in ["admin", "organizer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Build query
    query = select(Participant, User).join(User, Participant.user_id == User.id)
    
    if industry:
        query = query.where(Participant.industry.ilike(f"%{industry}%"))
    if organization:
        query = query.where(Participant.organization.ilike(f"%{organization}%"))
    if active_only:
        query = query.where(Participant.is_active)
    
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    participants_with_users = result.all()
    
    return [
        ParticipantResponse(
            id=participant.id,
            user_id=participant.user_id,
            organization=participant.organization,
            job_title=participant.job_title,
            industry=participant.industry,
            interests=participant.interests,
            dietary_restrictions=participant.dietary_restrictions,
            accessibility_needs=participant.accessibility_needs,
            emergency_contact=participant.emergency_contact,
            t_shirt_size=participant.t_shirt_size,
            linkedin_profile=participant.linkedin_profile,
            how_did_you_hear=participant.how_did_you_hear,
            registration_date=participant.registration_date,
            is_active=participant.is_active,
            full_name=user.full_name,
            email=user.email,
            phone=user.phone
        )
        for participant, user in participants_with_users
    ]


@router.get("/me", response_model=ParticipantResponse)
async def get_my_participant_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> ParticipantResponse:
    """
    Get current user's participant profile
    """
    result = await db.execute(
        select(Participant).where(Participant.user_id == current_user.id)
    )
    participant = result.scalar_one_or_none()
    
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participant profile not found"
        )
    
    return ParticipantResponse(
        id=participant.id,
        user_id=participant.user_id,
        organization=participant.organization,
        job_title=participant.job_title,
        industry=participant.industry,
        interests=participant.interests,
        dietary_restrictions=participant.dietary_restrictions,
        accessibility_needs=participant.accessibility_needs,
        emergency_contact=participant.emergency_contact,
        t_shirt_size=participant.t_shirt_size,
        linkedin_profile=participant.linkedin_profile,
        how_did_you_hear=participant.how_did_you_hear,
        registration_date=participant.registration_date,
        is_active=participant.is_active,
        full_name=current_user.full_name,
        email=current_user.email,
        phone=current_user.phone
    )


@router.put("/me", response_model=ParticipantResponse)
async def update_my_participant_profile(
    participant_data: ParticipantUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> ParticipantResponse:
    """
    Update current user's participant profile
    """
    result = await db.execute(
        select(Participant).where(Participant.user_id == current_user.id)
    )
    participant = result.scalar_one_or_none()
    
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participant profile not found"
        )
    
    # Update fields
    update_data = participant_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(participant, field, value)
    
    await db.commit()
    await db.refresh(participant)
    
    return ParticipantResponse(
        id=participant.id,
        user_id=participant.user_id,
        organization=participant.organization,
        job_title=participant.job_title,
        industry=participant.industry,
        interests=participant.interests,
        dietary_restrictions=participant.dietary_restrictions,
        accessibility_needs=participant.accessibility_needs,
        emergency_contact=participant.emergency_contact,
        t_shirt_size=participant.t_shirt_size,
        linkedin_profile=participant.linkedin_profile,
        how_did_you_hear=participant.how_did_you_hear,
        registration_date=participant.registration_date,
        is_active=participant.is_active,
        full_name=current_user.full_name,
        email=current_user.email,
        phone=current_user.phone
    )


@router.post("/registrations", response_model=RegistrationResponse)
async def register_for_event(
    registration_data: RegistrationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> RegistrationResponse:
    """
    Register current participant for an event
    """
    # Get participant profile
    result = await db.execute(
        select(Participant).where(Participant.user_id == current_user.id)
    )
    participant = result.scalar_one_or_none()
    
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participant profile not found. Please create a profile first."
        )
    
    # Check if already registered for this event
    result = await db.execute(
        select(ParticipantRegistration).where(
            and_(
                ParticipantRegistration.participant_id == participant.id,
                ParticipantRegistration.event_name == registration_data.event_name
            )
        )
    )
    existing_registration = result.scalar_one_or_none()
    
    if existing_registration:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already registered for this event"
        )
    
    # Create registration
    registration = ParticipantRegistration(
        participant_id=participant.id,
        event_name=registration_data.event_name,
        registration_status=RegistrationStatus.PENDING,
        notes=registration_data.notes
    )
    
    db.add(registration)
    await db.commit()
    await db.refresh(registration)
    
    return RegistrationResponse(
        id=registration.id,
        participant_id=registration.participant_id,
        event_name=registration.event_name,
        registration_status=registration.registration_status,
        registration_date=registration.registration_date,
        confirmation_date=registration.confirmation_date,
        notes=registration.notes,
        participant_name=current_user.full_name,
        participant_email=current_user.email
    )


@router.get("/registrations", response_model=List[RegistrationResponse])
async def get_my_registrations(
    status_filter: Optional[RegistrationStatus] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> List[RegistrationResponse]:
    """
    Get current participant's event registrations
    """
    # Get participant profile
    result = await db.execute(
        select(Participant).where(Participant.user_id == current_user.id)
    )
    participant = result.scalar_one_or_none()
    
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participant profile not found"
        )
    
    # Build query
    query = select(ParticipantRegistration).where(
        ParticipantRegistration.participant_id == participant.id
    )
    
    if status_filter:
        query = query.where(ParticipantRegistration.registration_status == status_filter)
    
    query = query.order_by(ParticipantRegistration.registration_date.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    registrations = result.scalars().all()
    
    return [
        RegistrationResponse(
            id=registration.id,
            participant_id=registration.participant_id,
            event_name=registration.event_name,
            registration_status=registration.registration_status,
            registration_date=registration.registration_date,
            confirmation_date=registration.confirmation_date,
            notes=registration.notes,
            participant_name=current_user.full_name,
            participant_email=current_user.email
        )
        for registration in registrations
    ]


@router.get("/registrations/all", response_model=List[RegistrationResponse])
async def get_all_registrations(
    event_name: Optional[str] = Query(None),
    status_filter: Optional[RegistrationStatus] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[RegistrationResponse]:
    """
    Get all event registrations (admin/organizer only)
    """
    if current_user.role not in ["admin", "organizer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Build query with joins
    query = select(ParticipantRegistration, Participant, User).join(
        Participant, ParticipantRegistration.participant_id == Participant.id
    ).join(
        User, Participant.user_id == User.id
    )
    
    if event_name:
        query = query.where(ParticipantRegistration.event_name.ilike(f"%{event_name}%"))
    if status_filter:
        query = query.where(ParticipantRegistration.registration_status == status_filter)
    
    query = query.order_by(ParticipantRegistration.registration_date.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    registration_data = result.all()
    
    return [
        RegistrationResponse(
            id=registration.id,
            participant_id=registration.participant_id,
            event_name=registration.event_name,
            registration_status=registration.registration_status,
            registration_date=registration.registration_date,
            confirmation_date=registration.confirmation_date,
            notes=registration.notes,
            participant_name=user.full_name,
            participant_email=user.email
        )
        for registration, participant, user in registration_data
    ]


@router.put("/registrations/{registration_id}", response_model=RegistrationResponse)
async def update_registration_status(
    registration_id: int,
    update_data: RegistrationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> RegistrationResponse:
    """
    Update registration status (admin/organizer only)
    """
    if current_user.role not in ["admin", "organizer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Get registration with participant and user info
    result = await db.execute(
        select(ParticipantRegistration, Participant, User).join(
            Participant, ParticipantRegistration.participant_id == Participant.id
        ).join(
            User, Participant.user_id == User.id
        ).where(ParticipantRegistration.id == registration_id)
    )
    registration_data = result.first()
    
    if not registration_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registration not found"
        )
    
    registration, participant, user = registration_data
    
    # Update registration
    registration.registration_status = update_data.registration_status
    if update_data.notes is not None:
        registration.notes = update_data.notes
    
    # Set confirmation date if status is confirmed
    if update_data.registration_status == RegistrationStatus.CONFIRMED:
        registration.confirmation_date = datetime.now()
    
    await db.commit()
    await db.refresh(registration)
    
    return RegistrationResponse(
        id=registration.id,
        participant_id=registration.participant_id,
        event_name=registration.event_name,
        registration_status=registration.registration_status,
        registration_date=registration.registration_date,
        confirmation_date=registration.confirmation_date,
        notes=registration.notes,
        participant_name=user.full_name,
        participant_email=user.email
    )
