import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd

if __name__ == "__main__":
    query = sys.argv[1]

    # 'join_order;execution_tree;time_total;mem_peak;time_load;mem_load;time_filters;mem_filters;time_joins;mem_joins'
    df = pd.read_csv(f"results/time_mem/{query}.csv", sep=";")
    df = df[df["join_order"].str.startswith("//") == False]

    grouped = df.groupby(["join_order"])

    times_min = np.array(grouped.min()["time_total"])
    times_mean = np.array(grouped.mean()["time_total"])
    times_max = np.array(grouped.max()["time_total"])
    times_err = [times_mean - times_min, times_max - times_mean]

    mem_min = np.array(grouped.min()["mem_peak"])
    mem_mean = np.array(grouped.mean()["mem_peak"])
    mem_max = np.array(grouped.max()["mem_peak"])
    mem_err = [mem_mean - mem_min, mem_max - mem_mean]

    plt.title(f"Execution Time vs Peak Memory Use\nper Random Join Orders of {query}")
    plt.xlabel("time [s]")
    plt.ylabel("memory [B]")

    if "-e" in sys.argv:
        plt.errorbar(x=times_mean, y=mem_mean, xerr=times_err, yerr=mem_err, fmt="o")
    else:
        plt.scatter(x=times_mean, y=mem_mean)

    plt.show()
