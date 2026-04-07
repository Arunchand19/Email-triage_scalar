# Documentation Index

## 📚 Complete Documentation Guide

### 🚀 Quick Start (Start Here!)

1. **GETTING_STARTED.md** - 5-minute setup guide
   - Install dependencies
   - Run mock inference (no API key needed)
   - Test all tasks
   - Start server

2. **QUICKSTART.md** - Quick reference for common tasks
   - Local setup
   - API testing
   - Docker commands
   - Validation

### 📖 Main Documentation

3. **README.md** - Complete project documentation
   - Environment description
   - Real-world utility
   - Action/observation spaces
   - Task descriptions
   - Reward function
   - Setup instructions
   - Baseline scores

### 🔧 Technical Guides

4. **INFERENCE_GUIDE.md** - Inference script usage
   - Mock mode vs real mode
   - Environment variables
   - Getting HF_TOKEN
   - Output format
   - Examples

5. **DEPLOYMENT.md** - Hugging Face Spaces deployment
   - Step-by-step deployment
   - Space configuration
   - Validation
   - Troubleshooting

6. **REFERENCE.md** - Quick reference card
   - Essential commands
   - Environment variables
   - API endpoints
   - Task overview
   - Grading formulas

### 🐛 Troubleshooting

7. **TROUBLESHOOTING.md** - Comprehensive troubleshooting
   - Common errors and solutions
   - Platform-specific issues
   - Performance optimization
   - Debugging tips

### ✅ Submission

8. **SUBMISSION_SUMMARY.md** - Complete submission checklist
   - All requirements verified
   - Expected scores
   - Deployment commands
   - Pre-submission checklist

---

## 📁 File Structure

### Core Files (Required)

| File | Purpose |
|------|---------|
| `app.py` | FastAPI server |
| `environment.py` | Environment logic |
| `models.py` | Pydantic models |
| `tasks.py` | Task definitions & graders |
| `inference.py` | Baseline agent (MANDATORY) |
| `openenv.yaml` | OpenEnv metadata |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Container definition |

### Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Main documentation |
| `GETTING_STARTED.md` | 5-minute quick start |
| `QUICKSTART.md` | Quick reference |
| `INFERENCE_GUIDE.md` | Inference usage |
| `DEPLOYMENT.md` | HF Spaces deployment |
| `REFERENCE.md` | Command reference |
| `TROUBLESHOOTING.md` | Problem solving |
| `SUBMISSION_SUMMARY.md` | Submission checklist |

### Configuration Files

| File | Purpose |
|------|---------|
| `.env.example` | Environment template |
| `.dockerignore` | Docker ignore rules |
| `.gitignore` | Git ignore rules |
| `docker-compose.yml` | Docker Compose config |
| `LICENSE` | MIT license |

### Testing & Validation

| File | Purpose |
|------|---------|
| `test_env.py` | Test suite |
| `validate-submission.sh` | Validation script |
| `setup.sh` | Automated setup |
| `run_mock_inference.sh` | Mock inference (Unix) |
| `run_mock_inference.bat` | Mock inference (Windows) |

### Metadata

| File | Purpose |
|------|---------|
| `README_HEADER.md` | HF Spaces header |

---

## 🎯 Usage Scenarios

### Scenario 1: First Time Setup

1. Read **GETTING_STARTED.md**
2. Run `pip install -r requirements.txt`
3. Run `python inference.py --mock`
4. ✅ Done!

### Scenario 2: Testing Environment

1. Run `python test_env.py`
2. Run `python inference.py --mock` for each task
3. Check **REFERENCE.md** for commands

### Scenario 3: Local Development

1. Follow **QUICKSTART.md**
2. Start server: `python app.py`
3. Test endpoints with curl
4. Refer to **REFERENCE.md** for API details

### Scenario 4: Docker Deployment

1. Check **QUICKSTART.md** Docker section
2. Build: `docker build -t email-triage-env .`
3. Run: `docker run -p 7860:7860 email-triage-env`
4. Validate: `bash validate-submission.sh http://localhost:7860`

### Scenario 5: Hugging Face Spaces

1. Follow **DEPLOYMENT.md** step-by-step
2. Copy files to HF Space repo
3. Add header from **README_HEADER.md**
4. Push and monitor build

### Scenario 6: Troubleshooting

