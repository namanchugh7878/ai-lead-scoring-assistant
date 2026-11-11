import os
import requests

API_VERSION = "v60.0"

def salesforce_is_configured() -> bool:
    return bool(os.getenv("SF_INSTANCE_URL") and os.getenv("SF_ACCESS_TOKEN"))

def create_salesforce_lead(lead: dict) -> dict:
    """Create a standard Salesforce Lead using a pre-generated OAuth access token."""
    instance_url = os.getenv("SF_INSTANCE_URL", "").rstrip("/")
    access_token = os.getenv("SF_ACCESS_TOKEN")
    if not instance_url or not access_token:
        raise RuntimeError("Set SF_INSTANCE_URL and SF_ACCESS_TOKEN first.")

    name = str(lead.get("name", "")).strip()
    parts = name.split(maxsplit=1)
    first_name = parts[0] if parts else ""
    last_name = parts[1] if len(parts) > 1 else "Unknown"

    payload = {
        "FirstName": first_name,
        "LastName": last_name,
        "Company": str(lead.get("company") or "Individual"),
        "Email": str(lead.get("email") or ""),
        "LeadSource": str(lead.get("source") or "Other"),
        "Description": (
            f"Demo lead score: {lead.get('score', 'not calculated')}. "
            "Created by AI Lead Scoring Assistant."
        )
    }
    response = requests.post(
        f"{instance_url}/services/data/{API_VERSION}/sobjects/Lead/",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=20
    )
    response.raise_for_status()
    return response.json()
