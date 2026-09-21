import json
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "sample.json"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "timeline.json"


def load_relationships():
    """Load relationships from the sample data file."""
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def build_timeline(relationships):
    """Sort relationships chronologically and create timeline events."""

    timeline = []

    for relation in relationships:
        timeline.append({
            "timestamp": relation.get("timestamp"),
            "event_type": relation.get("type"),
            "source": relation.get("source"),
            "target": relation.get("target"),
            "amount": relation.get("amount"),
            "evidence": relation.get("evidence")
        })

    timeline.sort(
        key=lambda event: datetime.strptime(
            event["timestamp"],
            "%Y-%m-%d %H:%M:%S"
        )
    )

    return timeline


def export_timeline(timeline):
    """Save the timeline as JSON."""

    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(timeline, file, indent=2)

    print(f"Timeline exported to: {OUTPUT_FILE}")


def main():
    relationships = load_relationships()

    timeline = build_timeline(relationships)

    print("\nInvestigation Timeline:")
    print("-" * 60)

    for event in timeline:
        amount = event["amount"]

        if amount is not None:
            print(
                f'{event["timestamp"]} | '
                f'{event["source"]} → {event["target"]} | '
                f'₹{amount}'
            )
        else:
            print(
                f'{event["timestamp"]} | '
                f'{event["source"]} → {event["target"]} | '
                f'{event["event_type"]}'
            )

    export_timeline(timeline)


if __name__ == "__main__":
    main()