import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    query = sys.argv[1]

    df_overhead = pd.read_csv(f"results/external_log/cpu/overhead.csv", sep=";")
    df_overhead = df_overhead.loc[df_overhead["query"].str.startswith("//") == False]
    time_overhead = np.mean(
        df_overhead.loc[df_overhead["query"] == "ssb/q41"].values[0][1:]
    )

    df_time = pd.read_csv(f"results/external_log/cpu/{query}.csv", sep=";", comment="/")

    times:dict[str, float] = {
        df_time.T[i][0]: np.mean(df_time.T[i][1:]) - time_overhead for i in df_time.T
    }
    std:dict[str, float] = {
        df_time.T[i][0]: float(np.std(df_time.T[i][1:])) for i in df_time.T
    }
    sorted_keys = sorted(times, key=times.__getitem__)
    sorted_values = [times[k] for k in sorted_keys]
    sorted_std = [std[k] for k in sorted_keys]

    plt.figure(figsize=(9,7))
    
    plt.title(f"Different join times of {query} with overhead (loading, filtering) subtracted")
    plt.xlabel("join order")
    plt.xticks(rotation=90)
    plt.ylabel("time [s]")

    plt.bar(sorted_keys, sorted_values)
    plt.errorbar(sorted_keys, sorted_values, yerr=sorted_std, fmt="r+")

    plt.savefig(f"results/figs/diff-join-times/cpu/{query}.png", dpi=500)
    
    # plt.show()
