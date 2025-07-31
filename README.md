# EventIQ - Corporate IT Event Management System

![EventIQ Logo](https://img.shields.io/badge/EventIQ-Corporate%20IT%20Events-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Cloud%20Ready-red)

## 🎯 **Project Overview**
EventIQ is a comprehensive corporate IT event management system built with Streamlit, designed for 10-member team collaboration and optimized for corporate technology companies.

## 🌐 **Live Demo**
🔗 **[View Live Application](https://eventiq-ai.streamlit.app)**

## 🌟 **Features**
- **Dashboard**: Real-time corporate event metrics and KPIs
- **Event Setup**: Corporate IT event configuration and templates
- **Budget Management**: Financial tracking with corporate IT budget categories
- **Participant Management**: Bulk import and registration for corporate events
- **Media Gallery**: Professional file upload and media processing
- **Vendor Management**: Contract and document handling for IT vendors
- **Certificate Generation**: Automated certificate creation for corporate training
- **Analytics**: Data visualization and reporting for executives
- **Settings**: System configuration and user management
- **Workflows**: Business process automation for corporate IT
- **Booths**: Exhibition and tech demo management
- **Feedback**: Collection and analysis for corporate events

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/your-username/eventiq-ai.git
cd eventiq-ai
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize database:
```bash
python scripts/init_db.py
```

6. Run the application:
```bash
# Start FastAPI backend
uvicorn app.main:app --reload --port 8000

# Start Streamlit frontend (in another terminal)
streamlit run app/frontend/main.py
```

## Project Structure

```
eventiq-ai/
├── app/
│   ├── api/                 # FastAPI routes
│   ├── core/                # Core configuration
│   ├── database/            # Database models and connection
│   ├── frontend/            # Streamlit pages
│   ├── models/              # SQLAlchemy models
│   ├── services/            # Business logic
│   └── utils/               # Utility functions
├── tests/                   # Test files
├── scripts/                 # Utility scripts
├── docs/                    # Documentation
├── .github/                 # GitHub workflows and instructions
└── requirements.txt         # Python dependencies
```

## Development

### Running Tests
```bash
pytest tests/ -v
```

### Code Quality
```bash
# Format code
black app/ tests/

# Lint code  
flake8 app/ tests/

# Type checking
mypy app/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- Project Lead: [Your Name]
- Email: [your.email@example.com]
- GitHub: [@your-username](https://github.com/your-username)
