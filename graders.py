"""Grader functions for Email Triage Environment tasks"""
from typing import Dict, Any
from tasks import TASKS, _clamp_score, _grade_classif, _grade_priority


def grade_easy(actions: Dict[str, Any]) -> float:
    """
    Grader for easy task: Classify 5 emails correctly
    Returns score strictly between 0 and 1
    """
    return TASKS["easy"]["grader"](actions)


def grade_medium(actions: Dict[str, Any]) -> float:
    """
    Grader for medium task: Classify 6 emails and draft responses
    Returns score strictly between 0 and 1
    """
    return TASKS["medium"]["grader"](actions)


def grade_hard(actions: Dict[str, Any]) -> float:
    """
    Grader for hard task: Full triage with classification, responses, and priority
    Returns score strictly between 0 and 1
    """
    return TASKS["hard"]["grader"](actions)


# Export graders for validator
__all__ = ["grade_easy", "grade_medium", "grade_hard"]
