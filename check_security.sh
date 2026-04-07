#!/usr/bin/env bash
# Security check before git commit

set -e

echo "=========================================="
echo "  Security Check Before Git Commit"
echo "=========================================="
echo ""

echo "[1/5] Checking .gitignore..."
if grep -q "^\.env$" .gitignore; then
    echo "✅ PASSED: .env is in .gitignore"
else
    echo "❌ FAILED: .env not in .gitignore"
    exit 1
fi
echo ""

echo "[2/5] Checking for tokens in .md files..."
if grep -r "hf_[A-Za-z0-9]\{30,\}" *.md 2>/dev/null | grep -v "hf_xxx"; then
    echo "❌ FAILED: Found potential token in .md files"
    exit 1
else
    echo "✅ PASSED: No tokens in .md files"
fi
echo ""

echo "[3/5] Checking for tokens in .py files..."
if grep -r "hf_[A-Za-z0-9]\{30,\}" *.py 2>/dev/null | grep -v "hf_xxx"; then
    echo "❌ FAILED: Found potential token in .py files"
    exit 1
else
    echo "✅ PASSED: No tokens in .py files"
fi
echo ""

echo "[4/5] Checking .env.example..."
if grep -q "your_huggingface_token_here" .env.example; then
    echo "✅ PASSED: .env.example has placeholder"
else
    echo "⚠️  WARNING: .env.example might not have placeholder"
    grep "HF_TOKEN" .env.example
fi
echo ""

echo "[5/5] Checking if .env will be committed..."
if git status 2>/dev/null | grep "\.env$" | grep -v ".env.example" | grep -v ".gitignore"; then
    echo "❌ FAILED: .env file will be committed!"
    echo "Run: git rm --cached .env"
    exit 1
else
    echo "✅ PASSED: .env will not be committed"
fi
echo ""

echo "=========================================="
echo "  ✅ ALL SECURITY CHECKS PASSED!"
echo "=========================================="
echo ""
echo "Safe to commit and push to GitHub"
echo ""
