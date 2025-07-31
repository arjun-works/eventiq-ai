@echo off
echo Starting EventIQ System Components...
echo.

echo Starting Test API Server on port 8000...
start cmd /k "cd /d "%~dp0" && python test_server.py"

timeout /t 3 /nobreak >nul

echo Starting Enhanced Frontend on port 8501...
start cmd /k "cd /d "%~dp0" && streamlit run enhanced_frontend.py --server.port 8501"

echo.
echo ===========================================
echo    EventIQ System Started Successfully!
echo ===========================================
echo.
echo API Server: http://localhost:8000
echo Frontend:   http://localhost:8501
echo.
echo Login Credentials:
echo   Admin:       admin@eventiq.com / admin123
echo   Organizer:   organizer@eventiq.com / organizer123  
echo   Volunteer:   volunteer1@example.com / volunteer123
echo   Participant: participant1@example.com / participant123
echo.
echo Press any key to exit this window...
pause >nul
