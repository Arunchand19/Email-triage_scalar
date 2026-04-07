import asyncio
import json
from environment import EmailTriageEnv
from models import Action, Classification

async def manual_test():
    env = EmailTriageEnv()
    
    # 1. Reset the environment (This is the 'Input' from the environment to you)
    obs = env.reset("easy")
    print("\n--- ENVIRONMENT OUTPUT (Observations) ---")
    print(f"Task: {obs.current_task}")
    print(f"Emails to process: {len(obs.emails)}")
    for e in obs.emails:
        print(f"  [ID {e.id}] From: {e.sender} | Subj: {e.subject}")

    # 2. Provide your 'Input' (The Action)
    # Let's give a perfect input for the easy task
    my_input = Action(
        classification={
            1: Classification.low,
            2: Classification.high,
            3: Classification.medium,
            4: Classification.medium,
            5: Classification.low
        },
        response={2: "I'll handle this immediately!"},
        priority_order=[2, 3, 4, 1, 5]
    )

    print("\n--- YOUR INPUT (Action) ---")
    print(json.dumps(my_input.model_dump(), indent=2))

    # 3. Validation (The environment checks your input)
    obs, reward_obj, done, info = env.step(my_input)
    
    print("\n--- VALIDATION RESULT (Rewards) ---")
    print(f"Score: {reward_obj.score:.2f}")
    print(f"Feedback: {reward_obj.feedback}")
    print(f"Is Task Complete? {done}")

if __name__ == "__main__":
    asyncio.run(manual_test())
