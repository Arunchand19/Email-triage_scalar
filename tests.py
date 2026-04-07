import pytest
import sys
sys.path.append('.')

from environment import EmailTriageEnv
from tasks import TASKS
from models import Action

def test_reset():
    env = EmailTriageEnv()
    obs = env.reset("easy")
    assert len(obs.emails) == 5
    assert obs.current_task

def test_step_basic():
    env = EmailTriageEnv()
    env.reset("easy")
    action = Action(classification={1: "low"})
    obs, reward, done, info = env.step(action)
    assert 0.0 <= reward.score <= 1.0
    assert not done

def test_graders():
    actions_easy = {"classification": {1:"low",2:"high",3:"medium",4:"medium",5:"low"}}
    score = TASKS["easy"]["grader"](actions_easy)
    assert 0.8 <= score <= 1.0  # Perfect

    actions_medium = {**actions_easy, "response": {2: "Processing refund."}}
    score_m = TASKS["medium"]["grader"](actions_medium)
    assert score_m > 0.5

@pytest.mark.skip("Hard requires full actions")
def test_hard_grader():
    pass

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

