import streamlit as st
from pathlib import Path
from engine import load_demo, load_file, reconcile, explain, supplier_email

st.set_page_config(
    page_title="GST Reconcile",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE = Path(__file__).parent

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 85% 5%, rgba(99, 102, 241, 0.10), transparent 28%),
            radial-gradient(circle at 10% 20%, rgba(14, 165, 233, 0.07), transparent 25%),
            #f7f8fc;
    }
    .block-container { max-width: 1450px; padding-top: 2rem; padding-bottom: 3rem; }
    [data-testid="stSidebar"] { background: #111827; border-right: 1px solid rgba(255,255,255,.08); }
    [data-testid="stSidebar"] * { color: #f9fafb; }
    [data-testid="stSidebar"] .stCaption { color: #9ca3af !important; }

    .hero {
        position: relative; overflow: hidden; padding: 34px 38px; border-radius: 24px; margin-bottom: 28px;
        color: white;
        background: radial-gradient(circle at 85% 20%, rgba(255,255,255,.16), transparent 25%),
                    linear-gradient(135deg, #111827 0%, #1e293b 45%, #312e81 100%);
        box-shadow: 0 18px 45px rgba(15,23,42,.16);
    }
    .hero::after { content:""; position:absolute; width:220px; height:220px; border-radius:50%; right:-70px; bottom:-110px; border:1px solid rgba(255,255,255,.12); }
    .hero-kicker { font-size:.78rem; font-weight:700; letter-spacing:.13em; text-transform:uppercase; opacity:.72; margin-bottom:10px; }
    .hero-title { font-size:2.65rem; line-height:1.05; font-weight:800; letter-spacing:-.04em; margin:0; }
    .hero-subtitle { font-size:1.08rem; margin-top:12px; color:rgba(255,255,255,.76); }
    .hero-badge { display:inline-flex; align-items:center; gap:7px; margin-top:20px; padding:7px 12px; border-radius:999px; background:rgba(255,255,255,.10); border:1px solid rgba(255,255,255,.14); font-size:.78rem; color:rgba(255,255,255,.88); }
    .hero-dot { width:7px; height:7px; border-radius:50%; background:#34d399; display:inline-block; box-shadow:0 0 10px rgba(52,211,153,.8); }

    .section-title { font-size:1.35rem; font-weight:800; color:#111827; letter-spacing:-.02em; margin-top:12px; margin-bottom:4px; }
    .section-subtitle { color:#6b7280; font-size:.92rem; margin-bottom:18px; }
    .panel { background:rgba(255,255,255,.90); border:1px solid #e5e7eb; border-radius:20px; padding:22px; box-shadow:0 7px 25px rgba(15,23,42,.045); margin-bottom:20px; }
    .panel-title { font-size:1.05rem; font-weight:800; color:#111827; margin-bottom:3px; }
    .panel-description { color:#6b7280; font-size:.84rem; margin-bottom:16px; }

    .priority-high,.priority-medium,.priority-low { display:inline-block; padding:5px 10px; border-radius:999px; font-size:.70rem; font-weight:800; letter-spacing:.04em; }
    .priority-high { color:#991b1b; background:#fee2e2; border:1px solid #fecaca; }
    .priority-medium { color:#92400e; background:#fef3c7; border:1px solid #fde68a; }
    .priority-low { color:#065f46; background:#d1fae5; border:1px solid #a7f3d0; }

    .case-card { background:linear-gradient(145deg,#fff,#f8fafc); border:1px solid #e2e8f0; border-radius:20px; padding:24px; margin-top:10px; box-shadow:0 10px 30px rgba(15,23,42,.055); }
    .case-supplier { font-size:1.3rem; font-weight:800; color:#111827; }
    .case-gstin { color:#6b7280; font-size:.78rem; margin-top:3px; font-family:monospace; }
    .exception-type { display:inline-block; padding:7px 11px; border-radius:9px; background:#eef2ff; color:#3730a3; font-size:.75rem; font-weight:800; letter-spacing:.03em; }
    .detail-box { background:#f8fafc; border:1px solid #e5e7eb; border-radius:13px; padding:14px; margin-top:8px; }
    .detail-label { color:#6b7280; font-size:.72rem; text-transform:uppercase; letter-spacing:.06em; font-weight:700; }
    .detail-value { color:#111827; font-size:1rem; font-weight:750; margin-top:4px; }
    .exposure-box { background:linear-gradient(135deg,#eef2ff,#f5f3ff); border:1px solid #ddd6fe; border-radius:15px; padding:17px; margin-top:15px; }
    .exposure-label { color:#6366f1; font-size:.72rem; font-weight:800; text-transform:uppercase; letter-spacing:.07em; }
    .exposure-value { color:#312e81; font-size:1.65rem; font-weight:850; margin-top:3px; }

    .email-card { background:#fff; border:1px solid #e5e7eb; border-radius:17px; padding:20px; margin-top:15px; box-shadow:0 7px 22px rgba(15,23,42,.045); }
    .email-label { color:#6366f1; font-size:.72rem; font-weight:800; letter-spacing:.08em; text-transform:uppercase; margin-bottom:8px; }
    .side-brand { padding:5px 0 20px 0; }
    .side-brand-title { font-size:1.25rem; font-weight:800; color:white; }
    .side-brand-sub { color:#9ca3af; font-size:.78rem; margin-top:3px; }
    .side-status { padding:13px; border-radius:13px; background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.08); margin-top:18px; margin-bottom:20px; }
    .side-status-title { color:#d1d5db; font-size:.72rem; text-transform:uppercase; letter-spacing:.07em; font-weight:700; }
    .side-status-value { color:#34d399; font-size:.85rem; font-weight:700; margin-top:4px; }
    .stButton > button { border-radius:11px; font-weight:700; min-height:43px; }
    [data-testid="stDataFrame"] { border-radius:14px; overflow:hidden; }
    hr { border-color:#e5e7eb; margin:25px 0; }

    /* Premium motion layer */
    .block-container { animation: pageEnter .65s ease-out; }
    @keyframes pageEnter { from {opacity:0; transform:translateY(10px);} to {opacity:1; transform:translateY(0);} }
    .hero { animation: heroEnter .8s ease-out; }
    @keyframes heroEnter { from {opacity:0; transform:translateY(-12px) scale(.99);} to {opacity:1; transform:translateY(0) scale(1);} }
    .hero::before { content:""; position:absolute; width:180px; height:180px; border-radius:50%; background:rgba(255,255,255,.06); top:-90px; left:-90px; animation:heroGlow 7s ease-in-out infinite; }
    @keyframes heroGlow { 0%,100% {transform:translate(0,0);} 50% {transform:translate(120px,70px);} }
    .stButton > button { transition:transform .18s ease, box-shadow .18s ease; }
    .stButton > button:hover { transform:translateY(-2px); box-shadow:0 8px 20px rgba(15,23,42,.12); }
    .stButton > button:active { transform:translateY(0) scale(.98); }
    .priority-high,.priority-medium,.priority-low { transition:transform .2s ease, box-shadow .2s ease; }
    .priority-high:hover,.priority-medium:hover,.priority-low:hover { transform:scale(1.05); }
    [data-testid="stDataFrame"] { transition:box-shadow .25s ease, transform .25s ease; }
    [data-testid="stDataFrame"]:hover { box-shadow:0 12px 30px rgba(15,23,42,.08); }
    .email-card { transition:transform .25s ease, box-shadow .25s ease; }
    .email-card:hover { transform:translateY(-3px); box-shadow:0 14px 32px rgba(15,23,42,.09); }
    .side-status { transition:background .25s ease, transform .25s ease; }
    .side-status:hover { background:rgba(255,255,255,.09); transform:translateX(3px); }
    .hero-dot { animation:statusPulse 2s ease-in-out infinite; }
    @keyframes statusPulse { 0%,100% {opacity:1; transform:scale(1);} 50% {opacity:.55; transform:scale(1.25);} }
    .section-title { animation:sectionReveal .55s ease-out; }
    .section-subtitle { animation:sectionReveal .7s ease-out; }
    @keyframes sectionReveal { from {opacity:0; transform:translateX(-8px);} to {opacity:1; transform:translateX(0);} }

    @media (max-width:900px) { .hero-title {font-size:2rem;} }
    @media (max-width:600px) { .hero-title {font-size:1.7rem;} }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">GST Operations Intelligence</div>
        <div class="hero-title">GST Reconcile</div>
        <div class="hero-subtitle">From reconciliation to resolution.</div>
        <div class="hero-badge"><span class="hero-dot"></span> Deterministic financial matching • Human-in-the-loop</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div class="side-brand">
            <div class="side-brand-title">GST Reconcile</div>
            <div class="side-brand-sub">Exception-to-action workflow</div>
        </div>
        <div class="side-status">
            <div class="side-status-title">Prototype status</div>
            <div class="side-status-value">● Live & ready</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.header("Reconciliation Controls")
    demo = st.toggle("Use demo data", value=True)
    tolerance = st.number_input("Value tolerance (₹)", min_value=0.0, value=1.0, step=1.0)

    books_file = None
    filing_file = None
    if not demo:
        books_file = st.file_uploader("Purchase Register (CSV/XLSX)", type=["csv", "xlsx"])
        filing_file = st.file_uploader("GST Filing / GSTR-2B (CSV/XLSX)", type=["csv", "xlsx"])
    else:
        st.caption("Demo dataset includes controlled matches and exceptions for the live presentation.")

    run = st.button("Run Reconciliation", type="primary", width="stretch")

if "result" not in st.session_state:
    st.session_state.result = None
if "error" not in st.session_state:
    st.session_state.error = None

if run:
    try:
        if demo:
            books, filing = load_demo()
        else:
            if not books_file or not filing_file:
                raise ValueError("Upload both datasets before running reconciliation.")
            books, filing = load_file(books_file), load_file(filing_file)
        st.session_state.result = reconcile(books, filing, tolerance)
        st.session_state.error = None
    except Exception as exc:
        st.session_state.result = None
        st.session_state.error = str(exc)

if st.session_state.error:
    st.error(st.session_state.error)

result = st.session_state.result
if result is None:
    st.info("Choose demo data or upload two datasets, then click **Run Reconciliation**.")
    st.stop()

exceptions = result[result["Exception Type"] != "MATCHED"]
matched = int((result["Exception Type"] == "MATCHED").sum())
total = len(result)
exception_count = len(exceptions)
match_rate = (matched / total * 100) if total else 0
exposure = float(exceptions["Exposure"].sum()) if not exceptions.empty else 0.0

# ============================================================
# KPI DASHBOARD
# ============================================================

st.markdown('<div class="section-title">Reconciliation Overview</div><div class="section-subtitle">A high-level view of what matched and what needs attention.</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Invoices Reviewed", f"{total:,}", help="Purchase register and filing records included in reconciliation output.")
with c2:
    st.metric("Matched", f"{matched:,}", delta=f"{match_rate:.1f}% match rate")
with c3:
    st.metric("Exceptions", f"{exception_count:,}", delta="Needs attention", delta_color="inverse")
with c4:
    st.metric("Exception Exposure", f"₹{exposure:,.0f}", delta="Associated with exceptions", delta_color="inverse")

st.divider()

# ============================================================
# SUPPLIER CHASE QUEUE
# ============================================================

st.markdown('<div class="section-title">Supplier Chase Queue</div><div class="section-subtitle">Prioritized suppliers where reconciliation has surfaced an exception.</div>', unsafe_allow_html=True)

if exceptions.empty:
    st.success("No exceptions found in the supplied data.")
else:
    queue = (
        exceptions.groupby(["Supplier Name", "Supplier GSTIN"], dropna=False)
        .agg(
            Exceptions=("Exception Type", "count"),
            Exposure=("Exposure", "sum"),
            High_Priority=("Priority", lambda s: int((s == "HIGH").sum())),
        )
        .reset_index()
    )
    queue["Priority"] = queue.apply(lambda r: "HIGH" if r["High_Priority"] > 0 else "MEDIUM", axis=1)
    queue["Action"] = queue["Priority"].map({"HIGH": "Contact supplier now", "MEDIUM": "Review + contact supplier"})
    queue = queue.sort_values(["Priority", "Exposure"], ascending=[True, False])
    display_queue = queue[["Priority", "Supplier Name", "Supplier GSTIN", "Exceptions", "Exposure", "Action"]].copy()
    display_queue["Exposure"] = display_queue["Exposure"].map(lambda x: f"₹{x:,.2f}")
    st.dataframe(display_queue, hide_index=True, width="stretch")

# ============================================================
# EXCEPTION ANALYST
# ============================================================

st.markdown('<div class="section-title">Exception Analyst</div><div class="section-subtitle">Investigate an exception and move directly from finding to action.</div>', unsafe_allow_html=True)

if not exceptions.empty:
    labels = [
        f"{i + 1} — {r['Supplier Name']} — {r['Invoice Number']} — {r['Exception Type']}"
        for i, (_, r) in enumerate(exceptions.iterrows())
    ]
    choice = st.selectbox("Select an exception", range(len(labels)), format_func=lambda i: labels[i])
    selected = exceptions.iloc[choice]
    priority = selected["Priority"]

    st.markdown("### Exception Details")
    a, b = st.columns(2)
    with a:
        st.write("**Supplier**", selected["Supplier Name"])
        st.write("**GSTIN**", selected["Supplier GSTIN"])
        st.write("**Invoice**", selected["Invoice Number"])
    with b:
        st.write("**Exception Type**", selected["Exception Type"])
        st.write("**Priority**", priority)
        st.write("**ITC / Exposure**", f"₹{float(selected['Exposure']):,.2f}")

    st.markdown("### Value Comparison")
    v1, v2 = st.columns(2)
    with v1:
        st.metric("Purchase Value", f"₹{float(selected['Taxable Value']):,.2f}")
    with v2:
        filing_value = float(selected.get("Filing Taxable Value", 0))
        st.metric("Filing Value", f"₹{filing_value:,.2f}")

    st.markdown("### What happened?")
    st.info(explain(selected))
    st.caption("Exposure is a reconciliation metric based on the supplied data, not a legal determination of ITC claimability.")

    st.markdown("### Recommended Action")
    if priority == "HIGH":
        st.error("Contact supplier immediately and request clarification/correction.")
    elif priority == "MEDIUM":
        st.warning("Review the invoice and contact the supplier for confirmation.")
    else:
        st.info("Review the exception before taking further action.")

    if st.button("Generate Supplier Follow-up", type="primary", width="stretch"):
        st.markdown('<div class="email-card"><div class="email-label">Ready-to-review supplier message</div></div>', unsafe_allow_html=True)
        st.text_area("Draft message", supplier_email(selected), height=230, label_visibility="collapsed")
        st.caption("Review the message before sending. The prototype does not automatically contact suppliers.")

# ============================================================
# FULL RESULTS
# ============================================================

with st.expander("View full reconciliation results"):
    clean_result = result.drop(columns=[c for c in ["_gstin", "_inv", "_key"] if c in result.columns])
    st.dataframe(clean_result, hide_index=True, width="stretch")

csv = clean_result.to_csv(index=False).encode("utf-8")
st.download_button("Download Reconciliation CSV", csv, file_name="gst_reconciliation_results.csv", mime="text/csv", width="stretch")

st.caption("Hackathon prototype. Human review is required before any accounting or tax action.")
