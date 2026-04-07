@echo off
REM run_mock_inference.bat - Run inference in mock mode (no API key needed)

echo ==========================================
echo   Email Triage Environment - Mock Test
echo ==========================================
echo.

echo Testing EASY task...
set EMAIL_TRIAGE_TASK=easy
python inference.py --mock
echo.

echo Testing MEDIUM task...
set EMAIL_TRIAGE_TASK=medium
python inference.py --mock
echo.

echo Testing HARD task...
set EMAIL_TRIAGE_TASK=hard
python inference.py --mock
echo.

echo ==========================================
echo   All tests complete!
echo ==========================================
pause
