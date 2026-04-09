"""Inference Script for Email Triage Environment"""
import asyncio
import os
import textwrap
import json
import sys
from typing import List, Optional
from pathlib import Path

from openai import OpenAI

from environment import EmailTriageEnv
from models import Action, Classification

# Load .env file if it exists
env_file = Path(__file__).parent / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip())

# MANDATORY environment variables - use API_KEY (injected by validator) or HF_TOKEN (local)
API_KEY = os.getenv("API_KEY") or os.getenv("HF_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
TASK_NAME = os.getenv("EMAIL_TRIAGE_TASK", "easy")
BENCHMARK = "email_triage_env"
MAX_STEPS = 10
TEMPERATURE = 0.3
MAX_TOKENS = 500
SUCCESS_SCORE_THRESHOLD = 0.5

# Check for mock mode
MOCK_MODE = "--mock" in sys.argv

def log_start(task: str, env: str, model: str) -> None: 
    print(f"[START] task={task} env={env} model={model}", flush=True) 

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None: 
    error_val = error if error else "null" 
    done_val = str(done).lower() 
    print( 
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}", 
        flush=True, 
    ) 

def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True) 

def get_mock_action(obs, task_name: str) -> Action:
    """Mock agent with correct answers for each task"""
    if task_name == "easy":
        return Action(
            classification={
                1: Classification.low,
                2: Classification.high,
                3: Classification.medium,
                4: Classification.medium,
                5: Classification.low
            },
            response={},
            priority_order=None
        )
    elif task_name == "medium":
        return Action(
            classification={
                1: Classification.low,
                2: Classification.high,
                3: Classification.medium,
                4: Classification.medium,
                5: Classification.low,
                6: Classification.high
            },
            response={
                2: "We apologize for the inconvenience. Your refund for order #123 has been processed.",
                3: "Yes, Thursday works. I'll send a calendar invite.",
                4: "Report submitted. Thank you for the reminder.",
                6: "Critical bug acknowledged. Team is investigating immediately."
            },
            priority_order=None
        )
    else:  # hard
        return Action(
            classification={
                1: Classification.low,
                2: Classification.high,
                3: Classification.medium,
                4: Classification.medium,
                5: Classification.low,
                6: Classification.high,
                7: Classification.high,
                8: Classification.high,
                9: Classification.medium,
                10: Classification.high
            },
            response={
                2: "Your refund request for order #123 is being processed. You'll receive confirmation within 24 hours.",
                6: "Production bug escalated to engineering team. Investigating root cause and deploying hotfix.",
                8: "Contract renewal approved. Legal team will finalize documents by EOD tomorrow.",
                10: "Security alert reviewed. Login from new IP verified as legitimate. No action needed."
            },
            priority_order=[2, 6, 10, 8, 1, 3, 4, 7, 9, 5]
        )

def build_system_prompt() -> str:
    return textwrap.dedent(
        """
        You are an AI assistant specialized in email triage.
        Output ONLY a JSON object:
        {
          "classification": {"1": "low", "2": "high"},
          "response": {"2": "Draft response"},
          "priority_order": [2, 1]
        }
        """
    ).strip()

def build_user_prompt(obs) -> str:
    emails_text = "\n".join([f"ID:{e.id} | From:{e.sender} | Subj:{e.subject}" for e in obs.emails])
    return f"Task: {obs.current_task}\n\nEmails:\n{emails_text}"

def get_model_action(client: OpenAI, obs, task_name: str) -> Action:
    if MOCK_MODE:
        return get_mock_action(obs, task_name)
        
    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(obs)
    
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        response_format={"type": "json_object"}
    )
    text = (completion.choices[0].message.content or "").strip()
    data = json.loads(text)
    return Action(**data)

async def main() -> None:
    if not MOCK_MODE and not API_KEY:
        print("[ERROR] API_KEY not found. Run with --mock or set API_KEY environment variable.", flush=True)
        print("\nExample usage:", flush=True)
        print("  Mock mode:  python inference.py --mock", flush=True)
        print("  Real mode:  export API_KEY='your_token' && python inference.py", flush=True)
        return

    # Initialize OpenAI client with environment variables
    client = None if MOCK_MODE else OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    env = EmailTriageEnv()

    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(task=TASK_NAME, env=BENCHMARK, model="MockAgent" if MOCK_MODE else MODEL_NAME)

    try:
        obs = env.reset(TASK_NAME)
        
        for step in range(1, MAX_STEPS + 1):
            action = get_model_action(client, obs, TASK_NAME)
            action_str = json.dumps(action.model_dump())[:100]  # Truncate for logging
            
            obs, reward_obj, done, info = env.step(action)
            
            reward = reward_obj.score
            rewards.append(reward)
            steps_taken = step
            
            log_step(step=step, action=action_str, reward=reward, done=done, error=None)
            
            if done:
                break

        score = rewards[-1] if rewards else 0.0
        success = score >= SUCCESS_SCORE_THRESHOLD

    except Exception as e:
        print(f"[DEBUG] Runtime error: {e}", flush=True)
    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

if __name__ == "__main__":
    asyncio.run(main())
