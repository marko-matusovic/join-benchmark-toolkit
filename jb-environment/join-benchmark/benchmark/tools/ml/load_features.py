import ast
import json

import pandas as pd
from benchmark.tools.ml.types import Features, TableFeatures, CrossFeatures, AllFeatures

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
