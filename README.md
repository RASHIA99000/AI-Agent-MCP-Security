# MCP TrustBridge — Zero-Trust Tool Access Monitor

A second, distinct educational project on **AI Agent and MCP Security Gateway**.

TrustBridge uses a policy-control design: each agent tool request is checked against a local tool registry, requester role, stated purpose, credential-like argument rules, and risk classification. Decisions are written to SQLite. High-risk simulated actions require a human approval click.

## Features
- Four mock tools with low, medium, high, and critical risk levels
- Role-based authorization (`viewer`, `analyst`, `admin`)
- Deny-by-default for unknown tools
- Risk scoring and human approval for high-risk actions
- Basic credential-like argument detection
- SQLite audit trail and Streamlit dashboard
- Unit tests for allow, deny, approval, and credential rejection cases

## Run
Python 3.10+ recommended.
```bash
pip install -r requirements.txt
streamlit run app.py
```
Open the local URL printed by Streamlit (usually `http://localhost:8501`).

## Tests
```bash
python -m unittest discover -s tests -v
```

## Demo cases
- viewer + search_public_docs → ALLOWED
- viewer + export_finance_data → DENIED
- admin + send_external_message → NEEDS_APPROVAL
- argument containing `api_key`, `token`, `password`, `secret`, or `private_key` → DENIED

## Architecture
`Streamlit UI → SecurityEngine → Tool Catalog → Mock Tool Runner`
`SecurityEngine → AuditStore (SQLite)`

## Scope and limitations
This is a local educational simulation. Tool actions are mocked; no real messages are sent or real data exported. It is not a full MCP wire-protocol implementation or a production security boundary.
