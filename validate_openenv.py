import os
import yaml
import sys
from pathlib import Path

def log(msg):
    print(f"[VALIDATOR] {msg}")

def fail(msg):
    print(f"[FAILED] {msg}")
    sys.exit(1)

def validate():
    repo_dir = Path(".")
    
    # 1. Check openenv.yaml
    yaml_path = repo_dir / "openenv.yaml"
    if not yaml_path.exists():
        fail("openenv.yaml not found")
    
    try:
        with open(yaml_path, 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        fail(f"Failed to parse openenv.yaml: {e}")
    
    required_keys = ["name", "tasks", "action", "observation", "reward"]
    for key in required_keys:
        if key not in config:
            fail(f"Missing required key in openenv.yaml: {key}")
    
    if len(config.get("tasks", [])) < 3:
        fail("At least 3 tasks must be defined in openenv.yaml")
    
    log("openenv.yaml validated")

    # 2. Check Dockerfile
    dockerfile_path = repo_dir / "Dockerfile"
    if not dockerfile_path.exists():
        fail("Dockerfile not found")
    log("Dockerfile validated")

    # 3. Check Models
    try:
        from models import Action, Observation, Reward
        log("Pydantic models validated")
    except ImportError as e:
        fail(f"Failed to import models: {e}")
    except Exception as e:
        fail(f"Model validation error: {e}")

    # 4. Check Environment & Tasks
    try:
        from environment import EmailTriageEnv
        from tasks import TASKS
        if len(TASKS) < 3:
            fail("At least 3 tasks must be defined in tasks.py")
        log("Environment and tasks validated")
    except ImportError as e:
        fail(f"Failed to import environment/tasks: {e}")

    print("\n[SUCCESS] Environment matches OpenEnv specification!")

if __name__ == "__main__":
    validate()
