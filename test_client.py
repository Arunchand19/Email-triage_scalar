import asyncio
import websockets
import json
from models import Action, Classification

async def test_env():
    uri = "ws://localhost:7860/ws"
    async with websockets.connect(uri) as websocket:
        # Reset the environment
        print("Resetting environment...")
        await websocket.send(json.dumps({"type": "reset", "task": "easy"}))
        response = await websocket.recv()
        obs = json.loads(response)
        print(f"Observation: {obs['data']['current_task']}")
        print(f"Emails: {len(obs['data']['emails'])}")

        # Take a step
        print("\nTaking a step...")
        action = Action(
            classification={
                1: Classification.low,
                2: Classification.high,
                3: Classification.medium,
                4: Classification.medium,
                5: Classification.low
            }
        )
        await websocket.send(json.dumps({
            "type": "step",
            "action": action.model_dump()
        }))
        response = await websocket.recv()
        result = json.loads(response)
        print(f"Reward: {result['data']['reward']['score']}")
        print(f"Feedback: {result['data']['reward']['feedback']}")
        print(f"Done: {result['data']['done']}")

        # Get state
        print("\nGetting state...")
        await websocket.send(json.dumps({"type": "state"}))
        response = await websocket.recv()
        state_msg = json.loads(response)
        if state_msg.get("type") == "error":
            print(f"Error getting state: {state_msg['message']}")
        else:
            print(f"Step count: {state_msg['data']['step_count']}")

if __name__ == "__main__":
    # Ensure websockets is installed
    try:
        asyncio.run(test_env())
    except ConnectionRefusedError:
        print("Error: Could not connect to the environment. Make sure app.py is running on port 7860.")
    except Exception as e:
        print(f"Error: {e}")
