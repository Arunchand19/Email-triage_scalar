#!/usr/bin/env bash
# Fix git history - Remove token from all commits

echo "=========================================="
echo "  Fixing Git History"
echo "=========================================="
echo ""

echo "This will rewrite git history to remove tokens from commit 33517ba2c16cad19ec2f64b7b970039d2efe2aed"
echo ""
echo "WARNING: This will change commit hashes!"
echo "Press Ctrl+C to cancel, or Enter to continue..."
read

echo ""
echo "Step 1: Creating backup branch..."
git branch backup-before-fix 2>/dev/null || echo "Backup branch already exists"

echo ""
echo "Step 2: Removing HOW_TO_RUN.md from problematic commit..."
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch HOW_TO_RUN.md' \
  --prune-empty --tag-name-filter cat -- 33517ba2c16cad19ec2f64b7b970039d2efe2aed..HEAD

echo ""
echo "Step 3: Removing SECURITY.md from problematic commit..."
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch SECURITY.md' \
  --prune-empty --tag-name-filter cat -- 33517ba2c16cad19ec2f64b7b970039d2efe2aed..HEAD

echo ""
echo "Step 4: Re-adding cleaned files..."
git add HOW_TO_RUN.md SECURITY.md
git commit --amend --no-edit

echo ""
echo "Step 5: Cleaning up..."
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo ""
echo "=========================================="
echo "  Git History Fixed!"
echo "=========================================="
echo ""
echo "Now you can push:"
echo "  git push -f origin main"
echo ""
