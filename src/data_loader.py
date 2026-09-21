import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
DATA_DIR = BASE_DIR / "data"


def load_json(filename, folder=OUTPUT_DIR):
    path = folder / filename

    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_analysis_data():
    return {
        "alerts": load_json("alerts.json"),
        "graph": load_json("graph.json"),
        "ml_anomalies": load_json("ml_anomalies.json"),
        "risk": load_json("risk.json"),
        "timeline": load_json("timeline.json"),
        "sample": load_json("sample.json", DATA_DIR),
    }