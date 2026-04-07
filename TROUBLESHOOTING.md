# Troubleshooting Guide

## Common Issues and Solutions

### 1. HF_TOKEN Error

**Error Message:**
```
[ERROR] HF_TOKEN not found. Run with --mock or set HF_TOKEN environment variable.
```

**Solution:**

**Option A: Use Mock Mode (Recommended for Testing)**
```bash
python inference.py --mock
```

**Option B: Set HF_TOKEN**

Linux/Mac:
```bash
export HF_TOKEN="your_huggingface_token_here"
python inference.py
```

Windows CMD:
```cmd
set HF_TOKEN=your_huggingface_token_here
python inference.py
```

Windows PowerShell:
```powershell
$env:HF_TOKEN="your_huggingface_token_here"
python inference.py
```

**Get HF_TOKEN:**
1. Visit https://huggingface.co/settings/tokens
2. Create new token with "Read" permission
3. Copy token (starts with `hf_`)

---

### 2. Module Not Found Errors

**Error Message:**
```
ModuleNotFoundError: No module named 'fastapi'
ModuleNotFoundError: No module named 'openai'
```

**Solution:**
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install specific packages
pip install fastapi uvicorn openai pydantic
```

**Verify Installation:**
```bash
pip list | grep -E "fastapi|uvicorn|openai|pydantic"
```

---

### 3. Port Already in Use

**Error Message:**
```
ERROR: [Errno 48] Address already in use
```

**Solution:**

Linux/Mac:
```bash
# Find process using port 7860
lsof -ti:7860

# Kill the process
lsof -ti:7860 | xargs kill -9

# Or use different port
PORT=8000 python app.py
```

Windows:
```cmd
# Find process
netstat -ano | findstr :7860

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or use different port
set PORT=8000
python app.py
```

---

### 4. Docker Build Fails

**Error Message:**
```
ERROR: failed to solve: process "/bin/sh -c pip install..." did not complete successfully
```

**Solutions:**

**Clear Docker Cache:**
```bash
docker build --no-cache -t email-triage-env .
```

**Check Dockerfile Syntax:**
```bash
docker build -t email-triage-env . 2>&1 | tee build.log
cat build.log
```

**Verify Requirements:**
```bash
# Test requirements.txt locally first
pip install -r requirements.txt
```

**Check Docker Version:**
```bash
docker --version
# Should be 20.10+ for best compatibility
```

---

### 5. Import Errors in Python

**Error Message:**
```
ImportError: cannot import name 'Action' from 'models'
```

**Solution:**

**Check Python Path:**
```bash
# Run from correct directory
cd email_triage_env
python inference.py --mock
```

**Verify Files Exist:**
```bash
ls -la models.py environment.py tasks.py
```

**Check Python Version:**
```bash
python --version
# Should be 3.9 or higher
```

---

### 6. API Connection Errors

**Error Message:**
```
openai.APIConnectionError: Connection error
```

**Solutions:**

**Test with Mock Mode First:**
```bash
python inference.py --mock
```

**Check Network:**
```bash
curl -I https://router.huggingface.co
```

**Verify API Key:**
```bash
echo $HF_TOKEN
# Should output your token
```

**Try Different Endpoint:**
```bash
export API_BASE_URL="https://api.openai.com/v1"
export MODEL_NAME="gpt-3.5-turbo"
python inference.py
```

---

### 7. Validation Script Fails

**Error Message:**
```
[FAILED] -- HF Space not reachable
```

**Solutions:**

**Start Server First:**
```bash
# Terminal 1
python app.py

# Terminal 2 (wait 5 seconds)
bash validate-submission.sh http://localhost:7860
```

**Test Endpoints Manually:**
```bash
# Health check
curl http://localhost:7860/health

# Reset endpoint
curl -X POST http://localhost:7860/reset \
  -H "Content-Type: application/json" \
  -d '{"task": "easy"}'
```

**Check Server Logs:**
```bash
# Run server with verbose output
python app.py
# Look for errors in output
```

---

### 8. Test Suite Fails

**Error Message:**
```
AssertionError: Expected score 1.0, got 0.8
```

**Solutions:**

**Run Individual Tests:**
```bash
python -c "from test_env import test_easy_task; test_easy_task()"
```

**Check Environment State:**
```python
from environment import EmailTriageEnv
env = EmailTriageEnv()
obs = env.reset("easy")
print(f"Emails: {len(obs.emails)}")
print(f"Task: {obs.current_task}")
```

**Verify Grader Logic:**
```python
from tasks import TASKS
actions = {'classification': {1: 'low', 2: 'high', 3: 'medium', 4: 'medium', 5: 'low'}}
score = TASKS['easy']['grader'](actions)
print(f"Score: {score}")
```

---

### 9. Docker Container Won't Start

**Error Message:**
```
docker: Error response from daemon: driver failed
```

**Solutions:**

**Check Docker Service:**
```bash
# Linux
sudo systemctl status docker

