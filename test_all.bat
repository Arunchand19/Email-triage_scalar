@echo off
REM Complete test script - Tests everything including server

echo ==========================================
echo   Email Triage Environment - Full Test
echo ==========================================
echo.

echo [1/5] Testing environment directly (no server)...
python test_env.py
if errorlevel 1 (
    echo FAILED: Environment tests failed
    pause
    exit /b 1
)
echo PASSED: Environment tests
echo.

echo [2/5] Testing mock inference (no server)...
python inference.py --mock
if errorlevel 1 (
    echo FAILED: Mock inference failed
    pause
    exit /b 1
)
echo PASSED: Mock inference
echo.

echo [3/5] Starting server...
start /B python app.py
timeout /t 5 /nobreak >nul
echo Server started
echo.

echo [4/5] Testing server endpoints...
curl -s http://localhost:7860/health >nul
if errorlevel 1 (
    echo FAILED: Server health check failed
    taskkill /F /IM python.exe >nul 2>&1
    pause
    exit /b 1
)
echo PASSED: Server health check
echo.

curl -s -X POST http://localhost:7860/reset -H "Content-Type: application/json" -d "{\"task\":\"easy\"}" >nul
if errorlevel 1 (
    echo FAILED: Server reset endpoint failed
    taskkill /F /IM python.exe >nul 2>&1
    pause
    exit /b 1
)
echo PASSED: Server reset endpoint
echo.

echo [5/5] Stopping server...
taskkill /F /IM python.exe >nul 2>&1
echo Server stopped
echo.

echo ==========================================
echo   ALL TESTS PASSED!
echo ==========================================
echo.
echo Your environment is ready for:
echo   - Local testing
echo   - Inference runs
echo   - Server deployment
echo   - Hugging Face Spaces
echo   - Hackathon submission
echo.
pause
