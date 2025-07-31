"""
Certificate management endpoints for EventIQ
Handles certificate generation for volunteers and participants
"""

from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.responses import StreamingResponse
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import io
from datetime import datetime
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from services.certificate_generator import CertificateGenerator, generate_certificate_for_volunteer

router = APIRouter()

class CertificateRequest(BaseModel):
    volunteer_id: int
    event_name: Optional[str] = "Campus Event 2025"
    organization: Optional[str] = "EventIQ Organization"

class CertificateResponse(BaseModel):
    certificate_id: str
    volunteer_name: str
    generated_date: str
    download_url: str

# Sample volunteer data for certificate generation
SAMPLE_VOLUNTEERS = {
    1: {
        'id': 1,
        'full_name': 'John Smith',
        'email': 'john.smith@example.com',
        'volunteer_role': 'Registration Coordinator',
        'total_hours': 25,
        'booth_assignment': 'Registration Desk',
        'skills': ['Communication', 'Organization'],
        'is_active': True
    },
    2: {
        'id': 2,
        'full_name': 'Sarah Johnson',
        'email': 'sarah.johnson@example.com',
        'volunteer_role': 'Event Setup Assistant',
        'total_hours': 18,
        'booth_assignment': 'Main Stage Area',
        'skills': ['Technical Setup', 'Coordination'],
        'is_active': True
    },
    3: {
        'id': 3,
        'full_name': 'Mike Wilson',
        'email': 'mike.wilson@example.com',
        'volunteer_role': 'Information Desk Volunteer',
        'total_hours': 22,
        'booth_assignment': 'Information Booth',
        'skills': ['Customer Service', 'Problem Solving'],
        'is_active': True
    }
}

@router.get("/")
async def get_certificates():
    """Get all available certificates"""
    certificates = []
    for vol_id, volunteer in SAMPLE_VOLUNTEERS.items():
        if volunteer['total_hours'] > 0:  # Only volunteers with hours can get certificates
            cert_id = f"CERT-{vol_id}-{datetime.now().strftime('%Y%m')}"
            certificates.append({
                "certificate_id": cert_id,
                "volunteer_id": vol_id,
                "volunteer_name": volunteer['full_name'],
                "volunteer_role": volunteer['volunteer_role'],
                "total_hours": volunteer['total_hours'],
                "eligible": True,
                "generated_date": datetime.now().isoformat()
            })
    
    return {"certificates": certificates, "total": len(certificates)}

@router.post("/generate/{volunteer_id}")
async def generate_certificate(volunteer_id: int, request: CertificateRequest = None):
    """Generate a certificate for a specific volunteer"""
    if volunteer_id not in SAMPLE_VOLUNTEERS:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    
    volunteer = SAMPLE_VOLUNTEERS[volunteer_id]
    
    if volunteer['total_hours'] <= 0:
        raise HTTPException(status_code=400, detail="Volunteer must have logged hours to receive certificate")
    
    try:
        # Generate the certificate PDF
        pdf_bytes = generate_certificate_for_volunteer(volunteer_id, volunteer)
        
        # Create certificate record
        cert_id = f"CERT-{volunteer_id}-{datetime.now().strftime('%Y%m%d%H%M')}"
        
        # Return the PDF as a downloadable response
        headers = {
            'Content-Disposition': f'attachment; filename="{volunteer["full_name"]}_Certificate.pdf"'
        }
        
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type='application/pdf',
            headers=headers
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating certificate: {str(e)}")

@router.get("/volunteer/{volunteer_id}")
async def get_volunteer_certificate_info(volunteer_id: int):
    """Get certificate eligibility and information for a volunteer"""
    if volunteer_id not in SAMPLE_VOLUNTEERS:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    
    volunteer = SAMPLE_VOLUNTEERS[volunteer_id]
    cert_id = f"CERT-{volunteer_id}-{datetime.now().strftime('%Y%m')}"
    
    return {
        "volunteer_id": volunteer_id,
        "volunteer_name": volunteer['full_name'],
        "volunteer_role": volunteer['volunteer_role'],
        "total_hours": volunteer['total_hours'],
        "booth_assignment": volunteer['booth_assignment'],
        "eligible_for_certificate": volunteer['total_hours'] > 0,
        "certificate_id": cert_id if volunteer['total_hours'] > 0 else None,
        "requirements_met": {
            "minimum_hours": volunteer['total_hours'] >= 5,  # Minimum 5 hours required
            "active_status": volunteer['is_active']
        }
    }

@router.post("/bulk-generate")
async def generate_bulk_certificates():
    """Generate certificates for all eligible volunteers"""
    eligible_volunteers = []
    
    for vol_id, volunteer in SAMPLE_VOLUNTEERS.items():
        if volunteer['total_hours'] > 0 and volunteer['is_active']:
            eligible_volunteers.append({
                "volunteer_id": vol_id,
                "volunteer_name": volunteer['full_name'],
                "total_hours": volunteer['total_hours'],
                "certificate_id": f"CERT-{vol_id}-{datetime.now().strftime('%Y%m%d')}"
            })
    
    return {
        "message": f"Bulk certificate generation initiated for {len(eligible_volunteers)} volunteers",
        "eligible_volunteers": eligible_volunteers,
        "generated_date": datetime.now().isoformat()
    }

@router.get("/download/{certificate_id}")
async def download_certificate(certificate_id: str):
    """Download a certificate by its ID"""
    # Extract volunteer ID from certificate ID
    try:
        parts = certificate_id.split("-")
        if len(parts) >= 2 and parts[0] == "CERT":
            volunteer_id = int(parts[1])
            
            if volunteer_id in SAMPLE_VOLUNTEERS:
                volunteer = SAMPLE_VOLUNTEERS[volunteer_id]
                pdf_bytes = generate_certificate_for_volunteer(volunteer_id, volunteer)
                
                headers = {
                    'Content-Disposition': f'attachment; filename="{certificate_id}.pdf"'
                }
                
                return StreamingResponse(
                    io.BytesIO(pdf_bytes),
                    media_type='application/pdf',
                    headers=headers
                )
    except (ValueError, IndexError):
        pass
    
    raise HTTPException(status_code=404, detail="Certificate not found")

@router.get("/stats")
async def get_certificate_stats():
    """Get certificate generation statistics"""
    total_volunteers = len(SAMPLE_VOLUNTEERS)
    eligible_count = sum(1 for v in SAMPLE_VOLUNTEERS.values() if v['total_hours'] > 0)
    total_hours = sum(v['total_hours'] for v in SAMPLE_VOLUNTEERS.values())
    
    return {
        "total_volunteers": total_volunteers,
        "eligible_for_certificates": eligible_count,
        "certificates_generated": eligible_count,  # Assuming all eligible have been generated
        "total_volunteer_hours": total_hours,
        "average_hours_per_volunteer": total_hours / total_volunteers if total_volunteers > 0 else 0,
        "certificate_types": ["Volunteer Service Certificate"],
        "last_updated": datetime.now().isoformat()
    }