1. Check **TROUBLESHOOTING.md** for your error
2. Try mock mode: `python inference.py --mock`
3. Run diagnostics: `python test_env.py`
4. Check **REFERENCE.md** for correct commands

### Scenario 7: Using Real LLM

1. Read **INFERENCE_GUIDE.md**
2. Get HF_TOKEN from https://huggingface.co/settings/tokens
3. Set environment variable
4. Run `python inference.py`

### Scenario 8: Submission Preparation

1. Review **SUBMISSION_SUMMARY.md**
2. Run all tests: `python test_env.py`
3. Run validation: `bash validate-submission.sh`
4. Verify all checkboxes are ✅

---

## 🔍 Finding Information

### "How do I run the inference script?"
→ **INFERENCE_GUIDE.md** or **GETTING_STARTED.md**

### "What are the environment variables?"
→ **REFERENCE.md** or **INFERENCE_GUIDE.md**

### "How do I deploy to Hugging Face?"
→ **DEPLOYMENT.md**

### "I'm getting an error"
→ **TROUBLESHOOTING.md**

### "What are the API endpoints?"
→ **REFERENCE.md** or **README.md**

### "How do tasks work?"
→ **README.md** (Tasks & Grading section)

### "What's the action/observation format?"
→ **README.md** (Action & Observation Space section)

### "How do I test everything?"
→ **QUICKSTART.md** or **GETTING_STARTED.md**

### "Is my submission ready?"
→ **SUBMISSION_SUMMARY.md**

### "Quick command reference?"
→ **REFERENCE.md**

---

## 📊 Documentation by Role

### For Developers

1. **README.md** - Understand the environment
2. **REFERENCE.md** - Quick command lookup
3. **TROUBLESHOOTING.md** - Debug issues

### For Testers

1. **GETTING_STARTED.md** - Quick setup
2. **INFERENCE_GUIDE.md** - Run tests
3. **REFERENCE.md** - Test commands

### For DevOps

1. **DEPLOYMENT.md** - Deploy to HF Spaces
2. **QUICKSTART.md** - Docker commands
3. **TROUBLESHOOTING.md** - Deployment issues

### For Evaluators

1. **README.md** - Environment overview
2. **SUBMISSION_SUMMARY.md** - Compliance checklist
3. **INFERENCE_GUIDE.md** - Run baseline

---

## 🎓 Learning Path

### Beginner (Never used OpenEnv)

1. **GETTING_STARTED.md** - Setup in 5 minutes
2. **README.md** - Understand the environment
3. **INFERENCE_GUIDE.md** - Run your first agent

### Intermediate (Familiar with OpenEnv)

1. **QUICKSTART.md** - Jump right in
2. **REFERENCE.md** - Command reference
3. **DEPLOYMENT.md** - Deploy to production

### Advanced (Building custom agents)

1. **README.md** - Deep dive into tasks
2. **models.py** - Study action/observation types
3. **tasks.py** - Understand grading logic
4. **environment.py** - Explore reward shaping

---

## 📞 Support Resources

### Documentation
- All `.md` files in this directory
- Inline code comments
- Docstrings in Python files

### External Resources
- OpenEnv: https://github.com/meta-pytorch/OpenEnv
- Hugging Face: https://huggingface.co/docs
- FastAPI: https://fastapi.tiangolo.com
- Docker: https://docs.docker.com

### Quick Help
```bash
# Test everything works
python inference.py --mock

# Get help on inference
python inference.py --help

# Check environment
python test_env.py

# Validate deployment
bash validate-submission.sh http://localhost:7860
```

---

## ✅ Checklist for Success

- [ ] Read **GETTING_STARTED.md**
- [ ] Run `python inference.py --mock` successfully
- [ ] All tests pass: `python test_env.py`
- [ ] Server starts: `python app.py`
- [ ] Docker builds: `docker build -t email-triage-env .`
- [ ] Validation passes: `bash validate-submission.sh`
- [ ] Read **SUBMISSION_SUMMARY.md**
- [ ] Ready to deploy!

---

## 🎯 TL;DR

**Just want to test it?**
```bash
pip install -r requirements.txt
python inference.py --mock
```

**Want to deploy?**
Read **DEPLOYMENT.md**

**Having issues?**
Check **TROUBLESHOOTING.md**

**Need quick reference?**
See **REFERENCE.md**

**Everything else?**
Read **README.md**
