from typing import List, Dict, Any
from models import Email, Classification

# Helper functions for grading
def _grade_classif(email_id: int, cls: str) -> bool:
    """Check if classification is correct"""
    correct = {
        1: "low", 2: "high", 3: "medium", 4: "medium", 5: "low",
        6: "high", 7: "high", 8: "high", 9: "medium", 10: "high"
    }
    return correct.get(email_id) == cls

def _grade_priority(order: List[int]) -> float:
    ideal = [2, 6, 10, 8, 1, 3, 4, 7, 9, 5]
    if len(order) != 10:
        return 0.01  # Minimum score instead of 0.0
    score = sum(1 for i, eid in enumerate(order[:5]) if i < len(ideal) and eid == ideal[i]) / 5.0
    tail_match = sum(1 for eid in ideal[5:] if eid in order[5:]) / 5.0
    raw_score = score * 0.8 + tail_match * 0.2
    # Clamp to (0.01, 0.99)
    return max(0.01, min(0.99, raw_score))

def _clamp_score(score: float) -> float:
    """Ensure score is strictly between 0 and 1"""
    if score <= 0.0:
        return 0.01
    elif score >= 1.0:
        return 0.99
    return score

# Hardcoded realistic emails
EASY_EMAILS = [
    Email(id=1, subject="Spam newsletter", body="Subscribe to our daily deals!", sender="newsletter@spam.com"),
    Email(id=2, subject="Urgent refund request", body="I need refund immediately, order #123", sender="customer@angry.com"),
    Email(id=3, subject="Meeting next week?", body="Can we schedule for next Thursday?", sender="boss@company.com"),
    Email(id=4, subject="Monthly report reminder", body="Reminder: submit by EOD", sender="hr@company.com"),
    Email(id=5, subject="Social invite", body="Party this weekend!", sender="friend@gmail.com"),
]

MEDIUM_EMAILS = EASY_EMAILS + [
    Email(id=6, subject="Critical bug report", body="Production down, fix ASAP", sender="dev@team.com"),
]

HARD_EMAILS = MEDIUM_EMAILS + [
    Email(id=7, subject="CEO schedule conflict", body="Meeting overlap, reschedule?", sender="ceo@exec.com"),
    Email(id=8, subject="Contract renewal", body="Approve by tomorrow or lose client", sender="legal@partner.com"),
    Email(id=9, subject="Team offsite planning", body="Book venue for 20 ppl", sender="manager@team.com"),
    Email(id=10, subject="Security alert", body="Suspicious login from new IP", sender="security@company.com"),
]

TASKS = {
    "easy": {
        "emails": EASY_EMAILS,
        "goal": "Classify all 5 emails correctly: spam=low, refund=high, meeting=medium, report=medium, invite=low",
        "grader": lambda actions: _clamp_score(
            sum(1 for eid, cls in actions.get('classification', {}).items() if _grade_classif(int(eid), cls)) / 5.0
        )
    },
    "medium": {
        "emails": MEDIUM_EMAILS,
        "goal": "Classify 6 emails and draft responses for high-priority items (refund, meeting, report, bug)",
        "grader": lambda actions: _clamp_score(
            sum(1 for eid, cls in actions.get('classification', {}).items() if _grade_classif(int(eid), cls)) / 6.0 * 0.6 +
            sum(1 for eid in [2, 3, 4, 6] if eid in actions.get('response', {}) and len(str(actions['response'][eid]).strip()) > 20) / 4.0 * 0.4
        )
    },
    "hard": {
        "emails": HARD_EMAILS,
        "goal": "Full triage: classify 10 emails, draft responses for critical items, and provide optimal priority order [2,6,10,8,1,3,4,7,9,5]",
        "grader": lambda actions: _clamp_score(
            0.3 * _grade_priority(actions.get('priority_order', [])) +
            0.4 * (sum(1 for eid in [2, 6, 8, 10] if eid in actions.get('response', {}) and len(str(actions['response'][eid])) > 20) / 4.0) +
            0.3 * (sum(1 for eid in [2, 6, 8, 10] if int(eid) in actions.get('classification', {}) and _grade_classif(int(eid), actions['classification'][int(eid)])) / 4.0)
        )
    }
}
