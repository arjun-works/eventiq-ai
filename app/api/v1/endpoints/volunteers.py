"""
Volunteers API Endpoints

This module handles volunteer management operations including registration,
attendance tracking, and role assignment.
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
from app.models.volunteer import Volunteer, VolunteerAttendance, VolunteerRole

router = APIRouter()

class VolunteerCreate(BaseModel):
    volunteer_role: VolunteerRole
    skills: Optional[str] = None
    availability: Optional[str] = None
    emergency_contact: Optional[str] = None
    t_shirt_size: Optional[str] = None
    dietary_restrictions: Optional[str] = None
    special_requirements: Optional[str] = None

class VolunteerResponse(BaseModel):
    id: int
    user_id: int
    volunteer_role: VolunteerRole
    skills: Optional[str]
    availability: Optional[str]
    emergency_contact: Optional[str]
    t_shirt_size: Optional[str]
    dietary_restrictions: Optional[str]
    special_requirements: Optional[str]
    is_active: bool
    total_hours: int
    rating: Optional[int]
    created_at: datetime
    
    # User details
    full_name: str
    email: str
    phone: Optional[str]

class AttendanceCreate(BaseModel):
    check_in_location: Optional[str] = None
    notes: Optional[str] = None

class AttendanceResponse(BaseModel):
    id: int
    volunteer_id: int
    check_in_time: datetime
    check_out_time: Optional[datetime]
    hours_worked: Optional[float]
    check_in_location: Optional[str]
    check_out_location: Optional[str]
    notes: Optional[str]
    created_at: datetime


@router.post("/", response_model=VolunteerResponse)
async def register_volunteer(
    volunteer_data: VolunteerCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> VolunteerResponse:
    """
    Register current user as a volunteer
    """
    # Check if user is already registered as volunteer
    result = await db.execute(
        select(Volunteer).where(Volunteer.user_id == current_user.id)
    )
    existing_volunteer = result.scalar_one_or_none()
    
    if existing_volunteer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already registered as a volunteer"
        )
    
    # Create new volunteer record
    volunteer = Volunteer(
        user_id=current_user.id,
        volunteer_role=volunteer_data.volunteer_role,
        skills=volunteer_data.skills,
        availability=volunteer_data.availability,
        emergency_contact=volunteer_data.emergency_contact,
        t_shirt_size=volunteer_data.t_shirt_size,
        dietary_restrictions=volunteer_data.dietary_restrictions,
        special_requirements=volunteer_data.special_requirements
    )
    
    db.add(volunteer)
    await db.commit()
    await db.refresh(volunteer)
    
    return VolunteerResponse(
        id=volunteer.id,
        user_id=volunteer.user_id,
        volunteer_role=volunteer.volunteer_role,
        skills=volunteer.skills,
        availability=volunteer.availability,
        emergency_contact=volunteer.emergency_contact,
        t_shirt_size=volunteer.t_shirt_size,
        dietary_restrictions=volunteer.dietary_restrictions,
        special_requirements=volunteer.special_requirements,
        is_active=volunteer.is_active,
        total_hours=volunteer.total_hours,
        rating=volunteer.rating,
        created_at=volunteer.created_at,
        full_name=current_user.full_name,
        email=current_user.email,
        phone=current_user.phone
    )


@router.get("/", response_model=List[VolunteerResponse])
async def get_volunteers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    role: Optional[VolunteerRole] = Query(None),
    active_only: bool = Query(True),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[VolunteerResponse]:
    """
    Get list of volunteers (admin/organizer only)
    """
    if current_user.role not in ["admin", "organizer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Build query
    query = select(Volunteer, User).join(User, Volunteer.user_id == User.id)
    
    if role:
        query = query.where(Volunteer.volunteer_role == role)
    if active_only:
        query = query.where(Volunteer.is_active)
    
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    volunteers_with_users = result.all()
    
    return [
        VolunteerResponse(
            id=volunteer.id,
            user_id=volunteer.user_id,
            volunteer_role=volunteer.volunteer_role,
            skills=volunteer.skills,
            availability=volunteer.availability,
            emergency_contact=volunteer.emergency_contact,
            t_shirt_size=volunteer.t_shirt_size,
            dietary_restrictions=volunteer.dietary_restrictions,
            special_requirements=volunteer.special_requirements,
            is_active=volunteer.is_active,
            total_hours=volunteer.total_hours,
            rating=volunteer.rating,
            created_at=volunteer.created_at,
            full_name=user.full_name,
            email=user.email,
            phone=user.phone
        )
        for volunteer, user in volunteers_with_users
    ]


@router.get("/me", response_model=VolunteerResponse)
async def get_my_volunteer_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> VolunteerResponse:
    """
    Get current user's volunteer profile
    """
    result = await db.execute(
        select(Volunteer).where(Volunteer.user_id == current_user.id)
    )
    volunteer = result.scalar_one_or_none()
    
    if not volunteer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Volunteer profile not found"
        )
    
    return VolunteerResponse(
        id=volunteer.id,
        user_id=volunteer.user_id,
        volunteer_role=volunteer.volunteer_role,
        skills=volunteer.skills,
        availability=volunteer.availability,
        emergency_contact=volunteer.emergency_contact,
        t_shirt_size=volunteer.t_shirt_size,
        dietary_restrictions=volunteer.dietary_restrictions,
        special_requirements=volunteer.special_requirements,
        is_active=volunteer.is_active,
        total_hours=volunteer.total_hours,
        rating=volunteer.rating,
        created_at=volunteer.created_at,
        full_name=current_user.full_name,
        email=current_user.email,
        phone=current_user.phone
    )


@router.post("/attendance/checkin", response_model=AttendanceResponse)
async def check_in(
    attendance_data: AttendanceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> AttendanceResponse:
    """
    Check in volunteer for attendance
    """
    # Get volunteer profile
    result = await db.execute(
        select(Volunteer).where(Volunteer.user_id == current_user.id)
    )
    volunteer = result.scalar_one_or_none()
    
    if not volunteer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Volunteer profile not found"
        )
    
    # Check if already checked in today
    today = date.today()
    result = await db.execute(
        select(VolunteerAttendance).where(
            and_(
                VolunteerAttendance.volunteer_id == volunteer.id,
                VolunteerAttendance.check_in_time >= datetime.combine(today, datetime.min.time()),
                VolunteerAttendance.check_out_time is None
            )
        )
    )
    existing_checkin = result.scalar_one_or_none()
    
    if existing_checkin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already checked in today"
        )
    
    # Create attendance record
    attendance = VolunteerAttendance(
        volunteer_id=volunteer.id,
        check_in_time=datetime.now(),
        check_in_location=attendance_data.check_in_location,
        notes=attendance_data.notes
    )
    
    db.add(attendance)
    await db.commit()
    await db.refresh(attendance)
    
    return AttendanceResponse(
        id=attendance.id,
        volunteer_id=attendance.volunteer_id,
        check_in_time=attendance.check_in_time,
        check_out_time=attendance.check_out_time,
        hours_worked=attendance.hours_worked,
        check_in_location=attendance.check_in_location,
        check_out_location=attendance.check_out_location,
        notes=attendance.notes,
        created_at=attendance.created_at
    )


@router.post("/attendance/checkout", response_model=AttendanceResponse)
async def check_out(
    checkout_location: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> AttendanceResponse:
    """
    Check out volunteer and calculate hours worked
    """
    # Get volunteer profile
    result = await db.execute(
        select(Volunteer).where(Volunteer.user_id == current_user.id)
    )
    volunteer = result.scalar_one_or_none()
    
    if not volunteer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Volunteer profile not found"
        )
    
    # Find today's check-in record
    today = date.today()
    result = await db.execute(
        select(VolunteerAttendance).where(
            and_(
                VolunteerAttendance.volunteer_id == volunteer.id,
                VolunteerAttendance.check_in_time >= datetime.combine(today, datetime.min.time()),
                VolunteerAttendance.check_out_time is None
            )
        )
    )
    attendance = result.scalar_one_or_none()
    
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No check-in record found for today"
        )
    
    # Update attendance with check-out
    checkout_time = datetime.now()
    hours_worked = (checkout_time - attendance.check_in_time).total_seconds() / 3600
    
    attendance.check_out_time = checkout_time
    attendance.check_out_location = checkout_location
    attendance.hours_worked = round(hours_worked, 2)
    
    # Update volunteer total hours
    volunteer.total_hours += int(hours_worked)
    
    await db.commit()
    await db.refresh(attendance)
    
    return AttendanceResponse(
        id=attendance.id,
        volunteer_id=attendance.volunteer_id,
        check_in_time=attendance.check_in_time,
        check_out_time=attendance.check_out_time,
        hours_worked=attendance.hours_worked,
        check_in_location=attendance.check_in_location,
        check_out_location=attendance.check_out_location,
        notes=attendance.notes,
        created_at=attendance.created_at
    )


@router.get("/attendance", response_model=List[AttendanceResponse])
async def get_attendance_history(
    volunteer_id: Optional[int] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[AttendanceResponse]:
    """
    Get attendance history
    """
    # If volunteer_id is provided, check permissions
    if volunteer_id and current_user.role not in ["admin", "organizer"]:
        # Users can only see their own attendance
        result = await db.execute(
            select(Volunteer).where(Volunteer.user_id == current_user.id)
        )
        user_volunteer = result.scalar_one_or_none()
        if not user_volunteer or user_volunteer.id != volunteer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    # If no volunteer_id provided, get current user's volunteer record
    if not volunteer_id:
        result = await db.execute(
            select(Volunteer).where(Volunteer.user_id == current_user.id)
        )
        volunteer = result.scalar_one_or_none()
        if not volunteer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Volunteer profile not found"
            )
        volunteer_id = volunteer.id
    
    # Build query
    query = select(VolunteerAttendance).where(VolunteerAttendance.volunteer_id == volunteer_id)
    
    if start_date:
        query = query.where(VolunteerAttendance.check_in_time >= datetime.combine(start_date, datetime.min.time()))
    if end_date:
        query = query.where(VolunteerAttendance.check_in_time <= datetime.combine(end_date, datetime.max.time()))
    
    query = query.order_by(VolunteerAttendance.check_in_time.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    attendance_records = result.scalars().all()
    
    return [
        AttendanceResponse(
            id=record.id,
            volunteer_id=record.volunteer_id,
            check_in_time=record.check_in_time,
            check_out_time=record.check_out_time,
            hours_worked=record.hours_worked,
            check_in_location=record.check_in_location,
            check_out_location=record.check_out_location,
            notes=record.notes,
            created_at=record.created_at
        )
        for record in attendance_records
    ]
