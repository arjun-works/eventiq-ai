"""
Booths API Endpoints

This module handles booth management including allocation,
vendor assignments, and booth layout for events.
"""

from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_user, get_current_active_user
from app.models.user import User
from app.models.booth import Booth, BoothAssignment, BoothStatus, BoothType

router = APIRouter()

# Pydantic schemas for request/response
class BoothCreate(BaseModel):
    booth_number: str
    booth_type: BoothType
    location: str
    size: Optional[str] = None
    amenities: Optional[str] = None
    hourly_rate: Optional[float] = None
    daily_rate: Optional[float] = None
    description: Optional[str] = None

class BoothUpdate(BaseModel):
    booth_number: Optional[str] = None
    booth_type: Optional[BoothType] = None
    location: Optional[str] = None
    size: Optional[str] = None
    amenities: Optional[str] = None
    hourly_rate: Optional[float] = None
    daily_rate: Optional[float] = None
    description: Optional[str] = None
    status: Optional[BoothStatus] = None
    is_active: Optional[bool] = None

class BoothResponse(BaseModel):
    id: int
    booth_number: str
    booth_type: BoothType
    location: str
    size: Optional[str]
    amenities: Optional[str]
    hourly_rate: Optional[float]
    daily_rate: Optional[float]
    description: Optional[str]
    status: BoothStatus
    is_active: bool
    created_at: datetime
    
    # Current assignment info
    current_vendor: Optional[str] = None
    assignment_start: Optional[datetime] = None
    assignment_end: Optional[datetime] = None

class AssignmentCreate(BaseModel):
    booth_id: int
    vendor_name: str
    start_time: datetime
    end_time: datetime
    total_cost: Optional[float] = None
    special_requirements: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    notes: Optional[str] = None

class AssignmentUpdate(BaseModel):
    vendor_name: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    total_cost: Optional[float] = None
    special_requirements: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    notes: Optional[str] = None
    is_confirmed: Optional[bool] = None

class AssignmentResponse(BaseModel):
    id: int
    booth_id: int
    vendor_name: str
    start_time: datetime
    end_time: datetime
    total_cost: Optional[float]
    special_requirements: Optional[str]
    contact_person: Optional[str]
    contact_phone: Optional[str]
    notes: Optional[str]
    is_confirmed: bool
    assigned_by: int
    assigned_at: datetime
    
    # Booth details
    booth_number: str
    booth_location: str
    booth_type: BoothType
    
    # Assigner details
    assigner_name: str


