#!/usr/bin/env python3
"""Final verification that graders meet OpenEnv Task Validation requirements"""

import yaml
from graders import grade_easy, grade_medium, grade_hard

print("=" * 70)
print("FINAL TASK VALIDATION VERIFICATION")
print("=" * 70)

# Load openenv.yaml
with open('openenv.yaml', 'r') as f:
    config = yaml.safe_load(f)

tasks = config['tasks']
print(f"\nFound {len(tasks)} tasks in openenv.yaml")

# Check each task has a grader
graders_found = 0
grader_map = {
    'grade_easy': grade_easy,
    'grade_medium': grade_medium,
    'grade_hard': grade_hard
}

for task in tasks:
    task_name = task['name']
    grader_path = task['grader']
    print(f"\nTask: {task_name}")
    print(f"  Grader: {grader_path}")
    
    # Parse grader path
    module, func = grader_path.split('.')
    
    if module == 'graders' and func in grader_map:
        grader = grader_map[func]
        
        # Test with empty actions
        test_actions = {
            'classification': {},
            'response': {},
            'priority_order': []
        }
        
        score = grader(test_actions)
        print(f"  Test score (empty): {score}")
        
        # Verify score is in valid range
        if 0.0 < score < 1.0:
            print(f"  [PASS] Score in valid range (0.0, 1.0)")
            graders_found += 1
        else:
            print(f"  [FAIL] Score {score} out of range")
    else:
        print(f"  [FAIL] Grader not found or invalid")

print("\n" + "=" * 70)
print(f"RESULT: {graders_found} graders validated")

if graders_found >= 3:
    print("[PASS] Task Validation requirements met (3+ graders)")
    print("=" * 70)
    print("\nREADY FOR SUBMISSION!")
else:
    print(f"[FAIL] Need at least 3 graders, found {graders_found}")
    print("=" * 70)
