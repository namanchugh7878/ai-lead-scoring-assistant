# ai-lead-scoring-assistant.
AI-powered sales lead scoring using Python, Gemini AI and Salesforce



A portfolio-ready demo that helps a sales team prioritize leads using transparent scoring rules, an optional Gemini explanation, and an optional Salesforce REST integration.

> **Project status:** Working local demo. Gemini and Salesforce integrations are optional and require your own credentials. Do not describe either integration as live until you configure and test it with your own accounts.

## Features

- Add and manage sales leads.
- Score leads from 0–100 using explainable business rules.
- Categorize leads as Hot, Warm, or Cold.
- View pipeline metrics and filter leads.
- Export lead records to CSV.
- Optionally ask Google Gemini to explain a lead score.
- Optional Salesforce REST API helper for creating a Lead record.

## Tech stack

- Python
- Streamlit
- Pandas
- Google Gemini API (optional)
- Salesforce REST API (optional)

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the app:

   ```bash
   streamlit run app.py
   ```

The app runs locally in your browser. It starts with sample leads and stores edits in the current Streamlit session.

## Optional Gemini setup

Set an API key in your environment before starting Streamlit:

```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your_api_key"

# macOS/Linux
export GEMINI_API_KEY="your_api_key"
```

The Gemini feature is used only to generate a plain-language explanation. The numeric score is calculated locally by the transparent scoring rules in `scoring.py`.

## Optional Salesforce setup

To enable Salesforce lead creation, set these environment variables:

- `SF_INSTANCE_URL` — your Salesforce instance URL, e.g. `https://your-domain.my.salesforce.com`
- `SF_ACCESS_TOKEN` — a valid OAuth access token with permission to create Lead records

Then restart the app. Use a sandbox account for testing. Access tokens are secrets: never commit them to GitHub.

The integration uses Salesforce's REST API and creates a standard Lead record. Salesforce API versions and org permissions can vary; check your org's current API support if an API-version error occurs.

## Scoring model

The demo uses a simple, explainable weighted model:

- Budget confirmed: +25
- Decision-maker: +20
- High-intent source (demo, referral, contact form): +20
- Timeline within 30 days: +20
- Company size of 50+ employees: +10
- Valid email supplied: +5

The score is capped at 100. Bands:

- **Hot:** 70–100
- **Warm:** 40–69
- **Cold:** 0–39

These weights are illustrative. A real sales team should calibrate them using historical conversion data and review for unfair or misleading proxies.

## Project structure

```text
ai-lead-scoring-assistant/
├── app.py
├── scoring.py
├── gemini_helper.py
├── salesforce_client.py
├── requirements.txt
├── .env.example
├── .gitignore
└── data/
    └── sample_leads.csv
```

## Important notes

- Sample records are fictional.
- This is a decision-support demo, not an automated hiring, lending, or other high-stakes decision system.
- Do not upload customer personal data, API keys, access tokens, or secrets to a public repository.
- The Gemini explanation is generated text and should be reviewed by a human.
