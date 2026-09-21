import json
import math
import random
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "sample.json"
MULTISOURCE_INPUT_FILE = BASE_DIR / "output" / "multisource_relationships.json"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_FILE = OUTPUT_DIR / "ml_anomalies.json"




def load_relationships():
    input_file = (
        MULTISOURCE_INPUT_FILE
        if MULTISOURCE_INPUT_FILE.exists()
        else INPUT_FILE
    )

    with open(input_file, "r", encoding="utf-8") as file:
        return json.load(file)



def build_features(relationships):
    """
    Convert relationship data into numerical behavioral
    features for each entity.
    """

    entities = {}

    for relation in relationships:
        source = relation["source"]
        target = relation["target"]

        for entity in [source, target]:
            if entity not in entities:
                entities[entity] = {
                    "transaction_count": 0,
                    "total_amount": 0.0,
                    "outgoing_count": 0,
                    "incoming_count": 0,
                }

        if relation.get("type") == "TRANSFERRED_TO":
            amount = relation.get("amount") or 0

            entities[source]["transaction_count"] += 1
            entities[target]["transaction_count"] += 1

            entities[source]["total_amount"] += amount
            entities[target]["total_amount"] += amount

            entities[source]["outgoing_count"] += 1
            entities[target]["incoming_count"] += 1

    return entities




def harmonic_number(n):
    """Calculate H(n)."""

    if n <= 0:
        return 0.0

    return sum(1.0 / i for i in range(1, n + 1))


def average_path_length(n):
    """
    Expected path length adjustment used by Isolation Forest.

    c(n) = 2H(n-1) - 2(n-1)/n
    """

    if n <= 1:
        return 0.0

    if n == 2:
        return 1.0

    return (
        2.0 * harmonic_number(n - 1)
        - (2.0 * (n - 1) / n)
    )



class IsolationTree:
    """
    One random isolation tree.

    Each split:
    1. Randomly selects a feature.
    2. Randomly selects a split value between the
       minimum and maximum values of that feature.
    """

    def __init__(self, max_depth, random_generator):
        self.max_depth = max_depth
        self.random = random_generator

        self.feature_index = None
        self.split_value = None

        self.left = None
        self.right = None

        self.size = 0
        self.is_leaf = False

    def fit(self, data, depth=0):

        self.size = len(data)

        # Stop conditions
        if (
            len(data) <= 1
            or depth >= self.max_depth
            or all(row == data[0] for row in data)
        ):
            self.is_leaf = True
            return

        number_of_features = len(data[0])

        # Random feature selection
        feature_index = self.random.randrange(number_of_features)

        values = [
            row[feature_index]
            for row in data
        ]

        minimum = min(values)
        maximum = max(values)

        # Cannot split if all values are identical
        if minimum == maximum:
            self.is_leaf = True
            return

        # Random split between min and max
        split_value = self.random.uniform(
            minimum,
            maximum
        )

        left_data = [
            row
            for row in data
            if row[feature_index] < split_value
        ]

        right_data = [
            row
            for row in data
            if row[feature_index] >= split_value
        ]

        # Safety check
        if not left_data or not right_data:
            self.is_leaf = True
            return

        self.feature_index = feature_index
        self.split_value = split_value

        self.left = IsolationTree(
            self.max_depth,
            self.random
        )

        self.right = IsolationTree(
            self.max_depth,
            self.random
        )

        self.left.fit(left_data, depth + 1)
        self.right.fit(right_data, depth + 1)

    def path_length(self, row, depth=0):

        if self.is_leaf:
            return depth + average_path_length(self.size)

        if row[self.feature_index] < self.split_value:
            return self.left.path_length(
                row,
                depth + 1
            )

        return self.right.path_length(
            row,
            depth + 1
        )



class IsolationForest:
    """
    A lightweight implementation of the Isolation Forest
    algorithm.

    No external ML libraries are required.
    """

    def __init__(
        self,
        n_trees=100,
        sample_size=256,
        random_state=42
    ):

        self.n_trees = n_trees
        self.sample_size = sample_size
        self.random = random.Random(random_state)

        self.trees = []
        self.training_size = 0

    def fit(self, data):

        self.training_size = len(data)

        if not data:
            return self

        actual_sample_size = min(
            self.sample_size,
            len(data)
        )

        max_depth = math.ceil(
            math.log2(actual_sample_size)
        )

        for _ in range(self.n_trees):

            # Random subsample
            if len(data) > actual_sample_size:
                sample = self.random.sample(
                    data,
                    actual_sample_size
                )
            else:
                sample = list(data)

            tree = IsolationTree(
                max_depth=max_depth,
                random_generator=self.random
            )

            tree.fit(sample)

            self.trees.append(tree)

        return self

    def anomaly_score(self, row):

        if not self.trees:
            return 0.0

        path_lengths = [
            tree.path_length(row)
            for tree in self.trees
        ]

        average_path = (
            sum(path_lengths)
            / len(path_lengths)
        )

        normalizer = average_path_length(
            self.training_size
        )

        if normalizer == 0:
            return 0.0

        score = 2 ** (
            -average_path / normalizer
        )

        return score



def detect_anomalies(features):

    entity_ids = list(features.keys())

    if not entity_ids:
        return []

    feature_names = [
        "transaction_count",
        "total_amount",
        "outgoing_count",
        "incoming_count",
    ]

    feature_matrix = []

    for entity_id in entity_ids:

        entity = features[entity_id]

        row = [
            entity[name]
            for name in feature_names
        ]

        feature_matrix.append(row)

    # Create and train the Isolation Forest
    model = IsolationForest(
        n_trees=100,
        sample_size=256,
        random_state=42
    )

    model.fit(feature_matrix)

    scored_entities = []

    for index, entity_id in enumerate(entity_ids):

        score = model.anomaly_score(
            feature_matrix[index]
        )

        scored_entities.append({
            "entity": entity_id,
            "anomaly_score": round(score, 4),
            "features": features[entity_id]
        })

    # Higher score = more unusual.
    #
    # We mark the top 20% as anomalous for the dashboard.
    # The actual continuous anomaly_score is preserved.
    scored_entities.sort(
        key=lambda item: item["anomaly_score"],
        reverse=True
    )

    anomaly_count = max(
        1,
        math.ceil(len(scored_entities) * 0.20)
    )

    for index, result in enumerate(scored_entities):

        result["anomaly"] = index < anomaly_count

    return scored_entities


# ---------------------------------------------------------
# SAVE RESULTS
# ---------------------------------------------------------

def save_results(results):

    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=2
        )

    print(
        f"ML anomaly results exported to: {OUTPUT_FILE}"
    )


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    relationships = load_relationships()

    features = build_features(
        relationships
    )

    results = detect_anomalies(
        features
    )

    save_results(results)

    print(
        f"Analysed {len(results)} entities."
    )

    print("\nMost anomalous entities:")

    for result in results[:5]:

        print(
            f"{result['entity']}: "
            f"{result['anomaly_score']}"
        )


if __name__ == "__main__":
    main()