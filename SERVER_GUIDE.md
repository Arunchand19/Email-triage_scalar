# When You Need Localhost (Server)

## 🎯 Two Ways to Use the Environment

### Option 1: Direct Usage (NO SERVER) ✅ Recommended for Testing
```bash
python inference.py
```
- Environment runs directly in the script
- No server needed
- Fastest for testing
- Use this for development and testing

### Option 2: Server Mode (WITH LOCALHOST) ✅ Required for Deployment
```bash
python app.py
```
- Environment runs as API server
- Accessible via HTTP endpoints
- Required for Hugging Face Spaces
- Required for remote access
- Required for validation

---

## 🚀 When to Use Server Mode

### 1. **Hugging Face Spaces Deployment** (REQUIRED)
The server must run for HF Spaces:
```bash
python app.py
# Server runs on http://localhost:7860
```

### 2. **Pre-Submission Validation** (REQUIRED)
```bash
# Terminal 1: Start server
python app.py

# Terminal 2: Run validator
bash validate-submission.sh http://localhost:7860
```

### 3. **Remote API Access**
Access environment from other applications:
```bash
python app.py
# Now accessible at http://localhost:7860
```

### 4. **Testing API Endpoints**
```bash
python app.py

# Test in another terminal
curl http://localhost:7860/health
curl -X POST http://localhost:7860/reset -d '{"task":"easy"}'
```

### 5. **WebSocket Connections**
For interactive sessions:
```bash
python app.py
# WebSocket available at ws://localhost:7860/ws
```

---

## 📋 Complete Server Usage Guide

### Start the Server

**Windows:**
```cmd
cd email_triage_env
python app.py
```

**Linux/Mac:**
```bash
cd email_triage_env
python app.py
```

**Expected Output:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:7860 (Press CTRL+C to quit)
```

### Test the Server

**1. Health Check:**
```bash
curl http://localhost:7860/health
```
Expected: `{"status":"healthy"}`

**2. Welcome Message:**
```bash
curl http://localhost:7860/
```
Expected: `{"message":"Welcome to the Email Triage OpenEnv!",...}`

**3. Reset Environment:**
```bash
curl -X POST http://localhost:7860/reset \
  -H "Content-Type: application/json" \
  -d '{"task":"easy"}'
```

**4. Execute Step:**
```bash
curl -X POST http://localhost:7860/ \
  -H "Content-Type: application/json" \
  -d '{
    "action": {
      "classification": {"1": "low", "2": "high"},
      "response": {},
      "priority_order": null
    },
    "task": "easy"
  }'
```

**5. Get State:**
```bash
curl http://localhost:7860/state
```

### Stop the Server

Press `CTRL+C` in the terminal where server is running.

---

## 🐳 Docker Server Mode

### Build and Run:
```bash
docker build -t email-triage-env .
docker run -p 7860:7860 email-triage-env
```

### Test:
```bash
curl http://localhost:7860/health
```

---

## 🔧 Server Configuration

### Change Port:
```bash
# Default port 7860
PORT=8000 python app.py
```

### Run in Background:
```bash
# Linux/Mac
python app.py &

# Windows (use separate terminal or Task Scheduler)
start python app.py
```

### Check if Server is Running:
```bash
# Linux/Mac
lsof -i :7860

# Windows
netstat -ano | findstr :7860
```

---

## 📊 Server vs Direct Comparison

| Feature | Direct (`inference.py`) | Server (`app.py`) |
|---------|------------------------|-------------------|
| Speed | ⚡ Fast | 🐢 Slower (HTTP overhead) |
| Setup | ✅ Simple | 🔧 Requires server |
| Use Case | Testing, Development | Deployment, Validation |
| Required for HF Spaces | ❌ No | ✅ Yes |
| Required for Validation | ❌ No | ✅ Yes |
| Remote Access | ❌ No | ✅ Yes |
| Multiple Clients | ❌ No | ✅ Yes |

---

## ✅ When You MUST Use Server

### 1. Hugging Face Spaces Deployment
```bash
# In Dockerfile CMD
CMD ["python", "app.py"]
```

### 2. Running Validation Script
```bash
python app.py &
bash validate-submission.sh http://localhost:7860
```

### 3. Submission Requirements
The hackathon requires:
- ✅ Server must respond to `/reset` endpoint
- ✅ Server must run on port 7860
- ✅ Server must have health check

---

## ✅ When You DON'T Need Server

### 1. Running Inference
```bash
python inference.py  # No server needed
```

### 2. Running Tests
```bash
python test_env.py  # No server needed
```

### 3. Development/Debugging
```bash
python inference.py --mock  # No server needed
```

---

## 🎯 Recommended Workflow

### For Development:
```bash
# 1. Test without server
python inference.py --mock

# 2. Test with real token
python inference.py

# 3. Run test suite
python test_env.py
```

### For Validation:
```bash
# 1. Start server
python app.py &

# 2. Wait 5 seconds
sleep 5

# 3. Run validation
bash validate-submission.sh http://localhost:7860

# 4. Stop server
kill %1  # or CTRL+C
```

### For Deployment:
```bash
# 1. Test locally with server
python app.py
# Open browser: http://localhost:7860

# 2. Test with Docker
docker build -t email-triage-env .
docker run -p 7860:7860 email-triage-env

# 3. Deploy to HF Spaces
# (Server runs automatically)
```

---

## 🚨 Troubleshooting Server

### Port Already in Use:
```bash
# Find process
lsof -i :7860  # Mac/Linux
netstat -ano | findstr :7860  # Windows

# Kill process
kill -9 <PID>  # Mac/Linux
taskkill /PID <PID> /F  # Windows
```

### Server Won't Start:
```bash
# Check dependencies
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.9+

# Run with debug
python app.py
```

### Can't Connect to Server:
```bash
# Check if running
curl http://localhost:7860/health

# Check firewall
# Allow port 7860 in firewall settings

# Try different port
PORT=8000 python app.py
curl http://localhost:8000/health
```

---

## 📝 Summary

### Use Direct Mode (No Server):
- ✅ Quick testing
- ✅ Development
- ✅ Running inference
- ✅ Running tests

### Use Server Mode (With Localhost):
- ✅ Hugging Face Spaces deployment
- ✅ Pre-submission validation
- ✅ Remote API access
- ✅ Multiple clients
- ✅ WebSocket connections

---

## 🎯 Quick Commands

```bash
# Start server
python app.py

# Test server
curl http://localhost:7860/health

# Run inference (no server)
python inference.py

# Run validation (needs server)
python app.py &
bash validate-submission.sh http://localhost:7860
```

---

## ✅ For Your Submission

You need BOTH:

1. **`inference.py`** - Baseline agent (runs without server)
2. **`app.py`** - API server (required for HF Spaces)

Both are already implemented and ready! 🎉
