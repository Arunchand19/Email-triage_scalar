#!/usr/bin/env python3
"""
Comprehensive test suite for Email Triage Environment
Tests all tasks, graders, and OpenEnv compliance
"""
import sys
from environment import EmailTriageEnv
from models import Action, Classification
from tasks import TASKS

def test_easy_task():
    """Test easy task with perfect agent"""
    print("Testing EASY task...")
    env = EmailTriageEnv()
    obs = env.reset("easy")
    
    assert len(obs.emails) == 5, f"Expected 5 emails, got {len(obs.emails)}"
    
    # Perfect classification
    action = Action(
        classification={
            1: Classification.low,
            2: Classification.high,
            3: Classification.medium,
            4: Classification.medium,
            5: Classification.low
        }
    )
    
    obs, reward, done, info = env.step(action)
    
    assert done, "Episode should be done after classifying all emails"
    assert reward.score == 1.0, f"Expected score 1.0, got {reward.score}"
    print(f"✓ EASY task passed: score={reward.score:.3f}")
    return True

def test_medium_task():
    """Test medium task with perfect agent"""
    print("Testing MEDIUM task...")
    env = EmailTriageEnv()
    obs = env.reset("medium")
    
    assert len(obs.emails) == 6, f"Expected 6 emails, got {len(obs.emails)}"
    
    # Perfect classification + responses
    action = Action(
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
        }
    )
    
    obs, reward, done, info = env.step(action)
    
    assert done, "Episode should be done"
    assert reward.score >= 0.95, f"Expected score >= 0.95, got {reward.score}"
    print(f"✓ MEDIUM task passed: score={reward.score:.3f}")
    return True

def test_hard_task():
    """Test hard task with perfect agent"""
    print("Testing HARD task...")
    env = EmailTriageEnv()
    obs = env.reset("hard")
    
    assert len(obs.emails) == 10, f"Expected 10 emails, got {len(obs.emails)}"
    
    # Perfect classification + responses + priority
    action = Action(
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
    
    obs, reward, done, info = env.step(action)
    
    assert done, "Episode should be done"
    assert reward.score >= 0.95, f"Expected score >= 0.95, got {reward.score}"
    print(f"✓ HARD task passed: score={reward.score:.3f}")
    return True

def test_graders():
    """Test grader functions directly"""
    print("Testing graders...")
    
    # Easy grader
    easy_actions = {
        'classification': {1: 'low', 2: 'high', 3: 'medium', 4: 'medium', 5: 'low'},
        'response': {},
        'priority_order': []
    }
    easy_score = TASKS['easy']['grader'](easy_actions)
    assert easy_score == 1.0, f"Easy grader: expected 1.0, got {easy_score}"
    
    # Medium grader
    medium_actions = {
        'classification': {1: 'low', 2: 'high', 3: 'medium', 4: 'medium', 5: 'low', 6: 'high'},
        'response': {
            2: "Refund processed for order #123",
            3: "Thursday meeting confirmed",
            4: "Report submitted on time",
            6: "Bug fix deployed to production"
        },
        'priority_order': []
    }
    medium_score = TASKS['medium']['grader'](medium_actions)
    assert medium_score >= 0.95, f"Medium grader: expected >= 0.95, got {medium_score}"
    
    # Hard grader
    hard_actions = {
        'classification': {1: 'low', 2: 'high', 3: 'medium', 4: 'medium', 5: 'low',
                          6: 'high', 7: 'high', 8: 'high', 9: 'medium', 10: 'high'},
        'response': {
            2: "Refund request processed within 24 hours",
            6: "Production bug escalated to engineering team",
            8: "Contract renewal approved by legal",
            10: "Security alert verified as legitimate"
        },
        'priority_order': [2, 6, 10, 8, 1, 3, 4, 7, 9, 5]
    }
    hard_score = TASKS['hard']['grader'](hard_actions)
    assert hard_score >= 0.95, f"Hard grader: expected >= 0.95, got {hard_score}"
    
    print(f"✓ All graders passed: easy={easy_score:.3f}, medium={medium_score:.3f}, hard={hard_score:.3f}")
    return True

def test_state_management():
    """Test state() method"""
    print("Testing state management...")
    env = EmailTriageEnv()
    
    # Should fail before reset
    try:
        env.state()
        assert False, "state() should fail before reset"
    except ValueError:
        pass
    
    # Should work after reset
    obs = env.reset("easy")
    state = env.state()
    assert state.step_count == 0, f"Expected step_count=0, got {state.step_count}"
    assert len(state.emails) == 5, f"Expected 5 emails, got {len(state.emails)}"
    
    # Should update after step
    action = Action(classification={1: Classification.low})
    env.step(action)
    state = env.state()
    assert state.step_count == 1, f"Expected step_count=1, got {state.step_count}"
    
    print("✓ State management passed")
    return True

def test_reward_shaping():
    """Test intermediate reward signals"""
    print("Testing reward shaping...")
    env = EmailTriageEnv()
    env.reset("easy")
    
    # Partial correct classification
    action = Action(classification={1: Classification.low, 2: Classification.high})
    obs, reward, done, info = env.step(action)
    
    assert not done, "Episode should not be done with partial classification"
    assert 0.0 <= reward.score <= 1.0, f"Reward out of range: {reward.score}"
    
    print(f"✓ Reward shaping passed: intermediate reward={reward.score:.3f}")
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("Email Triage Environment Test Suite")
    print("=" * 60)
    
    tests = [
        test_easy_task,
        test_medium_task,
        test_hard_task,
        test_graders,
        test_state_management,
        test_reward_shaping
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1
        print()
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
