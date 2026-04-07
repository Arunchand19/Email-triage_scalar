# Security Checklist

## ✅ Pre-Submission Security Verification

Before submitting or deploying, verify that no sensitive information is exposed:

### 1. API Keys and Tokens

- [ ] No actual `HF_TOKEN` in any files
- [ ] No actual `API_KEY` in any files
- [ ] No actual `OPENAI_API_KEY` in any files
- [ ] `.env.example` uses placeholders only
- [ ] `.env` file is in `.gitignore`

**Verify:**
```bash
# Search for potential tokens (should find nothing)
grep -r "hf_[A-Za-z0-9]" . --exclude-dir=.git
grep -r "sk-[A-Za-z0-9]" . --exclude-dir=.git
```

### 2. Personal Information

- [ ] No email addresses (except example/placeholder)
- [ ] No phone numbers
- [ ] No physical addresses
- [ ] No real names in code (team names in README are OK)

### 3. Credentials

- [ ] No database passwords
- [ ] No SSH keys
- [ ] No private keys
- [ ] No certificates

### 4. Configuration Files

- [ ] `.env` is in `.gitignore`
- [ ] `.env.example` has placeholders only
- [ ] No hardcoded secrets in code
- [ ] Environment variables used for sensitive data

### 5. Git History

- [ ] No sensitive data in commit history
- [ ] `.gitignore` configured before first commit
- [ ] No accidentally committed secrets

**Clean git history if needed:**
```bash
# Remove file from all commits (if accidentally committed)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all
```

### 6. Docker Images

- [ ] No secrets in Dockerfile
- [ ] No secrets in docker-compose.yml
- [ ] Secrets passed as environment variables at runtime
- [ ] `.dockerignore` excludes sensitive files

### 7. Documentation

- [ ] Example tokens are clearly marked as placeholders
- [ ] Instructions tell users to replace placeholders
- [ ] No actual credentials in examples

### 8. Code

- [ ] No hardcoded API keys
- [ ] All secrets from environment variables
- [ ] Default values are safe (non-functional)
- [ ] Error messages don't leak sensitive info

## 🔍 Automated Check

Run this script to verify:

```bash
#!/bin/bash
echo "=== Security Check ==="

# Check for common token patterns
echo "Checking for API tokens..."
if grep -r "hf_[A-Za-z0-9]\{30,\}" . --exclude-dir=.git --exclude-dir=venv 2>/dev/null; then
    echo "❌ Found potential HF token!"
else
    echo "✅ No HF tokens found"
fi

if grep -r "sk-[A-Za-z0-9]\{40,\}" . --exclude-dir=.git --exclude-dir=venv 2>/dev/null; then
    echo "❌ Found potential OpenAI token!"
else
    echo "✅ No OpenAI tokens found"
fi

# Check .env is ignored
if grep -q "^\.env$" .gitignore 2>/dev/null; then
    echo "✅ .env is in .gitignore"
else
    echo "❌ .env not in .gitignore!"
fi

# Check .env.example has placeholders
if [ -f .env.example ]; then
    if grep -q "your_.*_here\|<.*>\|xxx\|placeholder" .env.example; then
        echo "✅ .env.example uses placeholders"
    else
        echo "⚠️  .env.example might have real values"
    fi
fi

echo "=== Check Complete ==="
```

Save as `security_check.sh` and run: `bash security_check.sh`

## 🛡️ Best Practices

### Environment Variables

**✅ Good:**
```python
API_KEY = os.getenv("HF_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
```

**❌ Bad:**
```python
API_KEY = "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### Example Files

**✅ Good (.env.example):**
```bash
HF_TOKEN=your_huggingface_token_here
API_KEY=<your-api-key>
SECRET=placeholder_value
```

**❌ Bad (.env.example):**
```bash
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
API_KEY=sk-proj-abc123xyz
```

### Documentation

**✅ Good:**
```markdown
export HF_TOKEN="your_token_here"
```

**❌ Bad:**
```markdown
export HF_TOKEN="hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

## 🚨 If You Accidentally Exposed a Secret

### 1. Revoke the Token Immediately

**Hugging Face:**
1. Go to https://huggingface.co/settings/tokens
2. Find the exposed token
3. Click "Revoke"
4. Generate a new token

**OpenAI:**
1. Go to https://platform.openai.com/api-keys
2. Find the exposed key
3. Click "Revoke"
4. Generate a new key

### 2. Remove from Git History

```bash
# Remove file from all commits
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (if already pushed)
git push origin --force --all
```

### 3. Update All Instances

- Update local `.env` file with new token
- Update any deployed services
- Update CI/CD secrets
- Notify team members

### 4. Monitor for Abuse

- Check API usage logs
- Look for unauthorized requests
- Monitor billing/usage

## ✅ Final Verification

Before submitting:

```bash
# 1. Check no secrets in files
grep -r "hf_[A-Za-z0-9]" . --exclude-dir=.git --exclude-dir=venv

# 2. Check .env is ignored
cat .gitignore | grep "^\.env$"

# 3. Check .env.example has placeholders
cat .env.example | grep "your_.*_here"

# 4. Check git status
git status

# 5. Check what will be committed
git diff --cached
```

All checks should pass before:
- Committing to git
- Pushing to GitHub
- Deploying to Hugging Face Spaces
- Submitting to hackathon

## 📋 Submission Checklist

- [x] `.env.example` uses placeholders
- [x] `.env` is in `.gitignore`
- [x] No tokens in code files
- [x] No tokens in documentation
- [x] No tokens in Docker files
- [x] No tokens in git history
- [x] Environment variables used for secrets
- [x] Instructions tell users to replace placeholders

## 🎯 Current Status

✅ **All security checks passed!**

- `.env.example` uses placeholder: `your_huggingface_token_here`
- No actual tokens found in any files
- `.env` is properly ignored
- All sensitive data uses environment variables

**Your submission is secure and ready!**
