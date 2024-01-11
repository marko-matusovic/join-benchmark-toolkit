import json

import pandas as pd
from benchmark.tools.ml.types import DataFeatures, TableFeatures, CrossFeatures, AllDataFeatures


def load_data_features(db_set: str, training_set: int, res_path: str) -> AllDataFeatures:
    # Read the CSV file
    file = f"{res_path}/training_data/{db_set}/set_{training_set}_features.csv"
    df = pd.read_csv(file, sep=";", comment="#")

    # Initialize an empty dictionary for AllFeatures
    all_features: AllDataFeatures = {}

    # Iterate over each row in the dataframe
    for _index, row in df.iterrows():
        # Parse the JSON strings into dictionaries
        features = json.loads(row["FEATURES"])

        # Create a Features namedtuple
        features = DataFeatures(**features)

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


def load_hw_features(hw_name, res_path) -> list[float]:
    # Load the CSV file
    file_path = f"{res_path}/training_data/features_hw_{hw_name}.csv"
    df = pd.read_csv(file_path, delimiter=";", comment="#")

    # Group by 'DB_SET/QUERY' and calculate the mean
    grouped_df = df.groupby("DB_SET/QUERY")

    overhead_mean = grouped_df["OVERHEAD"].mean()
    joins_mean = grouped_df["JOINS"].mean()
    return [
        float(x)
        for x in [
            overhead_mean["query_cp_sm"],
            overhead_mean["query_cp_md"],
            overhead_mean["query_cp_lg"],
            joins_mean["query_11_sm"],
            joins_mean["query_11_md"],
            joins_mean["query_11_lg"],
            joins_mean["query_1n_sm"],
            joins_mean["query_1n_md"],
            joins_mean["query_1n_lg"],
            joins_mean["query_nn_sm"],
            joins_mean["query_nn_md"],
            joins_mean["query_nn_lg"],
        ]
    ]
