import json
from pathlib import Path

from src.graph import (
    load_relationships,
    build_graph,
    get_neighbors,
    find_path,
    get_entity,
    get_edge_details,
)


def test_relationships_load():
    relationships = load_relationships()

    assert len(relationships) > 0
    assert "source" in relationships[0]
    assert "target" in relationships[0]


def test_graph_builds():
    relationships = load_relationships()
    graph = build_graph(relationships)

    assert graph.number_of_nodes() > 0
    assert graph.number_of_edges() > 0


def test_upi_neighbors():
    relationships = load_relationships()
    graph = build_graph(relationships)

    neighbors = get_neighbors(graph, "UPI_001")

    assert "VICTIM_001" in neighbors
    assert "UPI_002" in neighbors
    assert "PHONE_001" in neighbors


def test_investigation_path():
    relationships = load_relationships()
    graph = build_graph(relationships)

    path = find_path(
        graph,
        "VICTIM_001",
        "UPI_003"
    )

    assert path == [
        "VICTIM_001",
        "UPI_001",
        "UPI_002",
        "UPI_003"
    ]


def test_get_entity():
    relationships = load_relationships()
    graph = build_graph(relationships)

    entity = get_entity(graph, "UPI_001")

    assert entity is not None
    assert entity["id"] == "UPI_001"
    assert entity["type"] == "UPI"


def test_get_edge_details():
    relationships = load_relationships()
    graph = build_graph(relationships)

    details = get_edge_details(
        graph,
        "UPI_001",
        "UPI_002"
    )

    assert len(details) == 1
    assert details[0]["type"] == "TRANSFERRED"
    assert details[0]["amount"] == 48000
    assert details[0]["evidence"] == "transactions.csv:2"