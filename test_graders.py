#!/usr/bin/env python3
"""Test script to verify graders meet OpenEnv validation requirements"""

import sys
from graders import grade_easy, grade_medium, grade_hard

def test_grader(name, grader_func, test_actions):
    """Test a grader function"""
    print(f"\nTesting {name}...")
    try:
        score = grader_func(test_actions)
        print(f"  Score: {score}")
        
        # Verify score is between 0 and 1
        if not (0.0 < score < 1.0):
            print(f"  [FAIL] Score {score} not in range (0.0, 1.0)")
            return False
        
        # Verify score is a float
        if not isinstance(score, float):
            print(f"  [FAIL] Score is not a float, got {type(score)}")
            return False
        
        print(f"  [PASS] Score is valid")
        return True
    except Exception as e:
        print(f"  [FAIL] {e}")
        return False

def main():
    print("=" * 60)
    print("OpenEnv Grader Validation Test")
    print("=" * 60)
    
    # Test data for each task
    easy_actions = {
        'classification': {
            1: 'low', 2: 'high', 3: 'medium', 4: 'medium', 5: 'low'
        }
    }
    
    medium_actions = {
        'classification': {
            1: 'low', 2: 'high', 3: 'medium', 4: 'medium', 5: 'low', 6: 'high'
        },
        'response': {
            2: 'I will process your refund request immediately and update you within 24 hours.',
            3: 'Meeting scheduled for next Thursday at 2 PM.',
            4: 'Monthly report has been submitted as requested.',
            6: 'Critical bug has been identified and fix is being deployed to production.'
        }
    }
    
    hard_actions = {
        'classification': {
            1: 'low', 2: 'high', 3: 'medium', 4: 'medium', 5: 'low',
            6: 'high', 7: 'high', 8: 'high', 9: 'medium', 10: 'high'
        },
        'response': {
            2: 'Your refund request has been processed and approved. Funds will be returned within 3-5 business days.',
            6: 'Critical production bug identified. Emergency fix deployed and monitoring system stability.',
            8: 'Contract renewal approved and signed. Documents forwarded to legal team for processing.',
            10: 'Security alert investigated. Login was from authorized device. No action required.'
        },
        'priority_order': [2, 6, 10, 8, 1, 3, 4, 7, 9, 5]
    }
    
    # Test all graders
    results = []
    results.append(test_grader("grade_easy", grade_easy, easy_actions))
    results.append(test_grader("grade_medium", grade_medium, medium_actions))
    results.append(test_grader("grade_hard", grade_hard, hard_actions))
    
    # Test with empty/minimal actions
    print("\nTesting edge cases...")
    empty_actions = {'classification': {}, 'response': {}, 'priority_order': []}
    results.append(test_grader("grade_easy (empty)", grade_easy, empty_actions))
    results.append(test_grader("grade_medium (empty)", grade_medium, empty_actions))
    results.append(test_grader("grade_hard (empty)", grade_hard, empty_actions))
    
    # Summary
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("[PASS] ALL TESTS PASSED - Graders are ready for submission")
        print("=" * 60)
        return 0
    else:
        print("[FAIL] SOME TESTS FAILED - Fix graders before submission")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
