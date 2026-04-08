@echo off
echo ========================================
echo Pushing to Hugging Face Space
echo ========================================
echo.
echo You will be prompted for your HF username and token
echo Get your token from: https://huggingface.co/settings/tokens
echo.

git push https://huggingface.co/spaces/Arunchand/my-env main

echo.
echo ========================================
echo Push complete!
echo Check your space at: https://huggingface.co/spaces/Arunchand/my-env
echo ========================================
pause
