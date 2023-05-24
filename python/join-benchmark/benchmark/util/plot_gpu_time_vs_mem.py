import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd

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
            break
    
    # Read Sum
    plt.title(f'Execution Time vs Total DRAM Read\nper Random Join Orders of {query}')
    plt.xlabel('time [s]')
    plt.ylabel('memory [B]')
    
    plt.scatter( \
        x=[stats[perm]["time"]['mean'] for perm in stats], \
        y=[stats[perm]["memory"]['read']['sum'] for perm in stats] \
    )
    
    plt.savefig(f'results/figs/gpu/TvM/{query}/time-mean-vs-mem-read-sum.png')
    
    # Read Max
    plt.figure()
    plt.title(f'Execution Time vs Max DRAM Read\nper Random Join Orders of {query}')
    plt.xlabel('time [s]')
    plt.ylabel('memory [B]')
    
    plt.scatter( \
        x=[stats[perm]["time"]['mean'] for perm in stats], \
        y=[stats[perm]["memory"]['read']['max'] for perm in stats] \
    )
    
    plt.savefig(f'results/figs/gpu/TvM/{query}/time-mean-vs-mem-read-max.png')
    
    # Write Sum
    plt.figure()
    plt.title(f'Execution Time vs Total DRAM Write\nper Random Join Orders of {query}')
    plt.xlabel('time [s]')
    plt.ylabel('memory [B]')
    
    plt.scatter( \
        x=[stats[perm]["time"]['mean'] for perm in stats], \
        y=[stats[perm]["memory"]['write']['sum'] for perm in stats] \
    )
    
    plt.savefig(f'results/figs/gpu/TvM/{query}/time-mean-vs-mem-write-sum.png')
    
    # Write Max
    plt.figure()
    plt.title(f'Execution Time vs Max DRAM Write\nper Random Join Orders of {query}')
    plt.xlabel('time [s]')
    plt.ylabel('memory [B]')
    
    plt.scatter( \
        x=[stats[perm]["time"]['mean'] for perm in stats], \
        y=[stats[perm]["memory"]['write']['max'] for perm in stats] \
    )
    
    plt.savefig(f'results/figs/gpu/TvM/{query}/time-mean-vs-mem-write-max.png')
