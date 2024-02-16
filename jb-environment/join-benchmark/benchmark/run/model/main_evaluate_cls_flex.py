import functools
import json
import math
import numpy as np
import pandas as pd
from benchmark.tools.ml import encode
from benchmark.tools.ml.encode import (
    encode_all_cls,
    encode_cls_jo_pair,
    encode_cls_jo_pair_flex,
    encode_feature,
    encode_query_reg,
    encode_query_cls,
)
from benchmark.tools.ml.load_all import load_all
from benchmark.tools.ml.load_features import load_hw_features
import pickle as pkl
from matplotlib import pyplot as plt
import os

from benchmark.tools.tools import flatten


def main(
    db_set: str,
    training_set: int,
    model_name: str,
    # hw_name: str,
    res_path: str | None = None,
):
    if res_path == None:
        res_path = "./results"

    # create a gradient boosting regressor
    normalize = False

    normalize = False
    model = pkl.load(open(f"{res_path}/models/{model_name}.pickle", "rb"))

    print(f"Model:", model_name)

    # load the evaluation set
    (data_features, measurements) = load_all(db_set, training_set, res_path, normalize)
    # hw_features = load_hw_features(hw_name, res_path)

    (X, y_real) = encode_all_cls(data_features, measurements, None, True, False)

    print(f"{db_set} has {len(X)} jo combinations")
    if len(X) == 0:
        exit(0)

    y_predict = model.predict(np.array(X))

    count = 0
    for real, pred in zip(y_real, y_predict):
        if real == pred:
            count += 1

    dir_path = f"{res_path}/figs/model-eval/{model_name}/{db_set}"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    avg_cor = []

    queries = set(data_features.keys()) & set(measurements.keys())
    for query in queries:
        jos = set(data_features[query].keys()) & set(measurements[query].keys())
        jos = sorted(list(jos))
        print(f"{query} has {len(jos)} join order, now sorting with predictor")

        true_order = [
            jo
            for jo, _ in sorted(
                [(jo, sum(measurements[query][jo].joins)) for jo in jos],
                key=lambda x: x[1],
            )
        ]

        def compare(jo1, jo2):
            ([x], _) = encode_cls_jo_pair_flex(
                data_features, measurements, query, (jo1, jo2), False
            )
            pred = model.predict(np.array([x]))[0]
            return pred * 2 - 1

        pred_order = sorted(jos, key=functools.cmp_to_key(compare))

        print(query)
        print("true order (jo)", true_order)
        print("pred order (jo)", pred_order)

        real_values = [sum(measurements[query][jo].joins) for jo in true_order]
        pred_values = [sum(measurements[query][jo].joins) for jo in pred_order]

        print("true order (time)", real_values)
        print("pred order (time)", pred_values)

        # ======================== PLOTTING ========================

        plt.figure(figsize=(10, 6))
        width = 0.35  # the width of the bars

        # Create a list of indices for the x-axis
        indices = range(len(real_values))

        # Plot the real values
        plt.bar(
            indices,
            real_values,
            width,
            label="Real",
            color="#1f77b4",
            alpha=0.9,
        )

        # Plot the predicted values
        plt.bar(
            [i + width for i in indices],
            pred_values,
            width,
            label="Predicted",
            color="#ff7f0e",
            alpha=0.9,
        )

        num_jo = len(real_values)
        ax = plt.gca()
        ax.text(
            0.5,
            0.95,
            f"#join-orders: {num_jo}",
            horizontalalignment="center",
            verticalalignment="top",
            transform=ax.transAxes,
        )

        # Calculate the correlation and print it
        s1 = pd.Series(real_values, index=range(len(real_values)))
        s2 = pd.Series(pred_values, index=range(len(real_values)))
        correlation = s1.corr(s2)
        if not math.isnan(correlation):
            avg_cor.append((correlation, num_jo))
        ax.text(
            0.5,
            0.90,
            f"Correlation: {correlation}",
            horizontalalignment="center",
            verticalalignment="top",
            transform=ax.transAxes,
        )

        plt.title("Comparison of Real and Predicted Values for Query: " + query)
        plt.xlabel("Join Order")
        plt.ylabel("Value")
        plt.legend()
        plt.savefig(f"{res_path}/figs/model-eval/{model_name}/" + query + ".png")
        plt.close()

        print(f"Query: {query:12} corr: {correlation:10.6}")

    total_cor = 0.0
    total_jo = 0
    for c, n in avg_cor:
        total_cor += c * n
        total_jo += n

    print(f"Correct {count} / all {len(X)}")
    print(f"Success rate: {100.0 * count / len(X)}%")

    print(f"Average correlation: {total_cor / total_jo}")
