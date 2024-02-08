import json
import math

import pandas as pd
from benchmark.tools.ml.types import (
    DataFeatures,
    TableFeatures,
    CrossFeatures,
    AllDataFeatures,
)


def load_data_features(
    db_set: str, training_set: int, res_path: str, normalize=False
) -> AllDataFeatures:
    # Read the CSV file
    file = f"{res_path}/training_data/{db_set}/set_{training_set}_features_data.csv"
    df = pd.read_csv(file, sep=";", comment="#")

    # Drop rows where "FEATURES" is null
    df = (
        df.groupby(["DB_SET/QUERY", "JOIN_PERMUTATION"])
        .apply(lambda x: x.dropna(subset=["FEATURES"]))
        .reset_index(drop=True)
    )

    # Initialize an empty dictionary for AllFeatures
    all_features: AllDataFeatures = {}

    # Iterate over each row in the dataframe
    for _index, row in df.iterrows():
        # Parse the JSON strings into dictionaries
        if row["FEATURES"] == None or row["FEATURES"] == math.nan:
            continue
        features = json.loads(row["FEATURES"])

        # Create a Features namedtuple
        # features = DataFeatures(*features[0])
        features = DataFeatures(
            TableFeatures(*features[0]),
            TableFeatures(*features[1]),
            CrossFeatures(*features[2]),
        )

        # Add the Features namedtuple to the AllFeatures dictionary
        n1 = str(row["DB_SET/QUERY"])
        n2 = str(row["JOIN_PERMUTATION"])
        n3 = str(int(row["JOIN_ID"]))

        if n1 not in all_features:
            all_features[n1] = {}
        if n2 not in all_features[n1]:
            all_features[n1][n2] = {}

        all_features[n1][n2][n3] = features

    # # Get rid of partially complete features
    # for db_set in list(all_features.keys()):
    #     for jo in list(all_features[db_set].keys()):
    #         if jo.count(",") + 1 != len(all_features[db_set][jo]):
    #             del all_features[db_set][jo]

    if normalize:
        return normalize_features(all_features)

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


def normalize_features(all_features: AllDataFeatures) -> AllDataFeatures:
    max_len = 0
    max_uni = 0
    max_rge = 0
    for query in all_features:
        for jo in all_features[query]:
            for jid in all_features[query][jo]:
                f = all_features[query][jo][jid]
                max_len = max(max_len, f.table_1.length)
                max_len = max(max_len, f.table_2.length)
                max_len = max(max_len, f.cross.len_res)
                max_len = max(max_len, f.cross.len_possible_max)
                max_len = max(max_len, f.cross.len_unique_max)
                max_uni = max(max_len, f.table_1.unique)
                max_uni = max(max_len, f.table_2.unique)
                max_rge = max(max_len, f.table_1.bounds_range)
                max_rge = max(max_len, f.table_2.bounds_range)

    scaling_len = 1.0 / max_len
    scaling_uni = 1.0 / max_uni
    scaling_rge = 1.0 / max_rge

    for query in all_features:
        for jo in all_features[query]:
            for jid in all_features[query][jo]:
                f = all_features[query][jo][jid]
                all_features[query][jo][jid] = DataFeatures(
                    table_1=f.table_1._replace(
                        length=f.table_1.length * scaling_len,
                        unique=f.table_1.unique * scaling_uni,
                        bounds_range=f.table_1.bounds_range * scaling_rge,
                    ),
                    table_2=f.table_2._replace(
                        length=f.table_2.length * scaling_len,
                        unique=f.table_2.unique * scaling_uni,
                        bounds_range=f.table_2.bounds_range * scaling_rge,
                    ),
                    cross=f.cross._replace(
                        len_res=f.cross.len_res * scaling_len,
                        len_possible_max=f.cross.len_possible_max * scaling_len,
                        len_unique_max=f.cross.len_unique_max * scaling_len,
                    ),
                )

    return all_features
