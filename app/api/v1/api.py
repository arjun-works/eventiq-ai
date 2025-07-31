"""
API v1 Router

Main router that includes all API endpoints for the EventIQ system.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth, users, volunteers, participants, budget, 
    booths, vendors, workflows, feedback, certificates, 
    media, admin, analytics
)

api_router = APIRouter()

# Authentication routes
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# User management routes
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Module-specific routes
api_router.include_router(volunteers.router, prefix="/volunteers", tags=["volunteers"])
api_router.include_router(participants.router, prefix="/participants", tags=["participants"])
api_router.include_router(budget.router, prefix="/budget", tags=["budget"])
api_router.include_router(booths.router, prefix="/booths", tags=["booths"])
api_router.include_router(vendors.router, prefix="/vendors", tags=["vendors"])
api_router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
api_router.include_router(feedback.router, prefix="/feedback", tags=["feedback"])
api_router.include_router(certificates.router, prefix="/certificates", tags=["certificates"])
api_router.include_router(media.router, prefix="/media", tags=["media"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
