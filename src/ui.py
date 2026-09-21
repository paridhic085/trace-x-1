import streamlit as st
import time
import textwrap


def animated_metric(label, value, prefix="", suffix=""):
    placeholder = st.empty()

    try:
        target = int(value)

    except (TypeError, ValueError):
        placeholder.metric(
            label,
            f"{prefix}{value}{suffix}"
        )
        return

    step = max(1, target // 20)

    for current in range(0, target + 1, step):

        if current > target:
            current = target

        placeholder.metric(
            label,
            f"{prefix}{current}{suffix}"
        )

        time.sleep(0.025)

    placeholder.metric(
        label,
        f"{prefix}{target}{suffix}"
    )


def investigation_status(status="ACTIVE"):

    if status == "ACTIVE":
        label = "INVESTIGATION ACTIVE"
        subtext = "Evidence-driven analysis in progress"

    else:
        label = "INVESTIGATION PAUSED"
        subtext = "Analysis is currently paused"

    html = f"""
    <div class="trace-status">

        <div class="trace-status-main">
            <span class="trace-status-dot"></span>
            <span>{label}</span>
        </div>

        <div class="trace-status-sub">
            {subtext}
        </div>

    </div>
    """

    st.html(html)

def render_risk_card(risk_score, risk_level, alert_count):

    if risk_level == "HIGH":
        badge = "HIGH RISK"
        badge_class = "risk-high"

    elif risk_level == "MEDIUM":
        badge = "MEDIUM RISK"
        badge_class = "risk-medium"

    else:
        badge = "LOW RISK"
        badge_class = "risk-low"

    html = f"""
    <div class="risk-card">

        <div class="risk-card-header">
            <span>THREAT ASSESSMENT</span>
            <span class="risk-live">● LIVE</span>
        </div>

        <div class="risk-score">
            {risk_score}
            <span>/100</span>
        </div>

        <div class="risk-badge {badge_class}">
            <span class="risk-dot"></span>
            {badge}
        </div>

        <div class="risk-description">
            {alert_count} risk indicator(s) detected
            for investigator review.
        </div>

        <div class="risk-bar">

            <div
                class="risk-bar-fill {badge_class}"
                style="width: {risk_score}%"
            ></div>

        </div>

    </div>
    """

    st.html(html)

def render_evidence_summary(evidence_files, entity_count, relationship_count):
    html = f"""
    <div class="evidence-summary">

        <div class="evidence-summary-header">
            <div>
                <div class="evidence-eyebrow">CASE INTELLIGENCE</div>
                <div class="evidence-title">Evidence Summary</div>
            </div>

            <div class="evidence-status">
                <span class="evidence-status-dot"></span>
                CORRELATED
            </div>
        </div>

        <div class="evidence-summary-grid">

            <div class="evidence-item">
                <div class="evidence-icon">◈</div>
                <div>
                    <div class="evidence-value">{evidence_files}</div>
                    <div class="evidence-label">SOURCE FILES</div>
                </div>
            </div>

            <div class="evidence-item">
                <div class="evidence-icon">◎</div>
                <div>
                    <div class="evidence-value">{entity_count}</div>
                    <div class="evidence-label">CORRELATED ENTITIES</div>
                </div>
            </div>

            <div class="evidence-item">
                <div class="evidence-icon">⛓</div>
                <div>
                    <div class="evidence-value">{relationship_count}</div>
                    <div class="evidence-label">RELATIONSHIPS</div>
                </div>
            </div>

        </div>

    </div>
    """

    st.html(html)
def render_analysis_pipeline():
    html = """
    <div class="analysis-pipeline">

        <div class="pipeline-header">
            <div>
                <div class="pipeline-eyebrow">ANALYSIS ENGINE</div>
                <div class="pipeline-title">Investigation Pipeline</div>
            </div>

            <div class="pipeline-live">
                <span class="pipeline-live-dot"></span>
                PROCESSING
            </div>
        </div>

        <div class="pipeline-stage">
            <div class="pipeline-stage-top">
                <span class="pipeline-stage-name">Evidence Ingestion</span>
                <span class="pipeline-stage-status">COMPLETE</span>
            </div>
            <div class="pipeline-track">
                <div class="pipeline-fill" style="width: 100%;"></div>
            </div>
        </div>

        <div class="pipeline-stage">
            <div class="pipeline-stage-top">
                <span class="pipeline-stage-name">Entity Correlation</span>
                <span class="pipeline-stage-status">COMPLETE</span>
            </div>
            <div class="pipeline-track">
                <div class="pipeline-fill" style="width: 100%;"></div>
            </div>
        </div>

        <div class="pipeline-stage">
            <div class="pipeline-stage-top">
                <span class="pipeline-stage-name">Risk Detection</span>
                <span class="pipeline-stage-status">COMPLETE</span>
            </div>
            <div class="pipeline-track">
                <div class="pipeline-fill" style="width: 100%;"></div>
            </div>
        </div>

        <div class="pipeline-stage">
            <div class="pipeline-stage-top">
                <span class="pipeline-stage-name">Network Reconstruction</span>
                <span class="pipeline-stage-status">READY</span>
            </div>
            <div class="pipeline-track">
                <div class="pipeline-fill" style="width: 100%;"></div>
            </div>
        </div>

        <div class="pipeline-stage">
            <div class="pipeline-stage-top">
                <span class="pipeline-stage-name">Evidence Integrity</span>
                <span class="pipeline-stage-status">VERIFIED</span>
            </div>
            <div class="pipeline-track">
                <div class="pipeline-fill" style="width: 100%;"></div>
            </div>
        </div>

    </div>
    """

    st.html(html)