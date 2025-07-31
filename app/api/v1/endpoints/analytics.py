"""
Analytics API Endpoints

This module provides analytics and reporting functionality
for administrators and organizers to monitor event metrics.
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

# Pydantic schemas for response
class DashboardMetrics(BaseModel):
    total_participants: int
    total_volunteers: int
    total_booths: int
    occupied_booths: int
    total_budget: float
    spent_amount: float
    pending_expenses: int
    confirmed_registrations: int
    pending_registrations: int
    recent_activities: List[Dict[str, Any]]

class FinancialSummary(BaseModel):
    budget_overview: Dict[str, Any]
    spending_by_category: List[Dict[str, Any]]
    recent_expenses: List[Dict[str, Any]]

class VolunteerMetrics(BaseModel):
    total_volunteers: int
    active_volunteers: int
    total_hours_worked: float
    average_hours_per_volunteer: float
    volunteers_by_role: List[Dict[str, Any]]
    recent_check_ins: List[Dict[str, Any]]


@router.get("/dashboard", response_model=DashboardMetrics)
async def get_dashboard_metrics(
    current_user: User = Depends(get_current_user)
) -> DashboardMetrics:
    """
    Get overall dashboard metrics (admin/organizer only)
    """
    if current_user.role not in ["admin", "organizer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Return sample data for now
    return DashboardMetrics(
        total_participants=25,
        total_volunteers=8,
        total_booths=6,
        occupied_booths=2,
        total_budget=50000.00,
        spent_amount=28500.00,
        pending_expenses=3,
        confirmed_registrations=18,
        pending_registrations=7,
        recent_activities=[
            {
                "type": "registration",
                "message": "New participant registered for TechCon 2024",
                "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
                "user": "Carol Davis"
            },
            {
                "type": "expense",
                "message": "Expense approved: Sound system rental",
                "timestamp": (datetime.now() - timedelta(hours=4)).isoformat(),
                "amount": 3500.00
            },
            {
                "type": "volunteer",
                "message": "Volunteer checked in for duty",
                "timestamp": (datetime.now() - timedelta(hours=6)).isoformat(),
                "volunteer": "Alice Johnson"
            },
            {
                "type": "booth",
                "message": "Booth A-01 assigned to TechCorp Solutions",
                "timestamp": (datetime.now() - timedelta(days=1)).isoformat(),
                "booth": "A-01"
            }
        ]
    )


@router.get("/financial", response_model=FinancialSummary)
async def get_financial_summary(
    current_user: User = Depends(get_current_user)
) -> FinancialSummary:
    """
    Get financial analytics summary (admin/organizer only)
    """
    if current_user.role not in ["admin", "organizer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return FinancialSummary(
        budget_overview={
            "total_budget": 50000.00,
            "allocated": 45000.00,
            "spent": 28500.00,
            "remaining": 21500.00,
            "allocation_percentage": 90.0,
            "spent_percentage": 57.0
        },
        spending_by_category=[
            {"category": "Venue", "allocated": 15000.00, "spent": 14500.00, "percentage": 96.7},
            {"category": "Catering", "allocated": 12000.00, "spent": 4000.00, "percentage": 33.3},
            {"category": "Technology", "allocated": 8000.00, "spent": 3500.00, "percentage": 43.8},
            {"category": "Marketing", "allocated": 5000.00, "spent": 2200.00, "percentage": 44.0},
            {"category": "Speakers", "allocated": 7000.00, "spent": 5000.00, "percentage": 71.4}
        ],
        recent_expenses=[
            {
                "date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
                "amount": 1200.00,
                "category": "Catering",
                "vendor": "Coffee Express",
                "status": "pending"
            },
            {
                "date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
                "amount": 2200.00,
                "category": "Marketing",
                "vendor": "Digital Marketing Inc.",
                "status": "approved"
            },
            {
                "date": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
                "amount": 5000.00,
                "category": "Speakers",
                "vendor": "Dr. Jane Speaker",
                "status": "approved"
            }
        ]
    )


@router.get("/volunteers", response_model=VolunteerMetrics)
async def get_volunteer_metrics(
    current_user: User = Depends(get_current_user)
) -> VolunteerMetrics:
    """
    Get volunteer analytics metrics (admin/organizer only)
    """
    if current_user.role not in ["admin", "organizer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return VolunteerMetrics(
        total_volunteers=8,
        active_volunteers=6,
        total_hours_worked=156.5,
        average_hours_per_volunteer=19.6,
        volunteers_by_role=[
            {"role": "coordinator", "count": 2, "hours": 48.0},
            {"role": "usher", "count": 3, "hours": 42.0},
            {"role": "technical", "count": 2, "hours": 38.5},
            {"role": "registration", "count": 1, "hours": 28.0}
        ],
        recent_check_ins=[
            {
                "volunteer": "Alice Johnson",
                "role": "coordinator",
                "check_in_time": (datetime.now() - timedelta(hours=2)).isoformat(),
                "location": "Main Entrance"
            },
            {
                "volunteer": "Bob Smith",
                "role": "usher",
                "check_in_time": (datetime.now() - timedelta(hours=3)).isoformat(),
                "location": "Registration Desk"
            }
        ]
    )


@router.get("/export/participants")
async def export_participants_data(
    current_user: User = Depends(get_current_user)
):
    """
    Export participants data as CSV (admin/organizer only)
    """
    if current_user.role not in ["admin", "organizer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return {
        "message": "Participants data export initiated",
        "download_url": "/downloads/participants_export.csv",
        "estimated_completion": (datetime.now() + timedelta(minutes=5)).isoformat()
    }


@router.get("/export/financial")
async def export_financial_data(
    current_user: User = Depends(get_current_user)
):
    """
    Export financial data as Excel (admin/organizer only)
    """
    if current_user.role not in ["admin", "organizer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return {
        "message": "Financial data export initiated",
        "download_url": "/downloads/financial_export.xlsx",
        "estimated_completion": (datetime.now() + timedelta(minutes=3)).isoformat()
    }
