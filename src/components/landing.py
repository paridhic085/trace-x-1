import streamlit as st


def render_landing_screen():

    html = """
    <style>

    .trace-landing {
        position: fixed;
        inset: 0;
        z-index: 999999;
        overflow: hidden;
        background:
            radial-gradient(
                circle at 50% 45%,
                rgba(20, 55, 65, 0.22),
                transparent 42%
            ),
            #070a0f;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: landingExit 1.2s ease 4.8s forwards;
        pointer-events: none;
    }

    /* moving EPR / data lines */

    .trace-lines {
        position: absolute;
        inset: 0;
        overflow: hidden;
        opacity: 0.65;
    }

    .trace-line {
        position: absolute;
        height: 1px;
        width: 55vw;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(66, 214, 164, 0.05),
            #42d6a4,
            rgba(66, 214, 164, 0.05),
            transparent
        );
        box-shadow: 0 0 12px rgba(66, 214, 164, 0.45);
        transform: rotate(-12deg);
        animation: traceSweep linear infinite;
    }

    .trace-line:nth-child(1) {
        top: 25%;
        left: -60%;
        animation-duration: 3.5s;
    }

    .trace-line:nth-child(2) {
        top: 34%;
        left: -70%;
        animation-duration: 4.2s;
        animation-delay: 0.7s;
    }

    .trace-line:nth-child(3) {
        top: 61%;
        left: -55%;
        animation-duration: 3.8s;
        animation-delay: 1.1s;
    }

    .trace-line:nth-child(4) {
        top: 72%;
        left: -65%;
        animation-duration: 4.5s;
        animation-delay: 1.8s;
    }

    .trace-line.red {
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 70, 90, 0.05),
            #ff4058,
            rgba(255, 70, 90, 0.05),
            transparent
        );
        box-shadow: 0 0 12px rgba(255, 64, 88, 0.45);
    }

    @keyframes traceSweep {
        0% {
            transform: translateX(-20vw) rotate(-12deg);
            opacity: 0;
        }

        15% {
            opacity: 1;
        }

        85% {
            opacity: 1;
        }

        100% {
            transform: translateX(150vw) rotate(-12deg);
            opacity: 0;
        }
    }

    /* central interface */

    .trace-center {
        position: relative;
        z-index: 5;
        text-align: center;
        animation: centerIn 1.3s ease-out forwards;
    }

    .trace-eyebrow {
        margin-bottom: 18px;
        color: #42d6a4;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.38em;
        opacity: 0.75;
    }

    .trace-logo {
        font-family: Impact, Haettenschweiler, "Arial Narrow Bold", sans-serif;
        font-size: clamp(72px, 10vw, 150px);
        line-height: 0.9;
        letter-spacing: 0.06em;
        color: #f3f7fb;
        text-shadow:
            0 0 10px rgba(255,255,255,0.35),
            0 0 35px rgba(66,214,164,0.15);
    }

    .trace-logo-x {
        color: #ff4058;
        text-shadow:
            0 0 12px rgba(255,64,88,0.7),
            0 0 35px rgba(255,64,88,0.35);
    }

    .trace-tagline {
        margin-top: 22px;
        color: #8e9aaa;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.34em;
    }

    .trace-status {
        margin-top: 42px;
        color: #42d6a4;
        font-size: 9px;
        font-weight: 800;
        letter-spacing: 0.22em;
    }

    .trace-status-bar {
        width: min(420px, 55vw);
        height: 3px;
        margin: 12px auto 0;
        overflow: hidden;
        background: rgba(255,255,255,0.08);
        border-radius: 999px;
    }

    .trace-status-fill {
        height: 100%;
        width: 0%;
        background: #42d6a4;
        box-shadow: 0 0 12px rgba(66,214,164,0.8);
        animation: loadingBar 4.2s ease-out forwards;
    }

    @keyframes loadingBar {
        0% { width: 0%; }
        100% { width: 100%; }
    }

    @keyframes centerIn {
        0% {
            opacity: 0;
            transform: scale(0.92);
            filter: blur(12px);
        }

        100% {
            opacity: 1;
            transform: scale(1);
            filter: blur(0);
        }
    }

    @keyframes landingExit {
        0% {
            opacity: 1;
        }

        100% {
            opacity: 0;
            visibility: hidden;
        }
    }

    </style>

    <div class="trace-landing">

        <div class="trace-lines">
            <div class="trace-line"></div>
            <div class="trace-line red"></div>
            <div class="trace-line"></div>
            <div class="trace-line red"></div>
        </div>

        <div class="trace-center">

            <div class="trace-eyebrow">
                DIGITAL FORENSICS // INVESTIGATION SYSTEM
            </div>

            <div class="trace-logo">
                TRACE<span class="trace-logo-x">-X</span>
            </div>

            <div class="trace-tagline">
                FOLLOW THE EVIDENCE
            </div>

            <div class="trace-status">
                INITIALIZING INVESTIGATION ENVIRONMENT
            </div>

            <div class="trace-status-bar">
                <div class="trace-status-fill"></div>
            </div>

        </div>

    </div>
    """

    st.html(html)