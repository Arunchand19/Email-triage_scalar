@echo off
REM Simple script to run inference with your token

echo ==========================================
echo   Running Email Triage Inference
echo ==========================================
echo.

echo Your token is configured in .env file
echo.

echo Running inference with real LLM...
python inference.py

echo.
echo ==========================================
echo   Inference Complete!
echo ==========================================
pause
