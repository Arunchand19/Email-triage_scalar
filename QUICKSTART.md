# Quick Start Guide

## 1. Test Environment Locally

```bash
# Run test suite
python test_env.py

# Expected output: All tests pass
```

## 2. Start Server

```bash
# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
python app.py

# Server runs on http://localhost:7860
```

## 3. Test API Endpoints

```bash
# Health check
curl http://localhost:7860/health

# Reset environment
curl -X POST http://localhost:7860/reset \
  -H "Content-Type: application/json" \
  -d '{"task": "easy"}'

# Step with action
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

## 4. Run Inference

```bash
# Mock mode (no API key needed) - RECOMMENDED FOR TESTING
python inference.py --mock

# Or use the convenience script:
# On Windows:
run_mock_inference.bat

# On Linux/Mac:
bash run_mock_inference.sh

# Real LLM mode (requires HF_TOKEN)
export HF_TOKEN="your_token_here"
python inference.py
```

## 5. Build Docker Image

```bash
# Build
docker build -t email-triage-env .

# Run
docker run -p 7860:7860 email-triage-env

# Test
curl http://localhost:7860/health
```

## 6. Validate Submission

```bash
# Start server first
python app.py &

# Run validator
bash validate-submission.sh http://localhost:7860
```

## Expected Results

### Mock Inference Output
```
[START] task=easy env=email_triage_env model=MockAgent
[STEP] step=1 action={"classification":{"1":"low","2":"high","3":"medium","4":"medium","5":"low"}...} reward=1.00 done=true error=null
[END] success=true steps=1 score=1.000 rewards=1.00
```

### Validation Output
```
[PASSED] -- HF Space is live and responds to /reset
[PASSED] -- Docker build succeeded
[PASSED] -- openenv validate passed

All 3/3 checks passed!
Your submission is ready to submit.
```

## Troubleshooting

### Port Already in Use
```bash
# Kill existing process
lsof -ti:7860 | xargs kill -9

# Or use different port
PORT=8000 python app.py
```

### Docker Build Fails
```bash
# Check Dockerfile syntax
docker build --no-cache -t email-triage-env .

# View build logs
docker build -t email-triage-env . 2>&1 | tee build.log
```

### Inference Fails
```bash
# Use mock mode first
python inference.py --mock

# Check environment variables
echo $HF_TOKEN
echo $API_BASE_URL
echo $MODEL_NAME
```
