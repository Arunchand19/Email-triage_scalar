@echo off
REM Fix git history - Remove token from all commits

echo ==========================================
echo   Fixing Git History
echo ==========================================
echo.

echo This will rewrite git history to remove tokens
echo.
echo WARNING: This will change commit hashes!
echo Press Ctrl+C to cancel, or any key to continue...
pause >nul

echo.
echo Step 1: Creating backup branch...
git branch backup-before-fix 2>nul

echo.
echo Step 2: Amending the problematic commit...
git add HOW_TO_RUN.md SECURITY.md
git commit --amend --no-edit

echo.
echo Step 3: Cleaning up git history...
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo.
echo ==========================================
echo   Git History Fixed!
echo ==========================================
echo.
echo Now you can push:
echo   git push -f origin main
echo.
pause
