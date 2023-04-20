import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

def main():
    query = sys.argv[1]
    
    # 'join_order;execution_tree;time_total;mem_peak;time_load;mem_load;time_filters;mem_filters;time_joins;mem_joins'
    df = pd.read_csv(f"results/time_mem/{query}.csv", sep=';')
    df = df[df['join_order'].str.startswith("//") == False]
    
    join_count = df['join_order'][1][1:-1].count(', ') + 1
    
    times = {}
    for run in df.T:
        order = df['join_order'][run]
        if order not in times:
            times[order] = {i : [] for i in range(join_count)}
        time_start = float(df['time_filters'][run])
        absolute_times = df['time_joins'][run][1:-1].split(', ')
        times_join = [float(absolute_times[0]) - time_start]
        for i in range(len(absolute_times)-1):
            times_join.append(float(absolute_times[i+1]) - float(absolute_times[i]))
        for join, time in zip(order[1:-1].split(', '), times_join):
            join = int(join)
            times[order][join].append(time)
    
    times_mean_global = []
    for order in times:
        times_mean_global.append([np.mean(times[order][join]) for join in range(join_count)])
        
    times_mean_global = np.mean(times_mean_global, axis=0)
    
    try:
        order = df['join_order'].unique()[int(sys.argv[2])]
        plot_order(df, query, order, times_mean_global)
    except:
        for order in df['join_order'].unique():
            plot_order(df, query, order, times_mean_global)
    
def plot_order(df, query, order, times_mean_global):
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
    plt.title(f'Mean Execution Time per Join of {query}\nin join order {order}')
    plt.xlabel('join id')
    plt.ylabel('time [s]')
    
    plt.bar(x=labels, height=times_mean)
    if '-e' in sys.argv:
        plt.errorbar(x=labels, y=times_mean, yerr=times_err, fmt='r+')
    if '-m' in sys.argv:
        plt.plot(range(len(times_mean_global)), times_mean_global, 'yo')

    plt.show()
    
if __name__ == '__main__':
    main()