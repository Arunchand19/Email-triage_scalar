{
  "action": {
    "classification": {"1": "low", "2": "high"},
    "response": {"2": "Drafting your refund now."},
    "priority_order": [2, 1]
  }
}
import asyncio 
import json
from typing import List, Optional 

from environment import EmailTriageEnv
from models import Action, Classification

# Mock configuration
TASK_NAME = "easy" 
BENCHMARK = "email_triage_env" 
MODEL_NAME = "MockAgent-v1"

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
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}", flush=True) 

def get_mock_action(obs) -> Action:
    # A mock agent that knows the correct answers for the 'easy' task
    # 1: low, 2: high, 3: medium, 4: medium, 5: low
    return Action(
        classification={
            1: Classification.low,
            2: Classification.high,
            3: Classification.medium,
            4: Classification.medium,
            5: Classification.low
        },
        response={},
        priority_order=[2, 3, 4, 1, 5]
    )

async def main() -> None: 
    env = EmailTriageEnv()
    rewards: List[float] = [] 
    steps_taken = 0 
    success = False 

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME) 

    try: 
        obs = env.reset(TASK_NAME)
        print(f"[DEBUG] Input received: {len(obs.emails)} emails loaded from environment.")
        
        # Take one perfect step
        action = get_mock_action(obs)
        action_str = json.dumps(action.model_dump())
        
        obs, reward_obj, done, info = env.step(action)
        
        reward = reward_obj.score
        rewards.append(reward)
        steps_taken = 1
        
        log_step(step=1, action=action_str, reward=reward, done=done, error=None) 
        
        score = reward
        success = score >= 0.5 

    except Exception as e:
        print(f"[DEBUG] Runtime error: {e}", flush=True)
        return
    finally: 
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards) 

if __name__ == "__main__": 
    asyncio.run(main())
