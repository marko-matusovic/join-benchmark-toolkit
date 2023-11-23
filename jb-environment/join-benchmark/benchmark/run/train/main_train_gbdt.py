from typing import NamedTuple, TypeAlias
from sklearn.ensemble import GradientBoostingRegressor
import pandas as pd
import pickle as pkl
import json
import ast

# ======== CONSTANTS =============================================

JOINS_IN_BLOCK = 4

# ======== TYPES =================================================


class TableFeatures(NamedTuple):
    length: float
    unique: float
    row_size: float
    cache_age: float


class CrossFeatures(NamedTuple):
    selectivity: float


class Features(NamedTuple):
    table_1: TableFeatures
    table_2: TableFeatures
    cross: CrossFeatures


# The features dictionary has 3 levels:
#   1. by query name
#   2. by join order
#   3. by join id
AllFeatures: TypeAlias = dict[str, dict[str, dict[str, Features]]]


class Measurements(NamedTuple):
    parsing: float
    overhead: float
    filters: list[float]
    joins: list[float]


# The measurements dictionary has 2 levels:
#   1. by query name
#   2. by join order
AllMeasurements: TypeAlias = dict[str, dict[str, Measurements]]


# ======== MAIN ==================================================


# TODO: support multiple db_sets
def main(db_set: str, training_set: int, res_path: str | None = None):
    if res_path == None:
        res_path = "./results"

    # create a gradient boosting regressor
    model = GradientBoostingRegressor(
        n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0
    )

    (features, measurements) = load_all(db_set, training_set, res_path)

    (X, y) = prepare_data(features, measurements)

    # train the model
    model.fit(X, y)

    dbs = "".join(f"_{db}" for db in [db_set])
    with open(
        f"{res_path}/models/gbdt/set_{training_set}{dbs}.pickle", "wb"
    ) as file_out:
        pkl.dump(model, file_out)


def prepare_data(
    features: AllFeatures, measurements: AllMeasurements
) -> tuple[list[list[float]], list[float]]:
    X: list[list[float]] = []
    Y: list[float] = []
    for query in set(features.keys()) & set(measurements.keys()):
        for jo in set(features[query].keys()) & set(measurements[query].keys()):
            fs = features[query][jo]
            ms = measurements[query][jo]

            encoded_fs = [encode_feature(fs[j]) for j in jo.split(",")]
            encoded_ms = ms.joins

            assert len(encoded_fs) == len(encoded_ms)

            # Fold encoded fs and ms to blocks of N and fill the end with 0s
            for j in range(0, len(encoded_fs), JOINS_IN_BLOCK):
                x: list[float] = []
                y = 0.0
                for i in range(j, j + JOINS_IN_BLOCK):
                    if i < len(encoded_fs):
                        x += encoded_fs[i]
                        y += encoded_ms[i]
                    else:
                        x += encode_feature()
                        y += 0.0

                X.append(x)
                Y.append(y)

    return (X, Y)


def encode_feature(features: Features | None = None) -> list[float]:
    if features == None:
        return [0.0] * 9
    else:
        return [
            features.table_1.length,
            features.table_1.unique,
            features.table_1.row_size,
            features.table_1.cache_age,
            features.table_2.length,
            features.table_2.unique,
            features.table_2.row_size,
            features.table_2.cache_age,
            features.cross.selectivity,
        ]


def load_all(
    db_set: str, training_set: int, res_path: str
) -> tuple[AllFeatures, AllMeasurements]:
    features = load_features(db_set, training_set, res_path)
    measurements = load_measurements(db_set, training_set, res_path)

    # Find the intersection
    # Assuming features and measurements are your dictionaries
    common_keys = set(features.keys()) & set(measurements.keys())

    filtered_features = {k: features[k] for k in common_keys}
    filtered_measurements = {k: measurements[k] for k in common_keys}

    for key in common_keys:
        sub_common_keys = set(features[key].keys()) & set(measurements[key].keys())
        filtered_features[key] = {k: features[key][k] for k in sub_common_keys}
        filtered_measurements[key] = {k: measurements[key][k] for k in sub_common_keys}

    return (filtered_features, filtered_measurements)


def load_features(db_set: str, training_set: int, res_path: str) -> AllFeatures:
    # Read the CSV file
    file = f"{res_path}/training_data/{db_set}/set_{training_set}_features.csv"
    df = pd.read_csv(file, sep=";", comment="#")

    # Initialize an empty dictionary for AllFeatures
    all_features: AllFeatures = {}

    # Iterate over each row in the dataframe
    for _index, row in df.iterrows():
        # Parse the JSON strings into dictionaries
        features_1 = json.loads(row["FEATURES_1"])
        features_2 = json.loads(row["FEATURES_2"])
        features_mix = json.loads(row["FEATURES_MIX"])

        # Create TableFeatures namedtuples from the dictionaries
        table_1 = TableFeatures(**features_1)
        table_2 = TableFeatures(**features_2)
        cross = CrossFeatures(**features_mix)

        # Create a Features namedtuple
        features = Features(table_1, table_2, cross)

        # Add the Features namedtuple to the AllFeatures dictionary
        n1 = str(row["DB_SET/QUERY"])
        n2 = str(row["JOIN_PERMUTATION"])
        n3 = str(row["JOIN_ID"])

        if n1 not in all_features:
            all_features[n1] = {}
        if n2 not in all_features[n1]:
            all_features[n1][n2] = {}

        all_features[n1][n2][n3] = features

    return all_features


def avg_list(lst):
    if type(lst[lst.index[0]]) == float:
        return [sum(lst) / len(lst)]
    return [sum(group) / len(group) for group in zip(*lst)]


def load_measurements(db_set: str, training_set: int, res_path: str) -> AllMeasurements:
    # Read the CSV file
    file = f"{res_path}/training_data/{db_set}/set_{training_set}_measurement.csv"
    df = pd.read_csv(file, sep=";", comment="#")

    # Filter the dataframe by EXIT_CODE == 200
    df = df[df["EXIT_CODE"] == 200]

    # Convert list strings into actual lists
    df["FILTERS"] = df["FILTERS"].apply(ast.literal_eval)
    df["JOINS"] = df["JOINS"].apply(ast.literal_eval)

    # Group by DB_SET/QUERY and JOIN_PERMUTATION and calculate averages
    df = (
        df.groupby(["DB_SET/QUERY", "JOIN_PERMUTATION"])
        .agg(
            {
                "PARSING": "mean",
                "OVERHEAD": "mean",
                "FILTERS": avg_list,
                "JOINS": avg_list,
            }
        )
        .reset_index()
    )

    # Initialize an empty dictionary for AllMeasurements
    all_measurements: AllMeasurements = {}

    # Iterate over each row in the dataframe
    for _index, row in df.iterrows():
        # Create a Measurements namedtuple
        measurements = Measurements(
            row["PARSING"], row["OVERHEAD"], row["FILTERS"], row["JOINS"]
        )

        # Add the Measurements namedtuple to the AllMeasurements dictionary
        n1 = str(row["DB_SET/QUERY"])
        n2 = str(row["JOIN_PERMUTATION"])

        if n1 not in all_measurements:
            all_measurements[n1] = {}

        all_measurements[n1][n2] = measurements

    return all_measurements
