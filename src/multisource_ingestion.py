import json
import re
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "integration" / "person1_2_dataset"


def normalize_phone(value):
    if value is None:
        return None

    digits = re.sub(r"\D", "", str(value))

    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]

    return digits


def normalize_imei(value):
    if value is None:
        return None

    return re.sub(r"\D", "", str(value))


def normalize_upi(value):
    if value is None:
        return None

    return str(value).strip().lower()


def normalize_timestamp(value):
    if value is None:
        return None

    formats = [
        "%m/%d/%Y %H:%M:%S",
        "%d-%b-%Y %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(str(value), fmt).isoformat()
        except ValueError:
            continue

    return None


def load_json(filename):
    path = DATA_DIR / filename

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def build_relationships():
    devices = load_json("devices.json")
    cdr = load_json("cdr.json")
    ipdr = load_json("ipdr.json")
    transactions = load_json("transactions.json")

    relationships = []

    # Phone -> IMEI / IMSI
    for index, row in enumerate(devices, start=1):
        phone = normalize_phone(row.get("phone_number"))
        imei = normalize_imei(row.get("imei"))
        imsi = normalize_imei(row.get("imsi"))
        timestamp = normalize_timestamp(row.get("activation_date"))

        if phone and imei:
            relationships.append({
                "source": f"PHONE_{phone}",
                "target": f"IMEI_{imei}",
                "type": "USES_IMEI",
                "timestamp": timestamp,
                "evidence": f"devices.json:{index}",
            })

        if phone and imsi:
            relationships.append({
                "source": f"PHONE_{phone}",
                "target": f"IMSI_{imsi}",
                "type": "USES_IMSI",
                "timestamp": timestamp,
                "evidence": f"devices.json:{index}",
            })

    # Phone -> Phone from CDR
    for index, row in enumerate(cdr, start=1):
        caller = normalize_phone(row.get("caller_msisdn"))
        callee = normalize_phone(row.get("callee_msisdn"))
        timestamp = normalize_timestamp(row.get("call_time"))

        if caller and callee:
            relationships.append({
                "source": f"PHONE_{caller}",
                "target": f"PHONE_{callee}",
                "type": "CALLED",
                "timestamp": timestamp,
                "evidence": f"cdr.json:{index}",
                "duration_sec": row.get("duration_sec"),
                "cell_tower_id": row.get("cell_tower_id"),
            })

    # Phone -> IP from IPDR
    for index, row in enumerate(ipdr, start=1):
        phone = normalize_phone(row.get("msisdn"))
        ip = row.get("ip_address")
        timestamp = normalize_timestamp(row.get("session_start"))

        if phone and ip:
            relationships.append({
                "source": f"PHONE_{phone}",
                "target": f"IP_{ip}",
                "type": "CONNECTED_TO_IP",
                "timestamp": timestamp,
                "evidence": f"ipdr.json:{index}",
                "session_end": normalize_timestamp(row.get("session_end")),
            })

    # UPI -> UPI from successful transactions only
    for index, row in enumerate(transactions, start=1):
        sender = normalize_upi(row.get("sender_upi"))
        receiver = normalize_upi(row.get("receiver_upi"))
        status = str(row.get("status", "")).strip().upper()
        timestamp = normalize_timestamp(row.get("timestamp"))

        if sender and receiver and status == "SUCCESS":
            relationships.append({
                "source": f"UPI_{sender}",
                "target": f"UPI_{receiver}",
                "type": "TRANSFERRED_TO",
                "amount": row.get("amount"),
                "timestamp": timestamp,
                "evidence": f"transactions.json:{index}",
                "transaction_id": row.get("txn_id"),
                "status": status,
            })

    return relationships


def main():
    relationships = build_relationships()

    output_file = BASE_DIR / "output" / "multisource_relationships.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(relationships, file, indent=2)

    print(f"Generated {len(relationships)} relationships")
    print(f"Output: {output_file}")


if __name__ == "__main__":
    main()