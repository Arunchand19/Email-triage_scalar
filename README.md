# 📧 Email Triage OpenEnv

[![OpenEnv Compliance](https://img.shields.io/badge/OpenEnv-Compliant-green)](https://github.com/meta-pytorch/OpenEnv)
[![Docker Support](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)

## 📝 Environment Description

The **Email Triage Environment** simulates the real-world task of managing a professional inbox under information overload. This is a genuine workplace challenge faced daily by customer support agents, executive assistants, and knowledge workers.

### Real-World Utility

This environment models authentic email management scenarios:
- **Customer Support**: Prioritizing urgent refund requests and bug reports
- **Executive Assistance**: Managing calendar conflicts and contract deadlines  
- **Team Coordination**: Balancing meeting requests with project deliverables
- **Security Response**: Identifying and acting on security alerts

Unlike toy classification tasks, agents must:
1. **Assess Urgency**: Dynamically categorize emails by priority (low/medium/high)
2. **Draft Contextual Responses**: Generate professional, actionable replies
3. **Optimize Workflow**: Establish strategic priority ordering for maximum efficiency

### Motivation

Email overload costs organizations billions annually in lost productivity. Training AI agents to handle triage effectively can:
- Reduce response times for critical issues
- Improve customer satisfaction through faster resolution
- Free human workers for high-value tasks requiring creativity and judgment
- Provide 24/7 coverage for global operations

---

## 🛠 Action & Observation Space

### Action Space (Typed Pydantic Model)

Agents submit structured actions via the `Action` model:

```python
class Action(BaseModel):
    classification: Dict[int, Classification]  # email_id -> "low"|"medium"|"high"
    response: Dict[int, str]                   # email_id -> draft response (max 200 chars)
    priority_order: Optional[List[int]]        # ordered list of email IDs
```

**Field Descriptions:**
- `classification`: Maps email ID to urgency level. Required for all tasks.
- `response`: Draft responses for specific emails. Required for medium/hard tasks.
- `priority_order`: Sequence of email IDs for resolution order. Required for hard task.

### Observation Space (Typed Pydantic Model)

```python
class Observation(BaseModel):
    emails: List[Email]           # List of email objects
    current_task: str             # Task objective description
    task_progress: str            # Feedback on actions taken

class Email(BaseModel):
    id: int                       # Unique identifier
    subject: str                  # Email subject line
    body: str                     # Email content
    sender: str                   # Sender email address
```

**Field Descriptions:**
- `emails`: Complete inbox contents with metadata
- `current_task`: High-level mission objective
- `task_progress`: Dynamic feedback on agent performance

---

## 📊 Tasks & Grading

The environment features three tasks with progressive difficulty:

### Task 1: Easy Classification (🟢 Difficulty: Low)

**Objective**: Classify 5 emails by urgency

**Emails**:
1. Spam newsletter (low)
2. Urgent refund request (high)
3. Meeting scheduling (medium)
4. Monthly report reminder (medium)
5. Social invitation (low)

**Grader**: `score = correct_classifications / 5.0`
- Returns 1.0 for perfect classification
- Returns 0.0 for all incorrect

**Expected Difficulty**: Frontier models should achieve 0.8-1.0

### Task 2: Medium Response (🟡 Difficulty: Medium)

**Objective**: Classify 6 emails AND draft responses for high-priority items

**Additional Email**:
6. Critical bug report (high)

**Grader**: `score = 0.6 * (correct_classifications / 6) + 0.4 * (quality_responses / 4)`
- Classification accuracy: 60% weight
- Response quality: 40% weight (must be >20 chars for emails 2, 3, 4, 6)

**Expected Difficulty**: Frontier models should achieve 0.6-0.9

### Task 3: Hard Prioritization (🔴 Difficulty: High)

**Objective**: Full triage cycle for 10 emails with optimal priority ordering

**Additional Emails**:
7. CEO schedule conflict (high)
8. Contract renewal deadline (high)
9. Team offsite planning (medium)
10. Security alert (high)

**Grader**: `score = 0.3 * priority_accuracy + 0.4 * response_quality + 0.3 * classification_accuracy`
- Priority ordering: 30% weight (ideal: [2,6,10,8,1,3,4,7,9,5])
- Response quality: 40% weight (>20 chars for emails 2, 6, 8, 10)
- Classification: 30% weight (for critical emails only)

**Expected Difficulty**: Frontier models should achieve 0.4-0.7

---

## 🎯 Reward Function

The environment provides **dense reward signals** to facilitate learning:

### Positive Reinforcement
- `+0.10` per correct urgency classification
- `+0.15` per substantive response (>20 chars)
- `+0.05` per minimal response (>0 chars)
- `+0.20` bonus for complete priority ordering

### Penalties
- `-0.05` per incorrect classification
- `-0.10` for excessive steps (>20 steps)

### Episode Termination
- **Success**: Agent classifies all emails OR reaches 30 steps
- **Final Score**: Task-specific grader evaluates complete action (0.0-1.0)

---

## 🐳 Setup & Deployment

### Prerequisites
- Python 3.9+
- Docker (for containerized deployment)
- OpenAI-compatible API key (for inference)

### Local Setup

```bash
# Clone repository
git clone <your-repo-url>
cd email_triage_env

# Install dependencies
pip install -r requirements.txt

# Start environment server
python app.py
# Server runs on http://localhost:7860
```

### Docker Deployment

```bash
# Build image
docker build -t email-triage-env .

# Run container
docker run -p 7860:7860 email-triage-env

# Verify health
curl http://localhost:7860/health
```

### Hugging Face Spaces Deployment

1. Create new Space on Hugging Face
2. Select "Docker" as Space SDK
3. Push code to Space repository
4. Space will auto-build and deploy
5. Verify with: `curl -X POST https://your-space.hf.space/reset -H "Content-Type: application/json" -d '{"task": "easy"}'`

---

## 🧪 Running Inference

### Environment Variables

Set these before running inference:

```bash
export HF_TOKEN="your-huggingface-token"          # Required
export API_BASE_URL="https://router.huggingface.co/v1"  # Optional (default shown)
export MODEL_NAME="Qwen/Qwen2.5-72B-Instruct"     # Optional (default shown)
export EMAIL_TRIAGE_TASK="easy"                   # Optional: easy|medium|hard
```

### Run Baseline Agent

```bash
# With real LLM (requires HF_TOKEN)
python inference.py

# Mock mode (no API calls, uses hardcoded correct answers)
python inference.py --mock
```

### Expected Output Format

```
[START] task=easy env=email_triage_env model=Qwen/Qwen2.5-72B-Instruct
[STEP] step=1 action={"classification":{"1":"low","2":"high"...}} reward=0.85 done=true error=null
[END] success=true steps=1 score=1.000 rewards=0.85
```

---

## 📈 Baseline Scores

Evaluated with mock agent (perfect knowledge):

| Task | Score | Steps |
|------|-------|-------|
| Easy | 1.00  | 1     |
| Medium | 1.00 | 1     |
| Hard | 1.00  | 1     |

Expected scores for frontier LLMs (GPT-4, Claude-3, Gemini-1.5):

| Task | Expected Score Range |
|------|---------------------|
| Easy | 0.80 - 1.00         |
| Medium | 0.60 - 0.90       |
| Hard | 0.40 - 0.70         |

---

## ✅ Validation

Before submission, run the validation script:

```bash
# Start local server first
python app.py &

# Run validator (requires bash)
bash validate-submission.sh http://localhost:7860
```

Validator checks:
1. ✅ HF Space responds to `/reset` endpoint
2. ✅ Docker image builds successfully
3. ✅ OpenEnv spec compliance (`openenv validate`)

---

## 📋 OpenEnv Spec Compliance

### Typed Models (Pydantic)
- ✅ `Action`: classification, response, priority_order
- ✅ `Observation`: emails, current_task, task_progress
- ✅ `Reward`: score (0.0-1.0), feedback
- ✅ `State`: complete environment state

### Required Methods
- ✅ `reset(task: str) -> Observation`
- ✅ `step(action: Action) -> (Observation, Reward, bool, dict)`
- ✅ `state() -> State`

### Metadata
- ✅ `openenv.yaml` with task definitions
- ✅ 3 tasks with difficulty progression
- ✅ Deterministic graders returning 0.0-1.0

### Deployment
- ✅ FastAPI server with HTTP endpoints
- ✅ Dockerfile with health checks
- ✅ WebSocket support for interactive sessions

---

## 🏗 Project Structure

```
email_triage_env/
├── app.py                 # FastAPI server
├── environment.py         # Core environment logic
├── models.py              # Pydantic type definitions
├── tasks.py               # Task definitions & graders
├── inference.py           # Baseline agent script
├── openenv.yaml           # OpenEnv metadata
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container definition
├── README.md              # This file
└── validate-submission.sh # Pre-submission validator
```

---

## 👥 Team

**Team Dragon**
- Mallarapu Arun Chand (Lead) - arunchandmallarapu@gmail.com
- T. Someswararao - someshtellakula@gmail.com

---

## 📄 License

MIT License - See LICENSE file for details