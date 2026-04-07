# How to Run Inference with Your Token

## ✅ Your Token is Now Configured

Your actual HF_TOKEN has been saved in `.env` file (which is ignored by git for security).

## 🚀 Run Inference

### Option 1: Using .env file (Recommended)

The inference script will automatically read from `.env` file:

```bash
cd email_triage_env
python inference.py
```

### Option 2: Set Environment Variable Manually

**Windows CMD:**
```cmd
set HF_TOKEN=your_huggingface_token_here
python inference.py
```

**Windows PowerShell:**
```powershell
$env:HF_TOKEN="your_huggingface_token_here"
python inference.py
```

**Linux/Mac:**
```bash
export HF_TOKEN="your_huggingface_token_here"
python inference.py
```

### Option 3: Mock Mode (No API calls)

Test without using your token:

```bash
python inference.py --mock
```

## 📊 Expected Output

### With Real Token:
```
[START] task=easy env=email_triage_env model=Qwen/Qwen2.5-72B-Instruct
[STEP] step=1 action={"classification":{...}} reward=0.85 done=true error=null
[END] success=true steps=1 score=0.850 rewards=0.85
```

### With Mock Mode:
```
[START] task=easy env=email_triage_env model=MockAgent
[STEP] step=1 action={"classification":{...}} reward=1.00 done=true error=null
[END] success=true steps=1 score=1.000 rewards=1.00
```

## 🔒 Security Notes

1. ✅ `.env` file is in `.gitignore` - won't be committed
2. ✅ `.env.example` has placeholder - safe to commit
3. ⚠️ Never share your actual token publicly
4. ⚠️ Never commit `.env` file to git

## 🧪 Test All Tasks

```bash
# Easy task
python inference.py

# Medium task
set EMAIL_TRIAGE_TASK=medium
python inference.py

# Hard task
set EMAIL_TRIAGE_TASK=hard
python inference.py
```

## ❓ Troubleshooting

### Error: "HF_TOKEN not found"

**Solution**: The `.env` file should be in the same directory as `inference.py`

Check:
```bash
# Verify .env exists
dir .env

# Verify it contains your token
type .env
```

### Error: "API connection failed"

**Solution**: Try mock mode first to verify environment works:
```bash
python inference.py --mock
```

### Token Not Working

1. Verify token is valid at https://huggingface.co/settings/tokens
2. Check token has "Read" permission
3. Try regenerating token if needed

## ✅ Quick Test

Run this to verify everything works:

```bash
# Test with mock (no API call)
python inference.py --mock

# Test with real token (uses API)
python inference.py
```

Both should complete successfully!
