import streamlit as st
import pandas as pd
from src.styles import apply_styles
from src.components.landing import render_landing_screen
from src.ui import (
    animated_metric,
    investigation_status,
    render_risk_card,
    render_evidence_summary,
    render_analysis_pipeline
)
from src.components.header import render_command_bar
from src.components.graph import (
    render_graph_header,
    render_graph_legend,
    get_entity_color,
    get_entity_border,
    get_entity_size
)
import json
import hashlib
from pathlib import Path
from pyvis.network import Network
import streamlit.components.v1 as components
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from src.data_loader import load_analysis_data
analysis_data = load_analysis_data()

alerts_data = analysis_data["alerts"]
graph_data = analysis_data["graph"]
ml_anomalies_data = analysis_data["ml_anomalies"]
risk_data = analysis_data["risk"]
timeline_data = analysis_data["timeline"]
sample_data = analysis_data["sample"]

def generate_investigation_report(
    output_path,
    case_id,
    investigator,
    transactions_df,
    entity_links,
    risk_alerts,
    hash_records
):

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=35,
        leftMargin=35,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]

    story = []

    # ------------------------------------------------
    # TITLE
    # ------------------------------------------------

    story.append(
        Paragraph(
            "TRACE-X Investigation Report",
            title_style
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            f"<b>Case ID:</b> {case_id}<br/>"
            f"<b>Investigator:</b> {investigator}<br/>"
            f"<b>Analysis Mode:</b> Evidence-driven",
            body_style
        )
    )

    story.append(Spacer(1, 12))

    # ------------------------------------------------
    # CASE SUMMARY
    # ------------------------------------------------

    story.append(
        Paragraph(
            "1. Case Summary",
            heading_style
        )
    )

    story.append(
        Paragraph(
            "TRACE-X analyzed the available mock telecom, "
            "IP and financial evidence to identify "
            "relationships and transaction-flow indicators "
            "for investigator review.",
            body_style
        )
    )

    story.append(Spacer(1, 8))

    # ------------------------------------------------
    # EVIDENCE SUMMARY
    # ------------------------------------------------

    story.append(
        Paragraph(
            "2. Evidence Summary",
            heading_style
        )
    )

    evidence_data = [
        ["Evidence Type", "Records"],
        ["Financial / UPI", str(len(transactions_df))],
        ["CDR", str(len(cdr_df))],
        ["IPDR", str(len(ipdr_df))],
        ["Entity Relationships", str(len(entity_links))]
    ]

    evidence_table = Table(
        evidence_data,
        colWidths=[250, 100]
    )

    evidence_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("PADDING", (0, 0), (-1, -1), 5)
        ])
    )

    story.append(evidence_table)

    story.append(Spacer(1, 10))

    # ------------------------------------------------
    # TRANSACTION FLOW
    # ------------------------------------------------

    story.append(
        Paragraph(
            "3. Transaction Flow",
            heading_style
        )
    )

    if not transactions_df.empty:

        transaction_data = [
            [
                "Sender",
                "Receiver",
                "Amount",
                "Transaction ID"
            ]
        ]

        for _, row in transactions_df.iterrows():

            transaction_data.append([
                str(row.get("sender_upi", "")),
                str(row.get("receiver_upi", "")),
                f"₹{float(row.get('amount', 0)):,.0f}",
                str(row.get("transaction_id", ""))
            ])

        transaction_table = Table(
            transaction_data,
            colWidths=[105, 105, 70, 90]
        )

        transaction_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 7),
                ("PADDING", (0, 0), (-1, -1), 4)
            ])
        )

        story.append(transaction_table)

    else:

        story.append(
            Paragraph(
                "No financial transaction records available.",
                body_style
            )
        )

    story.append(Spacer(1, 10))

    # ------------------------------------------------
    # RISK INDICATORS
    # ------------------------------------------------

    story.append(
        Paragraph(
            "4. Risk Indicators",
            heading_style
        )
    )

    if risk_alerts:

        for alert in risk_alerts:

            description = alert.get(
                "description",
                "Risk indicator detected."
            )

            severity = alert.get(
                "severity",
                "UNKNOWN"
            )

            story.append(
                Paragraph(
                    f"<b>{severity}</b> — {description}",
                    body_style
                )
            )

    else:

        story.append(
            Paragraph(
                "No active risk alerts are currently available.",
                body_style
            )
        )

    story.append(Spacer(1, 10))

    # ------------------------------------------------
    # EVIDENCE INTEGRITY
    # ------------------------------------------------

    story.append(
        Paragraph(
            "5. Evidence Integrity",
            heading_style
        )
    )

    if hash_records:

        hash_data = [
            ["Evidence File", "SHA-256"]
        ]

        for record in hash_records:

            hash_data.append([
                record["Evidence File"],
                record["SHA-256"]
            ])

        hash_table = Table(
            hash_data,
            colWidths=[120, 280]
        )

        hash_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 6),
                ("PADDING", (0, 0), (-1, -1), 4)
            ])
        )

        story.append(hash_table)

    story.append(Spacer(1, 8))

    # ------------------------------------------------
    # INVESTIGATOR NOTE
    # ------------------------------------------------

    story.append(
        Paragraph(
            "<b>Investigator Note:</b> "
            "The relationships and risk indicators in this report "
            "are derived from the available evidence records and "
            "are intended for investigative review. "
            "They do not by themselves establish attribution or guilt.",
            body_style
        )
    )

    doc.build(story)

