# Hugging Face Spaces Deployment Guide

## Prerequisites

1. Hugging Face account: https://huggingface.co/join
2. Git installed locally
3. Docker installed (for local testing)

## Step 1: Create New Space

1. Go to https://huggingface.co/new-space
2. Fill in details:
   - **Space name**: `email-triage-env` (or your choice)
   - **License**: MIT
   - **Select SDK**: Docker
   - **Space hardware**: CPU basic (free tier works)
   - **Visibility**: Public

3. Click "Create Space"

## Step 2: Clone Space Repository

```bash
# Clone your new Space
git clone https://huggingface.co/spaces/YOUR_USERNAME/email-triage-env
cd email-triage-env
```

## Step 3: Copy Environment Files

```bash
# Copy all files from email_triage_env/ to the Space repo
cp -r /path/to/email_triage_env/* .

# Ensure these files are present:
# - Dockerfile
# - app.py
# - environment.py
# - models.py
# - tasks.py
# - inference.py
# - openenv.yaml
# - requirements.txt
# - README.md
```

## Step 4: Create README.md Header

Add this to the top of your README.md:

```yaml
---
title: Email Triage Environment
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
tags:
  - openenv
  - reinforcement-learning
  - email-triage
  - real-world
---
```

## Step 5: Push to Hugging Face

```bash
# Add all files
git add .

# Commit
git commit -m "Initial deployment of Email Triage OpenEnv"

# Push to Hugging Face
git push
```

## Step 6: Monitor Build

1. Go to your Space URL: `https://huggingface.co/spaces/YOUR_USERNAME/email-triage-env`
2. Click "Logs" tab to monitor Docker build
3. Wait for "Running" status (usually 2-5 minutes)

## Step 7: Verify Deployment

```bash
# Test health endpoint
curl https://YOUR_USERNAME-email-triage-env.hf.space/health

# Test reset endpoint
curl -X POST https://YOUR_USERNAME-email-triage-env.hf.space/reset \
  -H "Content-Type: application/json" \
  -d '{"task": "easy"}'

# Should return JSON with emails array
```

## Step 8: Run Validation

```bash
# From local machine
bash validate-submission.sh https://YOUR_USERNAME-email-triage-env.hf.space
```

Expected output:
```
[PASSED] -- HF Space is live and responds to /reset
[PASSED] -- Docker build succeeded
[PASSED] -- openenv validate passed

All 3/3 checks passed!
```

## Troubleshooting

### Build Fails

Check logs in HF Space interface. Common issues:
- Missing dependencies in requirements.txt
- Dockerfile syntax errors
- Port not exposed (must be 7860)

### Space Shows "Building" Forever

- Check if Docker image is too large (>10GB)
- Verify Dockerfile has proper CMD instruction
- Check for infinite loops in app.py

### API Returns 500 Errors

- Check app logs in HF Space
- Verify all Python files are present
- Test locally first: `docker build . && docker run -p 7860:7860`

### Validation Script Fails

```bash
# Test each step manually
curl -X POST https://YOUR_SPACE.hf.space/reset -d '{"task":"easy"}'
docker build .
openenv validate
```

## Environment Variables (Optional)

If your Space needs API keys:

1. Go to Space Settings
2. Add secrets:
   - `HF_TOKEN`: Your Hugging Face token
   - `API_BASE_URL`: LLM endpoint
   - `MODEL_NAME`: Model identifier

3. Reference in Dockerfile:
```dockerfile
ENV HF_TOKEN=${HF_TOKEN}
ENV API_BASE_URL=${API_BASE_URL}
```

## Post-Deployment

### Update Space

```bash
# Make changes locally
git add .
git commit -m "Update description"
git push

# Space will auto-rebuild
```

### Monitor Usage

- View analytics in Space settings
- Check API logs for errors
- Monitor response times

### Share Your Space

- Add to OpenEnv registry
- Share URL in hackathon submission
- Tweet with #OpenEnv hashtag

## Final Checklist

- [ ] Space is public and accessible
- [ ] `/health` endpoint returns 200
- [ ] `/reset` endpoint returns valid observation
- [ ] Docker build completes in <10 minutes
- [ ] `validate-submission.sh` passes all checks
- [ ] README includes setup instructions
- [ ] `inference.py` runs successfully
- [ ] All 3 tasks have working graders

## Support

- HF Spaces docs: https://huggingface.co/docs/hub/spaces
- OpenEnv docs: https://github.com/meta-pytorch/OpenEnv
- Docker docs: https://docs.docker.com/

## Example Spaces

Reference these for inspiration:
- https://huggingface.co/spaces/openenv/example-env
- https://huggingface.co/spaces/openenv/miniwob-env
