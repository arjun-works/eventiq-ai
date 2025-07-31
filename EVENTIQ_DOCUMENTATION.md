# EventIQ - Comprehensive Event Management System

## 🎯 System Overview

EventIQ is a full-stack event management platform built with FastAPI backend and Streamlit frontend, designed to handle all aspects of event organization from volunteer coordination to budget management.

## 🏗️ Architecture

### Backend (FastAPI)
- **Authentication System**: Role-based access control (Admin, Organizer, Volunteer, Participant)
- **RESTful API**: Comprehensive endpoints for all modules
- **Database Models**: SQLAlchemy ORM with async support
- **Security**: JWT token-based authentication with password hashing

### Frontend (Streamlit)
- **Role-Based Dashboards**: Customized interfaces for each user type
- **Real-Time Data**: Live API integration with interactive charts
- **Responsive Design**: Modern UI with custom CSS styling
- **Session Management**: Secure login/logout with state persistence

### Test Server
- **Mock API**: Complete endpoint simulation for development
- **CORS Support**: Cross-origin requests enabled
- **Sample Data**: Comprehensive test datasets for all modules

## 📋 Core Modules

### 1. 👥 User Management
- User registration and authentication
- Role-based permissions (Admin, Organizer, Volunteer, Participant)
- Profile management with custom fields per role

### 2. 🤝 Volunteer Management
- Volunteer registration with role assignment
- Attendance tracking with check-in/check-out
- Skills and availability management
- Hours tracking and performance metrics

### 3. 👤 Participant Management
- Participant profile creation
- Event registration system
- Organization and industry tracking
- Dietary restrictions and accessibility needs

### 4. 💰 Budget Management
- Event budget creation and allocation
- Category-based expense tracking
- Approval workflow for expenses
- Financial reporting and analytics

### 5. 🏢 Booth Management
- Booth creation with amenities and pricing
- Vendor assignment and scheduling
- Occupancy tracking and status management
- Revenue calculation and reporting

### 6. 📊 Analytics & Reporting
- Real-time dashboard metrics
- Financial summaries and spending analysis
- Volunteer performance tracking
- Exportable reports (CSV, Excel)

## 🚀 Getting Started

### Prerequisites
```bash
# Install Python dependencies
pip install streamlit requests pandas plotly

# For full FastAPI setup (optional)
pip install fastapi uvicorn sqlalchemy aiosqlite pydantic
```

### Quick Start
1. **Download the project files**
2. **Run the startup script**:
   ```bash
   # On Windows
   start_eventiq.bat
   
   # On Mac/Linux
   python test_server.py &
   streamlit run enhanced_frontend.py --server.port 8501
   ```

3. **Access the system**:
   - Frontend: http://localhost:8501
   - API Server: http://localhost:8000

### Demo Credentials
| Role | Email | Password |
|------|-------|----------|
| Admin | admin@eventiq.com | admin123 |
| Organizer | organizer@eventiq.com | organizer123 |
| Volunteer | volunteer1@example.com | volunteer123 |
| Participant | participant1@example.com | participant123 |

## 🎮 User Experience by Role

### 👑 Admin Dashboard
- **System Overview**: Complete metrics across all modules
- **User Management**: Create, edit, and manage all user accounts
- **Financial Control**: Full budget oversight and expense approval
- **Analytics**: Comprehensive reporting and data export
- **System Configuration**: Platform settings and customization

### 📋 Organizer Dashboard
- **Event Management**: Create and manage events
- **Resource Allocation**: Booth assignments and scheduling
- **Budget Oversight**: Category management and expense approval
- **Team Coordination**: Volunteer and participant management
- **Performance Tracking**: Event metrics and success indicators

### 🤝 Volunteer Dashboard
- **Profile Management**: Skills, availability, and contact information
- **Attendance System**: Quick check-in/check-out functionality
- **Hours Tracking**: Personal attendance history and totals
- **Task Assignment**: Role-specific duties and responsibilities
- **Recognition**: Performance ratings and achievements

### 👥 Participant Dashboard
- **Event Registration**: Browse and register for events
- **Profile Customization**: Professional information and preferences
- **Registration Status**: Track application and confirmation status
- **Networking**: Connect with other participants and organizers
- **Resource Access**: Event materials and documentation

## 🔧 Technical Features

