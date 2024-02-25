import math
import numpy as np
import pandas as pd
import pickle as pkl
from benchmark.tools.ml.encode import feature_length
from benchmark.tools.ml.encode_reg import encode_all_reg, encode_query_reg
from benchmark.tools.ml.load_all import load_all
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt

from benchmark.tools.tools import ensure_dir


def main(
    db_sets: list[str],
    training_set: int,
    extra_features: list[str],
    res_path: str,
    plot: bool,
):
    if training_set not in [4, 5]:
        print(
            "Warning: this script was designed to use training sets 4 or 5.",
            "Note that if you're using a different training set, you should know what you're doing.",
        )

    if "t_length" not in extra_features:
        extra_features.insert(0, "t_length")

    print("Loading and encoding...")

    db_encoded = {}
    for db_set in db_sets:
        (data_features, measurements) = load_all(db_set, training_set, res_path)
        db_encoded[db_set] = {}
        for query in sorted(data_features.keys()):
            jos = set(data_features[query].keys()) & set(measurements[query].keys())
            db_encoded[db_set][query] = {}
            for jo in jos:
                (x, y) = encode_query_reg(
                    data_features, measurements, query, 1, jo=jo, select=extra_features
                )
                db_encoded[db_set][query][jo] = (np.sum(x, axis=0), np.sum(y))

    # === Train =================================================

    print("Exploring coefficients...")

    step = 0.1
    min_progress = 1e-24
    gen = 0

    coefs = np.ones(feature_length(select=extra_features)) * 100
    max_corr = 0
    max_explore_i = 0

    while max_explore_i != -1:
        gen += 1
        # print("Gen")
        max_explore_i = -1
        for i in range(len(coefs)):
            # print("\tExplore")
            explore = coefs.copy()
            # explore[i] += step
            explore[i] *= 1 + step
            explore_norm = explore / np.sum(explore)

            total_corr = 0.0
            total_jos = 0

            for db_set in db_encoded:
                for query in db_encoded[db_set]:
                    (X, y_real) = zip(*db_encoded[db_set][query].values())
                    y_pred = np.sum(X * explore_norm, axis=1)

                    indeces = np.argsort(y_real)

                    s1 = pd.Series(np.array(y_real)[indeces])
                    s2 = pd.Series(np.array(y_pred)[indeces])
                    total_corr += s1.corr(s2) * len(indeces)
                    total_jos += len(indeces)

            corr = total_corr / total_jos
            # print(f"\tAverage correlation: {corr}")
            # print(f"\tCoefficients: {explore}")
            if corr >= max_corr + min_progress:
                max_corr = corr
                max_explore_i = i
                coefs = explore
        print(f"Gen: {gen:4} Corr: {max_corr:<20}", end="\r")
    print()

    coefs /= np.sum(coefs)

    print(f"Took {gen} generations")
    print(f"Found max correlation: {max_corr}")
    print("Coefficients:")
    for c in coefs:
        print("\t", c)

    # === Printing individual correlations =========================

    for db_set in db_sets:
        for query in db_encoded[db_set]:
            # Data processing

            sorted_keys = list(db_encoded[db_set][query].keys())
            sorted_keys.sort(key=lambda jo: db_encoded[db_set][query][jo][1])

            real_values = [db_encoded[db_set][query][jo][1] for jo in sorted_keys]
            pred_values = [
                np.sum(db_encoded[db_set][query][jo][0] * coefs) for jo in sorted_keys
            ]

            # Correlation
            s1 = pd.Series(real_values, index=range(len(sorted_keys)))
            s2 = pd.Series(pred_values, index=range(len(sorted_keys)))
            correlation = s1.corr(s2)

            print(
                f"Query: {query:16}",
                f"#jo: {len(db_encoded[db_set][query]):3}",
                f"corr: {correlation:-10.6}",
            )

    # === Evaluate =================================================

    if plot:
        print("Plotting figures...")

        for db_set in db_sets:
            for query in db_encoded[db_set]:
                # Data processing

                sorted_keys = list(db_encoded[db_set][query].keys())
                sorted_keys.sort(key=lambda jo: db_encoded[db_set][query][jo][1])

                real_values = [db_encoded[db_set][query][jo][1] for jo in sorted_keys]
                pred_values = [
                    np.sum(db_encoded[db_set][query][jo][0] * coefs)
                    for jo in sorted_keys
                ]

                # Correlation
                s1 = pd.Series(real_values, index=range(len(sorted_keys)))
                s2 = pd.Series(pred_values, index=range(len(sorted_keys)))
                correlation = s1.corr(s2)

                # ======================== PLOTTING ========================

                plt.figure(figsize=(10, 6))
                width = 0.35  # the width of the bars

                # Create a list of indices for the x-axis
                indices = range(len(sorted_keys))

                # Plot the real values on the first y-axis
                # ax1 = plt.bar(indices, real_values, width, label="Real", color="#1f77b4", alpha=0.9)
                # plt.ylabel('Real Values')
                ax1 = plt.gca()
                ax1.bar(
                    indices,
                    real_values,
                    width,
                    label="Real",
                    color="#1f77b4",
                    alpha=0.9,
                )
                ax1.set_ylabel("Real Values")
                ax1.set_ylim(bottom=min(real_values))

                # Create a second y-axis that shares the same x-axis
                ax2 = plt.twinx()

                # Plot the predicted values on the second y-axis
                ax2.bar(
                    [i + width for i in indices],
                    pred_values,
                    width,
                    label="Predicted",
                    color="#ff7f0e",
                    alpha=0.9,
                )
                ax2.set_ylabel("Predicted Values")
                ax2.set_ylim(bottom=min(pred_values))

                num_jo = len(real_values)
                ax1.text(
                    0.1,
                    0.95,
                    f"#join-orders: {num_jo}",
                    horizontalalignment="left",
                    verticalalignment="top",
                    transform=ax1.transAxes,
                )

                ax1.text(
                    0.1,
                    0.90,
                    f"Correlation: {correlation}",
                    horizontalalignment="left",
                    verticalalignment="top",
                    transform=ax1.transAxes,
                )

                plt.title("Comparison of Real and Predicted Values for Query: " + query)
                plt.xlabel("Join Order")
                plt.xticks([i + width / 2 for i in indices], sorted_keys, rotation=45)
                plt.legend()

                model_name = f"lin_reg/{'+'.join(extra_features)}/set_{training_set}"
                dir_path = f"{res_path}/figs/model-eval/{model_name}/{query}.png"
                ensure_dir(dir_path)
                plt.savefig(dir_path)

                plt.close()

    print("Done!")