def calculate_sha256(file_path):

    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as file:

        for chunk in iter(
            lambda: file.read(4096),
            b""
        ):
            sha256_hash.update(chunk)

    return sha256_hash.hexdigest()

st.set_page_config(
    page_title="TRACE-X",
    page_icon="🔎",
    layout="wide"
)
apply_styles()
render_landing_screen()
investigation_status("ACTIVE")
# ============================================================
# DATA DIRECTORY
# ============================================================

DATA_DIR = Path(__file__).parent / "data"


# ============================================================
# LOAD TRANSACTIONS JSON
# ============================================================

TRANSACTIONS_FILE = DATA_DIR / "transactions.json"

if TRANSACTIONS_FILE.exists():

    with open(
        TRANSACTIONS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        transaction_records = json.load(file)

    transactions_df = pd.DataFrame(
        transaction_records
    )

else:

    transactions_df = pd.DataFrame()


# ============================================================
# LOAD CDR JSON
# ============================================================

CDR_FILE = DATA_DIR / "cdr.json"

if CDR_FILE.exists():

    with open(
        CDR_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        cdr_records = json.load(file)

    cdr_df = pd.DataFrame(
        cdr_records
    )

else:

    cdr_df = pd.DataFrame()


# ============================================================
# LOAD IPDR JSON
# ============================================================

IPDR_FILE = DATA_DIR / "ipdr.json"

if IPDR_FILE.exists():

    with open(
        IPDR_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        ipdr_records = json.load(file)

    ipdr_df = pd.DataFrame(
        ipdr_records
    )

else:

    ipdr_df = pd.DataFrame()


# ============================================================
# RISK DETECTION
# ==============risk_alerts = []==============================================

risk_alerts = alerts_data.copy()

if not transactions_df.empty:

    transactions_df["timestamp"] = pd.to_datetime(
        transactions_df["timestamp"]
    )

    transactions_df = transactions_df.sort_values(
        "timestamp"
    )

    for _, incoming in transactions_df.iterrows():

        receiver = incoming["receiver_upi"]
        incoming_time = incoming["timestamp"]

        onward = transactions_df[
            (transactions_df["sender_upi"] == receiver)
            &
            (transactions_df["timestamp"] > incoming_time)
        ]

        for _, outgoing in onward.iterrows():

            time_difference = (
                outgoing["timestamp"]
                - incoming_time
            ).total_seconds() / 60

            if time_difference <= 5:

                risk_alerts.append({

                    "severity": "HIGH",

                    "type": "RAPID_ONWARD_TRANSFER",

                    "entity": receiver,

                    "description": (
                        f"{receiver} received "
                        f"₹{incoming['amount']:,.0f} and transferred "
                        f"₹{outgoing['amount']:,.0f} onward "
                        f"within {time_difference:.0f} minutes."
                    ),

                    "incoming_transaction":
                        incoming["transaction_id"],

                    "outgoing_transaction":
                        outgoing["transaction_id"],

                    "evidence_file":
                        "transactions.json"
                })

# Detect multi-hop transaction chains
if not transactions_df.empty:

    for _, first_txn in transactions_df.iterrows():

        first_receiver = first_txn["receiver_upi"]

        second_hop = transactions_df[
            transactions_df["sender_upi"] == first_receiver
        ]

        for _, second_txn in second_hop.iterrows():

            second_receiver = second_txn["receiver_upi"]

            third_hop = transactions_df[
                transactions_df["sender_upi"] == second_receiver
            ]

            for _, third_txn in third_hop.iterrows():

                chain = (
                    f"{first_txn['sender_upi']} → "
                    f"{first_receiver} → "
                    f"{second_receiver} → "
                    f"{third_txn['receiver_upi']}"
                )

                risk_alerts.append({
                    "severity": "HIGH",
                    "type": "MULTI_HOP_TRANSACTION_CHAIN",
                    "entity": first_receiver,
                    "description": (
                        "Multi-hop fund movement detected: "
                        f"{chain}"
                    ),
                    "incoming_transaction": first_txn["transaction_id"],
                    "outgoing_transaction": third_txn["transaction_id"],
                    "evidence_file": "transactions.json"
                })

# ============================================================
# RISK SCORE
# ============================================================
# Detect high-velocity transaction activity
if not transactions_df.empty:

    velocity_alerted_entities = set()

    for _, txn in transactions_df.iterrows():

        entity = txn["sender_upi"]
        current_time = txn["timestamp"]

        activity_window = transactions_df[
            (
                (
                    transactions_df["sender_upi"] == entity
                )
                |
                (
                    transactions_df["receiver_upi"] == entity
                )
            )
            &
            (
                transactions_df["timestamp"] >= current_time
            )
            &
            (
                transactions_df["timestamp"]
                <= current_time + pd.Timedelta(minutes=15)
            )
        ]

        if len(activity_window) >= 2 and entity not in velocity_alerted_entities:

            velocity_alerted_entities.add(entity)

            risk_alerts.append({
                "severity": "MEDIUM",
                "type": "HIGH_VELOCITY_TRANSACTION_ACTIVITY",
                "entity": entity,
                "description": (
                    f"{entity} was involved in "
                    f"{len(activity_window)} transactions "
                    "within a 15-minute window."
                ),
                "incoming_transaction": (
                    activity_window.iloc[0]["transaction_id"]
                ),
                "outgoing_transaction": (
                    activity_window.iloc[-1]["transaction_id"]
                ),
                "evidence_file": "transactions.json"
            })

# Calculate weighted investigation risk score
# Calculate evidence-aware risk score
detected_types = {
    alert["type"]
    for alert in risk_alerts
}

risk_score = 0

if "RAPID_ONWARD_TRANSFER" in detected_types:
    risk_score += 30

if "MULTI_HOP_TRANSACTION_CHAIN" in detected_types:
    risk_score += 30

if "HIGH_VELOCITY_TRANSACTION_ACTIVITY" in detected_types:
    risk_score += 20

risk_score = min(risk_score, 100)

if risk_score >= 75:

    risk_level = "HIGH"

elif risk_score >= 25:

    risk_level = "MEDIUM"

else:

    risk_level = "LOW"


render_command_bar(
    case_id="TRX-001",
    risk_level=risk_level,
    alert_count=len(risk_alerts)
)
    # ============================================================
# ENTITY CORRELATION
# ============================================================

entity_links = []

# ------------------------------------------------------------
# CDR: PHONE → IMEI
# ------------------------------------------------------------

if not cdr_df.empty:

    for _, row in cdr_df.iterrows():

        phone = str(row["caller"])
        imei = str(row["imei"])

        entity_links.append({
            "source_entity": phone,
            "source_type": "PHONE",
            "target_entity": imei,
            "target_type": "IMEI",
            "relationship": "USES",
            "evidence_source": "cdr.json",
            "evidence_id": row["cdr_id"]
        })


# ------------------------------------------------------------
# IPDR: PHONE → IP
# ------------------------------------------------------------

if not ipdr_df.empty:

    for _, row in ipdr_df.iterrows():

        phone = str(row["phone_number"])
        ip_address = str(row["source_ip"])

        entity_links.append({
            "source_entity": phone,
            "source_type": "PHONE",
            "target_entity": ip_address,
            "target_type": "IP",
            "relationship": "USED_IP",
            "evidence_source": "ipdr.json",
            "evidence_id": row["ipdr_id"]
        })




# ============================================================
# LOAD JSON TRANSACTION EVIDENCE
# ============================================================

DATA_DIR = Path(__file__).parent / "data"

TRANSACTIONS_FILE = DATA_DIR / "transactions.json"

# ============================================================
# LOAD CDR EVIDENCE
# ============================================================

CDR_FILE = DATA_DIR / "cdr.json"

if CDR_FILE.exists():

    with open(
        CDR_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        cdr_records = json.load(file)

    cdr_df = pd.DataFrame(
        cdr_records
    )

else:

    cdr_df = pd.DataFrame()


# ============================================================
# LOAD IPDR EVIDENCE
# ============================================================

IPDR_FILE = DATA_DIR / "ipdr.json"

if IPDR_FILE.exists():

    with open(
        IPDR_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        ipdr_records = json.load(file)

    ipdr_df = pd.DataFrame(
        ipdr_records
    )

else:

    ipdr_df = pd.DataFrame()





# ============================================================
# HEADER
# ============================================================



# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header(" TRACE-X")

    st.markdown("### Investigation")

    case_id = st.text_input(
        "Case ID",
        value="TRX-2026-001"
    )

    investigator = st.text_input(
        "Investigator",
        value="Digital Forensics Analyst"
    )

    st.selectbox(
        "Case Status",
        [
            "Active Investigation",
            "Under Review",
            "Closed"
        ]
    )

    st.divider()
    if "active_module" not in st.session_state:
     st.session_state.active_module = "Overview"
    st.markdown("### Investigation")

    investigation_module = st.radio(
    "INVESTIGATION",
    [
        "Overview",
        "Network",
        "Timeline",
        "Alerts",
        "Evidence & Report"
    ],
    key="active_module",
    label_visibility="collapsed"
)


    st.markdown("### Evidence Sources")

    st.checkbox("CDR", value=True)
    st.checkbox("IPDR", value=True)
    st.checkbox("Financial / UPI", value=True)
    st.checkbox("Email Headers", value=False)
    st.checkbox("Android Logs", value=False)

    st.divider()

    st.caption("TRACE-X PoC")
    st.caption("Offline-first investigation workflow")

# ============================================================
# CASE INFORMATION
# ============================================================

st.header("Investigation Overview")

case_col1, case_col2, case_col3 = st.columns(3)

with case_col1:
    st.write("**Case ID**")
    st.write(case_id)

with case_col2:
    st.write("**Investigator**")
    st.write(investigator)

with case_col3:
    st.write("**Analysis Mode**")
    st.write("Evidence-driven")

st.divider()

# ============================================================
# KEY METRICS
# ============================================================

st.subheader("Investigation Metrics")

col1, col2, col3, col4 = st.columns(4)


with col1:

    evidence_files = sum([
        not transactions_df.empty,
        not cdr_df.empty,
        not ipdr_df.empty
    ])

    animated_metric(
        "Evidence Files",
        evidence_files
    )


with col2:

    if not transactions_df.empty:
        entities = set(transactions_df["sender_upi"])
        entities.update(transactions_df["receiver_upi"])
        entity_count = len(entities)
    else:
        entity_count = 0

    animated_metric(
        "Entities",
        entity_count
    )


with col3:

    animated_metric(
        "Relationships",
        len(entity_links)
    )


with col4:

    animated_metric(
        "Risk Alerts",
        len(risk_alerts)
    )

render_evidence_summary(
    evidence_files=evidence_files,
    entity_count=entity_count,
    relationship_count=len(entity_links)
)
# ============================================================
# RISK STATUS
# ============================================================

risk_col1, risk_col2 = st.columns([1, 2])

with risk_col1:

    st.subheader("Risk Status")

    render_risk_card(
        risk_score,
        risk_level,
        len(risk_alerts)
    )

with risk_col2:

   render_analysis_pipeline()
st.divider()

# ============================================================
# INVESTIGATION MODULES
# ============================================================




# ============================================================
# OVERVIEW TAB
# ============================================================

if investigation_module == "Overview":
    # =========================================================
# TRACE-X COMMAND CENTER OVERVIEW
# =========================================================

 st.markdown(
    """
    <div class="trace-overview-header">
        <div>
            <div class="trace-overview-kicker">ACTIVE INVESTIGATION</div>
            <div class="trace-overview-title">Investigation Command Center</div>
            <div class="trace-overview-subtitle">
                Evidence correlation, transaction flow and threat intelligence
            </div>
        </div>
        <div class="trace-overview-status">
            <span class="trace-live-dot"></span>
            LIVE ANALYSIS
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

    # =========================================================
# TRACE-X RISK ANALYZER
# =========================================================

risk_types = {}

for alert in risk_alerts:
    alert_type = alert.get("type", "UNKNOWN")

    if alert_type not in risk_types:
        risk_types[alert_type] = 0

    risk_types[alert_type] += 1

risk_rows = []

for alert_type, count in risk_types.items():
    if alert_type == "RAPID_ONWARD_TRANSFER":
        label = "Rapid onward transfer"
        description = "Funds were forwarded shortly after receipt."
        severity = "HIGH"

    elif alert_type == "MULTI_HOP_TRANSACTION_CHAIN":
        label = "Multi-hop transaction chain"
        description = "Funds moved through multiple intermediary accounts."
        severity = "HIGH"

    elif alert_type == "HIGH_VELOCITY_TRANSACTION_ACTIVITY":
        label = "High transaction velocity"
        description = "Multiple financial events occurred within a short time window."
        severity = "MEDIUM"

    else:
        label = alert_type.replace("_", " ").title()
        description = "Risk indicator detected from available evidence."
        severity = "MEDIUM"

    risk_rows.append({
        "label": label,
        "description": description,
        "severity": severity,
        "count": count
    })

st.html(
    """
    <div class="trace-risk-panel">
        <div class="trace-risk-header">
            <div>
                <div class="trace-risk-kicker">THREAT INTELLIGENCE</div>
                <div class="trace-risk-title">Risk Analyzer</div>
                <div class="trace-risk-subtitle">
                    Evidence-backed indicators detected across the investigation
                </div>
            </div>

            <div class="trace-risk-live">
                <span></span>
                ANALYSIS ACTIVE
            </div>
        </div>
    </div>
    """
)

risk_cols = st.columns(3)

for index, risk in enumerate(risk_rows):
    with risk_cols[index % 3]:

        if risk["severity"] == "HIGH":
            severity_class = "trace-risk-high"
        else:
            severity_class = "trace-risk-medium"

        st.html(
            f"""
            <div class="trace-risk-card trace-risk-card-{severity_class.lower()}">
                <div class="trace-risk-card-top">
                    <span class="trace-risk-severity">
                        {risk["severity"]}
                    </span>
                    <span class="trace-risk-count">
                        ×{risk["count"]}
                    </span>
                </div>

                <div class="trace-risk-card-title">
                    {risk["label"]}
                </div>

                <div class="trace-risk-card-description">
                    {risk["description"]}
                </div>

                <div class="trace-risk-card-bar">
                    <div></div>
                </div>
            </div>
            """,
            
        )

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("### Evidence Source Summary")

st.markdown("### Entity Correlation")

if entity_links:

    correlation_df = pd.DataFrame(entity_links)

    st.dataframe(
        correlation_df[
            [
                "source_entity",
                "source_type",
                "relationship",
                "target_entity",
                "target_type",
                "evidence_source",
                "evidence_id"
            ]
    ],
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No cross-source entity relationships detected."
    )

source_col1, source_col2, source_col3 = st.columns(3)

with source_col1:
    st.metric(
        "Financial / UPI Records",
        len(transactions_df)
    )

with source_col2:
    st.metric(
        "CDR Records",
        len(cdr_df)
    )

with source_col3:
    st.metric(
        "IPDR Records",
        len(ipdr_df)
    )


# ============================================================
# NETWORK TAB
# ============================================================

if investigation_module == "Network":


    render_graph_header(
        entity_count=len(set(
            [link["source_entity"] for link in entity_links] +
            [link["target_entity"] for link in entity_links]
        )),
        relationship_count=len(entity_links)
    )

    render_graph_legend()
    
    if entity_links:

        net = Network(
            height="610px",
            width="100%",
            bgcolor="#0e1117",
            font_color="white",
            directed=True
        )

        # Track nodes so they are not added repeatedly
        added_nodes = set()
                # ----------------------------------------------------
        # ADD TELECOM / IP RELATIONSHIPS
        # ----------------------------------------------------

        for link in entity_links:

            source = link["source_entity"]
            target = link["target_entity"]

            source_type = link["source_type"]
            target_type = link["target_type"]

            if source not in added_nodes:

                net.add_node(
    source,
    label=f"{source}\n({source_type})",
    title=f"Type: {source_type}",
    color={
        "background": get_entity_color(source_type),
        "border": get_entity_border(source_type),
        "highlight": {
            "background": get_entity_color(source_type),
            "border": get_entity_border(source_type)
        }
    }
)

                added_nodes.add(source)

            if target not in added_nodes:

                net.add_node(
    target,
    label=f"{target}\n({target_type})",
    title=f"Type: {target_type}",
    color={
        "background": get_entity_color(target_type),
        "border": "#ffffff",
        "highlight": {
            "background": get_entity_color(target_type),
            "border": "#ffffff"
        }
    }
)

                added_nodes.add(target)

            net.add_edge(
    source,
    target,
    label=link["relationship"],
    title=(
        f"Evidence: {link['evidence_source']} | "
        f"ID: {link['evidence_id']}"
    ),
    color={
        "color": "#53657d",
        "highlight": "#8da5c2",
        "hover": "#8da5c2"
    },
    width=1.5,
    arrows="to"
)


        # ----------------------------------------------------
        # ADD FINANCIAL / UPI TRANSACTIONS
        # ----------------------------------------------------

        if not transactions_df.empty:

            for _, transaction in transactions_df.iterrows():

                sender = str(
                    transaction["sender_upi"]
                )

                receiver = str(
                    transaction["receiver_upi"]
                )

                amount = float(
                    transaction["amount"]
                )

                transaction_id = str(
                    transaction["transaction_id"]
                )

                if sender not in added_nodes:

                    net.add_node(
    sender,
    label=f"{sender}\n(UPI)",
    title="Type: UPI",
    color={
        "background": get_entity_color("UPI"),
        "border": "#ffffff",
        "highlight": {
            "background": get_entity_color("UPI"),
            "border": "#ffffff"
        }
    }
)

                    added_nodes.add(sender)

                if receiver not in added_nodes:

                    net.add_node(
    receiver,
    label=f"{receiver}\n(UPI)",
    title="Type: UPI",
    color={
        "background": get_entity_color("UPI"),
        "border": "#ffffff",
        "highlight": {
            "background": get_entity_color("UPI"),
            "border": "#ffffff"
        }
    }
)

                    added_nodes.add(receiver)

                net.add_edge(
    sender,
    receiver,
    label=f"₹{amount:,.0f}",
    title=(
        f"Transaction: {transaction_id} | "
        f"Amount: ₹{amount:,.0f} | "
        f"Evidence: transactions.json"
    ),
    color={
        "color": "#42d6a4",
        "highlight": "#7ff2cb",
        "hover": "#7ff2cb"
    },
    width=2.5,
    arrows="to"
)

    

        net.set_options("""
{
  "physics": {
    "enabled": true,
    "stabilization": {
      "iterations": 200
    },
    "barnesHut": {
      "gravitationalConstant": -3000,
      "centralGravity": 0.2,
      "springLength": 180,
      "springConstant": 0.04,
      "damping": 0.15
    }
  },
  "interaction": {
    "hover": true,
    "navigationButtons": true,
    "dragNodes": true,
    "zoomView": true
  },
  "edges": {
    "smooth": {
      "enabled": true,
      "type": "dynamic"
    },
    "arrows": {
      "to": {
        "enabled": true,
        "scaleFactor": 0.7
      }
    },
    "font": {
      "size": 12,
      "color": "#ffffff",
      "strokeWidth": 0
    }
  },
  "nodes": {
    "shape": "dot",
    "size": 22,
    "font": {
      "size": 22,
      "color": "#ffffff"
    },
    "borderWidth": 2
  }
}
""")
        graph_html = net.generate_html()

        components.html(
            graph_html,
            height=650,
            scrolling=False
        )

    else:

        st.info(
            "No entity relationships are available "
            "for network visualization."
        )

# ============================================================
# TIMELINE TAB
# ============================================================

if investigation_module == "Timeline":

    st.subheader("🕒 Investigation Timeline")

    if transactions_df.empty:

        st.warning("No transaction evidence available.")

    else:

        st.write(
            "Chronological view of financial events found in "
            "the transaction evidence."
        )

        timeline_df = transactions_df.copy()

        timeline_df["timestamp"] = pd.to_datetime(
            timeline_df["timestamp"]
        )

        timeline_df = timeline_df.sort_values(
            "timestamp"
        )

        for _, row in timeline_df.iterrows():

            st.markdown(
                f"""
                **{row['timestamp'].strftime('%d %b %Y, %H:%M:%S')}**

                `{row['sender_upi']}` → `{row['receiver_upi']}`

                **₹{row['amount']:,.0f}**  
                Transaction ID: `{row['transaction_id']}`  
                Bank Reference: `{row['bank_reference']}`
                """
            )

            st.divider()

# ============================================================
# ALERTS TAB
# ============================================================

if investigation_module == "Alerts":

    st.subheader("🚨 Risk Alerts")

    if not risk_alerts:

        st.success("No risk indicators detected.")

    else:

        st.warning(
            f"{len(risk_alerts)} risk indicator(s) detected."
        )

        for index, alert in enumerate(risk_alerts, start=1):

            severity = alert.get("severity", "UNKNOWN")
            pattern = alert.get("type", "UNKNOWN")
            entity = alert.get("entity", "UNKNOWN")
            description = alert.get(
                "description",
                "Risk indicator detected."
            )

            incoming = alert.get(
                "incoming_transaction",
                "N/A"
            )

            outgoing = alert.get(
                "outgoing_transaction",
                "N/A"
            )

            evidence_file = alert.get(
                "evidence_file",
                "N/A"
            )

            st.html(
                f"""
                
                <div class="trace-alert-card">

                    <div class="trace-alert-top">

                        <div>
                            <div class="trace-alert-index">
                                ALERT {index:02d}
                            </div>

                            <div class="trace-alert-title">
                                {pattern}
                            </div>
                        </div>

                        <div class="trace-alert-severity">
                            {severity}
                        </div>

                    </div>

                    <div class="trace-alert-entity">
                        <span>ENTITY</span>
                        <strong>{entity}</strong>
                    </div>

                    <div class="trace-alert-description">
                        {description}
                    </div>

                    <div class="trace-alert-flow">

                        <div class="trace-alert-flow-item">
                            <span>INCOMING TRANSACTION</span>
                            <strong>{incoming}</strong>
                        </div>

                        <div class="trace-alert-arrow">
                            →
                        </div>

                        <div class="trace-alert-flow-item">
                            <span>OUTGOING TRANSACTION</span>
                            <strong>{outgoing}</strong>
                        </div>

                    </div>

                    <div class="trace-alert-evidence">
                        <span>EVIDENCE SOURCE</span>
                        <strong>{evidence_file}</strong>
                    </div>

                </div>
                """,
                
            )

            st.divider()

# ============================================================
# EVIDENCE & REPORT TAB
# ============================================================

if investigation_module == "Evidence & Report":

    st.subheader("🔐 Evidence Integrity")

st.write(
    "SHA-256 hashes provide an integrity reference "
    "for the evidence files used by TRACE-X."
)

evidence_files = [
    "data/cdr.json",
    "data/ipdr.json",
    "data/transactions.json"
]

hash_records = []

for evidence_file in evidence_files:

    path = Path(evidence_file)

    if path.exists():

        file_hash = calculate_sha256(path)

        hash_records.append({
            "Evidence File": path.name,
            "SHA-256": file_hash
        })

if hash_records:

    st.dataframe(
        pd.DataFrame(hash_records),
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning(
        "No evidence files found."
    )

    st.subheader("Evidence & Report")

    st.write(
        "Evidence integrity, SHA-256 hashes, source references "
        "and investigation report generation will appear here."
    )

    st.button(
        "Generate Investigation Report"
    )
st.divider()

st.subheader("📄 Investigation Report")

st.write(
    "Generate a standardized PDF report containing "
    "case details, transaction flow, risk indicators "
    "and evidence integrity references."
)

if st.button(
    "Generate Investigation Report",
    type="primary"
):

    report_path = "reports/TRACE-X_Investigation_Report.pdf"

    generate_investigation_report(
        report_path,
        case_id,
        investigator,
        transactions_df,
        entity_links,
        risk_alerts,
        hash_records
    )

    with open(report_path, "rb") as report_file:

        st.download_button(
            label="⬇️ Download Investigation Report",
            data=report_file,
            file_name="TRACE-X_Investigation_Report.pdf",
            mime="application/pdf"
        )

    st.success(
        "Investigation report generated successfully."
    )
# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "TRACE-X | Cyber Fraud Analysis & Investigation PoC"
)