### API Endpoints
- **Authentication**: `/api/v1/auth/login`, `/api/v1/auth/me`
- **Volunteers**: `/api/v1/volunteers/`, `/api/v1/volunteers/attendance/`
- **Participants**: `/api/v1/participants/`, `/api/v1/participants/registrations`
- **Budget**: `/api/v1/budget/`, `/api/v1/budget/expenses`
- **Booths**: `/api/v1/booths/`, `/api/v1/booths/assignments`
- **Analytics**: `/api/v1/analytics/dashboard`, `/api/v1/analytics/financial`

### Database Schema
- **Users**: Core user information with role-based fields
- **Volunteers**: Extended profile with skills and attendance
- **Participants**: Organization details and event registrations
- **Budget**: Financial tracking with categories and expenses
- **Booths**: Venue management with assignments and pricing

### Security Features
- **Password Hashing**: SHA256 encryption for user passwords
- **Session Management**: Secure token-based authentication
- **Role-Based Access**: Endpoint protection by user permissions
- **CORS Support**: Cross-origin request handling

## 📈 Sample Data

The system includes comprehensive sample data:
- **8 Users** across all roles with realistic profiles
- **25+ Participants** with diverse organizations and industries
- **Budget Data** with $50,000 allocation across 6 categories
- **6 Booths** with different types and pricing structures
- **Event Registrations** and attendance records
- **Financial Transactions** and expense tracking

## 🔄 Development Workflow

### File Structure
```
eventiq-ai/
├── app/
│   ├── api/v1/endpoints/     # API endpoint implementations
│   ├── core/                 # Configuration and security
│   ├── models/              # Database models
│   └── schemas/             # Pydantic schemas
├── scripts/                 # Database initialization
├── test_server.py          # Mock API server
├── enhanced_frontend.py    # Streamlit application
├── simple_frontend.py      # Basic frontend (legacy)
└── start_eventiq.bat      # System startup script
```

### Development Commands
```bash
# Start test server only
python test_server.py

# Start frontend only  
streamlit run enhanced_frontend.py

# Full FastAPI server (requires dependencies)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🎯 Key Achievements

### ✅ Complete Authentication System
- Multi-role user management
- Secure password handling
- Session state management
- Role-based UI customization

### ✅ Comprehensive API Implementation
- 4 major modules (Volunteers, Participants, Budget, Booths)
- RESTful design with proper HTTP methods
- Data validation and error handling
- Mock server for development testing

### ✅ Modern Frontend Interface
- Responsive Streamlit application
- Interactive charts and visualizations
- Real-time data updates
- Professional styling and UX

### ✅ Business Logic Implementation
- Volunteer attendance tracking
- Event registration workflows
- Budget allocation and expense approval
- Booth assignment and scheduling

## 🚀 Next Development Steps

### Phase 1: Enhanced Features
- [x] ~~Real database integration (PostgreSQL/SQLite)~~ Using test server with mock data
- [x] **Certificate generation system with PDF export** ✅ **COMPLETED**
- [x] ~~File upload functionality for receipts/documents~~ Basic structure ready
- [ ] Email notification system
- [x] **PDF certificate generation with ReportLab** ✅ **COMPLETED**

### Phase 2: Advanced Functionality
- [ ] Real-time messaging between roles
- [ ] Calendar integration for event scheduling  
- [ ] Payment processing for booth rentals
- [ ] Mobile-responsive design improvements

### Phase 3: Enterprise Features
- [ ] Multi-event support
- [ ] Advanced analytics with ML insights
- [ ] Integration with external systems (CRM, Accounting)
- [ ] Audit logging and compliance features

## 📞 Support & Documentation

### API Documentation
- Access interactive API docs at: http://localhost:8000/docs (when FastAPI server running)
- All endpoints include request/response schemas
- Built-in testing interface available

### Troubleshooting
- **Connection Issues**: Ensure both server and frontend are running
- **Login Problems**: Use the provided demo credentials
- **Data Not Loading**: Check console for API errors
- **Port Conflicts**: Modify ports in configuration files

### Performance Optimization
- **Frontend**: Streamlit caching for API responses
- **Backend**: Async database operations
- **Data**: Pagination for large datasets
- **Security**: Rate limiting and request validation

---

**EventIQ** - Making event management simple, efficient, and comprehensive! 🎉
