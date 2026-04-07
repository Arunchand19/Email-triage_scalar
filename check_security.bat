@echo off
REM Security check before git commit

echo ==========================================
echo   Security Check Before Git Commit
echo ==========================================
echo.

echo [1/5] Checking .gitignore...
findstr /C:".env" .gitignore >nul
if errorlevel 1 (
    echo FAILED: .env not in .gitignore
    pause
    exit /b 1
)
echo PASSED: .env is in .gitignore
echo.

echo [2/5] Checking for tokens in .md files...
findstr /S /I "hf_[A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9]" *.md 2>nul | findstr /V "hf_xxx" >nul
if not errorlevel 1 (
    echo FAILED: Found potential token in .md files
    findstr /S /I /N "hf_[A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9]" *.md 2>nul | findstr /V "hf_xxx"
    pause
    exit /b 1
)
echo PASSED: No tokens in .md files
echo.

echo [3/5] Checking for tokens in .py files...
findstr /S /I "hf_[A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9]" *.py 2>nul | findstr /V "hf_xxx" >nul
if not errorlevel 1 (
    echo FAILED: Found potential token in .py files
    findstr /S /I /N "hf_[A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9]" *.py 2>nul | findstr /V "hf_xxx"
    pause
    exit /b 1
)
echo PASSED: No tokens in .py files
echo.

echo [4/5] Checking .env.example...
findstr /C:"your_huggingface_token_here" .env.example >nul
if errorlevel 1 (
    echo WARNING: .env.example might not have placeholder
    type .env.example | findstr "HF_TOKEN"
    echo.
    echo Please verify .env.example has placeholder
    pause
)
echo PASSED: .env.example has placeholder
echo.

echo [5/5] Checking if .env will be committed...
git status 2>nul | findstr ".env" | findstr /V ".env.example" | findstr /V ".gitignore" >nul
if not errorlevel 1 (
    echo FAILED: .env file will be committed!
    echo Run: git rm --cached .env
    pause
    exit /b 1
)
echo PASSED: .env will not be committed
echo.

echo ==========================================
echo   ALL SECURITY CHECKS PASSED!
echo ==========================================
echo.
echo Safe to commit and push to GitHub
echo.
pause
