@echo off
REM ONE-COMMAND FIX - Run this to fix GitHub push error

echo.
echo ========================================
echo   FIXING GITHUB PUSH ERROR
echo ========================================
echo.
echo This will start fresh and push to GitHub
echo.
pause

REM Remove git history
echo Removing old git history...
rmdir /s /q .git 2>nul

REM Initialize fresh
echo Creating fresh repository...
git init

REM Add files
echo Adding files...
git add .

REM Commit
echo Creating clean commit...
git commit -m "Initial commit: Email Triage OpenEnv environment"

REM Add remote
echo Adding remote...
git remote add origin https://github.com/Arunchand19/Email-triage_scalar.git 2>nul

REM Push
echo.
echo ========================================
echo   Pushing to GitHub...
echo ========================================
echo.

REM Check which branch we're on
for /f "tokens=*" %%i in ('git branch --show-current') do set BRANCH=%%i
echo Current branch: %BRANCH%

REM Push to the current branch
git push -f origin %BRANCH%

echo.
if errorlevel 1 (
    echo ========================================
    echo   PUSH FAILED
    echo ========================================
    echo.
    echo See FIX_GITHUB_ERROR.md for solutions
) else (
    echo ========================================
    echo   SUCCESS! Push completed!
    echo ========================================
)
echo.
pause
