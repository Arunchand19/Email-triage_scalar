@echo off
REM Start the Email Triage Environment Server

echo ==========================================
echo   Starting Email Triage Server
echo ==========================================
echo.

echo Server will run on: http://localhost:7860
echo.
echo Press CTRL+C to stop the server
echo.
echo ==========================================
echo.

python app.py

pause
