# Quick Reference Card

## Essential Commands

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python test_env.py

# Start server
python app.py

# Test endpoints
curl http://localhost:7860/health
curl -X POST http://localhost:7860/reset -d '{"task":"easy"}'
```

### Inference
```bash
# Mock mode (no API key)
python inference.py --mock

# Real mode (requires HF_TOKEN)
export HF_TOKEN="your_token_here"
python inference.py

# Different tasks
export EMAIL_TRIAGE_TASK="medium"
python inference.py --mock
```

### Docker
```bash
# Build
docker build -t email-triage-env .

# Run
docker run -p 7860:7860 email-triage-env

# Run with compose
docker-compose up

# Stop
docker-compose down
```

### Validation
```bash
# Start server first
python app.py &

# Run validator
bash validate-submission.sh http://localhost:7860

# Expected: All 3/3 checks passed
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `HF_TOKEN` | Yes* | - | Hugging Face API token |
| `API_BASE_URL` | No | `https://router.huggingface.co/v1` | LLM endpoint |
| `MODEL_NAME` | No | `Qwen/Qwen2.5-72B-Instruct` | Model identifier |
| `EMAIL_TRIAGE_TASK` | No | `easy` | Task: easy/medium/hard |

*Not required for `--mock` mode

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/reset` | POST | Initialize environment |
| `/` | POST | Execute step |
| `/state` | GET | Get current state |
| `/ws` | WebSocket | Interactive session |

## Task Overview

| Task | Emails | Objective | Expected Score |
|------|--------|-----------|----------------|
| easy | 5 | Classify only | 0.80-1.00 |
| medium | 6 | Classify + respond | 0.60-0.90 |
| hard | 10 | Full triage + priority | 0.40-0.70 |

## Grading Formulas

```python
# Easy
score = correct_classifications / 5.0

# Medium
score = 0.6 * (correct / 6) + 0.4 * (quality_responses / 4)

# Hard
score = 0.3 * priority_accuracy + 0.4 * response_quality + 0.3 * classification_accuracy
```

## Action Format

```json
{
  "classification": {
    "1": "low",
    "2": "high",
    "3": "medium"
  },
  "response": {
    "2": "Your refund has been processed."
  },
  "priority_order": [2, 1, 3]
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 7860 in use | `lsof -ti:7860 \| xargs kill -9` |
| Docker build fails | `docker build --no-cache .` |
| Import errors | `pip install -r requirements.txt` |
| API errors | Check `HF_TOKEN` is set |
| Tests fail | Verify Python 3.9+ |

## File Structure

```
email_triage_env/
├── app.py              # FastAPI server
├── environment.py      # Core logic
├── models.py           # Pydantic models
├── tasks.py            # Task definitions
├── inference.py        # Baseline agent
├── openenv.yaml        # Metadata
├── Dockerfile          # Container
├── requirements.txt    # Dependencies
└── README.md           # Documentation
```

## Deployment Checklist

- [ ] Tests pass: `python test_env.py`
- [ ] Server starts: `python app.py`
- [ ] Health check: `curl localhost:7860/health`
- [ ] Docker builds: `docker build .`
- [ ] Inference runs: `python inference.py --mock`
- [ ] Validation passes: `bash validate-submission.sh`
- [ ] HF Space deployed
- [ ] README complete

## Support

- **Documentation**: See README.md, QUICKSTART.md, DEPLOYMENT.md
- **Issues**: Check SUBMISSION_SUMMARY.md
- **Testing**: Run `python test_env.py`
- **Validation**: Run `bash validate-submission.sh`

## Quick Test

```bash
# One-liner to test everything
python test_env.py && \
python inference.py --mock && \
echo "✓ All tests passed!"
```
