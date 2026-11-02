import streamlit as st, json
from trustbridge.engine import SecurityEngine
from trustbridge.audit import AuditStore
from trustbridge.tools import TOOL_CATALOG, run_mock_tool

st.set_page_config(page_title="MCP TrustBridge", page_icon="🛡️", layout="wide")
st.title("🛡️ MCP TrustBridge")
st.caption("Zero-trust policy control centre for AI-agent tool requests")
st.info("Educational simulation: tool calls are mocked locally; this is not a production MCP server.")
store, engine = AuditStore(), SecurityEngine()
with st.sidebar:
    st.header("Requester")
    agent = st.selectbox("AI agent", ["ResearchBot", "SupportBot", "FinanceBot"])
    role = st.selectbox("Role", ["viewer", "analyst", "admin"])
    st.write("Policy: deny by default · least privilege · human approval for sensitive actions")
a, b = st.columns(2)
with a:
    st.subheader("Create a tool request")
    tool = st.selectbox("Tool", list(TOOL_CATALOG))
    raw = st.text_area("Arguments (JSON)", TOOL_CATALOG[tool]["example"])
    reason = st.text_input("Reason", "Complete the user's task")
    submit = st.button("Evaluate security policy", type="primary")
with b:
    st.subheader("Tool registry")
    for name, info in TOOL_CATALOG.items():
        st.markdown(f"**{name}** — {info['description']}")
        st.caption(f"Risk: {info['risk']} · Required role: {info['role']}")
if submit:
    try:
        args = json.loads(raw or "{}")
        decision = engine.evaluate(agent, role, tool, args, reason)
        store.record(agent, role, tool, args, decision)
        st.session_state["decision"] = decision
        st.session_state["request"] = (tool, args)
    except Exception as e:
        st.error(f"Invalid JSON/request: {e}")
d = st.session_state.get("decision")
if d:
    st.divider()
    st.subheader("Security decision")
    st.write(f"**{d['status']}** — {d['message']}")
    st.metric("Risk score", f"{d['risk_score']}/100")
    st.progress(d["risk_score"] / 100)
    for c in d["checks"]:
        st.write(("✅ " if c["passed"] else "❌ ") + c["name"] + " — " + c["detail"])
    if d["status"] == "ALLOWED" and st.button("Execute mock tool"):
        st.json(run_mock_tool(*st.session_state["request"]))
    elif d["status"] == "NEEDS_APPROVAL" and st.button("Approve once and execute mock tool"):
        st.success("Approved for this demo session.")
        st.json(run_mock_tool(*st.session_state["request"]))
st.divider()
st.subheader("Audit trail")
rows = store.recent()
st.dataframe(rows, use_container_width=True, hide_index=True) if rows else st.caption("No requests recorded yet.")
