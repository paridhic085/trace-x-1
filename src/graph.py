import json
import networkx as nx
from pathlib import Path


# File locations
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "sample.json"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "graph.json"


def load_relationships():
    """Load relationship data from the JSON input file."""
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def build_graph(relationships):
    """Build a NetworkX investigation graph."""

    graph = nx.MultiDiGraph()

    for relation in relationships:
        source = relation["source"]
        target = relation["target"]

        # Add nodes
        graph.add_node(
            source,
            id=source,
            type=source.split("_")[0]
        )

        graph.add_node(
            target,
            id=target,
            type=target.split("_")[0]
        )

        # Add relationship
        graph.add_edge(
            source,
            target,
            type=relation["type"],
            amount=relation.get("amount"),
            timestamp=relation.get("timestamp"),
            evidence=relation.get("evidence")
        )

    return graph


def export_graph(graph):
    """Export the graph into a JSON file."""

    OUTPUT_DIR.mkdir(exist_ok=True)

    graph_data = {
        "nodes": [],
        "edges": []
    }

    # Export nodes
    for node_id, attributes in graph.nodes(data=True):
        graph_data["nodes"].append({
            "id": node_id,
            "type": attributes.get("type")
        })

    # Export edges
    for source, target, attributes in graph.edges(data=True):
        graph_data["edges"].append({
            "source": source,
            "target": target,
            "type": attributes.get("type"),
            "amount": attributes.get("amount"),
            "timestamp": attributes.get("timestamp"),
            "evidence": attributes.get("evidence")
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(graph_data, file, indent=2)

    print(f"Graph exported to: {OUTPUT_FILE}")


def get_neighbors(graph, entity_id):
    """Return entities directly connected to an entity."""

    if entity_id not in graph:
        return []

    neighbors = set()

    for neighbor in graph.successors(entity_id):
        neighbors.add(neighbor)

    for neighbor in graph.predecessors(entity_id):
        neighbors.add(neighbor)

    return sorted(neighbors)


def find_path(graph, source, target):
    """Find a path between two entities."""

    try:
        return nx.shortest_path(graph, source, target)
    except nx.NetworkXNoPath:
        return []
    except nx.NodeNotFound:
        return []

def get_entity(graph, entity_id):
    """Return basic information about an entity."""
    if entity_id not in graph:
        return None

    attributes = graph.nodes[entity_id]

    return {
        "id": entity_id,
        "type": attributes.get("type")
    }

def get_edge_details(graph, source, target):
    """Return all relationships between two entities."""
    if source not in graph or target not in graph:
        return []

    relationships = []

    edge_data = graph.get_edge_data(source, target)

    if not edge_data:
        return []

    for attributes in edge_data.values():
        relationships.append({
            "type": attributes.get("type"),
            "amount": attributes.get("amount"),
            "timestamp": attributes.get("timestamp"),
            "evidence": attributes.get("evidence")
        })

    return relationships


def main():
    relationships = load_relationships()

    graph = build_graph(relationships)

    print(f"Nodes: {graph.number_of_nodes()}")
    print(f"Relationships: {graph.number_of_edges()}")

    # Example investigation
    print("\nNeighbors of UPI_001:")
    print(get_neighbors(graph, "UPI_001"))

    print("\nPath from VICTIM_001 to UPI_003:")
    print(find_path(graph, "VICTIM_001", "UPI_003"))

    export_graph(graph)


if __name__ == "__main__":
    main()
    