@router.post("/", response_model=BoothResponse)
async def create_booth(
    booth_data: BoothCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> BoothResponse:
    """
    Create a new booth (admin/organizer only)
    """
    if current_user.role not in ["admin", "organizer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check if booth number already exists
    result = await db.execute(
        select(Booth).where(Booth.booth_number == booth_data.booth_number)
    )
    existing_booth = result.scalar_one_or_none()
    
    if existing_booth:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booth number already exists"
        )
    
    # Create booth
    booth = Booth(
        booth_number=booth_data.booth_number,
        booth_type=booth_data.booth_type,
        location=booth_data.location,
        size=booth_data.size,
        amenities=booth_data.amenities,
        hourly_rate=booth_data.hourly_rate,
        daily_rate=booth_data.daily_rate,
        description=booth_data.description,
        status=BoothStatus.AVAILABLE
    )
    
    db.add(booth)
    await db.commit()
    await db.refresh(booth)
    
    return BoothResponse(
        id=booth.id,
        booth_number=booth.booth_number,
        booth_type=booth.booth_type,
        location=booth.location,
        size=booth.size,
        amenities=booth.amenities,
        hourly_rate=booth.hourly_rate,
        daily_rate=booth.daily_rate,
        description=booth.description,
        status=booth.status,
        is_active=booth.is_active,
        created_at=booth.created_at
    )


@router.get("/", response_model=List[BoothResponse])
async def get_booths(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    booth_type: Optional[BoothType] = Query(None),
    status: Optional[BoothStatus] = Query(None),
    location: Optional[str] = Query(None),
    available_only: bool = Query(False),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[BoothResponse]:
    """
    Get list of booths with optional filters
    """
    # Build base query
    query = select(Booth)
    
    # Apply filters
    if booth_type:
        query = query.where(Booth.booth_type == booth_type)
    if status:
        query = query.where(Booth.status == status)
    if location:
        query = query.where(Booth.location.ilike(f"%{location}%"))
    if available_only:
        query = query.where(Booth.status == BoothStatus.AVAILABLE)
    
    query = query.where(Booth.is_active).offset(skip).limit(limit)
    
    result = await db.execute(query)
    booths = result.scalars().all()
    
    # Get current assignments for each booth
    booth_responses = []
    for booth in booths:
        # Check for current active assignment
        current_time = datetime.now()
        assignment_result = await db.execute(
            select(BoothAssignment).where(
                and_(
                    BoothAssignment.booth_id == booth.id,
                    BoothAssignment.start_time <= current_time,
                    BoothAssignment.end_time >= current_time,
                    BoothAssignment.is_confirmed == True
                )
            )
        )
        current_assignment = assignment_result.scalar_one_or_none()
        
        booth_responses.append(BoothResponse(
            id=booth.id,
            booth_number=booth.booth_number,
            booth_type=booth.booth_type,
            location=booth.location,
            size=booth.size,
            amenities=booth.amenities,
            hourly_rate=booth.hourly_rate,
            daily_rate=booth.daily_rate,
            description=booth.description,
            status=booth.status,
            is_active=booth.is_active,
            created_at=booth.created_at,
            current_vendor=current_assignment.vendor_name if current_assignment else None,
            assignment_start=current_assignment.start_time if current_assignment else None,
            assignment_end=current_assignment.end_time if current_assignment else None
        ))
    
    return booth_responses


@router.get("/{booth_id}", response_model=BoothResponse)
async def get_booth(
    booth_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> BoothResponse:
    """
    Get specific booth details
    """
    result = await db.execute(
        select(Booth).where(Booth.id == booth_id)
    )
    booth = result.scalar_one_or_none()
    
    if not booth:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booth not found"
        )
    
    # Get current assignment
    current_time = datetime.now()
    assignment_result = await db.execute(
        select(BoothAssignment).where(
            and_(
                BoothAssignment.booth_id == booth.id,
                BoothAssignment.start_time <= current_time,
                BoothAssignment.end_time >= current_time,
                BoothAssignment.is_confirmed == True
            )
        )
    )
    current_assignment = assignment_result.scalar_one_or_none()
    
    return BoothResponse(
        id=booth.id,
        booth_number=booth.booth_number,
        booth_type=booth.booth_type,
        location=booth.location,
        size=booth.size,
        amenities=booth.amenities,
        hourly_rate=booth.hourly_rate,
        daily_rate=booth.daily_rate,
        description=booth.description,
        status=booth.status,
        is_active=booth.is_active,
        created_at=booth.created_at,
        current_vendor=current_assignment.vendor_name if current_assignment else None,
        assignment_start=current_assignment.start_time if current_assignment else None,
        assignment_end=current_assignment.end_time if current_assignment else None
    )


@router.put("/{booth_id}", response_model=BoothResponse)
async def update_booth(
    booth_id: int,
    update_data: BoothUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> BoothResponse:
    """
    Update booth details (admin/organizer only)
    """
    if current_user.role not in ["admin", "organizer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    result = await db.execute(
        select(Booth).where(Booth.id == booth_id)
    )
    booth = result.scalar_one_or_none()
    
    if not booth:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booth not found"
        )
    
    # Check if booth number is being changed and if it already exists
    if update_data.booth_number and update_data.booth_number != booth.booth_number:
        result = await db.execute(
            select(Booth).where(Booth.booth_number == update_data.booth_number)
        )
        existing_booth = result.scalar_one_or_none()
        
        if existing_booth:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Booth number already exists"
            )
    
    # Update fields
    update_fields = update_data.dict(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(booth, field, value)
    
    await db.commit()
    await db.refresh(booth)
    
    return BoothResponse(
        id=booth.id,
        booth_number=booth.booth_number,
        booth_type=booth.booth_type,
        location=booth.location,
        size=booth.size,
        amenities=booth.amenities,
        hourly_rate=booth.hourly_rate,
        daily_rate=booth.daily_rate,
        description=booth.description,
        status=booth.status,
        is_active=booth.is_active,
        created_at=booth.created_at
    )


@router.post("/assignments", response_model=AssignmentResponse)
async def create_booth_assignment(
    assignment_data: AssignmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> AssignmentResponse:
    """
    Assign booth to vendor (admin/organizer only)
    """
    if current_user.role not in ["admin", "organizer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Verify booth exists
    result = await db.execute(
        select(Booth).where(Booth.id == assignment_data.booth_id)
    )
    booth = result.scalar_one_or_none()
    
    if not booth:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booth not found"
        )
    
    # Check for conflicting assignments
    result = await db.execute(
        select(BoothAssignment).where(
            and_(
                BoothAssignment.booth_id == assignment_data.booth_id,
                BoothAssignment.is_confirmed == True,
                # Check for time overlap
                BoothAssignment.start_time < assignment_data.end_time,
                BoothAssignment.end_time > assignment_data.start_time
            )
        )
    )
    conflicting_assignment = result.scalar_one_or_none()
    
    if conflicting_assignment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booth has conflicting assignment during this time period"
        )
    
    # Validate time range
    if assignment_data.start_time >= assignment_data.end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time must be before end time"
        )
    
    # Create assignment
    assignment = BoothAssignment(
        booth_id=assignment_data.booth_id,
        vendor_name=assignment_data.vendor_name,
        start_time=assignment_data.start_time,
        end_time=assignment_data.end_time,
        total_cost=assignment_data.total_cost,
        special_requirements=assignment_data.special_requirements,
        contact_person=assignment_data.contact_person,
        contact_phone=assignment_data.contact_phone,
        notes=assignment_data.notes,
        assigned_by=current_user.id,
        is_confirmed=False  # Requires confirmation
    )
    
    db.add(assignment)
    
    # Update booth status
    booth.status = BoothStatus.RESERVED
    
    await db.commit()
    await db.refresh(assignment)
    
    return AssignmentResponse(
        id=assignment.id,
        booth_id=assignment.booth_id,
        vendor_name=assignment.vendor_name,
        start_time=assignment.start_time,
        end_time=assignment.end_time,
        total_cost=assignment.total_cost,
        special_requirements=assignment.special_requirements,
        contact_person=assignment.contact_person,
        contact_phone=assignment.contact_phone,
        notes=assignment.notes,
        is_confirmed=assignment.is_confirmed,
        assigned_by=assignment.assigned_by,
        assigned_at=assignment.assigned_at,
        booth_number=booth.booth_number,
        booth_location=booth.location,
        booth_type=booth.booth_type,
        assigner_name=current_user.full_name
    )


@router.get("/assignments", response_model=List[AssignmentResponse])
async def get_booth_assignments(
    booth_id: Optional[int] = Query(None),
    vendor_name: Optional[str] = Query(None),
    confirmed_only: bool = Query(False),
    upcoming_only: bool = Query(False),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[AssignmentResponse]:
    """
    Get booth assignments with optional filters
    """
    if current_user.role not in ["admin", "organizer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Build query with joins
    query = select(BoothAssignment, Booth, User.full_name.label("assigner_name")).join(
        Booth, BoothAssignment.booth_id == Booth.id
    ).join(
        User, BoothAssignment.assigned_by == User.id
    )
    
    # Apply filters
    if booth_id:
        query = query.where(BoothAssignment.booth_id == booth_id)
    if vendor_name:
        query = query.where(BoothAssignment.vendor_name.ilike(f"%{vendor_name}%"))
    if confirmed_only:
        query = query.where(BoothAssignment.is_confirmed == True)
    if upcoming_only:
        current_time = datetime.now()
        query = query.where(BoothAssignment.start_time > current_time)
    
    query = query.order_by(BoothAssignment.start_time.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    assignment_data = result.all()
    
    return [
        AssignmentResponse(
            id=assignment.id,
            booth_id=assignment.booth_id,
            vendor_name=assignment.vendor_name,
            start_time=assignment.start_time,
            end_time=assignment.end_time,
            total_cost=assignment.total_cost,
            special_requirements=assignment.special_requirements,
            contact_person=assignment.contact_person,
            contact_phone=assignment.contact_phone,
            notes=assignment.notes,
            is_confirmed=assignment.is_confirmed,
            assigned_by=assignment.assigned_by,
            assigned_at=assignment.assigned_at,
            booth_number=booth.booth_number,
            booth_location=booth.location,
            booth_type=booth.booth_type,
            assigner_name=assigner_name
        )
        for assignment, booth, assigner_name in assignment_data
    ]


@router.put("/assignments/{assignment_id}/confirm", response_model=AssignmentResponse)
async def confirm_booth_assignment(
    assignment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> AssignmentResponse:
    """
    Confirm booth assignment (admin/organizer only)
    """
    if current_user.role not in ["admin", "organizer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Get assignment with booth and assigner info
    result = await db.execute(
        select(BoothAssignment, Booth, User.full_name.label("assigner_name"))
        .join(Booth, BoothAssignment.booth_id == Booth.id)
        .join(User, BoothAssignment.assigned_by == User.id)
        .where(BoothAssignment.id == assignment_id)
    )
    assignment_data = result.first()
    
    if not assignment_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    assignment, booth, assigner_name = assignment_data
    
    if assignment.is_confirmed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assignment is already confirmed"
        )
    
    # Confirm assignment
    assignment.is_confirmed = True
    
    # Update booth status to occupied if assignment is current
    current_time = datetime.now()
    if assignment.start_time <= current_time <= assignment.end_time:
        booth.status = BoothStatus.OCCUPIED
    else:
        booth.status = BoothStatus.RESERVED
    
    await db.commit()
    await db.refresh(assignment)
    
    return AssignmentResponse(
        id=assignment.id,
        booth_id=assignment.booth_id,
        vendor_name=assignment.vendor_name,
        start_time=assignment.start_time,
        end_time=assignment.end_time,
        total_cost=assignment.total_cost,
        special_requirements=assignment.special_requirements,
        contact_person=assignment.contact_person,
        contact_phone=assignment.contact_phone,
        notes=assignment.notes,
        is_confirmed=assignment.is_confirmed,
        assigned_by=assignment.assigned_by,
        assigned_at=assignment.assigned_at,
        booth_number=booth.booth_number,
        booth_location=booth.location,
        booth_type=booth.booth_type,
        assigner_name=assigner_name
    )
