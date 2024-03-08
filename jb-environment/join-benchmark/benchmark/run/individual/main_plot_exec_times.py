import pandas as pd
from benchmark.tools.tools import ensure_dir
from matplotlib import pyplot as plt


def main(
    db_sets: list[str] = ["ssb", "job", "tpcds"],
    set_number: int = 4,
    res_path: str = "./results",
):
    if set_number not in [4, 5]:
        print(
            "Warning: this script was designed to use training sets 4 or 5.",
            "Note that if you're using a different training set, you should know what you're doing.",
        )

    for db_set in sorted(db_sets):
        file = f"{res_path}/training_data/{db_set}/set_{set_number}_measurements.csv"
        df = pd.read_csv(file, sep=";", comment="#")

        # Filter the dataframe by EXIT_CODE == 200
        df = df[df["EXIT_CODE"] == 200]

        # Convert list strings into actual lists
        df["JOINS"] = df["JOINS"].apply(
            lambda x: float(sum([float(i) for i in x.split(",")]))
        )

        # Group by 'DB_SET/QUERY' and 'JOIN_PERMUTATION', then apply the sum_and_stats function
        # grouped_df = df.groupby(['DB_SET/QUERY', 'JOIN_PERMUTATION'])['JOINS'].agg(['mean', 'std'])

        for query in df["DB_SET/QUERY"].unique():
            print("Working on", query, "...")
            # ======================== DATA EXTRACTION ========================
            df_q = df[df["DB_SET/QUERY"] == query]

            # Group by 'JOIN_PERMUTATION' and calculate the mean and std of 'mean' and 'std'
            query_grouped = df_q.groupby("JOIN_PERMUTATION")["JOINS"].agg(
                ["mean", "std"]
            )

            # Extract the means, stds, and JOIN_PERMUTATIONS into separate lists
            means = query_grouped["mean"].tolist()
            stds = query_grouped["std"].tolist()
            keys = query_grouped.index.tolist()  # Get the JOIN_PERMUTATION values

            # ======================== SORTING ========================

            # Pair each element of means, stds, and keys
            pairs = list(zip(means, stds, keys))

            # Sort the pairs based on the means values
            sorted_pairs = sorted(pairs, key=lambda x: x[0])

            # Unzip the sorted pairs back into separate lists
            sorted_means, sorted_stds, sorted_keys = zip(*sorted_pairs)

            # Convert the lists back to their original types (if necessary)
            sorted_means = list(sorted_means)
            sorted_stds = list(sorted_stds)
            sorted_keys = list(sorted_keys)

            # ======================== PLOTTING ========================

            plt.figure(figsize=(10, 6))

            # Plot the real values on the first y-axis
            plt.bar(
                sorted_keys,
                sorted_means,
                color="#1f77b4",
                alpha=0.9,
            )
            plt.errorbar(sorted_keys, sorted_means, yerr=sorted_stds, fmt="r+")

            plt.ylabel("Time [s]")
            plt.xticks(rotation=30)

            # Add text in the top left corner
            plt.text(
                0.01,
                0.95,
                f"#join-orders: {len(sorted_means)}",
                transform=plt.gca().transAxes,
                fontsize=12,
                verticalalignment="top",
            )

            # Assuming each character is approximately 0.01 inches wide, adjust as needed
            # Since all labels are guaranteed to be the same length, you can use the length of any label
            label_length = len(sorted_keys[0])
            bottom_margin = 0.1 + label_length * 0.006
            plt.subplots_adjust(bottom=bottom_margin)

            plt.title(
                ("CPU" if set_number == 4 else "GPU")
                + " Execution Times of Various Join-orders for Query: "
                + query
            )
            plt.xlabel("Join Order")

            dir_path = f"{res_path}/figs/exec-times/set_{set_number}/{query}.png"
            ensure_dir(dir_path)
            plt.savefig(dir_path)

            plt.close()
            # Data processing

    print("Done!")
