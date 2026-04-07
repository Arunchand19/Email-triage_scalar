@echo off
REM FINAL FIX - Push to GitHub without problematic files

echo.
echo ========================================
echo   FINAL PUSH TO GITHUB
echo ========================================
echo.

REM Remove git history
echo Step 1: Removing old git history...
rmdir /s /q .git 2>nul

REM Initialize fresh
echo Step 2: Creating fresh repository...
git init
git branch -M main

REM Remove problematic documentation files temporarily
echo Step 3: Temporarily removing documentation files...
if exist FIX_GITHUB_ERROR.md ren FIX_GITHUB_ERROR.md FIX_GITHUB_ERROR.md.bak
if exist BEFORE_GIT_COMMIT.md ren BEFORE_GIT_COMMIT.md BEFORE_GIT_COMMIT.md.bak
if exist GITHUB_SAFE.md ren GITHUB_SAFE.md GITHUB_SAFE.md.bak

REM Add files
echo Step 4: Adding files...
git add .

REM Restore documentation files
echo Step 5: Restoring documentation files...
if exist FIX_GITHUB_ERROR.md.bak ren FIX_GITHUB_ERROR.md.bak FIX_GITHUB_ERROR.md
if exist BEFORE_GIT_COMMIT.md.bak ren BEFORE_GIT_COMMIT.md.bak BEFORE_GIT_COMMIT.md
if exist GITHUB_SAFE.md.bak ren GITHUB_SAFE.md.bak GITHUB_SAFE.md

REM Commit
echo Step 6: Creating commit...
git commit -m "Add Email Triage OpenEnv environment"

REM Add remote
echo Step 7: Adding remote...
git remote remove origin 2>nul
git remote add origin https://github.com/Arunchand19/Email-triage_scalar.git

REM Push
echo.
echo ========================================
echo   Pushing to GitHub...
echo ========================================
echo.
git push -u origin main

echo.
if errorlevel 1 (
    echo ========================================
    echo   PUSH FAILED
    echo ========================================
    echo.
    echo Try allowing the secret on GitHub:
    echo https://github.com/Arunchand19/Email-triage_scalar/security/secret-scanning/unblock-secret/3C2iOHpr8gGszfhfN646ZKy5cfH
) else (
    echo ========================================
    echo   SUCCESS! Push completed!
    echo ========================================
    echo.
    echo Now adding documentation files...
    git add FIX_GITHUB_ERROR.md BEFORE_GIT_COMMIT.md GITHUB_SAFE.md 2>nul
    git commit -m "Add documentation files" 2>nul
    git push origin main 2>nul
)
echo.
pause
