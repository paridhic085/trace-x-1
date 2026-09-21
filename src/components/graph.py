import streamlit as st


def render_graph_header(entity_count, relationship_count):

    html = f"""
    <div class="trace-graph-header">

        <div class="graph-header-left">

            <div class="graph-eyebrow">
                RELATIONSHIP INTELLIGENCE
            </div>

            <div class="graph-title">
                Investigation Network
            </div>

            <div class="graph-subtitle">
                Correlated entities across telecom, network and financial evidence
            </div>

        </div>

        <div class="graph-stats">

            <div class="graph-stat">
                <span class="graph-stat-value">
                    {entity_count}
                </span>

                <span class="graph-stat-label">
                    ENTITIES
                </span>
            </div>

            <div class="graph-stat-divider"></div>

            <div class="graph-stat">
                <span class="graph-stat-value">
                    {relationship_count}
                </span>

                <span class="graph-stat-label">
                    LINKS
                </span>
            </div>

        </div>

    </div>
    """

    st.html(html)


def get_entity_color(entity_type):

    colors = {
        "PHONE": "#4da3ff",
        "IMEI": "#a875ff",
        "IP": "#ffb84d",
        "UPI": "#42d6a4",
    }

    return colors.get(entity_type, "#8fa3bf")


def get_entity_border(entity_type):

    borders = {
        "PHONE": "#7dc4ff",
        "IMEI": "#c49aff",
        "IP": "#ffd27a",
        "UPI": "#7ff2cb",
    }

    return borders.get(entity_type, "#b7c3d4")


def get_entity_size(entity_type):

    sizes = {
        "UPI": 28,
        "PHONE": 24,
        "IMEI": 22,
        "IP": 18,
    }

    return sizes.get(entity_type, 20)


def render_graph_legend():

    html = """
    <div class="trace-graph-legend">

        <div class="legend-title">
            ENTITY TYPES
        </div>

        <div class="legend-items">

            <div class="legend-item">
                <span class="legend-dot legend-phone"></span>
                <span>PHONE</span>
            </div>

            <div class="legend-item">
                <span class="legend-dot legend-imei"></span>
                <span>IMEI</span>
            </div>

            <div class="legend-item">
                <span class="legend-dot legend-ip"></span>
                <span>IP</span>
            </div>

            <div class="legend-item">
                <span class="legend-dot legend-upi"></span>
                <span>UPI</span>
            </div>

            <div class="legend-divider"></div>

            <div class="legend-item legend-flow">
                <span class="legend-line"></span>
                <span>FUND FLOW</span>
            </div>

        </div>

    </div>
    """

    st.html(html)