import os
import pandas as pd
import streamlit as st

from scoring import score_lead, score_band
from gemini_helper import explain_score
from salesforce_client import create_salesforce_lead, salesforce_is_configured

st.set_page_config(page_title="AI Lead Scoring Assistant", page_icon="🎯", layout="wide")

st.title("🎯 AI Lead Scoring Assistant")
st.caption("Prioritize sales leads with transparent scoring and optional AI explanations.")

COLUMNS = [
    "name", "email", "company", "source", "budget_confirmed",
    "decision_maker", "timeline_days", "employees"
]

def load_sample_data():
    path = os.path.join("data", "sample_leads.csv")
    df = pd.read_csv(path)
    for col in ("budget_confirmed", "decision_maker"):
        df[col] = df[col].astype(bool)
    return df

if "leads" not in st.session_state:
    st.session_state.leads = load_sample_data()

with st.sidebar:
    st.header("Add a lead")
    with st.form("add_lead_form", clear_on_submit=True):
        name = st.text_input("Full name *")
        email = st.text_input("Work email")
        company = st.text_input("Company")
        source = st.selectbox("Lead source", ["Website", "Contact Form", "Demo Request", "Referral", "LinkedIn", "Cold Outreach"])
        budget = st.checkbox("Budget confirmed")
        decision_maker = st.checkbox("Decision-maker")
        timeline = st.selectbox("Expected buying timeline", [7, 14, 30, 60, 90, 180], format_func=lambda x: f"{x} days")
        employees = st.number_input("Company employees", min_value=1, max_value=100000, value=25)
        submitted = st.form_submit_button("Add lead", use_container_width=True)
        if submitted:
            if not name.strip():
                st.error("Please enter the lead's name.")
            else:
                new = {
                    "name": name.strip(), "email": email.strip(), "company": company.strip(),
                    "source": source, "budget_confirmed": budget,
                    "decision_maker": decision_maker, "timeline_days": int(timeline),
                    "employees": int(employees)
                }
                st.session_state.leads = pd.concat(
                    [st.session_state.leads, pd.DataFrame([new])], ignore_index=True
                )
                st.success(f"Added {name.strip()}.")

df = st.session_state.leads.copy()
if df.empty:
    st.info("Add a lead from the sidebar to get started.")
    st.stop()

scores = df.apply(lambda row: score_lead(row.to_dict()), axis=1)
df["score"] = scores
df["priority"] = df["score"].apply(score_band)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total leads", len(df))
m2.metric("Hot leads", int((df["priority"] == "Hot").sum()))
m3.metric("Warm leads", int((df["priority"] == "Warm").sum()))
m4.metric("Average score", f"{df['score'].mean():.0f}/100")

st.divider()
left, right = st.columns([1.5, 1])
with left:
    st.subheader("Lead pipeline")
    priorities = st.multiselect("Filter by priority", ["Hot", "Warm", "Cold"], default=["Hot", "Warm", "Cold"])
    visible = df[df["priority"].isin(priorities)].sort_values("score", ascending=False)
    display_cols = ["name", "company", "source", "score", "priority"]
    st.dataframe(visible[display_cols], use_container_width=True, hide_index=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Export leads as CSV", csv, "scored_leads.csv", "text/csv")

with right:
    st.subheader("Priority distribution")
    counts = df["priority"].value_counts().reindex(["Hot", "Warm", "Cold"], fill_value=0)
    st.bar_chart(counts)

st.divider()
st.subheader("Lead score details")
selected_name = st.selectbox("Choose a lead", df["name"].tolist())
selected = df[df["name"] == selected_name].iloc[0].to_dict()
score, reasons = score_lead(selected, include_reasons=True)
st.metric("Lead score", f"{score}/100", score_band(score))
st.write("**Why this lead received this score:**")
for reason in reasons:
    st.write(f"- {reason}")

if st.button("Generate AI explanation", type="primary"):
    if not os.getenv("GEMINI_API_KEY"):
        st.warning("Gemini is not configured. Set GEMINI_API_KEY and restart the app.")
    else:
        with st.spinner("Asking Gemini to explain the score..."):
            try:
                st.info(explain_score(selected, score, reasons))
            except Exception as exc:
                st.error(f"Gemini request failed: {exc}")

st.divider()
st.subheader("Optional Salesforce sync")
if salesforce_is_configured():
    if st.button("Create selected lead in Salesforce"):
        with st.spinner("Creating Salesforce Lead..."):
            try:
                result = create_salesforce_lead(selected)
                st.success(f"Salesforce lead created. Record ID: {result.get('id', 'created')}")
            except Exception as exc:
                st.error(f"Salesforce sync failed: {exc}")
else:
    st.caption("Not connected. Configure SF_INSTANCE_URL and SF_ACCESS_TOKEN to enable Salesforce sync.")
