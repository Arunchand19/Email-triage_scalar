# Inference Script Usage Guide

## Overview

The `inference.py` script runs a baseline agent against the Email Triage environment. It supports two modes:

1. **Mock Mode**: Uses hardcoded correct answers (no API calls)
2. **Real Mode**: Uses OpenAI-compatible LLM API

## Quick Start

### Option 1: Mock Mode (Recommended for Testing)

No API key required. Uses perfect agent with hardcoded answers.

```bash
python inference.py --mock
```

**Expected Output:**
```
[START] task=easy env=email_triage_env model=MockAgent
[STEP] step=1 action={"classification":{"1":"low","2":"high"...}} reward=1.00 done=true error=null
[END] success=true steps=1 score=1.000 rewards=1.00
```

### Option 2: Real Mode (Requires API Key)

Uses actual LLM to generate responses.

#### On Linux/Mac:
```bash
export HF_TOKEN="your_huggingface_token_here"
python inference.py
```

#### On Windows (CMD):
```cmd
set HF_TOKEN=your_huggingface_token_here
python inference.py
```

#### On Windows (PowerShell):
```powershell
$env:HF_TOKEN="your_huggingface_token_here"
python inference.py
```

## Environment Variables

### Required (for Real Mode)

| Variable | Description | Example |
|----------|-------------|---------|
| `HF_TOKEN` | Hugging Face API token | `hf_xxxxxxxxxxxxx` |

### Optional (with Defaults)

| Variable | Default | Description |
|----------|---------|-------------|
| `API_BASE_URL` | `https://router.huggingface.co/v1` | LLM API endpoint |
| `MODEL_NAME` | `Qwen/Qwen2.5-72B-Instruct` | Model identifier |
| `EMAIL_TRIAGE_TASK` | `easy` | Task: easy/medium/hard |

## Examples

### Test All Tasks (Mock Mode)

```bash
# Easy task
python inference.py --mock

# Medium task
EMAIL_TRIAGE_TASK=medium python inference.py --mock

# Hard task
EMAIL_TRIAGE_TASK=hard python inference.py --mock
```

### Use Different Model

```bash
export HF_TOKEN="your_token"
export MODEL_NAME="meta-llama/Llama-3.1-70B-Instruct"
python inference.py
```

### Use Custom API Endpoint

```bash
export HF_TOKEN="your_token"
export API_BASE_URL="https://api.openai.com/v1"
export MODEL_NAME="gpt-4"
python inference.py
```

## Getting HF_TOKEN

1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Give it a name (e.g., "openenv-inference")
4. Select "Read" permission
5. Click "Generate"
6. Copy the token (starts with `hf_`)

## Output Format

The script outputs structured logs in the required format:

### [START] Line
```
[START] task=<task_name> env=<benchmark> model=<model_name>
```

### [STEP] Lines (one per step)
```
[STEP] step=<n> action=<action_json> reward=<0.00> done=<true|false> error=<null>
```

### [END] Line (always emitted)
```
[END] success=<true|false> steps=<n> score=<0.000> rewards=<r1,r2,...>
```

## Troubleshooting

### Error: "HF_TOKEN not found"

**Solution**: Run in mock mode or set the environment variable:
```bash
python inference.py --mock
# OR
export HF_TOKEN="your_token"
python inference.py
```

### Error: "Connection refused" or "API error"

**Possible causes**:
1. Invalid HF_TOKEN
2. Network connectivity issues
3. API endpoint down

**Solution**: Test with mock mode first:
```bash
python inference.py --mock
```

### Error: "Module not found"

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Slow execution

**Cause**: LLM API calls can be slow

**Solution**: 
- Use mock mode for testing: `python inference.py --mock`
- Use faster model: `export MODEL_NAME="Qwen/Qwen2.5-7B-Instruct"`

## Performance Expectations

### Mock Mode
- **Runtime**: <5 seconds per task
- **Score**: 1.000 (perfect)
- **Steps**: 1 per task

### Real Mode (LLM)
- **Runtime**: 10-60 seconds per task (depends on API)
- **Score**: 0.4-1.0 (depends on model and task)
- **Steps**: 1-10 per task

## Batch Testing

Test all tasks at once:

```bash
#!/bin/bash
for task in easy medium hard; do
    echo "Testing $task task..."
    EMAIL_TRIAGE_TASK=$task python inference.py --mock
    echo ""
done
```

Save as `test_all.sh` and run:
```bash
chmod +x test_all.sh
./test_all.sh
```

## Integration with Validation

The inference script is used by the validation system:

```bash
# Start server
python app.py &

# Run validation (includes inference test)
bash validate-submission.sh http://localhost:7860
```

## Advanced Usage

### Save Output to File

```bash
python inference.py --mock > results.txt 2>&1
```

### Parse Results

```python
import re

with open('results.txt') as f:
    content = f.read()
    
# Extract score
match = re.search(r'score=(\d+\.\d+)', content)
if match:
    score = float(match.group(1))
    print(f"Final score: {score}")
```

### Run Multiple Times

```bash
# Run 5 times and average scores
for i in {1..5}; do
    python inference.py --mock | grep "score=" | cut -d'=' -f5 | cut -d' ' -f1
done | awk '{sum+=$1} END {print "Average:", sum/NR}'
```

## Support

- **Documentation**: See README.md
- **Issues**: Check SUBMISSION_SUMMARY.md
- **Quick Reference**: See REFERENCE.md
- **API Docs**: https://huggingface.co/docs/api-inference/

## Summary

**For testing**: Always use `--mock` flag
```bash
python inference.py --mock
```

**For real evaluation**: Set HF_TOKEN and run
```bash
export HF_TOKEN="your_token"
python inference.py
```
