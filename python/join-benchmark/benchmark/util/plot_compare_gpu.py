import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd

def calc_print_plot_bins(real_data, cost_model_data, label, unit):
    BINS = int(sys.argv[sys.argv.index('-b') + 1]) if '-b' in sys.argv else 10
    perm_bins = [[] for _ in range(BINS)]
    
    method = sys.argv[sys.argv.index('-m')+1] if '-m' in sys.argv else 'bin_width'
    
    if method == 'bin_size':
        real_data_keys_sorted = np.array(sorted(real_data, key=real_data.get))
        bin_size = len(real_data_keys_sorted) / BINS
        for (i, perm) in enumerate(real_data_keys_sorted):
            perm_bins[ int(i / bin_size) ].append(perm)
    
    elif method == 'bin_width':
        bin_min = min(real_data.values())
        bin_max = max(real_data.values()) + 1E-9
        bin_width = (bin_max - bin_min) / BINS
        for (perm, time) in real_data.items():
            perm_bins[ int((time - bin_min) / bin_width) ].append(perm)
    
    real_data_bins = [[real_data[perm] for perm in perm_bin] for perm_bin in perm_bins]
    cost_model_data_bins = [[cost_model_data[perm] for perm in perm_bin] for perm_bin in perm_bins]
    
    # Print results
    for b in range(BINS):
        print('-'*95)
        print(f'| BIN {b+1:3}/{BINS:<3} SIZE {len(perm_bins[b]):<8} | {"MEAN":30} | {"STANDARD DEVIATION":30} |')
        print(f'| {"Real "+label:>25} | {np.mean(real_data_bins[b]):30.8f} | {np.std(real_data_bins[b]):30.8f} |')
        print(f'| {"Cost "+label:>25} | {np.mean(cost_model_data_bins[b]):30.8f} | {np.std(cost_model_data_bins[b]):30.8f} |')
    print('-'*95)
    
    bin_lables = [f'Bin {i+1}' for i in range(BINS)]
    data = {
        'measurement': real_data_bins,
        'cost model': cost_model_data_bins,
    }

    x = np.arange(len(bin_lables))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

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
    ax.set_ylabel(f'{label} ({unit})')
    ax.set_title(f'Measurement and Cost Model {label} Comparison')
    ax.set_xticks(x + width, bin_lables)
    ax.legend(loc='upper left', ncols=len(data))

    plt.savefig(f'results/figs/cost-comparison/gpu/{query}/{label.lower()}.png', dpi=250)

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
    
    real_times = {perm: stats[perm]["time"]['mean'] for perm in stats}
    df_approx = pd.read_csv(open(f'results/approx_time_mem/{query}.csv', 'r'), comment='/', sep=';')
    cost_model_times = {
        df_approx['permutation'][i] : df_approx['time_cost'][i] 
        for i in range(len(df_approx.index))
    }
    calc_print_plot_bins(real_times, cost_model_times, "Time", "s")
    
    real_mem_sum = {perm: stats[perm]["memory"]['read']["sum"] for perm in stats}
    cost_model_mem_sum = {
        df_approx['permutation'][i] : df_approx['memory_sum_cost'][i] 
        for i in range(len(df_approx.index))
    }
    calc_print_plot_bins(real_mem_sum, cost_model_mem_sum, "Read Memory Sum", "B")
    
    real_mem_max = {perm: stats[perm]["memory"]['read']["max"] for perm in stats}
    cost_model_mem_max = {
        df_approx['permutation'][i] : df_approx['memory_max_cost'][i] 
        for i in range(len(df_approx.index))
    }
    calc_print_plot_bins(real_mem_max, cost_model_mem_max, "Read Memory Max", "B")
    