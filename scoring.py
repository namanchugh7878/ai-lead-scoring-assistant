from typing import Any

HIGH_INTENT_SOURCES = {"demo request", "referral", "contact form"}

def score_lead(lead: dict[str, Any], include_reasons: bool = False):
    """Return an explainable 0–100 lead score."""
    score = 0
    reasons = []

    if bool(lead.get("budget_confirmed", False)):
        score += 25
        reasons.append("+25: Budget is confirmed")

    if bool(lead.get("decision_maker", False)):
        score += 20
        reasons.append("+20: Contact is a decision-maker")

    source = str(lead.get("source", "")).strip().lower()
    if source in HIGH_INTENT_SOURCES:
        score += 20
        reasons.append("+20: High-intent lead source")

    try:
        timeline = int(lead.get("timeline_days", 9999))
    except (TypeError, ValueError):
        timeline = 9999
    if timeline <= 30:
        score += 20
        reasons.append("+20: Buying timeline is within 30 days")

    try:
        employees = int(lead.get("employees", 0))
    except (TypeError, ValueError):
        employees = 0
    if employees >= 50:
        score += 10
        reasons.append("+10: Company has at least 50 employees")

    if "@" in str(lead.get("email", "")):
        score += 5
        reasons.append("+5: Email address is provided")

    score = min(score, 100)
    return (score, reasons) if include_reasons else score


def score_band(score: int) -> str:
    if score >= 70:
        return "Hot"
    if score >= 40:
        return "Warm"
    return "Cold"