# Mac
# Check Docker Desktop is running

# Windows
# Check Docker Desktop is running
```

**Remove Old Containers:**
```bash
docker ps -a
docker rm $(docker ps -aq)
```

**Check Logs:**
```bash
docker logs <container_id>
```

**Rebuild Image:**
```bash
docker rmi email-triage-env
docker build -t email-triage-env .
```

---

### 10. JSON Parsing Errors

**Error Message:**
```
json.decoder.JSONDecodeError: Expecting value
```

**Solutions:**

**Use Mock Mode:**
```bash
# Mock mode has guaranteed valid JSON
python inference.py --mock
```

**Check LLM Response:**
```python
# Add debug logging in inference.py
print(f"[DEBUG] Raw LLM response: {text}")
```

**Use JSON Mode:**
```python
# Already configured in inference.py
response_format={"type": "json_object"}
```

---

## Environment-Specific Issues

### Windows

**Issue: Bash scripts don't work**
- Use `.bat` files instead: `run_mock_inference.bat`
- Or install Git Bash / WSL

**Issue: Path separators**
- Use `\` instead of `/` in paths
- Or use `os.path.join()` in Python

### Mac

**Issue: Permission denied**
```bash
chmod +x setup.sh
chmod +x run_mock_inference.sh
./setup.sh
```

**Issue: Docker not found**
- Install Docker Desktop for Mac
- Ensure Docker is running

### Linux

**Issue: Docker permission denied**
```bash
sudo usermod -aG docker $USER
# Log out and back in
```

**Issue: Port 7860 requires sudo**
```bash
# Use port > 1024
PORT=8000 python app.py
```

---

## Performance Issues

### Slow Inference

**Cause:** LLM API latency

**Solutions:**
- Use mock mode for testing: `python inference.py --mock`
- Use faster model: `export MODEL_NAME="Qwen/Qwen2.5-7B-Instruct"`
- Reduce MAX_TOKENS in inference.py

### High Memory Usage

**Cause:** Large model or many concurrent requests

**Solutions:**
- Restart server periodically
- Use smaller model
- Limit concurrent connections in app.py

### Docker Build Timeout

**Cause:** Slow network or large dependencies

**Solutions:**
- Use Docker BuildKit: `DOCKER_BUILDKIT=1 docker build .`
- Increase timeout: `docker build --timeout 1800 .`
- Use local pip cache

---

## Debugging Tips

### Enable Debug Logging

```python
# Add to app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Components Individually

```bash
# Test environment only
python -c "from environment import EmailTriageEnv; env = EmailTriageEnv(); print(env.reset('easy'))"

# Test models only
python -c "from models import Action, Classification; print(Action(classification={1: Classification.low}))"

# Test tasks only
python -c "from tasks import TASKS; print(TASKS.keys())"
```

### Check Dependencies

```bash
pip check
pip list --outdated
```

### Verify File Integrity

```bash
# Check all required files exist
ls -la app.py environment.py models.py tasks.py inference.py openenv.yaml Dockerfile requirements.txt
```

---

## Getting Help

### Documentation
- **README.md** - Main documentation
- **QUICKSTART.md** - Quick start guide
- **INFERENCE_GUIDE.md** - Inference usage
- **REFERENCE.md** - Quick reference

### Testing
```bash
# Run full test suite
python test_env.py

# Run mock inference
python inference.py --mock

# Validate deployment
bash validate-submission.sh http://localhost:7860
```

### Community
- OpenEnv GitHub: https://github.com/meta-pytorch/OpenEnv
- Hugging Face Forums: https://discuss.huggingface.co
- Docker Docs: https://docs.docker.com

---

## Quick Diagnostic

Run this to check your setup:

```bash
#!/bin/bash
echo "=== System Check ==="
python --version
pip --version
docker --version
echo ""

echo "=== Files Check ==="
ls -la *.py *.yaml Dockerfile requirements.txt
echo ""

echo "=== Dependencies Check ==="
pip list | grep -E "fastapi|uvicorn|openai|pydantic"
echo ""

echo "=== Test Environment ==="
python -c "from environment import EmailTriageEnv; print('✓ Environment OK')"
echo ""

echo "=== Test Inference ==="
python inference.py --mock | head -3
echo ""

echo "=== All checks complete ==="
```

Save as `diagnostic.sh` and run: `bash diagnostic.sh`
