import random
from typing import Dict, Tuple, Any, Optional, List
from models import Observation, Action, Reward, State
from tasks import TASKS
from pydantic import ValidationError

class EmailTriageEnv:
    def __init__(self):
        self._state: Optional[State] = None
        self.task_name: str = ""

    def reset(self, task: str = "easy", emails: Optional[List[Any]] = None, goal: Optional[str] = None) -> Observation:
        self.task_name = task
        if emails and goal:
            # Custom task provided by user
            self._state = State(
                emails=emails,
                task=goal,
                progress="Custom inbox loaded. Take actions.",
                step_count=0
            )
        else:
            # Load from hardcoded tasks
            task_data = TASKS.get(task, TASKS["easy"])
            self._state = State(
                emails=task_data["emails"],
                task=task_data["goal"],
                progress="Inbox full. Take actions.",
                step_count=0
            )
        return Observation(
            emails=self._state.emails,
            current_task=self._state.task,
            task_progress=self._state.progress
        )

    def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
        if not self._state:
            raise ValueError("Call reset first")
        
        self._state.actions_history.append(action.model_dump())
        self._state.step_count += 1
        
        # Convert Classification enums to strings for grading
        classification_dict = {eid: cls.value if hasattr(cls, 'value') else cls 
                              for eid, cls in action.classification.items()}
        response_dict = action.response if action.response else {}
        priority_list = action.priority_order if action.priority_order else []
        
        # Compute intermediate reward for progress
        raw_reward = self._compute_reward(action)
        score = min(1.0, max(0.0, raw_reward))
        
        # Update progress
        progress = f"Step {self._state.step_count}: Classified {len(classification_dict)} emails, drafted {len(response_dict)} responses"
        self._state.progress = progress
        
        # Episode ends after max steps or when agent signals completion
        done = self._state.step_count >= 30 or len(classification_dict) >= len(self._state.emails)
        
        if done:
            # Use task grader for final score
            grader_input = {
                'classification': classification_dict,
                'response': response_dict,
                'priority_order': priority_list
            }
            final_score = TASKS[self.task_name]["grader"](grader_input)
            score = min(1.0, max(0.0, final_score))
        
        reward = Reward(score=score, feedback=f"Score: {score:.2f}")
        
        obs = Observation(
            emails=self._state.emails,
            current_task=self._state.task,
            task_progress=progress
        )
        
        return obs, reward, done, {"task": self.task_name}

    def state(self) -> State:
        if not self._state:
            raise ValueError("No active episode")
        return self._state

    def _compute_reward(self, action: Action) -> float:
        """Compute intermediate reward for progress tracking"""
        reward = 0.0
        
        # Convert enums to strings
        classification_dict = {eid: cls.value if hasattr(cls, 'value') else cls 
                              for eid, cls in action.classification.items()}
        
        # Correct classification bonus
        for eid, cls in classification_dict.items():
            if self._is_correct_classif(eid, cls):
                reward += 0.1
            else:
                reward -= 0.05
        
        # Response quality
        if action.response:
            for resp in action.response.values():
                if len(resp.strip()) > 20:
                    reward += 0.15
                elif len(resp.strip()) > 0:
                    reward += 0.05
        
        # Priority bonus
        if action.priority_order and len(action.priority_order) >= len(self._state.emails):
            reward += 0.2
        
        # Efficiency penalty for excessive steps
        if self._state.step_count > 20:
            reward -= 0.1
        
        return reward

    def _is_correct_classif(self, eid: int, cls: str) -> bool:
        from tasks import _grade_classif
        return _grade_classif(eid, cls)  # Reuse

