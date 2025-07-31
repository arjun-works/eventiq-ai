"""
Certificate Generation Service for EventIQ
Generates PDF certificates for volunteers using ReportLab
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.units import inch
from reportlab.lib.colors import Color, blue, black, gold
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
from datetime import datetime
from typing import Dict, Any, Optional
import base64

class CertificateGenerator:
    """Generate professional PDF certificates for EventIQ volunteers"""
    
    def __init__(self):
        self.page_size = A4
        self.margin = 0.75 * inch
        
    def generate_volunteer_certificate(
        self, 
        volunteer_data: Dict[str, Any], 
        event_name: str = "Campus Event 2025",
        organization: str = "EventIQ Organization"
    ) -> bytes:
        """
        Generate a professional certificate for a volunteer
        
        Args:
            volunteer_data: Dictionary containing volunteer information
            event_name: Name of the event
            organization: Organization issuing the certificate
            
        Returns:
            bytes: PDF certificate as bytes
        """
        # Create a bytes buffer for the PDF
        buffer = io.BytesIO()
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=self.page_size,
            rightMargin=self.margin,
            leftMargin=self.margin,
            topMargin=self.margin,
            bottomMargin=self.margin
        )
        
        # Build the certificate content
        story = self._build_certificate_content(volunteer_data, event_name, organization)
        
        # Build the PDF
        doc.build(story, onFirstPage=self._add_certificate_border)
        
        # Get the PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def _build_certificate_content(
        self, 
        volunteer_data: Dict[str, Any], 
        event_name: str, 
        organization: str
    ) -> list:
        """Build the content elements for the certificate"""
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=blue,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=18,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=black
        )
        
        name_style = ParagraphStyle(
            'VolunteerName',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=blue,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CertificateBody',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=15,
            alignment=TA_CENTER,
            leading=18
        )
        
        # Certificate Header
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(f"🏆 CERTIFICATE OF APPRECIATION", title_style))
        story.append(Paragraph(f"<i>{organization}</i>", subtitle_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Certificate Body
        story.append(Paragraph("This is to certify that", body_style))
        story.append(Paragraph(f"<b>{volunteer_data.get('full_name', 'Volunteer Name')}</b>", name_style))
        
        story.append(Paragraph(
            f"has successfully completed volunteer service for <b>{event_name}</b> "
            f"with dedication and excellence.", 
            body_style
        ))
        
        # Volunteer Details Table
        volunteer_details = [
            ["Volunteer Role:", volunteer_data.get('volunteer_role', 'General Volunteer')],
            ["Total Hours Served:", f"{volunteer_data.get('total_hours', 0)} hours"],
            ["Booth Assignment:", volunteer_data.get('booth_assignment', 'Multiple Locations')],
            ["Service Period:", volunteer_data.get('service_period', 'Event Duration')],
            ["Performance Rating:", volunteer_data.get('rating', 'Excellent')]
        ]
        
        table = Table(volunteer_details, colWidths=[2.5*inch, 3*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [None, Color(0.95, 0.95, 0.95)]),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(Spacer(1, 0.3*inch))
        story.append(table)
        story.append(Spacer(1, 0.4*inch))
        
        # Recognition Statement
        story.append(Paragraph(
            "We recognize your valuable contribution and commitment to making this event successful. "
            "Your efforts have made a significant impact on our community.",
            body_style
        ))
        
        # Date and Signatures
        story.append(Spacer(1, 0.5*inch))
        
        current_date = datetime.now().strftime("%B %d, %Y")
        
        signature_data = [
            [f"Date: {current_date}", "", "Authorized Signature"],
            ["", "", "Event Organizer"]
        ]
        
        sig_table = Table(signature_data, colWidths=[2*inch, 1*inch, 2*inch])
        sig_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        story.append(sig_table)
        
        # Certificate ID
        cert_id = f"CERT-{volunteer_data.get('id', '000')}-{datetime.now().strftime('%Y%m')}"
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph(f"Certificate ID: {cert_id}", ParagraphStyle(
            'CertID',
            parent=styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=Color(0.5, 0.5, 0.5)
        )))
        
        return story
    
    def _add_certificate_border(self, canvas, doc):
        """Add decorative border to the certificate"""
        canvas.saveState()
        
        # Get page dimensions
        width, height = doc.pagesize
        
        # Draw outer border
        canvas.setStrokeColor(blue)
        canvas.setLineWidth(3)
        canvas.rect(0.5*inch, 0.5*inch, width-1*inch, height-1*inch)
        
        # Draw inner border
        canvas.setStrokeColor(gold)
        canvas.setLineWidth(1)
        canvas.rect(0.6*inch, 0.6*inch, width-1.2*inch, height-1.2*inch)
        
        # Add corner decorations
        self._add_corner_decorations(canvas, width, height)
        
        canvas.restoreState()
    
    def _add_corner_decorations(self, canvas, width, height):
        """Add decorative elements to certificate corners"""
        canvas.setStrokeColor(gold)
        canvas.setLineWidth(2)
        
        # Top-left corner
        canvas.line(0.5*inch, height-0.8*inch, 0.8*inch, height-0.8*inch)
        canvas.line(0.8*inch, height-0.5*inch, 0.8*inch, height-0.8*inch)
        
        # Top-right corner
        canvas.line(width-0.8*inch, height-0.8*inch, width-0.5*inch, height-0.8*inch)
        canvas.line(width-0.8*inch, height-0.5*inch, width-0.8*inch, height-0.8*inch)
        
        # Bottom-left corner
        canvas.line(0.5*inch, 0.8*inch, 0.8*inch, 0.8*inch)
        canvas.line(0.8*inch, 0.5*inch, 0.8*inch, 0.8*inch)
        
        # Bottom-right corner
        canvas.line(width-0.8*inch, 0.8*inch, width-0.5*inch, 0.8*inch)
        canvas.line(width-0.8*inch, 0.5*inch, width-0.8*inch, 0.8*inch)

def generate_certificate_for_volunteer(volunteer_id: int, volunteer_data: Dict[str, Any]) -> bytes:
    """
    Helper function to generate certificate for a specific volunteer
    
    Args:
        volunteer_id: ID of the volunteer
        volunteer_data: Volunteer information dictionary
        
    Returns:
        bytes: PDF certificate as bytes
    """
    generator = CertificateGenerator()
    
    # Add booth assignment if available
    if 'booth_assignments' in volunteer_data:
        booths = volunteer_data['booth_assignments']
        if booths:
            volunteer_data['booth_assignment'] = ", ".join([booth['booth_name'] for booth in booths])
    
    # Add service period
    volunteer_data['service_period'] = "Event Duration 2025"
    volunteer_data['rating'] = "Excellent"
    
    return generator.generate_volunteer_certificate(volunteer_data)

# Example usage for testing
if __name__ == "__main__":
    # Sample volunteer data for testing
    sample_volunteer = {
        'id': 1,
        'full_name': 'John Doe',
        'volunteer_role': 'Registration Coordinator',
        'total_hours': 25,
        'booth_assignment': 'Registration Desk, Information Booth',
        'email': 'john.doe@example.com'
    }
    
    # Generate certificate
    pdf_bytes = generate_certificate_for_volunteer(1, sample_volunteer)
    
    # Save to file for testing
    with open('sample_certificate.pdf', 'wb') as f:
        f.write(pdf_bytes)
    
    print("Sample certificate generated: sample_certificate.pdf")
