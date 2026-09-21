import streamlit as st


def apply_styles():
    st.markdown(
        """
        <style>

        .stApp {
            background: #0b0e14;
        }

        [data-testid="stMetric"] {
            background: rgba(20, 24, 34, 0.72);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 14px;
            padding: 18px;
            transition: transform 0.2s ease,
                        border-color 0.2s ease,
                        box-shadow 0.2s ease;
        }

        [data-testid="stMetric"]:hover {
            transform: translateY(-3px);
            border-color: rgba(120, 140, 255, 0.35);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.28);
        }

        [data-testid="stExpander"] {
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 12px;
            background: rgba(18, 22, 31, 0.72);
        }

        [data-testid="stExpander"]:hover {
            border-color: rgba(120, 140, 255, 0.32);
        }

        .stButton > button {
            border-radius: 9px;
            transition: transform 0.18s ease,
                        box-shadow 0.18s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
        }

        [data-testid="stSidebar"] {
            background: #11141c;
            border-right: 1px solid rgba(255, 255, 255, 0.06);
        }

        button[data-baseweb="tab"] {
            transition: transform 0.2s ease;
        }

        button[data-baseweb="tab"]:hover {
            transform: translateY(-1px);
        }
        /* ---------- ACTIVE INVESTIGATION ---------- */

.trace-status {
    display: inline-flex;
    flex-direction: column;
    gap: 4px;

    padding: 10px 14px;

    border: 1px solid rgba(80, 220, 180, 0.18);
    border-radius: 10px;

    background: rgba(20, 35, 34, 0.55);

    margin-bottom: 16px;
}

.trace-status-main {
    display: flex;
    align-items: center;
    gap: 8px;

    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.08em;
}

.trace-status-sub {
    font-size: 11px;
    opacity: 0.55;
}

.trace-status-dot {
    width: 8px;
    height: 8px;

    border-radius: 50%;

    background: #42d6a4;

    box-shadow:
        0 0 6px rgba(66, 214, 164, 0.8),
        0 0 14px rgba(66, 214, 164, 0.45);

    animation: tracePulse 1.8s infinite;
}

@keyframes tracePulse {

    0% {
        transform: scale(1);
        opacity: 1;
    }

    50% {
        transform: scale(1.35);
        opacity: 0.55;
    }

    100% {
        transform: scale(1);
        opacity: 1;
    }
}
/* ---------- RISK CARD ---------- */

.risk-card {
    position: relative;
    padding: 22px;
    border-radius: 16px;

    background:
        linear-gradient(
            145deg,
            rgba(25, 29, 42, 0.95),
            rgba(14, 18, 27, 0.95)
        );

    border: 1px solid rgba(255, 255, 255, 0.08);

    box-shadow:
        0 12px 35px rgba(0, 0, 0, 0.28);

    overflow: hidden;
}

.risk-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.12em;

    opacity: 0.65;
}

.risk-live {
    color: #42d6a4;

    animation: riskLivePulse 1.8s infinite;
}

.risk-score {
    margin-top: 12px;

    font-size: 48px;
    font-weight: 800;
    line-height: 1;

    letter-spacing: -0.04em;
}

.risk-score span {
    font-size: 18px;
    opacity: 0.45;
    font-weight: 500;
}

.risk-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;

    margin-top: 16px;
    padding: 7px 12px;

    border-radius: 999px;

    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.08em;
}

.risk-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;

    animation: riskDotPulse 1.5s infinite;
}

.risk-high {
    color: #ff7d8a;
    background: rgba(255, 70, 90, 0.12);
    border: 1px solid rgba(255, 70, 90, 0.22);
}

.risk-medium {
    color: #ffd36a;
    background: rgba(255, 190, 60, 0.12);
    border: 1px solid rgba(255, 190, 60, 0.22);
}

.risk-low {
    color: #55ddb0;
    background: rgba(50, 210, 160, 0.12);
    border: 1px solid rgba(50, 210, 160, 0.22);
}

.risk-high .risk-dot {
    background: #ff5368;
    box-shadow: 0 0 12px rgba(255, 83, 104, 0.8);
}

.risk-medium .risk-dot {
    background: #ffc44d;
    box-shadow: 0 0 12px rgba(255, 196, 77, 0.8);
}

.risk-low .risk-dot {
    background: #42d6a4;
    box-shadow: 0 0 12px rgba(66, 214, 164, 0.8);
}

.risk-description {
    margin-top: 14px;

    font-size: 12px;
    opacity: 0.55;
}

.risk-bar {
    height: 6px;

    margin-top: 18px;

    border-radius: 999px;

    background: rgba(255, 255, 255, 0.07);

    overflow: hidden;
}

.risk-bar-fill {
    height: 100%;

    border-radius: inherit;

    animation: riskBarAppear 1s ease-out;
}

.risk-bar-fill.risk-high {
    background: #ff5368;
}

.risk-bar-fill.risk-medium {
    background: #ffc44d;
}

.risk-bar-fill.risk-low {
    background: #42d6a4;
}

@keyframes riskBarAppear {
    from {
        width: 0 !important;
    }
}

@keyframes riskDotPulse {
    0% {
        transform: scale(1);
        opacity: 1;
    }

    50% {
        transform: scale(1.35);
        opacity: 0.55;
    }

    100% {
        transform: scale(1);
        opacity: 1;
    }
}

@keyframes riskLivePulse {
    0% {
        opacity: 1;
    }

    50% {
        opacity: 0.45;
    }

    100% {
        opacity: 1;
    }
}
/* =========================================================
   TRACE-X COMMAND CENTER
   ========================================================= */

.trace-command-bar {
    display: grid;
    grid-template-columns: 1.7fr 1fr 1.25fr 1fr auto;
    align-items: center;
    gap: 18px;

    width: 100%;
    min-height: 82px;

    padding: 14px 18px;

    background:
        linear-gradient(
            135deg,
            rgba(20, 25, 38, 0.98),
            rgba(10, 14, 23, 0.98)
        );

    border: 1px solid rgba(120, 150, 190, 0.14);
    border-radius: 16px;

    box-shadow:
        0 18px 45px rgba(0, 0, 0, 0.30),
        inset 0 1px 0 rgba(255, 255, 255, 0.035);

    position: relative;
    overflow: hidden;
}


/* subtle top scan line */

.trace-command-bar::before {
    content: "";
    position: absolute;

    top: 0;
    left: 0;
    right: 0;

    height: 1px;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(66, 214, 164, 0.65),
            transparent
        );

    opacity: 0.75;
}


/* brand */

.command-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}


.command-logo {
    width: 42px;
    height: 42px;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 11px;

    background:
        linear-gradient(
            135deg,
            rgba(66, 214, 164, 0.18),
            rgba(66, 214, 164, 0.04)
        );

    border: 1px solid rgba(66, 214, 164, 0.28);

    color: #65e6bd;

    font-size: 14px;
    font-weight: 900;
    letter-spacing: 0.08em;

    box-shadow:
        0 0 18px rgba(66, 214, 164, 0.08);
}


.command-title {
    font-size: 19px;
    font-weight: 850;
    letter-spacing: 0.08em;

    line-height: 1.1;
}


.command-subtitle {
    margin-top: 4px;

    font-size: 9px;
    font-weight: 700;

    letter-spacing: 0.16em;

    opacity: 0.42;
}


/* case */

.command-case,
.command-status,
.command-risk,
.command-alerts {
    min-height: 48px;

    padding-left: 16px;

    border-left:
        1px solid rgba(255, 255, 255, 0.07);

    display: flex;
    flex-direction: column;
    justify-content: center;
}


.command-label,
.command-risk-label,
.command-alert-label {
    font-size: 8px;
    font-weight: 800;

    letter-spacing: 0.16em;

    opacity: 0.38;
}


.command-case-id {
    margin-top: 5px;

    font-family: monospace;

    font-size: 14px;
    font-weight: 700;

    letter-spacing: 0.04em;
}


/* system status */

.command-live {
    display: flex;
    align-items: center;
    gap: 7px;

    font-size: 10px;
    font-weight: 800;

    letter-spacing: 0.08em;

    color: #65e6bd;
}


.command-live-dot {
    width: 7px;
    height: 7px;

    border-radius: 50%;

    background: #42d6a4;

    box-shadow:
        0 0 7px rgba(66, 214, 164, 0.9),
        0 0 16px rgba(66, 214, 164, 0.45);

    animation: commandLivePulse 1.8s infinite;
}


.command-meta {
    margin-top: 5px;

    font-size: 9px;

    opacity: 0.38;
}


/* risk */

.command-risk-value {
    display: flex;
    align-items: center;
    gap: 7px;

    margin-top: 5px;

    font-size: 11px;
    font-weight: 800;
}


.command-risk-dot {
    width: 7px;
    height: 7px;

    border-radius: 50%;
}


.command-risk-high {
    color: #ff7180;
}


.command-risk-high .command-risk-dot {
    background: #ff5368;

    box-shadow:
        0 0 8px rgba(255, 83, 104, 0.85);
}


.command-risk-medium {
    color: #ffd166;
}


.command-risk-medium .command-risk-dot {
    background: #ffc44d;

    box-shadow:
        0 0 8px rgba(255, 196, 77, 0.85);
}


.command-risk-low {
    color: #65e6bd;
}


.command-risk-low .command-risk-dot {
    background: #42d6a4;

    box-shadow:
        0 0 8px rgba(66, 214, 164, 0.85);
}


/* alerts */

.command-alerts {
    min-width: 72px;
}


.command-alerts {
    flex-direction: row;
    align-items: center;
    gap: 9px;
}


.command-alert-number {
    font-size: 24px;
    font-weight: 850;

    line-height: 1;
}


.command-alert-label {
    line-height: 1.35;
}


/* animation */

@keyframes commandLivePulse {

    0% {
        transform: scale(1);
        opacity: 1;
    }

    50% {
        transform: scale(1.35);
        opacity: 0.5;
    }

    100% {
        transform: scale(1);
        opacity: 1;
    }

}
/* =========================================================
   INVESTIGATION NETWORK
   ========================================================= */

.trace-graph-header {
    display: flex;
    align-items: center;
    justify-content: space-between;

    margin-top: 8px;
    margin-bottom: 10px;

    padding: 18px 20px;

    background:
        linear-gradient(
            135deg,
            rgba(19, 24, 36, 0.96),
            rgba(10, 14, 22, 0.96)
        );

    border: 1px solid rgba(120, 150, 190, 0.12);
    border-bottom: 1px solid rgba(66, 214, 164, 0.16);

    border-radius: 14px 14px 0 0;

    box-shadow:
        0 12px 30px rgba(0, 0, 0, 0.18);

    position: relative;
    overflow: hidden;
}


/* subtle forensic scan line */

.trace-graph-header::after {
    content: "";

    position: absolute;

    left: 0;
    bottom: 0;

    width: 34%;
    height: 2px;

    background:
        linear-gradient(
            90deg,
            rgba(66, 214, 164, 0.8),
            transparent
        );

    opacity: 0.65;
}


.graph-header-left {
    min-width: 0;
}


.graph-eyebrow {
    font-size: 9px;
    font-weight: 800;

    letter-spacing: 0.18em;

    color: #58dcb0;

    opacity: 0.75;
}


.graph-title {
    margin-top: 5px;

    font-size: 22px;
    font-weight: 800;

    letter-spacing: -0.025em;
}


.graph-subtitle {
    margin-top: 5px;

    font-size: 11px;

    opacity: 0.42;
}


.graph-stats {
    display: flex;
    align-items: center;

    gap: 18px;

    margin-left: 30px;
}


.graph-stat {
    display: flex;
    flex-direction: column;

    min-width: 65px;
}


.graph-stat-value {
    font-size: 22px;
    font-weight: 800;

    line-height: 1;
}


.graph-stat-label {
    margin-top: 5px;

    font-size: 8px;
    font-weight: 800;

    letter-spacing: 0.14em;

    opacity: 0.38;
}


.graph-stat-divider {
    width: 1px;
    height: 30px;

    background:
        rgba(255, 255, 255, 0.08);
}


/* responsive */

@media (max-width: 900px) {

    .trace-graph-header {
        align-items: flex-start;
        gap: 18px;
    }

    .graph-stats {
        margin-left: 0;
    }

}


@media (max-width: 650px) {

    .trace-graph-header {
        flex-direction: column;
    }

    .graph-stats {
        width: 100%;
    }

}
/* =========================================================
   GRAPH LEGEND
   ========================================================= */

.trace-graph-legend {
    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 9px 14px;

    background: rgba(13, 18, 28, 0.92);

    border-left: 1px solid rgba(120, 150, 190, 0.12);
    border-right: 1px solid rgba(120, 150, 190, 0.12);
    border-bottom: 1px solid rgba(120, 150, 190, 0.10);

    font-size: 9px;

    letter-spacing: 0.08em;
}


.legend-title {
    font-weight: 800;
    opacity: 0.38;
}


.legend-items {
    display: flex;
    align-items: center;
    gap: 16px;
}


.legend-item {
    display: flex;
    align-items: center;
    gap: 6px;

    font-size: 8px;
    font-weight: 750;

    opacity: 0.65;
}


.legend-dot {
    width: 7px;
    height: 7px;

    border-radius: 50%;
}


.legend-phone {
    background: #4da3ff;
    box-shadow: 0 0 7px rgba(77, 163, 255, 0.55);
}


.legend-imei {
    background: #a875ff;
    box-shadow: 0 0 7px rgba(168, 117, 255, 0.55);
}


.legend-ip {
    background: #ffb84d;
    box-shadow: 0 0 7px rgba(255, 184, 77, 0.55);
}


.legend-upi {
    background: #42d6a4;
    box-shadow: 0 0 7px rgba(66, 214, 164, 0.55);
}


.legend-divider {
    width: 1px;
    height: 16px;

    background: rgba(255, 255, 255, 0.10);
}


.legend-line {
    width: 20px;
    height: 2px;

    background: #42d6a4;

    box-shadow: 0 0 7px rgba(66, 214, 164, 0.45);
}
.evidence-summary {
    margin-top: 18px;
    padding: 18px 20px;
    background: linear-gradient(
        135deg,
        rgba(19,24,36,0.96),
        rgba(10,14,22,0.96)
    );
    border: 1px solid rgba(120,150,190,0.12);
    border-radius: 14px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.18);
}

.evidence-summary-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
}

.evidence-eyebrow {
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 0.16em;
    color: #42d6a4;
    opacity: 0.75;
}

.evidence-title {
    margin-top: 3px;
    font-size: 18px;
    font-weight: 800;
    letter-spacing: 0.02em;
    color: #f2f5f8;
}

.evidence-status {
    display: flex;
    align-items: center;
    gap: 7px;
    padding: 6px 10px;
    border: 1px solid rgba(66,214,164,0.18);
    border-radius: 999px;
    font-size: 8px;
    font-weight: 800;
    letter-spacing: 0.12em;
    color: #42d6a4;
    background: rgba(66,214,164,0.06);
}

.evidence-status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #42d6a4;
    box-shadow: 0 0 8px rgba(66,214,164,0.65);
}

.evidence-summary-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
}

.evidence-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 13px 14px;
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.055);
    border-radius: 10px;
    transition: all 0.2s ease;
}

.evidence-item:hover {
    transform: translateY(-2px);
    border-color: rgba(66,214,164,0.20);
    background: rgba(66,214,164,0.035);
}

.evidence-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    border-radius: 9px;
    background: rgba(66,214,164,0.08);
    color: #42d6a4;
    font-size: 16px;
}

.evidence-value {
    font-size: 20px;
    font-weight: 800;
    color: #f2f5f8;
}

.evidence-label {
    margin-top: 2px;
    font-size: 8px;
    font-weight: 750;
    letter-spacing: 0.10em;
    color: #8491a5;
}
.analysis-pipeline {
    margin-top: 4px;
    padding: 18px 20px;
    background: linear-gradient(
        135deg,
        rgba(19,24,36,0.96),
        rgba(10,14,22,0.96)
    );
    border: 1px solid rgba(120,150,190,0.12);
    border-radius: 14px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.18);
}

.pipeline-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 18px;
}

.pipeline-eyebrow {
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 0.16em;
    color: #42d6a4;
    opacity: 0.75;
}

.pipeline-title {
    margin-top: 3px;
    font-size: 18px;
    font-weight: 800;
    color: #f2f5f8;
}

.pipeline-live {
    display: flex;
    align-items: center;
    gap: 7px;
    padding: 6px 10px;
    border-radius: 999px;
    border: 1px solid rgba(66,214,164,0.18);
    background: rgba(66,214,164,0.06);
    color: #42d6a4;
    font-size: 8px;
    font-weight: 800;
    letter-spacing: 0.12em;
}

.pipeline-live-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #42d6a4;
    box-shadow: 0 0 8px rgba(66,214,164,0.65);
    animation: pipelinePulse 1.6s ease-in-out infinite;
}

.pipeline-stage {
    margin-bottom: 14px;
}

.pipeline-stage:last-child {
    margin-bottom: 0;
}

.pipeline-stage-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 7px;
}

.pipeline-stage-name {
    font-size: 11px;
    font-weight: 700;
    color: #dce3ec;
}

.pipeline-stage-status {
    font-size: 8px;
    font-weight: 800;
    letter-spacing: 0.10em;
    color: #42d6a4;
}

.pipeline-track {
    width: 100%;
    height: 5px;
    border-radius: 999px;
    overflow: hidden;
    background: rgba(255,255,255,0.07);
}

.pipeline-fill {
    height: 100%;
    border-radius: 999px;
    background: #42d6a4;
    box-shadow: 0 0 10px rgba(66,214,164,0.35);
}

@keyframes pipelinePulse {
    0%, 100% {
        opacity: 0.45;
        transform: scale(0.85);
    }
    50% {
        opacity: 1;
        transform: scale(1);
    }
}
/* =========================================================
   TRACE-X COMMAND CENTER MOTION
   ========================================================= */

.trace-command-bar {
    position: relative;
    overflow: hidden;
    isolation: isolate;
}

/* animated forensic scan */

.command-scanline {
    position: absolute;
    top: 0;
    left: -30%;
    width: 22%;
    height: 100%;

    background: linear-gradient(
        90deg,
        transparent,
        rgba(66, 214, 164, 0.04),
        rgba(66, 214, 164, 0.22),
        rgba(66, 214, 164, 0.04),
        transparent
    );

    transform: skewX(-18deg);
    animation: commandScan 4s linear infinite;
    pointer-events: none;
    z-index: 0;
}

/* make actual header content stay above scan */

.command-brand,
.command-case,
.command-system,
.command-risk,
.command-alerts {
    position: relative;
    z-index: 2;
}

/* TRACE-X logo pulse */

.command-logo {
    position: relative;
}

.command-logo::after {
    content: "";
    position: absolute;
    inset: -5px;

    border-radius: 10px;

    border: 1px solid rgba(66, 214, 164, 0.20);

    animation: logoPulse 2.2s ease-in-out infinite;
}

/* red X */

.command-title span {
    color: #ff4058;

    text-shadow:
        0 0 8px rgba(255, 64, 88, 0.45),
        0 0 18px rgba(255, 64, 88, 0.18);
}

/* active case status */

.command-case-status {
    margin-top: 4px;

    font-size: 7px;
    font-weight: 800;

    letter-spacing: 0.12em;

    color: #42d6a4;
    opacity: 0.75;
}

/* engine status */

.command-meta {
    margin-top: 6px;

    font-size: 7px;

    letter-spacing: 0.07em;

    color: #718096;
}

.command-meta span {
    color: #42d6a4;
    margin: 0 3px;
}

/* live indicators */

.command-live-dot,
.command-risk-dot {
    animation: livePulse 1.5s ease-in-out infinite;
}

/* alert counter */

.command-alert-number {
    animation: alertGlow 2s ease-in-out infinite;
}

/* =========================================================
   ANIMATIONS
   ========================================================= */

@keyframes commandScan {

    0% {
        left: -30%;
        opacity: 0;
    }

    12% {
        opacity: 1;
    }

    70% {
        opacity: 1;
    }

    100% {
        left: 125%;
        opacity: 0;
    }
}

@keyframes logoPulse {

    0%,
    100% {
        opacity: 0.25;
        transform: scale(0.96);
    }

    50% {
        opacity: 0.85;
        transform: scale(1.04);
    }
}

@keyframes livePulse {

    0%,
    100% {
        opacity: 0.45;

        box-shadow:
            0 0 3px rgba(66, 214, 164, 0.2);
    }

    50% {
        opacity: 1;

        box-shadow:
            0 0 8px rgba(66, 214, 164, 0.8),
            0 0 16px rgba(66, 214, 164, 0.35);
    }
}

@keyframes alertGlow {

    0%,
    100% {
        text-shadow: none;
    }

    50% {
        text-shadow:
            0 0 8px rgba(255, 64, 88, 0.45),
            0 0 18px rgba(255, 64, 88, 0.18);
    }
}
/* TRACE-X ALERT CARDS */

.trace-alert-card {
    margin: 18px 0;
    padding: 22px 24px;
    border: 1px solid rgba(255, 64, 88, 0.25);
    border-radius: 14px;
    background: rgba(15, 21, 30, 0.96);
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.35);
}

.trace-alert-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 18px;
}

.trace-alert-index {
    color: #8e9aaa;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.2em;
}

.trace-alert-title {
    margin-top: 5px;
    color: #f3f7fb;
    font-size: 17px;
    font-weight: 800;
}

.trace-alert-severity {
    padding: 6px 12px;
    border: 1px solid rgba(255, 64, 88, 0.5);
    border-radius: 999px;
    color: #ff4058;
    background: rgba(255, 64, 88, 0.1);
    font-size: 10px;
    font-weight: 900;
    letter-spacing: 0.14em;
}

.trace-alert-entity {
    display: flex;
    gap: 12px;
    margin-bottom: 14px;
}

.trace-alert-entity span,
.trace-alert-flow-item span,
.trace-alert-evidence span {
    color: #718096;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 0.16em;
}

.trace-alert-entity strong {
    color: #42d6a4;
    font-size: 13px;
}

.trace-alert-description {
    margin-bottom: 18px;
    color: #c6d0dc;
    font-size: 13px;
    line-height: 1.6;
}

.trace-alert-flow {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    gap: 14px;
    margin-bottom: 18px;
}

.trace-alert-flow-item {
    padding: 13px 15px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.025);
}

.trace-alert-flow-item strong {
    display: block;
    margin-top: 7px;
    color: #f3f7fb;
    font-size: 12px;
}

.trace-alert-arrow {
    color: #ff4058;
    font-size: 22px;
    font-weight: 900;
}

.trace-alert-evidence {
    display: flex;
    gap: 12px;
    padding-top: 14px;
    border-top: 1px solid rgba(255, 255, 255, 0.07);
}

.trace-alert-evidence strong {
    color: #8fa3bf;
    font-size: 11px;
}
/* =========================================================
   TRACE-X COMMAND CENTER THEME
   ========================================================= */

body {
    background:
        radial-gradient(circle at 50% 0%, rgba(30, 190, 220, 0.035), transparent 35%),
        #05070a !important;
}

/* subtle forensic grid */
[data-testid="stAppViewContainer"] {
    background:
        linear-gradient(rgba(70, 190, 210, 0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(70, 190, 210, 0.025) 1px, transparent 1px),
        #05070a !important;
    background-size: 42px 42px;
}

/* sidebar */
[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, #090d12 0%, #070a0e 100%) !important;
    border-right: 1px solid rgba(70, 210, 230, 0.16) !important;
}

/* sidebar content */
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

/* metric cards */
[data-testid="stMetric"] {
    background:
        linear-gradient(145deg, rgba(16, 23, 31, 0.98), rgba(8, 12, 17, 0.98));
    border: 1px solid rgba(80, 170, 195, 0.16);
    border-radius: 14px;
    padding: 18px;
    box-shadow:
        0 12px 30px rgba(0, 0, 0, 0.30),
        inset 0 1px 0 rgba(255, 255, 255, 0.025);
}

/* metric label */
[data-testid="stMetricLabel"] {
    color: #728394 !important;
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* metric value */
[data-testid="stMetricValue"] {
    color: #edf7fa !important;
    font-weight: 700 !important;
}

/* tables */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(80, 170, 195, 0.15);
    border-radius: 14px;
    overflow: hidden;
}

/* buttons */
.stButton > button {
    background: #0c1219 !important;
    color: #cbd8df !important;
    border: 1px solid rgba(80, 170, 195, 0.18) !important;
    border-radius: 9px !important;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #42d6e8 !important;
    color: #ffffff !important;
    box-shadow: 0 0 18px rgba(66, 214, 232, 0.12);
}

/* active / selected controls */
.stRadio label[data-baseweb="radio"] {
    color: #b9c8d0 !important;
}

.stRadio label[data-baseweb="radio"]:hover {
    color: #42d6e8 !important;
}

/* section headings */
h1, h2, h3 {
    color: #edf5f7 !important;
    letter-spacing: -0.02em;
}

/* dividers */
hr {
    border-color: rgba(100, 150, 170, 0.15) !important;
}

/* success / info / warning cards */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    background: rgba(12, 18, 25, 0.92) !important;
}

/* cyan forensic accent */
.trace-cyan {
    color: #42d6e8;
}

/* amber investigation accent */
.trace-amber {
    color: #e4ad52;
}

/* red threat accent */
.trace-red {
    color: #ff5366;
}

/* green evidence accent */
.trace-green {
    color: #42d6a4;
}
/* =========================================================
   TRACE-X — RISK ANALYZER
   ========================================================= */

.trace-risk-panel {
    width: 100%;
    margin: 28px 0 34px 0;
    padding: 26px 28px 30px 28px;
    box-sizing: border-box;
    background:
        radial-gradient(circle at 8% 0%, rgba(66,214,164,0.08), transparent 30%),
        linear-gradient(145deg, #0b0d12, #090b10);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 16px;
    box-shadow:
        0 18px 45px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.025);
}

.trace-risk-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 24px;
}

.trace-risk-kicker {
    color: #42d6a4;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 7px;
}

.trace-risk-title {
    color: #f4f7fb;
    font-size: 25px;
    font-weight: 800;
    line-height: 1.1;
}

.trace-risk-subtitle {
    margin-top: 7px;
    color: #7f8b9d;
    font-size: 12px;
}

.trace-risk-live {
    display: flex;
    align-items: center;
    gap: 7px;
    color: #42d6a4;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 0.12em;
    padding: 8px 12px;
    border: 1px solid rgba(66,214,164,0.25);
    border-radius: 999px;
    background: rgba(66,214,164,0.05);
}

.trace-risk-live span {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #42d6a4;
    box-shadow: 0 0 12px rgba(66,214,164,0.9);
    animation: traceRiskPulse 1.5s infinite;
}

.trace-risk-card {
    position: relative;
    overflow: hidden;
    min-height: 150px;
    padding: 22px;
    box-sizing: border-box;
    background: #0f1219;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 13px;
    transition:
        transform 0.25s ease,
        border-color 0.25s ease,
        box-shadow 0.25s ease;
}

.trace-risk-card:hover {
    transform: translateY(-4px);
    border-color: rgba(66,214,164,0.38);
    box-shadow:
        0 14px 35px rgba(0,0,0,0.35),
        0 0 25px rgba(66,214,164,0.06);
}

.trace-risk-card::after {
    content: "";
    position: absolute;
    left: 0;
    bottom: 0;
    width: 100%;
    height: 3px;
    background: #42d6a4;
    opacity: 0.8;
}

.trace-risk-card-high::after {
    background: #ffbf47;
    box-shadow: 0 0 14px rgba(255,191,71,0.45);
}

.trace-risk-card-medium::after {
    background: #42d6a4;
}

.trace-risk-card-low::after {
    background: #53657d;
}

.trace-risk-card-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 18px;
}

.trace-risk-severity {
    color: #ffbf47;
    font-size: 10px;
    font-weight: 900;
    letter-spacing: 0.14em;
}

.trace-risk-count {
    color: #718096;
    font-size: 11px;
    font-weight: 700;
}

.trace-risk-card-title {
    color: #f1f4f8;
    font-size: 17px;
    font-weight: 750;
    margin-bottom: 10px;
}

.trace-risk-card-description {
    color: #8792a3;
    font-size: 12px;
    line-height: 1.55;
}

.trace-risk-card-bar {
    height: 4px;
    margin-top: 20px;
    overflow: hidden;
    background: rgba(255,255,255,0.06);
    border-radius: 99px;
}

.trace-risk-card-bar > div {
    width: 70%;
    height: 100%;
    background: linear-gradient(
        90deg,
        #42d6a4,
        #7ff2cb
    );
    border-radius: 99px;
    box-shadow: 0 0 12px rgba(66,214,164,0.35);
}

.trace-risk-card:hover .trace-risk-card-bar > div {
    animation: traceRiskScan 1.2s ease-in-out infinite alternate;
}

@keyframes traceRiskPulse {
    0%, 100% {
        opacity: 1;
        transform: scale(1);
    }
    50% {
        opacity: 0.45;
        transform: scale(0.7);
    }
}

@keyframes traceRiskScan {
    from {
        transform: translateX(-8%);
    }
    to {
        transform: translateX(8%);
    }
}
</style>
        """,
        unsafe_allow_html=True,
    )



