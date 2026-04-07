@echo off
REM Start fresh - Remove all git history and create clean commit

echo ==========================================
echo   Starting Fresh - Clean Git History
echo ==========================================
echo.

echo This will:
echo   1. Remove all git history
echo   2. Create a fresh commit with clean files
echo   3. Force push to GitHub
echo.
echo WARNING: All previous commits will be lost!
echo Press Ctrl+C to cancel, or any key to continue...
pause >nul

echo.
echo Step 1: Removing .git directory...
rmdir /s /q .git

echo.
echo Step 2: Initializing fresh git repository...
git init

echo.
echo Step 3: Adding all files (except .env)...
git add .

echo.
echo Step 4: Creating clean commit...
git commit -m "Initial commit: Email Triage OpenEnv environment"

echo.
echo Step 5: Adding remote...
git remote add origin https://github.com/Arunchand19/Email-triage_scalar.git

echo.
echo ==========================================
echo   Ready to Push!
echo ==========================================
echo.
echo Run this command to push:
echo   git push -f origin main
echo.
pause
