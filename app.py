from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Dict, Any, Union, List, Optional
import uvicorn
import json
from models import Observation, Action, Reward, State, Email
from environment import EmailTriageEnv

app = FastAPI(title="Email Triage Env")
env = EmailTriageEnv() # Global for HTTP (single session)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    env = EmailTriageEnv()
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            msg_type = message.get("type")
            
            if msg_type == "reset":
                task = message.get("task", "easy")
                emails_data = message.get("emails")
                goal = message.get("goal")
                
                # Convert email dicts to models if provided
                from models import Email
                emails = [Email(**e) for e in emails_data] if emails_data else None
                
                obs = env.reset(task=task, emails=emails, goal=goal)
                await websocket.send_json({"type": "observation", "data": obs.model_dump()})
            
            elif msg_type == "step":
                action_data = message.get("action")
                if not action_data:
                    await websocket.send_json({"type": "error", "message": "Missing action"})
                    continue
                action = Action(**action_data)
                obs, reward, done, info = env.step(action)
                await websocket.send_json({
                    "type": "step_result",
                    "data": {
                        "observation": obs.model_dump(),
                        "reward": reward.model_dump(),
                        "done": done,
                        "info": info
                    }
                })
            
            elif msg_type == "state":
                try:
                    state = env.state()
                    await websocket.send_json({"type": "state", "data": state.model_dump()})
                except Exception as e:
                    await websocket.send_json({"type": "error", "message": str(e)})
            
            else:
                await websocket.send_json({"type": "error", "message": f"Unknown message type: {msg_type}"})
                
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"type": "error", "message": str(e)})

class StepRequest(BaseModel):
    action: Action
    task: str = "easy"

class ResetRequest(BaseModel):
    task: str = "easy"
    emails: Optional[List[Email]] = None
    goal: Optional[str] = None

@app.post("/", response_model=Dict[str, Any])
def step(request: StepRequest):
    try:
        obs, reward, done, info = env.step(request.action)
        return {
            "observation": obs.model_dump(),
            "reward": reward.model_dump(),
            "done": done,
            "info": info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_model=Dict[str, str])
def welcome():
    return {
        "message": "Welcome to the Email Triage OpenEnv!",
        "docs": "Check /docs for API documentation",
        "health": "/health",
        "status": "online"
    }

@app.post("/reset", response_model=Dict[str, Any])
def reset(request: ResetRequest):
    obs = env.reset(task=request.task, emails=request.emails, goal=request.goal)
    return obs.model_dump()

@app.get("/state", response_model=State)
def get_state():
    try:
        return env.state().model_dump()
    except:
        raise HTTPException(status_code=400, detail="Call reset first")

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)

