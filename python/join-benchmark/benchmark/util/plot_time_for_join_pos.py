import numpy as np
import matplotlib.pyplot as plt
import sys
from benchmark.engine.engine import get_engine

def main():
    query = sys.argv[1]
    
    # 'join_order;execution_tree;time_total;mem_peak;time_load;mem_load;time_filters;mem_filters;time_joins;mem_joins'
    df = get_engine().read_csv(f"results/time_mem/{query}.csv", sep=';')
    df = df[df['join_order'].str.startswith("//") == False]
    
    join_count = df['join_order'][1][1:-1].count(', ') + 1
    
    times = {}
    for run in df.T:
        order = df['join_order'][run]
        if order not in times:
            times[order] = {str(i) : [] for i in range(join_count)}
        time_start = float(df['time_filters'][run])
        absolute_times = df['time_joins'][run][1:-1].split(', ')
        times_run = [float(absolute_times[0]) - time_start]
        for i in range(len(absolute_times)-1):
            times_run.append(float(absolute_times[i+1]) - float(absolute_times[i]))
        for join, time in zip(order[1:-1].split(', '), times_run):
            times[order][join].append(time)
    
    # average run times per order for all joins
    times = {order: {join: np.mean(times[order][join]) for join in times[order]} for order in times}
    
    join_times = {str(join) : [[] for pos in range(join_count)] for join in range(join_count)}
    for order in times:
        for join in times[order]:
            join 
            pos = order[1:-1].split(', ').index(join)
            time = times[order][join]
            join_times[join][pos].append(time)
    
    try:
        join = sys.argv[2]
        assert join in join_times
        plot_join(query, join, join_times)
    except:
        for join in range(join_count):
            plot_join(query, str(join), join_times)
    
def plot_join(query, join, join_times):

    times_min = np.array([np.min(pos) for pos in join_times[join]])
    times_max = np.array([np.max(pos) for pos in join_times[join]])
    times_mean = np.array([np.mean(pos) for pos in join_times[join]])
    times_err = [times_mean - times_min, times_max - times_mean]
    
    plt.clf()
    plt.title(f'Mean Execution Time of join {join} per position in {query}')
    plt.xlabel('join position')
    plt.ylabel('time [s]')
    
    plt.bar(x=range(len(times_mean)), height=times_mean)
    if '-e' in sys.argv:
        plt.errorbar(x=range(len(times_mean)), y=times_mean, yerr=times_err, fmt='r+')

    plt.show()
    
if __name__ == '__main__':
    main()