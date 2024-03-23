from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd
from benchmark.tools.tools import ensure_dir
from matplotlib import pyplot as plt


def load_df(db_set, set_num, res_path):
    file = f"{res_path}/training_data/{db_set}/set_{set_num}_measurements.csv"
    df = pd.read_csv(file, sep=";", comment="#")

    # Filter the dataframe by EXIT_CODE == 200
    df = df[df["EXIT_CODE"] == 200]

    # Convert list strings into actual lists
    for field in ["FILTERS", "JOINS"]:
        df[field] = df[field].apply(lambda x: [float(i) for i in x.split(",")])

    return df


def main(
    db_set: str,
    res_path: str = "./results",
):

    df_cpu = load_df(db_set, 4, res_path)
    df_gpu = load_df(db_set, 5, res_path)

    queries = sorted(
        list(
            set(df_cpu["DB_SET/QUERY"].unique()).intersection(
                df_gpu["DB_SET/QUERY"].unique()
            )
        )
    )

    for query in queries:
        print("Working on", query, "...")
        
        
        # ======================== DATA EXTRACTION ========================
        df_c_q = df_cpu[df_cpu["DB_SET/QUERY"] == query]
        df_g_q = df_gpu[df_gpu["DB_SET/QUERY"] == query]
        
        jo = list(df_c_q["JOIN_PERMUTATION"])[0]
        df_c_q = df_c_q[df_c_q["JOIN_PERMUTATION"] == jo]
        df_g_q = df_g_q[df_g_q["JOIN_PERMUTATION"] == jo]

        n_filter = len(list(df_c_q["FILTERS"])[0])
        n_join = len(list(df_c_q["JOINS"])[0])
        keys = [
            "parsing",
            "overhead",
            *[f"filter {n}" for n in range(n_filter)],
            *[f"join {n}" for n in range(n_join)],
        ]

        means_cpu = [
            np.mean(df_c_q["PARSING"]),
            np.mean(df_c_q["OVERHEAD"]),
            *[np.mean([row[fn] for row in df_c_q["FILTERS"]]) for fn in range(n_filter)],
            *[np.mean([row[jn] for row in df_c_q["JOINS"]]) for jn in range(n_join)],
        ]
        
        stds_cpu = [
            np.std(df_c_q["PARSING"]),
            np.std(df_c_q["OVERHEAD"]),
            *[np.std([row[fn] for row in df_c_q["FILTERS"]]) for fn in range(n_filter)],
            *[np.std([row[jn] for row in df_c_q["JOINS"]]) for jn in range(n_join)],
        ]
        
        means_gpu = [
            np.mean(df_g_q["PARSING"]),
            np.mean(df_g_q["OVERHEAD"]),
            *[np.mean([row[fn] for row in df_g_q["FILTERS"]]) for fn in range(n_filter)],
            *[np.mean([row[jn] for row in df_g_q["JOINS"]]) for jn in range(n_join)],
        ]
        
        stds_gpu = [
            np.std(df_g_q["PARSING"]),
            np.std(df_g_q["OVERHEAD"]),
            *[np.std([row[fn] for row in df_g_q["FILTERS"]]) for fn in range(n_filter)],
            *[np.std([row[jn] for row in df_g_q["JOINS"]]) for jn in range(n_join)],
        ]
        
        # ======================== PLOTTING ========================

        plt.figure(figsize=(10, 8))
        width = 0.35  # the width of the bars

        # Create a list of indices for the x-axis
        indices = range(len(keys))

        # Plot CPU means with error bars on the first y-axis
        ax1 = plt.gca()
        ax1.bar(
            indices,
            means_cpu,
            width,
            yerr=stds_cpu,
            label="CPU",
            color="#1f77b4",
            alpha=0.9,
            capsize=5,  # Optional: adds caps to the error bars
        )

        # Plot GPU means with error bars, slightly offset on the x-axis for clarity
        ax1.bar(
            [i + width for i in indices],
            means_gpu,
            width,
            yerr=stds_gpu,
            label="GPU",
            color="#ff7f0e",
            alpha=0.9,
            capsize=5,  # Optional: adds caps to the error bars
        )

        # Adjust the y-axis scale if needed
        ax1.set_yscale("log")
        ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: '{:}'.format(x)))


        # Set the x-axis ticks and labels
        ax1.set_xticks([i + width / 2 for i in indices])
        ax1.set_xticklabels(keys, rotation=30)

        # Set the x-axis label and add the legend
        ax1.set_xlabel("Stages")
        ax1.set_ylabel("Execution Time [s] log")
        ax1.legend(loc='upper left', bbox_to_anchor=(0.01, 0.99))

        # Set the plot title
        plt.title("Execution Time for Stages of Query: " + query)

        # Save the plot
        dir_path = f"{res_path}/figs/query-details/{query}.png"
        ensure_dir(dir_path)
        plt.savefig(dir_path)

        # Close the plot to free up memory
        plt.close()

    print("Done!")