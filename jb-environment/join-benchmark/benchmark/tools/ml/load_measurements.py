import ast

import pandas as pd
from benchmark.tools.ml.types import AllMeasurements, Measurements


def avg_list(lst):
    if type(lst[lst.index[0]]) == float:
        return [sum(lst) / len(lst)]
    return [sum(group) / len(group) for group in zip(*lst)]


def load_measurements(db_set: str, training_set: int, res_path: str) -> AllMeasurements:
    # Read the CSV file
    file = f"{res_path}/training_data/{db_set}/set_{training_set}_measurements.csv"
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
