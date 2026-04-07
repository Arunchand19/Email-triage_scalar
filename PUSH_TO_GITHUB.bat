@echo off
REM FIXED - ONE-COMMAND FIX for GitHub push error

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

REM Set default branch to main
echo Setting default branch to main...
git config --global init.defaultBranch main 2>nul
git branch -M main

REM Add files
echo Adding files...
git add .

REM Check if .env is being added (it shouldn't be)
git status | findstr "\.env$" | findstr /V ".env.example" | findstr /V ".gitignore" >nul
if not errorlevel 1 (
    echo.
    echo WARNING: .env file is being added!
    echo Removing .env from staging...
    git rm --cached .env
)

REM Commit
echo Creating clean commit...
git commit -m "Initial commit: Email Triage OpenEnv environment"

REM Add remote
echo Adding remote...
git remote remove origin 2>nul
git remote add origin https://github.com/Arunchand19/Email-triage_scalar.git

REM Push
echo.
echo ========================================
echo   Pushing to GitHub...
echo ========================================
echo.
git push -f origin main

echo.
if errorlevel 1 (
    echo ========================================
    echo   PUSH FAILED
    echo ========================================
    echo.
    echo Trying alternative: git push -u origin main
    git push -u origin main
    if errorlevel 1 (
        echo.
        echo Still failed. See FIX_GITHUB_ERROR.md for solutions
    ) else (
        echo.
        echo ========================================
        echo   SUCCESS! Push completed!
        echo ========================================
    )
) else (
    echo ========================================
    echo   SUCCESS! Push completed!
    echo ========================================
)
echo.
pause
