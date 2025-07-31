# EventIQ Development Setup Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- Node.js (for future frontend expansion)
- Git
- VS Code (recommended)

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/your-username/eventiq-ai.git
cd eventiq-ai

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install core dependencies
pip install fastapi uvicorn sqlalchemy aiosqlite python-jose[cryptography] passlib[bcrypt] python-multipart

# Install frontend dependencies
pip install streamlit plotly pandas requests
```

### 2. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
# At minimum, set:
# - SECRET_KEY (generate a secure key)
# - DATABASE_URL (default SQLite works for development)
```

### 3. Initialize Database

```bash
# Run database initialization script
python scripts/init_db.py
```

### 4. Start the Application

#### Option A: Using VS Code Tasks
1. Open VS Code in the project directory
2. Press `Ctrl+Shift+P` and select "Tasks: Run Task"
3. Select "Start EventIQ API Server"
4. Open another terminal and run: `streamlit run app/frontend/main.py`

#### Option B: Manual Start

Terminal 1 (API Server):
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 (Frontend):
```bash
streamlit run app/frontend/main.py
```

#### Option C: Docker (Production-like)

```bash
# Build and start all services
docker-compose up --build

# Or for development with auto-reload
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

### 5. Access the Application

- **API Documentation**: http://localhost:8000/docs
- **Streamlit Frontend**: http://localhost:8501
- **API Health Check**: http://localhost:8000/health

## 🔐 Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@eventiq.com | admin123 |
| Organizer | organizer@eventiq.com | organizer123 |
| Volunteer | volunteer1@example.com | volunteer123 |
| Participant | participant1@example.com | participant123 |

## 📁 Project Structure

```
eventiq-ai/
├── app/
│   ├── api/v1/endpoints/     # API route handlers
│   ├── core/                 # Core configuration and security
│   ├── frontend/             # Streamlit interface
│   ├── models/               # Database models
│   ├── schemas/              # Pydantic models
│   ├── services/             # Business logic
│   └── main.py              # FastAPI application
├── scripts/                  # Utility scripts
├── tests/                    # Test files
├── .github/                  # GitHub workflows and instructions
├── requirements.txt          # Python dependencies
└── docker-compose.yml        # Docker configuration
```

## 🛠️ Development Workflow

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/
```

### Code Quality
```bash
# Format code
pip install black
black app/ tests/

# Lint code
pip install flake8
flake8 app/ tests/

# Type checking
pip install mypy
mypy app/
```

### Database Migrations
```bash
# Create migration (when models change)
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head
```

## 🎯 Key Features Implemented

### ✅ Core Features
- [x] User Authentication & Authorization
- [x] Database Models for all modules
- [x] FastAPI Backend with async support
- [x] Streamlit Frontend
- [x] Sample data initialization
- [x] Docker containerization

### 🚧 In Progress
- [ ] Complete API endpoints for all modules
- [ ] AI sentiment analysis for feedback
- [ ] Certificate PDF generation
- [ ] QR code generation and scanning
- [ ] File upload handling
- [ ] Email notifications

### 📋 Module Status

| Module | Models | API | Frontend | Status |
|--------|--------|-----|----------|--------|
| Authentication | ✅ | ✅ | ✅ | Complete |
| Users | ✅ | ✅ | ✅ | Complete |
| Volunteers | ✅ | 🚧 | ✅ | Partial |
| Participants | ✅ | 🚧 | ✅ | Partial |
| Budget | ✅ | 🚧 | 🚧 | Basic |
| Booths | ✅ | 🚧 | 🚧 | Basic |
| Vendors | ✅ | 🚧 | 🚧 | Basic |
| Workflows | ✅ | 🚧 | 🚧 | Basic |
| Feedback | ✅ | 🚧 | 🚧 | Basic |
| Certificates | ✅ | 🚧 | 🚧 | Basic |
| Media | ✅ | 🚧 | 🚧 | Basic |
| Admin | ✅ | 🚧 | 🚧 | Basic |
| Analytics | ✅ | 🚧 | 🚧 | Basic |

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**: Make sure virtual environment is activated
2. **Database Issues**: Run `python scripts/init_db.py` to reinitialize
3. **Port Conflicts**: Check if ports 8000 or 8501 are already in use
4. **Permission Issues**: On Windows, run as administrator if needed

### Logs Location
- Application logs: `logs/eventiq.log`
- Database file: `eventiq.db` (SQLite)
- Uploaded files: `uploads/`
- Generated certificates: `certificates/`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run tests and ensure code quality checks pass
5. Commit changes: `git commit -m 'Add amazing feature'`
6. Push to branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 🚀 Deployment

### Production Deployment
1. Set environment variables for production
2. Use PostgreSQL instead of SQLite
3. Configure proper SSL/TLS
4. Set up monitoring and logging
5. Use Docker Compose with production profile

### Environment Variables for Production
```bash
DEBUG=False
ENVIRONMENT=production
DATABASE_URL=postgresql://user:pass@host:5432/eventiq
SECRET_KEY=your-super-secure-secret-key
OPENAI_API_KEY=your-openai-key
SENDGRID_API_KEY=your-sendgrid-key
```

## 📚 API Documentation

Once the server is running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## 🎪 Sample Data

The system comes with comprehensive sample data:
- 6 Users across different roles
- 3 Event booths with different categories
- Volunteer and participant registrations
- Budget items and expenses
- Vendor information
- Feedback entries with AI sentiment analysis
- System issues and admin logs
- Event overview statistics

This sample data is perfect for development, testing, and demonstrations.

## 📞 Support

- Create an issue on GitHub for bugs
- Check existing issues for solutions
- Review the documentation in `/docs`
- Use the demo credentials for quick testing
