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
        
        # # SKIPPING MEMORY USAGE READING FROM NCU FILES
        # try:
        #     df_mem = pd.read_csv(f"results/ncu/{query}/{perm}.csv", sep=",", comment="=")
            
        #     df_mem_read = df_mem[df_mem['Metric Name'] == 'dram__bytes_read.sum']
        #     group_read = df_mem_read.groupby(['Kernel Name'])
            
        #     df_mem_write = df_mem[df_mem['Metric Name'] == 'dram__bytes_write.sum']
        #     group_write = df_mem_write.groupby(['Kernel Name'])
            
        #     stats[perm]["memory"] = {
        #         "read": {
        #             "sum": np.sum(df_mem_read["Metric Value"]),
        #             "max": np.max(group_read.sum(numeric_only=True)["Metric Value"]),
        #         },
        #         "write": {
        #             "sum": np.sum(df_mem_write["Metric Value"]),
        #             "max": np.max(group_write.sum(numeric_only=True)["Metric Value"]),
        #         }
        #     }
        # except:
        #     del stats[perm]
        #     break
    
    # Sort real and cost time data
    real_times = {perm: stats[perm]["time"]['mean'] for perm in stats}
    
    df_approx = pd.read_csv(open(f'results/approx_time_mem/{query}.csv', 'r'), comment='/', sep=';')
    cost_times = {
        df_approx['permutation'][i] : df_approx['time_cost'][i] 
        for i in range(len(df_approx.index))
    }
    
    real_times_keys_sorted = np.array(sorted(real_times, key=real_times.get))
    
    # Make BINs
    BINS = 10
    perm_bins = [[] for i in range(BINS)]
    bin_size = len(real_times_keys_sorted) / BINS
    for (i, perm) in enumerate(real_times_keys_sorted):
        perm_bins[ int(i / bin_size) ].append(perm)
    
    real_times_bins = [[real_times[perm] for perm in perm_bin] for perm_bin in perm_bins]
    cost_times_bins = [[cost_times[perm] for perm in perm_bin] for perm_bin in perm_bins]
    
    # Print results
    for b in range(BINS):
        print('-'*63)
        print(f'| BIN {b+1:3} / {BINS:<3} | {"MEAN":20} | {"STANDARD DEVIATION":20} |')
        print(f'|     Real Time | {np.mean(real_times_bins[b]):20.12f} | {np.std(real_times_bins[b]):20.12f} |')
        print(f'|     Cost Time | {np.mean(cost_times_bins[b]):20.12f} | {np.std(cost_times_bins[b]):20.12f} |')
    print('-'*63)