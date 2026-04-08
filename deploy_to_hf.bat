@echo off
setlocal

set PATH=%PATH%;C:\Users\arunc\.local\bin

echo ========================================
echo Step 1: Login to Hugging Face
echo ========================================
echo.
echo Get your token from: https://huggingface.co/settings/tokens
echo.

C:\Users\arunc\.local\bin\hf.exe auth login

echo.
echo ========================================
echo Step 2: Pushing to HF Space
echo ========================================
echo.

git push hf main

echo.
echo ========================================
echo Done! Check: https://huggingface.co/spaces/Arunchand/my-env
echo ========================================
pause
