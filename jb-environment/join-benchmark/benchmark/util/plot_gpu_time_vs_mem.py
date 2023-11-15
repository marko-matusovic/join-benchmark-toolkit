import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd

sys.path.append( 'benchmark' )
from tools.pareto import find_pareto_front

if __name__ == '__main__':
    query = sys.argv[1]
    
    df_time = pd.read_csv(f"results/external_log/gpu/{query}.csv", sep=';', comment="/")
    
    stats = {
        # The structure is the following:
        # {perm}: {
        #   "time": {
        #       "mean": {0},
        #       "min": {0},
        #       "max": {0}
        #   },
        #   "memory": {
        #       "read": {
        #           "sum": {0}, # sum of all reads
        #           "max": {0}  # max of (sum of a kernel)
        #       }
        #       "write": {
        #           "sum": {0},
        #           "max": {0}
        #       }
        #   }
        # }
    }
    
    for i in df_time.T:
        row = df_time.T[i]
        perm = row[0]
        stats[perm] = {
            "time": {
                "mean": np.mean(row[1:]),
                "min": np.min(row[1:]),
                "max": np.max(row[1:]),
            }
        }
        
        try:
            df_mem = pd.read_csv(f"results/ncu/{query}/{perm}.csv", sep=",", comment="=")
            
            df_mem_read = df_mem[df_mem['Metric Name'] == 'dram__bytes_read.sum']
            group_read = df_mem_read.groupby(['Kernel Name'])
            
            df_mem_write = df_mem[df_mem['Metric Name'] == 'dram__bytes_write.sum']
            group_write = df_mem_write.groupby(['Kernel Name'])
            
            stats[perm]["memory"] = {
                "read": {
                    "sum": np.sum(df_mem_read["Metric Value"]),
                    "max": np.max(group_read.sum(numeric_only=True)["Metric Value"]),
                },
                "write": {
                    "sum": np.sum(df_mem_write["Metric Value"]),
                    "max": np.max(group_write.sum(numeric_only=True)["Metric Value"]),
                }
            }
        except:
            del stats[perm]
            break
    
    
    for rw in ['read', 'write']:
        for item in ['sum', 'max']:
            plt.figure(figsize=(8,6))
            plt.title(f'Execution Time vs DRAM {rw.capitalize()} {item.capitalize()}\nper Random Join Orders of {query}')
            plt.xlabel('time [s]')
            plt.ylabel('memory [B]')
            
            points = np.array([[stats[perm]["time"]['mean'], stats[perm]["memory"][rw][item]] for perm in stats])
            front_mask = find_pareto_front(points, return_mask=True)
            plt.scatter(x=points.T[0], y=points.T[1], label='All Points')
            front_points = points[front_mask == True]
            plt.scatter(x=front_points.T[0], y=front_points.T[1], label='Pareto-Front')
            
            plt.legend()
            
            plt.savefig(f'results/figs/gpu/TvM/{query}/time-mean-vs-mem-{rw}-{item}.png')
