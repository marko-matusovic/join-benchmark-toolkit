from typing import NamedTuple, TypeAlias
import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd


class Stats(NamedTuple):
    mean: float
    min: float
    max: float


TPermStats: TypeAlias = dict[str, Stats]

if __name__ == "__main__":
    query = sys.argv[1]

    df_time = pd.read_csv(f"results/external_log/cpu/{query}.csv", sep=";", comment="/")

    stats: TPermStats = {}

    for i in df_time.T:
        row = df_time.T[i]
        perm = row[0]
        stats[perm] = Stats(
            mean=float(np.mean(row[1:])),
            min=float(np.min(row[1:])),
            max=float(np.max(row[1:])),
        )

    real_times: dict[str, float] = {perm: stats[perm].mean for perm in stats}
    df_approx = pd.read_csv(
        open(f"results/approx_time_mem/{query}.csv", "r"), comment="/", sep=";"
    )
    scale = lambda x : (((x * 3) ** 4) * 3) # for over-fitting SSB plots
    cost_model_times: dict[str, float] = {
        df_approx["permutation"][i]: scale(df_approx["time_cost"][i])
        for i in range(len(df_approx.index))
    }

    BINS = int(sys.argv[sys.argv.index("-b") + 1]) if "-b" in sys.argv else 10
    perm_bins = [[] for _ in range(BINS)]

    method = sys.argv[sys.argv.index("-m") + 1] if "-m" in sys.argv else "bin_width"

    if method == "bin_size":
        real_times_keys_sorted = np.array(sorted(real_times, key=real_times.__getitem__))
        bin_size = len(real_times_keys_sorted) / BINS
        for i, perm in enumerate(real_times_keys_sorted):
            perm_bins[int(i / bin_size)].append(perm)

    elif method == "bin_width":
        bin_min = min(real_times.values())
        bin_max = max(real_times.values()) + 1e-9
        bin_width = (bin_max - bin_min) / BINS
        for perm, time in real_times.items():
            perm_bins[int((time - bin_min) / bin_width)].append(perm)

    real_times_bins = [[real_times[perm] for perm in perm_bin] for perm_bin in perm_bins]
    cost_model_times_bins = [
        [cost_model_times[perm] for perm in perm_bin] for perm_bin in perm_bins
    ]
    
    print(f'Stats for query: {query}')
    # Print results
    for b in range(BINS):
        print("-" * 95)
        print(
            f'| BIN {b+1:3}/{BINS:<3} SIZE {len(perm_bins[b]):<8} | {"MEAN":30} | {"STANDARD DEVIATION":30} |'
        )
        print(
            f'| {"Real "+"Time":>25} | {np.mean(real_times_bins[b]):30.8f} | {np.std(real_times_bins[b]):30.8f} |'
        )
        print(
            f'| {"Cost "+"Time":>25} | {np.mean(cost_model_times_bins[b]):30.8f} | {np.std(cost_model_times_bins[b]):30.8f} |'
        )
    print("-" * 95)

    bin_lables = [f"Bin {i+1} [{len(perm_bins[i])}]" for i in range(BINS)] if BINS < len(real_times) else [bin[0] for bin in perm_bins]
    data = {
        "measurement": real_times_bins,
        "cost model": cost_model_times_bins,
    }
    
    x = np.arange(len(bin_lables))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout="constrained")
    fig.set_size_inches(9,7)

    for attribute, bin_data in data.items():
        mean = [np.mean(bin) for bin in bin_data]
        # data_min = [np.min(bin) for bin in bin_data]
        # data_max = [np.max(bin) for bin in bin_data]
        data_std = [np.std(bin) for bin in bin_data]

        offset = width * multiplier

        # mean bars
        rects = ax.bar(x + offset, mean, width, label=attribute)
        # ax.bar_label(rects, padding=3)

        # std errors
        ax.errorbar(x + offset, mean, yerr=data_std, fmt="r.")

        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel("Time (s)")
    ax.set_title(f"Measurement and Cost Model Time Comparison")
    ax.set_xticks(x + width, bin_lables, rotation=90)
    ax.legend(loc="upper left", ncols=len(data))

    plt.savefig(f"results/figs/cost-comparison/cpu/{query}.png", dpi=250)
