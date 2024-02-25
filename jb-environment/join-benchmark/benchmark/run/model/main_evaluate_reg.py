import math
import numpy as np
import pandas as pd
from benchmark.tools.ml.encode_reg import encode_query_reg
from benchmark.tools.ml.load_all import load_all
from benchmark.tools.ml.load_features import load_hw_features
import pickle as pkl
from matplotlib import pyplot as plt
import os


def main(
    db_set: str,
    training_set: int,
    model_name: str,
    # hw_name: str,
    res_path: str | None = None,
):
    if res_path == None:
        res_path = "./results"

    normalize = False
    # load the model
    model = pkl.load(open(f"{res_path}/models/{model_name}.pickle", "rb"))

    join_in_block = int(model_name.split("/")[-1].split("_")[2][2:])

    # load the evaluation set
    (data_features, measurements) = load_all(db_set, training_set, res_path, normalize)
    # hw_features = load_hw_features(hw_name, res_path)

    print(f"Model:", model_name)
    # print("Feature importances:")
    # print(model.feature_importances_)

    dir_path = f"{res_path}/figs/model-eval/{model_name}/{db_set}"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    times = {}
    avg_cor = []
    for query in data_features:
        times[query] = {}
        for jo in set(data_features[query].keys()) & set(measurements[query].keys()):
            (X, y_real) = encode_query_reg(
                data_features, measurements, query, join_in_block, jo
            )

            y_predict = model.predict(X)  # type: ignore

            times[query][jo] = {"real": sum(y_real), "pred": sum(y_predict)}

        # ======================== PLOTTING ========================
        sorted_keys = list(times[query].keys())
        sorted_keys.sort(key=lambda t: times[query][t]["real"])

        real_values = [times[query][key]["real"] for key in sorted_keys]
        pred_values = [times[query][key]["pred"] for key in sorted_keys]

        plt.figure(figsize=(10, 6))
        width = 0.35  # the width of the bars

        # Create a list of indices for the x-axis
        indices = range(len(sorted_keys))

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
        s1 = pd.Series(real_values, index=range(len(sorted_keys)))
        s2 = pd.Series(pred_values, index=range(len(sorted_keys)))
        correlation = s1.corr(s2)
        if not math.isnan(correlation):
            avg_cor.append((correlation, len(times[query])))
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
        plt.xticks([i + width / 2 for i in indices], sorted_keys, rotation=45)
        plt.legend()
        plt.savefig(f"{res_path}/figs/model-eval/{model_name}/" + query + ".png")
        plt.close()

        print(f"Query: {query:12} #jo: {len(times[query]):3}  corr: {correlation:10.6}")

    cor_sum = 0.0
    total_jos = 0.0
    for cr, cn in avg_cor:
        cor_sum += cr * cn
        total_jos += cn
    print(f"Average correlation: {cor_sum / total_jos}")
