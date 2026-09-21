import streamlit as st


def render_command_bar(case_id, risk_level, alert_count):

    if risk_level == "HIGH":
        risk_color = "#ff4058"
        risk_label = "HIGH RISK"
    elif risk_level == "MEDIUM":
        risk_color = "#ffbf47"
        risk_label = "MEDIUM RISK"
    else:
        risk_color = "#42d6a4"
        risk_label = "LOW RISK"

    html = f"""
    <style>

    .tx-command {{
        position: relative;
        width: 100%;
        height: 140px;
        margin: 12px 0 24px 0;
        overflow: hidden;

        display: grid;
        grid-template-columns:
            1.7fr
            1.05fr
            1.25fr
            1fr
            0.55fr;

        align-items: center;

        background:
            radial-gradient(
                circle at 15% 50%,
                rgba(66,214,164,0.08),
                transparent 28%
            ),
            linear-gradient(
                135deg,
                #121925 0%,
                #0b1019 55%,
                #090d14 100%
            );

        border:
            1px solid rgba(66,214,164,0.20);

        border-radius: 18px;

        box-shadow:
            0 20px 60px rgba(0,0,0,0.45),
            inset 0 1px 0 rgba(255,255,255,0.04),
            0 0 35px rgba(66,214,164,0.04);

        color: white;

        font-family:
            Inter,
            Arial,
            sans-serif;
    }}


    /* =====================================================
       MOVING FORENSIC SCAN
       ===================================================== */

    .tx-scan {{
        position: absolute;

        top: 0;
        left: -25%;

        width: 25%;
        height: 100%;

        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(66,214,164,0.03),
                rgba(66,214,164,0.22),
                rgba(66,214,164,0.03),
                transparent
            );

        transform: skewX(-18deg);

        animation:
            txScan 3.8s linear infinite;

        pointer-events: none;
    }}


    /* =====================================================
       BRAND
       ===================================================== */

    .tx-brand {{
        display: flex;
        align-items: center;
        gap: 14px;
        padding-left: 20px;
        position: relative;
        z-index: 2;
    }}


    .tx-logo {{
        position: relative;

        width: 48px;
        height: 48px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 13px;

        background:
            linear-gradient(
                135deg,
                rgba(66,214,164,0.18),
                rgba(66,214,164,0.03)
            );

        border:
            1px solid rgba(66,214,164,0.38);

        color: #42d6a4;

        font-family:
            Impact,
            Haettenschweiler,
            "Arial Narrow Bold",
            sans-serif;

        font-size: 18px;
        letter-spacing: 0.05em;

        box-shadow:
            0 0 18px rgba(66,214,164,0.10);
    }}


    .tx-logo::before {{
        content: "";

        position: absolute;
        inset: -5px;

        border-radius: 16px;

        border:
            1px solid rgba(66,214,164,0.14);

        animation:
            txPulse 2s ease-in-out infinite;
    }}


    .tx-brand-name {{
        font-family:
            Impact,
            Haettenschweiler,
            "Arial Narrow Bold",
            sans-serif;

        font-size: 38px;
        letter-spacing: 0.06em;

        line-height: 1;
    }}


    .tx-brand-name span {{
        color: #ff4058;

        text-shadow:
            0 0 12px rgba(255,64,88,0.55);
    }}


    .tx-brand-sub {{
        margin-top: 7px;

        color: #667386;

        font-size: 8px;
        font-weight: 800;

        letter-spacing: 0.20em;
    }}


    /* =====================================================
       CASE
       ===================================================== */

    .tx-case {{
        padding-left: 20px;

        border-left:
            1px solid rgba(255,255,255,0.07);

        position: relative;
        z-index: 2;
    }}


    .tx-label {{
        color: #566174;

        font-size: 7px;
        font-weight: 900;

        letter-spacing: 0.16em;
    }}


    .tx-value {{
        margin-top: 6px;

        color: #e8edf4;

        font-size: 13px;
        font-weight: 800;

        letter-spacing: 0.08em;
    }}


    .tx-case-state {{
        margin-top: 5px;

        color: #42d6a4;

        font-size: 7px;
        font-weight: 800;

        letter-spacing: 0.11em;
    }}


    /* =====================================================
       SYSTEM
       ===================================================== */

    .tx-system {{
        padding-left: 20px;

        border-left:
            1px solid rgba(255,255,255,0.07);

        position: relative;
        z-index: 2;
    }}


    .tx-online {{
        display: flex;
        align-items: center;
        gap: 7px;

        color: #42d6a4;

        font-size: 8px;
        font-weight: 900;

        letter-spacing: 0.13em;
    }}


    .tx-dot {{
        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: #42d6a4;

        box-shadow:
            0 0 7px #42d6a4,
            0 0 15px rgba(66,214,164,0.55);

        animation:
            txLive 1.3s ease-in-out infinite;
    }}


    .tx-engine {{
        margin-top: 7px;

        color: #596579;

        font-size: 7px;

        letter-spacing: 0.08em;
    }}


    /* =====================================================
       THREAT
       ===================================================== */

    .tx-threat {{
        padding-left: 20px;

        border-left:
            1px solid rgba(255,255,255,0.07);

        position: relative;
        z-index: 2;
    }}


    .tx-threat-value {{
        display: flex;
        align-items: center;
        gap: 8px;

        margin-top: 6px;

        color: {risk_color};

        font-size: 9px;
        font-weight: 900;

        letter-spacing: 0.10em;

        text-shadow:
            0 0 10px {risk_color}55;
    }}


    .tx-threat-dot {{
        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: {risk_color};

        box-shadow:
            0 0 8px {risk_color};

        animation:
            txThreat 1.5s ease-in-out infinite;
    }}


    /* =====================================================
       ALERT COUNTER
       ===================================================== */

    .tx-alerts {{
        height: 58px;

        display: flex;
        align-items: center;
        justify-content: center;
        gap: 9px;

        border-left:
            1px solid rgba(255,255,255,0.07);

        position: relative;
        z-index: 2;
    }}


    .tx-alert-number {{
        color: #ff4058;

        font-size: 27px;
        font-weight: 900;

        line-height: 1;

        text-shadow:
            0 0 14px rgba(255,64,88,0.42);

        animation:
            txAlertGlow 2s ease-in-out infinite;
    }}


    .tx-alert-label {{
        color: #697589;

        font-size: 7px;
        font-weight: 900;

        line-height: 1.35;

        letter-spacing: 0.10em;
    }}


    /* =====================================================
       ANIMATIONS
       ===================================================== */

    @keyframes txScan {{

        0% {{
            left: -25%;
            opacity: 0;
        }}

        15% {{
            opacity: 1;
        }}

        75% {{
            opacity: 1;
        }}

        100% {{
            left: 125%;
            opacity: 0;
        }}
    }}


    @keyframes txPulse {{

        0%, 100% {{
            opacity: 0.25;
            transform: scale(0.97);
        }}

        50% {{
            opacity: 0.85;
            transform: scale(1.04);
        }}
    }}


    @keyframes txLive {{

        0%, 100% {{
            opacity: 0.4;
            transform: scale(0.8);
        }}

        50% {{
            opacity: 1;
            transform: scale(1.15);
        }}
    }}


    @keyframes txThreat {{

        0%, 100% {{
            opacity: 0.45;
        }}

        50% {{
            opacity: 1;
        }}
    }}


    @keyframes txAlertGlow {{

        0%, 100% {{
            opacity: 0.75;
        }}

        50% {{
            opacity: 1;

            text-shadow:
                0 0 8px rgba(255,64,88,0.65),
                0 0 22px rgba(255,64,88,0.28);
        }}
    }}

    </style>


    <div class="tx-command">

        <div class="tx-scan"></div>


        <div class="tx-brand">

            <div class="tx-logo">
                TX
            </div>

            <div>

                <div class="tx-brand-name">
                    TRACE<span>-X</span>
                </div>

                <div class="tx-brand-sub">
                    DIGITAL FORENSICS // COMMAND CENTER
                </div>

            </div>

        </div>


        <div class="tx-case">

            <div class="tx-label">
                ACTIVE CASE
            </div>

            <div class="tx-value">
                {case_id}
            </div>

            <div class="tx-case-state">
                ● INVESTIGATION ACTIVE
            </div>

        </div>


        <div class="tx-system">

            <div class="tx-online">

                <span class="tx-dot"></span>

                SYSTEM ONLINE

            </div>

            <div class="tx-engine">
                EVIDENCE ENGINE
                •
                CORRELATION ENGINE
                •
                RISK ENGINE
            </div>

        </div>


        <div class="tx-threat">

            <div class="tx-label">
                THREAT LEVEL
            </div>

            <div class="tx-threat-value">

                <span class="tx-threat-dot"></span>

                {risk_label}

            </div>

        </div>


        <div class="tx-alerts">

            <div class="tx-alert-number">
                {alert_count}
            </div>

            <div class="tx-alert-label">
                ACTIVE<br>
                ALERTS
            </div>

        </div>

    </div>
    """

    st.html(html)