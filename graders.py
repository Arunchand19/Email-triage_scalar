"""Grader functions for Email Triage Environment tasks"""
from typing import Dict, Any, List


def _grade_classif(email_id: int, cls: str) -> bool:
    """Check if classification is correct"""
    correct = {
        1: "low", 2: "high", 3: "medium", 4: "medium", 5: "low",
        6: "high", 7: "high", 8: "high", 9: "medium", 10: "high"
    }
    return correct.get(email_id) == cls


def _grade_priority(order: List[int]) -> float:
    """Grade priority ordering"""
    ideal = [2, 6, 10, 8, 1, 3, 4, 7, 9, 5]
    if len(order) != 10:
        return 0.01
    score = sum(1 for i, eid in enumerate(order[:5]) if i < len(ideal) and eid == ideal[i]) / 5.0
    tail_match = sum(1 for eid in ideal[5:] if eid in order[5:]) / 5.0
    raw_score = score * 0.8 + tail_match * 0.2
    return max(0.01, min(0.99, raw_score))


def _clamp_score(score: float) -> float:
    """Ensure score is strictly between 0 and 1"""
    if score <= 0.0:
        return 0.01
    elif score >= 1.0:
        return 0.99
    return score


def grade_easy(actions: Dict[str, Any]) -> float:
    """
    Grader for easy task: Classify 5 emails correctly
    Returns score strictly between 0 and 1
    """
    classification = actions.get('classification', {})
    correct_count = sum(1 for eid, cls in classification.items() if _grade_classif(int(eid), cls))
    return _clamp_score(correct_count / 5.0)


def grade_medium(actions: Dict[str, Any]) -> float:
    """
    Grader for medium task: Classify 6 emails and draft responses
    Returns score strictly between 0 and 1
    """
    classification = actions.get('classification', {})
    responses = actions.get('response', {})
    
    classif_score = sum(1 for eid, cls in classification.items() if _grade_classif(int(eid), cls)) / 6.0
    response_score = sum(1 for eid in [2, 3, 4, 6] if eid in responses and len(str(responses[eid]).strip()) > 20) / 4.0
    
    return _clamp_score(classif_score * 0.6 + response_score * 0.4)


def grade_hard(actions: Dict[str, Any]) -> float:
    """
    Grader for hard task: Full triage with classification, responses, and priority
    Returns score strictly between 0 and 1
    """
    classification = actions.get('classification', {})
    responses = actions.get('response', {})
    priority_order = actions.get('priority_order', [])
    
    priority_score = _grade_priority(priority_order)
    response_score = sum(1 for eid in [2, 6, 8, 10] if eid in responses and len(str(responses[eid])) > 20) / 4.0
    classif_score = sum(1 for eid in [2, 6, 8, 10] if eid in classification and _grade_classif(int(eid), classification[eid])) / 4.0
    
    return _clamp_score(0.3 * priority_score + 0.4 * response_score + 0.3 * classif_score)


# Export graders for validator
__all__ = ["grade_easy", "grade_medium", "grade_hard"]
