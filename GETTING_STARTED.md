# Getting Started - 5 Minutes

## Step 1: Install Dependencies (1 minute)

```bash
cd email_triage_env
pip install -r requirements.txt
```

## Step 2: Run Mock Inference (1 minute)

**No API key needed!**

### Windows:
```cmd
python inference.py --mock
```

Or double-click: `run_mock_inference.bat`

### Linux/Mac:
```bash
python inference.py --mock
```

Or run: `bash run_mock_inference.sh`

### Expected Output:
```
[START] task=easy env=email_triage_env model=MockAgent
[STEP] step=1 action={"classification":{"1":"low","2":"high","3":"medium","4":"medium","5":"low"}...} reward=1.00 done=true error=null
[END] success=true steps=1 score=1.000 rewards=1.00
```

✅ **If you see this output, everything works!**

## Step 3: Test All Tasks (2 minutes)

```bash
# Easy task
python inference.py --mock

# Medium task
EMAIL_TRIAGE_TASK=medium python inference.py --mock

# Hard task
EMAIL_TRIAGE_TASK=hard python inference.py --mock
```

All should show `success=true` and `score=1.000`

## Step 4: Start Server (1 minute)

```bash
python app.py
```

Open browser: http://localhost:7860

You should see: `{"message": "Welcome to the Email Triage OpenEnv!", ...}`

## That's It! 🎉

Your environment is working correctly.

---

## Next Steps

### Run Full Tests
```bash
python test_env.py
```

### Build Docker Image
```bash
docker build -t email-triage-env .
docker run -p 7860:7860 email-triage-env
```

### Deploy to Hugging Face
See `DEPLOYMENT.md` for instructions

### Use Real LLM (Optional)
```bash
export HF_TOKEN="your_token_here"
python inference.py
```

Get token: https://huggingface.co/settings/tokens

---

## Troubleshooting

### Error: "HF_TOKEN not found"
✅ **This is normal!** Just run with `--mock` flag:
```bash
python inference.py --mock
```

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Error: "Port already in use"
```bash
# Kill existing process
lsof -ti:7860 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :7860   # Windows (then taskkill)
```

### More Help
See `TROUBLESHOOTING.md` for detailed solutions

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `python inference.py --mock` | Test inference (no API key) |
| `python test_env.py` | Run test suite |
| `python app.py` | Start server |
| `docker build -t email-triage-env .` | Build Docker image |
| `bash validate-submission.sh http://localhost:7860` | Validate deployment |

---

## Documentation

- **README.md** - Complete documentation
- **QUICKSTART.md** - Quick start guide
- **INFERENCE_GUIDE.md** - Inference details
- **TROUBLESHOOTING.md** - Common issues
- **REFERENCE.md** - Quick reference
- **DEPLOYMENT.md** - HF Spaces deployment

---

## Success Criteria

✅ `python inference.py --mock` runs without errors
✅ Output shows `[START]`, `[STEP]`, `[END]` lines
✅ Final line shows `success=true` and `score=1.000`
✅ `python app.py` starts server on port 7860
✅ Browser shows welcome message at http://localhost:7860

**If all above pass, you're ready to deploy!**
