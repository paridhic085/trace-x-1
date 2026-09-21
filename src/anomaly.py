import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "sample.json"
MULTISOURCE_INPUT_FILE = BASE_DIR / "output" / "multisource_relationships.json"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "alerts.json"


def load_relationships():
    """Load integrated relationships when available."""
    input_file = (
        MULTISOURCE_INPUT_FILE
        if MULTISOURCE_INPUT_FILE.exists()
        else INPUT_FILE
    )

    with open(input_file, "r", encoding="utf-8") as file:
        return json.load(file)


def parse_timestamp(timestamp):
    return datetime.fromisoformat(timestamp)


def detect_rapid_onward_transfers(relationships):
    alerts = []

    transfers = [
        r for r in relationships
        if r.get("type") == "TRANSFERRED_TO"
    ]

    for incoming in transfers:
        for outgoing in transfers:
            if incoming["target"] != outgoing["source"]:
                continue

            incoming_time = parse_timestamp(incoming["timestamp"])
            outgoing_time = parse_timestamp(outgoing["timestamp"])

            difference = (outgoing_time - incoming_time).total_seconds()

            if 0 <= difference <= 300:
                alerts.append({
                    "id": f"ALERT_{len(alerts) + 1:03d}",
                    "type": "RAPID_ONWARD_TRANSFER",
                    "entity": incoming["target"],
                    "severity": "high",
                    "reason": (
                        f'₹{incoming.get("amount", 0):,} received and '
                        f'₹{outgoing.get("amount", 0):,} transferred '
                        f'within {int(difference)} seconds'
                    ),
                    "evidence": [
                        incoming.get("evidence"),
                        outgoing.get("evidence")
                    ]
                })

    return alerts


def detect_shared_devices(relationships, start_id=1):
    alerts = []

    device_users = {}

    for relation in relationships:
        if relation.get("type") != "USES_IMEI":
            continue

        phone = relation["source"]
        imei = relation["target"]

        if imei not in device_users:
            device_users[imei] = []

        if phone not in device_users[imei]:
            device_users[imei].append(phone)

    for imei, phones in device_users.items():
        if len(phones) > 1:
            alerts.append({
                "id": f"ALERT_{start_id + len(alerts):03d}",
                "type": "SHARED_DEVICE",
                "entity": imei,
                "severity": "medium",
                "reason": (
                    f'{imei} is associated with multiple phones: '
                    f'{", ".join(phones)}'
                ),
                "evidence": [
                    relation.get("evidence")
                    for relation in relationships
                    if relation.get("type") == "USES_IMEI"
                    and relation.get("target") == imei
                ]
            })

    return alerts


def detect_high_transaction_velocity(relationships, start_id=1):
    alerts = []

    transfers = [
        r for r in relationships
        if r.get("type") == "TRANSFERRED_TO"
    ]

    entities = set()

    for transfer in transfers:
        entities.add(transfer["source"])
        entities.add(transfer["target"])

    for entity in entities:
        entity_transfers = [
            r for r in transfers
            if r["source"] == entity or r["target"] == entity
        ]

        entity_transfers.sort(
            key=lambda r: parse_timestamp(r["timestamp"])
        )

        if len(entity_transfers) >= 3:
            first_time = parse_timestamp(
                entity_transfers[0]["timestamp"]
            )
            last_time = parse_timestamp(
                entity_transfers[-1]["timestamp"]
            )

            difference = (last_time - first_time).total_seconds()

            if difference <= 600:
                alerts.append({
                    "id": f"ALERT_{start_id + len(alerts):03d}",
                    "type": "HIGH_TRANSACTION_VELOCITY",
                    "entity": entity,
                    "severity": "medium",
                    "reason": (
                        f'{len(entity_transfers)} transactions involving '
                        f'{entity} within {int(difference)} seconds'
                    ),
                    "evidence": [
                        r.get("evidence")
                        for r in entity_transfers
                    ]
                })

    return alerts


def detect_repeated_beneficiary(relationships, start_id=1):
    alerts = []

    transfers = [
        r for r in relationships
        if r.get("type") == "TRANSFERRED_TO"
    ]

    destination_counts = {}

    for transfer in transfers:
        target = transfer["target"]

        if target not in destination_counts:
            destination_counts[target] = []

        destination_counts[target].append(transfer)

    for target, transactions in destination_counts.items():
        if len(transactions) >= 2:
            alerts.append({
                "id": f"ALERT_{start_id + len(alerts):03d}",
                "type": "REPEATED_BENEFICIARY",
                "entity": target,
                "severity": "medium",
                "reason": (
                    f'{target} received {len(transactions)} '
                    f'transfers'
                ),
                "evidence": [
                    r.get("evidence")
                    for r in transactions
                ]
            })

    return alerts


def detect_anomalies(relationships):
    alerts = []

    rapid_alerts = detect_rapid_onward_transfers(relationships)
    alerts.extend(rapid_alerts)

    next_id = len(alerts) + 1

    shared_alerts = detect_shared_devices(
        relationships,
        start_id=next_id
    )
    alerts.extend(shared_alerts)

    next_id = len(alerts) + 1

    velocity_alerts = detect_high_transaction_velocity(
        relationships,
        start_id=next_id
    )
    alerts.extend(velocity_alerts)

    next_id = len(alerts) + 1

    beneficiary_alerts = detect_repeated_beneficiary(
        relationships,
        start_id=next_id
    )
    alerts.extend(beneficiary_alerts)

    return alerts


def export_alerts(alerts):
    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(alerts, file, indent=2)

    print(f"Alerts exported to: {OUTPUT_FILE}")


def main():
    relationships = load_relationships()

    alerts = detect_anomalies(relationships)

    print("\nDetected Anomalies:")
    print("-" * 60)

    for alert in alerts:
        print(
            f'{alert["id"]} | '
            f'{alert["type"]} | '
            f'{alert["entity"]} | '
            f'{alert["severity"]}'
        )
        print(f'  Reason: {alert["reason"]}')

    print(f"\nTotal alerts: {len(alerts)}")

    export_alerts(alerts)


if __name__ == "__main__":
    main()