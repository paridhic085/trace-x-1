import json
import networkx as nx
from pathlib import Path


# File locations
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "sample.json"
MULTISOURCE_INPUT_FILE = BASE_DIR / "output" / "multisource_relationships.json"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "graph.json"


def load_relationships():
    """Load the original sample relationship data."""
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def load_multisource_relationships():
    """Load normalized relationships from Person 1 and 2 datasets."""
    with open(MULTISOURCE_INPUT_FILE, "r", encoding="utf-8") as file:
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

        # Preserve all relationship metadata.
        edge_attributes = {
            key: value
            for key, value in relation.items()
            if key not in {"source", "target"}
        }

        graph.add_edge(
            source,
            target,
            **edge_attributes
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
        edge = {
            "source": source,
            "target": target
        }

        # Preserve every relationship field.
        edge.update(attributes)

        graph_data["edges"].append(edge)

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
        relationships.append(dict(attributes))

    return relationships


def main():
    # Use the integrated multi-source data when available.
    if MULTISOURCE_INPUT_FILE.exists():
        relationships = load_multisource_relationships()
        print("Using multi-source integrated relationships.")
    else:
        relationships = load_relationships()
        print("Using original sample relationships.")

    graph = build_graph(relationships)

    print(f"Nodes: {graph.number_of_nodes()}")
    print(f"Relationships: {graph.number_of_edges()}")

    export_graph(graph)


if __name__ == "__main__":
    main()