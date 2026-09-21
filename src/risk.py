import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

ALERTS_FILE = BASE_DIR / "output" / "alerts.json"
ML_FILE = BASE_DIR / "output" / "ml_anomalies.json"

OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "risk.json"


RISK_WEIGHTS = {
    "RAPID_ONWARD_TRANSFER": 30,
    "HIGH_TRANSACTION_VELOCITY": 20,
    "SHARED_DEVICE": 15,
    "REPEATED_BENEFICIARY": 15
}


MAX_ML_POINTS = 20


def load_alerts():
    with open(ALERTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def load_ml_anomalies():
    """
    Load ML anomaly results.

    If the ML output does not exist, return an empty list
    so the rule-based risk system can still work.
    """

    if not ML_FILE.exists():
        print("Warning: ml_anomalies.json not found.")
        return []

    with open(ML_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def calculate_ml_points(anomaly_score):
    """
    Convert the Isolation Forest anomaly score into
    a maximum of 20 risk points.

    Isolation Forest score is approximately in the
    range 0 to 1, with higher values indicating
    stronger anomaly behavior.
    """

    score = max(0.0, min(float(anomaly_score), 1.0))

    return round(score * MAX_ML_POINTS, 2)


def calculate_risk(alerts, ml_anomalies):
    """
    Combine rule-based alerts and ML anomaly scores.
    """

    entity_scores = {}
    entity_alerts = {}

    for alert in alerts:

        entity = alert["entity"]
        alert_type = alert["type"]

        points = RISK_WEIGHTS.get(
            alert_type,
            10
        )

        if entity not in entity_scores:
            entity_scores[entity] = 0
            entity_alerts[entity] = []

        entity_scores[entity] += points

        entity_alerts[entity].append(alert)


    ml_scores = {}

    for result in ml_anomalies:

        entity = result["entity"]

        anomaly_score = result.get(
            "anomaly_score",
            0
        )

        ml_points = calculate_ml_points(
            anomaly_score
        )

        ml_scores[entity] = {
            "anomaly_score": anomaly_score,
            "ml_risk_points": ml_points,
            "ml_anomaly": result.get(
                "anomaly",
                False
            )
        }


    all_entities = set(entity_scores.keys())

    all_entities.update(
        ml_scores.keys()
    )

    results = []

    for entity in all_entities:

        rule_score = entity_scores.get(
            entity,
            0
        )

        rule_alerts = entity_alerts.get(
            entity,
            []
        )

        ml_data = ml_scores.get(
            entity,
            {
                "anomaly_score": 0,
                "ml_risk_points": 0,
                "ml_anomaly": False
            }
        )

        ml_points = ml_data[
            "ml_risk_points"
        ]

        # Combined score
        final_score = min(
            rule_score + ml_points,
            100
        )

        # Risk level
        if final_score >= 70:
            level = "HIGH"

        elif final_score >= 40:
            level = "MEDIUM"

        else:
            level = "LOW"

        results.append({

            "entity": entity,

            "risk_score": final_score,

            "risk_level": level,

            # Explainable breakdown
            "rule_based_score": rule_score,

            "ml_anomaly_score": ml_data[
                "anomaly_score"
            ],

            "ml_risk_points": ml_points,

            "ml_anomaly": ml_data[
                "ml_anomaly"
            ],

            "alert_count": len(
                rule_alerts
            ),

            "alert_types": [
                alert["type"]
                for alert in rule_alerts
            ],

            "evidence": [
                evidence
                for alert in rule_alerts
                for evidence in alert.get(
                    "evidence",
                    []
                )
            ]
        })

    # Highest risk first
    results.sort(
        key=lambda item: item["risk_score"],
        reverse=True
    )

    return results


def export_risk(risk_results):

    OUTPUT_DIR.mkdir(
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            risk_results,
            file,
            indent=2
        )

    print(
        f"Risk report exported to: {OUTPUT_FILE}"
    )


def main():

    alerts = load_alerts()

    ml_anomalies = load_ml_anomalies()

    risk_results = calculate_risk(
        alerts,
        ml_anomalies
    )

    print("\nRisk Analysis:")
    print("-" * 70)

    for result in risk_results:

        print(
            f'{result["entity"]} | '
            f'Final: {result["risk_score"]} | '
            f'Rule: {result["rule_based_score"]} | '
            f'ML: {result["ml_risk_points"]} | '
            f'Level: {result["risk_level"]}'
        )

    export_risk(
        risk_results
    )


if __name__ == "__main__":
    main()