import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd

sys.path.append("benchmark")

if __name__ == "__main__":
    query = sys.argv[1]

    df_approx = pd.read_csv(
        open(f"results/approx_time_mem/{query}.csv", "r"), comment="/", sep=";"
    )
    df_front = pd.read_csv(
        open(f"results/optimization/{query}.csv", "r"), comment="/", sep=";"
    )

    # plt.figure(figsize=(8, 6))
    plt.title(
        f"Search Space of Time and Memory Cost Optimization\nof {query} for various join orders."
    )
    plt.xlabel("time [s]")
    plt.ylabel("memory [B]")

    plt.scatter(
        x=df_approx["time_cost"], y=df_approx["memory_sum_cost"], label="All Points"
    )
    plt.scatter(
        x=df_front["time_cost"],
        y=df_front["memory_sum_cost"],
        label="Pareto Front found by Optimization",
    )

    plt.legend()

    plt.show()
    # plt.savefig(f'results/figs/optimization-front/{query}.png', dpi=250)
