from math import ceil, floor
import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd

if __name__ == '__main__':
    query = sys.argv[1]
    
    # 'join_order;execution_tree;time_total;mem_peak;time_load;mem_load;time_filters;mem_filters;time_joins;mem_joins'
    df = pd.read_csv(f"results/time_mem/{query}.csv", sep=';')
    df = df[df['join_order'].str.startswith("//") == False]
    
    b_min = floor(df['time_filters'].min())
    b_max = ceil(df['time_filters'].max())
    b_count = int(b_max - b_min) * 2
    
    counts, bins = np.histogram(df['time_filters'], b_count, (b_min, b_max))
    counts = counts * 100.0 / np.sum(counts)

    plt.title(f'Overhead (data load + filtering) of {query}')
    plt.xlabel('time [s]')
    plt.ylabel('number of samples [%]')
    
    # plt.stairs(counts, bins)
    _, _, bars = plt.hist(bins[:-1], bins, weights=counts) # type: ignore
    plt.bar_label(bars, fmt="%3.1f")
    
    plt.show()