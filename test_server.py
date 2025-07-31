"""
Minimal FastAPI server for testing without external dependencies
This is a temporary solution to test the authentication flow.
"""

import json
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Simple in-memory user store for testing
USERS_DB = {
    "admin@eventiq.com": {
        "id": 1,
        "email": "admin@eventiq.com",
        "hashed_password": "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9",  # 'admin123'
        "full_name": "System Administrator",
        "role": "admin",
        "is_active": True,
        "is_verified": True,
        "created_at": "2024-01-01T00:00:00",
        "phone": "+1-555-0001",
        "organization": "EventIQ",
        "bio": "System administrator for EventIQ platform"
    },
    "organizer@eventiq.com": {
        "id": 2,
        "email": "organizer@eventiq.com", 
        "hashed_password": "9ed814e67a9da028eea6f1984a8bdecf9b50c7aec557df25331d66834656eb77",  # 'organizer123'
        "full_name": "Event Organizer",
        "role": "organizer",
        "is_active": True,
        "is_verified": True,
        "created_at": "2024-01-01T00:00:00",
        "phone": "+1-555-0002",
        "organization": "Tech University",
        "bio": "Lead organizer for campus events"
    },
    "volunteer1@example.com": {
        "id": 3,
        "email": "volunteer1@example.com",
        "hashed_password": "25a21eab5feca60534fc732ff65e27984b61e43d0c7a4614b9710cd01456c37a",  # 'volunteer123'
        "full_name": "Alice Johnson",
        "role": "volunteer", 
        "is_active": True,
        "is_verified": True,
        "created_at": "2024-01-01T00:00:00",
        "phone": "+1-555-0003",
        "organization": "Computer Science Club",
        "bio": "Passionate about technology and helping others"
    },
    "participant1@example.com": {
        "id": 4,
        "email": "participant1@example.com",
        "hashed_password": "c9b0da21ed83f433a029d35685e0a7e26b1b075c8482086a6210e410ffdc8db5",  # 'participant123'
        "full_name": "Carol Davis",
        "role": "participant",
        "is_active": True,
        "is_verified": True,
        "created_at": "2024-01-01T00:00:00",
        "phone": "+1-555-0005",
        "organization": "Marketing Department",
        "bio": "Interested in AI and technology trends"
    }
}

def hash_password(password: str) -> str:
    """Simple password hashing for testing"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return hash_password(plain_password) == hashed_password

def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate user"""
    user = USERS_DB.get(email)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a simple access token (not JWT for simplicity)"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire.isoformat()})
    # In a real app, this would be properly signed
    return json.dumps(to_encode)

# Simple HTTP server

class EventIQHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/v1/auth/login':
            self.handle_login()
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"detail": "Not found"}).encode())

    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "message": "EventIQ API Server",
                "version": "1.0.0",
                "status": "running"
            }).encode())
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy"}).encode())
        elif self.path == '/api/v1/auth/me':
            self.handle_me()
        elif self.path.startswith('/api/v1/'):
            self.handle_api_endpoint()
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"detail": "Not found"}).encode())

    def handle_api_endpoint(self):
        """Handle various API endpoints with sample data"""
        print(f"DEBUG: Requested path: '{self.path}'")  # Debug logging
        
        endpoint_handlers = {
            '/api/v1/volunteers/': self.get_volunteers,
            '/api/v1/volunteers/me': self.get_volunteer_me,
            '/api/v1/participants/': self.get_participants,
            '/api/v1/participants/me': self.get_participant_me,
            '/api/v1/participants/registrations': self.get_participant_registrations,
            '/api/v1/budget/': self.get_budgets,
            '/api/v1/budget/1/categories': self.get_budget_categories,
            '/api/v1/budget/expenses': self.get_budget_expenses,
            '/api/v1/booths/': self.get_booths,
            '/api/v1/booths/assignments': self.get_booth_assignments,
            '/api/v1/analytics/dashboard': self.get_analytics_dashboard,
            '/api/v1/analytics/financial': self.get_analytics_financial,
            '/api/v1/analytics/volunteers': self.get_analytics_volunteers,
            
            # Certificate endpoints
            '/api/v1/certificates/': self.get_certificates,
            '/api/v1/certificates/stats': self.get_certificate_stats,
            '/api/v1/certificates/bulk-generate': self.generate_bulk_certificates,
        }
        
        handler = endpoint_handlers.get(self.path)
        if handler:
            print(f"DEBUG: Found handler for {self.path}")  # Debug logging
            handler()
        else:
            print(f"DEBUG: No handler found for {self.path}")  # Debug logging
            print(f"DEBUG: Available endpoints: {list(endpoint_handlers.keys())}")  # Debug logging
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"detail": f"Endpoint not implemented: {self.path}"}).encode())
    
    def get_volunteers(self):
        """Return sample volunteers data"""
        data = {
            "volunteers": [
                {
                    "id": 1, "user_id": 3, "volunteer_role": "coordinator",
                    "full_name": "Alice Johnson", "email": "volunteer1@example.com",
                    "skills": "Event Management, Leadership", "total_hours": 24,
                    "is_active": True, "created_at": "2024-01-15T10:00:00Z"
                }
            ]
        }
        self.send_json_response(data)
    
    def get_volunteer_me(self):
        """Return current volunteer profile"""
        data = {
            "id": 1, "user_id": 3, "volunteer_role": "coordinator",
            "full_name": "Alice Johnson", "email": "volunteer1@example.com",
            "skills": "Event Management, Leadership", "total_hours": 24,
            "availability": "Full-time during event days",
            "emergency_contact": "Jane Doe - +1-555-9999",
            "t_shirt_size": "L", "dietary_restrictions": "Vegetarian",
            "is_active": True, "created_at": "2024-01-15T10:00:00Z"
        }
        self.send_json_response(data)
    
    def get_participants(self):
        """Return sample participants data"""
        data = {
            "participants": [
                {
                    "id": 1, "user_id": 4, "full_name": "Carol Davis",
                    "email": "participant1@example.com", "organization": "Marketing Department",
                    "job_title": "Marketing Manager", "industry": "Technology",
                    "interests": "AI, Digital Marketing", "registration_date": "2024-01-10T12:00:00Z"
                }
            ]
        }
        self.send_json_response(data)
    
    def get_participant_me(self):
        """Return current participant profile"""
        data = {
            "id": 1, "user_id": 4, "full_name": "Carol Davis",
            "email": "participant1@example.com", "organization": "Marketing Department",
            "job_title": "Marketing Manager", "industry": "Technology",
            "interests": "AI, Digital Marketing, Web Development",
            "dietary_restrictions": "No nuts", "emergency_contact": "John Smith - +1-555-8888",
            "t_shirt_size": "M", "linkedin_profile": "https://linkedin.com/in/caroldavis",
            "how_did_you_hear": "Social Media", "registration_date": "2024-01-10T12:00:00Z",
            "is_active": True
        }
        self.send_json_response(data)
    
    def get_participant_registrations(self):
        """Return participant registrations"""
        data = {
            "registrations": [
                {
                    "id": 1, "event_name": "TechCon 2024", "registration_status": "confirmed",
                    "registration_date": "2024-01-10T12:00:00Z",
                    "confirmation_date": "2024-01-12T09:00:00Z"
                },
                {
                    "id": 2, "event_name": "AI Workshop", "registration_status": "pending",
                    "registration_date": "2024-01-15T16:00:00Z"
                }
            ]
        }
        self.send_json_response(data)
    
    def get_budgets(self):
        """Return budget data"""
        data = {
            "budgets": [
                {
                    "id": 1, "event_name": "TechCon 2024", "total_budget": 50000.00,
                    "allocated_amount": 45000.00, "spent_amount": 28500.00,
                    "remaining_amount": 21500.00, "creator_name": "Event Organizer",
                    "created_at": "2024-01-01T10:00:00Z", "is_active": True
                }
            ]
        }
        self.send_json_response(data)
    
    def get_budget_categories(self):
        """Return budget categories"""
        data = {
            "categories": [
                {"id": 1, "name": "Venue", "allocated_amount": 15000.00, "spent_amount": 14500.00, "remaining_amount": 500.00},
                {"id": 2, "name": "Catering", "allocated_amount": 12000.00, "spent_amount": 4000.00, "remaining_amount": 8000.00},
                {"id": 3, "name": "Technology", "allocated_amount": 8000.00, "spent_amount": 3500.00, "remaining_amount": 4500.00}
            ]
        }
        self.send_json_response(data)
    
    def get_budget_expenses(self):
        """Return budget expenses"""
        data = {
            "expenses": [
                {
                    "id": 1, "category_name": "Venue", "vendor_name": "Grand Conference Center",
                    "description": "Venue rental for 3 days", "amount": 14500.00,
                    "status": "approved", "submitted_at": "2024-01-05T10:00:00Z",
                    "submitter_name": "Event Organizer"
                },
                {
                    "id": 2, "category_name": "Catering", "vendor_name": "Premier Catering Co.",
                    "description": "Opening day lunch", "amount": 2800.00,
                    "status": "approved", "submitted_at": "2024-01-08T14:00:00Z",
                    "submitter_name": "Event Organizer"
                }
            ]
        }
        self.send_json_response(data)
    
    def get_booths(self):
        """Return booths data"""
        data = {
            "booths": [
                {
                    "id": 1, "booth_number": "A-01", "booth_type": "standard",
                    "location": "Main Hall - Section A", "size": "10x10 ft",
                    "amenities": "Power, WiFi, Table, 2 Chairs", "hourly_rate": 100.0,
                    "daily_rate": 800.0, "status": "reserved", "is_active": True,
                    "current_vendor": "TechCorp Solutions"
                },
                {
                    "id": 2, "booth_number": "A-02", "booth_type": "premium",
                    "location": "Main Hall - Section A", "size": "15x15 ft",
                    "amenities": "Power, WiFi, Premium Setup, Storage", "hourly_rate": 150.0,
                    "daily_rate": 1200.0, "status": "available", "is_active": True
                }
            ]
        }
        self.send_json_response(data)
    
    def get_booth_assignments(self):
        """Return booth assignments"""
        data = {
            "assignments": [
                {
                    "id": 1, "booth_id": 1, "booth_number": "A-01",
                    "vendor_name": "TechCorp Solutions", "start_time": "2024-01-22T09:00:00Z",
                    "end_time": "2024-01-24T18:00:00Z", "total_cost": 2400.0,
                    "contact_person": "John Tech", "contact_phone": "+1-555-1001",
                    "is_confirmed": True, "assigner_name": "Event Organizer"
                }
            ]
        }
        self.send_json_response(data)
    
    def get_analytics_dashboard(self):
        """Return analytics dashboard data"""
        data = {
            "total_participants": 25,
            "total_volunteers": 8,
            "total_booths": 6,
            "occupied_booths": 2,
            "total_budget": 50000.00,
            "spent_amount": 28500.00,
            "pending_expenses": 3,
            "confirmed_registrations": 18,
            "pending_registrations": 7,
            "recent_activities": [
                {"type": "registration", "message": "New participant registered for TechCon 2024", "timestamp": "2024-01-20T15:30:00Z"},
                {"type": "expense", "message": "Expense approved: Sound system rental", "timestamp": "2024-01-20T14:20:00Z"},
                {"type": "volunteer", "message": "Volunteer checked in for duty", "timestamp": "2024-01-20T08:00:00Z"}
            ]
        }
        self.send_json_response(data)
    
    def get_analytics_financial(self):
        """Return financial analytics data"""
        data = {
            "budget_overview": {
                "total_budget": 50000.00,
                "allocated": 45000.00,
                "spent": 28500.00,
                "remaining": 21500.00,
                "allocation_percentage": 90.0,
                "spent_percentage": 57.0
            },
            "spending_by_category": [
                {"category": "Venue", "allocated": 15000.00, "spent": 14500.00, "percentage": 96.7},
                {"category": "Catering", "allocated": 12000.00, "spent": 4000.00, "percentage": 33.3},
                {"category": "Technology", "allocated": 8000.00, "spent": 3500.00, "percentage": 43.8},
                {"category": "Marketing", "allocated": 5000.00, "spent": 2200.00, "percentage": 44.0}
            ],
            "recent_expenses": [
                {"date": "2024-01-20", "amount": 1200.00, "category": "Catering", "vendor": "Coffee Express"},
                {"date": "2024-01-19", "amount": 2200.00, "category": "Marketing", "vendor": "Digital Marketing Inc."}
            ]
        }
        self.send_json_response(data)
    
    def get_analytics_volunteers(self):
        """Return volunteer analytics data"""
        data = {
            "total_volunteers": 8,
            "active_volunteers": 6,
            "total_hours_worked": 156.5,
            "average_hours_per_volunteer": 19.6,
            "volunteers_by_role": [
                {"role": "coordinator", "count": 2, "hours": 48.0},
                {"role": "usher", "count": 3, "hours": 42.0}
            ],
            "recent_check_ins": [
                {"volunteer": "Alice Johnson", "role": "coordinator", "check_in_time": "2024-01-20T08:00:00Z", "location": "Main Entrance"}
            ]
        }
        self.send_json_response(data)

    def get_certificates(self):
        """Get all available certificates"""
        certificates = []
        for vol_id, volunteer in self.sample_volunteers.items():
            if volunteer['total_hours'] > 0:
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
        
        data = {"certificates": certificates, "total": len(certificates)}
        self.send_json_response(data)

    def get_certificate_stats(self):
        """Get certificate generation statistics"""
        total_volunteers = len(self.sample_volunteers)
        eligible_count = sum(1 for v in self.sample_volunteers.values() if v['total_hours'] > 0)
        total_hours = sum(v['total_hours'] for v in self.sample_volunteers.values())
        
        data = {
            "total_volunteers": total_volunteers,
            "eligible_for_certificates": eligible_count,
            "certificates_generated": eligible_count,
            "total_volunteer_hours": total_hours,
            "average_hours_per_volunteer": total_hours / total_volunteers if total_volunteers > 0 else 0,
            "certificate_types": ["Volunteer Service Certificate"],
            "last_updated": datetime.now().isoformat()
        }
        self.send_json_response(data)

    def generate_bulk_certificates(self):
        """Generate certificates for all eligible volunteers"""
        eligible_volunteers = []
        
        for vol_id, volunteer in self.sample_volunteers.items():
            if volunteer['total_hours'] > 0 and volunteer['is_active']:
                eligible_volunteers.append({
                    "volunteer_id": vol_id,
                    "volunteer_name": volunteer['full_name'],
                    "total_hours": volunteer['total_hours'],
                    "certificate_id": f"CERT-{vol_id}-{datetime.now().strftime('%Y%m%d')}"
                })
        
        data = {
            "message": f"Bulk certificate generation initiated for {len(eligible_volunteers)} volunteers",
            "eligible_volunteers": eligible_volunteers,
            "generated_date": datetime.now().isoformat()
        }
        self.send_json_response(data)
    
    def send_json_response(self, data):
        """Send JSON response with CORS headers"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def handle_login(self):
        """Handle login requests"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Handle both JSON and form data
            email = None
            password = None
            
            content_type = self.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                data = json.loads(post_data.decode('utf-8'))
                email = data.get('username')  # FastAPI OAuth2PasswordRequestForm uses 'username'
                password = data.get('password')
            else:
                # Handle form data
                import urllib.parse
                data = urllib.parse.parse_qs(post_data.decode('utf-8'))
                email = data.get('username', [None])[0]
                password = data.get('password', [None])[0]
            
            if not email or not password:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"detail": "Email and password required"}).encode())
                return
            
            user = authenticate_user(email, password)
            if not user:
                self.send_response(401)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"detail": "Incorrect email or password"}).encode())
                return
            
            access_token = create_access_token(data={"sub": user["email"], "user_id": user["id"]})
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "access_token": access_token,
                "token_type": "bearer"
            }
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            print(f"Login error: {e}")  # Debug logging
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"detail": f"Internal server error: {str(e)}"}).encode())

    def handle_me(self):
        """Handle /auth/me requests"""
        try:
            auth_header = self.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                self.send_response(401)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"detail": "Missing or invalid token"}).encode())
                return
            
            token = auth_header[7:]  # Remove 'Bearer ' prefix
            try:
                token_data = json.loads(token)
                user_email = token_data.get('sub')
                user = USERS_DB.get(user_email)
                
                if not user:
                    self.send_response(401)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({"detail": "Invalid token"}).encode())
                    return
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                user_response = {
                    "id": user["id"],
                    "email": user["email"],
                    "full_name": user["full_name"],
                    "role": user["role"],
                    "is_active": user["is_active"],
                    "is_verified": user["is_verified"],
                    "phone": user["phone"],
                    "organization": user["organization"],
                    "bio": user["bio"]
                }
                self.wfile.write(json.dumps(user_response).encode())
                
            except json.JSONDecodeError:
                self.send_response(401)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"detail": "Invalid token format"}).encode())
                
        except Exception as e:
            print(f"Auth me error: {e}")  # Debug logging
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"detail": f"Internal server error: {str(e)}"}).encode())

    def log_message(self, format, *args):
        """Custom log message format"""
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {format % args}")

def run_server(port=8000):
    """Run the test server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, EventIQHandler)
    print(f"EventIQ Test Server running on http://localhost:{port}")
    print("Available endpoints:")
    print("  GET  / - API info")
    print("  GET  /health - Health check")
    print("  GET  /api/v1/auth/me - Get current user")
    print("  POST /api/v1/auth/login - Login")
    print("")
    print("Test credentials:")
    print("  Admin: admin@eventiq.com / admin123")
    print("  Organizer: organizer@eventiq.com / organizer123")
    print("  Volunteer: volunteer1@example.com / volunteer123")
    print("  Participant: participant1@example.com / participant123")
    print("")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()

if __name__ == "__main__":
    run_server()
