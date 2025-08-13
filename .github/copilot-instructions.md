<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# EventIQ Copilot Instructions

## Project Overview
This is EventIQ, a comprehensive AI-powered event management system built with Python, FastAPI, Streamlit, and SQLAlchemy. The system manages large-scale campus events with multiple stakeholders and complex workflows.

## Code Style Guidelines

### Python Code Standards
- Follow PEP 8 for Python code formatting
- Use type hints for all function parameters and return values
- Use descriptive variable and function names
- Add comprehensive docstrings for all classes and functions
- Use async/await for database operations and API calls
- Implement proper error handling with custom exceptions

### Database Patterns
- Use SQLAlchemy ORM with declarative base
- Implement database models with proper relationships
- Use Alembic for database migrations
- Follow naming conventions: snake_case for tables and columns
- Add proper indexes for performance optimization

### API Development
- Use FastAPI with Pydantic models for request/response validation
- Implement proper HTTP status codes and error responses
- Add comprehensive API documentation with descriptions
- Use dependency injection for database sessions
- Implement proper authentication and authorization

### Frontend Development
- Use Streamlit for user interfaces with clean, intuitive layouts
- Implement proper state management using st.session_state
- Add input validation and error handling
- Use caching for expensive operations
- Follow consistent UI/UX patterns across modules

### AI/ML Integration
- Use Hugging Face transformers for sentiment analysis
- Implement proper error handling for AI API calls
- Add fallback mechanisms for AI service failures
- Use appropriate model sizes for performance
- Cache AI results when appropriate

## Architecture Patterns

### Module Structure
Each module should follow this structure:
```
module_name/
├── __init__.py
├── models.py      # SQLAlchemy models
├── schemas.py     # Pydantic schemas
├── routes.py      # FastAPI routes
├── services.py    # Business logic
├── frontend.py    # Streamlit interface
└── tests.py       # Module tests
```

### Service Layer Pattern
- Implement business logic in service classes
- Keep routes thin and delegate to services
- Use dependency injection for service dependencies
- Implement proper transaction management

### Error Handling
- Create custom exception classes for different error types
- Implement global exception handlers in FastAPI
- Log errors with appropriate context
- Return user-friendly error messages

### Security Considerations
- Implement JWT-based authentication
- Use password hashing with bcrypt
- Validate all user inputs
- Implement rate limiting for API endpoints
- Follow OWASP security guidelines

## Testing Guidelines
- Write unit tests for all business logic
- Use pytest fixtures for test data
- Mock external dependencies
- Aim for high test coverage (>80%)
- Write integration tests for API endpoints

## AI Assistant Specific
When generating code for the AI assistant module:
- Use OpenRouter API for chat completions
- Implement conversation history management
- Add context-aware responses based on event data
- Include proper error handling for API failures
- Use appropriate prompt templates

## Common Patterns to Follow

### Database Operations
```python
async def get_item(db: AsyncSession, item_id: int) -> Optional[Item]:
    result = await db.execute(select(Item).where(Item.id == item_id))
    return result.scalar_one_or_none()
```

### API Route Structure
```python
@router.post("/items/", response_model=ItemResponse)
async def create_item(
    item: ItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ItemResponse:
    return await item_service.create_item(db, item, current_user.id)
```

### Streamlit Page Structure
```python
def render_page():
    st.title("Page Title")
    
    with st.form("form_name"):
        # Form inputs
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            # Handle form submission
            pass
```

## Environment-Specific Notes
- Use environment variables for all configuration
- Implement different settings for dev/staging/prod
- Use SQLite for development, PostgreSQL for production
- Implement proper logging with different levels per environment

## Performance Considerations
- Use database connection pooling
- Implement caching for frequently accessed data
- Use async operations for I/O bound tasks
- Optimize database queries with proper indexing
- Use lazy loading for large datasets
