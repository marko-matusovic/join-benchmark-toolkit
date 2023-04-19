import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

if __name__ == '__main__':
    query = sys.argv[1]
    # ordering = int(sys.argv[2])
    
    # 'join_order;execution_tree;time_total;mem_peak;time_load;mem_load;time_filters;mem_filters;time_joins;mem_joins'
    df = pd.read_csv(f"results/time_mem/{query}.csv", sep=';')
    df = df[df['join_order'].str.startswith("//") == False]
    
    # order = df['join_order'].unique()[ordering]
    for order in df['join_order'].unique():
    
        series = df[df['join_order'] == order]
        
        times = []
        for run in series.T:
            time_start = float(series.T[run]['time_filters'])
            absolute_times = series.T[run]['time_joins'][1:-1].split(', ')
            times_join = [float(absolute_times[0]) - time_start]
            for i in range(len(absolute_times)-1):
                times_join.append(float(absolute_times[i+1]) - float(absolute_times[i]))
            times.append(times_join)
        
        times_min = np.min(times, axis=0)
        times_max = np.max(times, axis=0)
        times_mean = np.mean(times, axis=0)
        times_err = [times_mean - times_min, times_max - times_mean]
        
        labels = order[1:-1].split(', ')
        
        plt.clf()
        
        plt.bar(x=labels, height=times_mean)
        if '-e' in sys.argv:
            plt.errorbar(x=labels, y=times_mean, yerr=times_err, fmt='r+')

        plt.show()
        