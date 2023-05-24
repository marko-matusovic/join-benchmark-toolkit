import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd

if __name__ == '__main__':
    query = sys.argv[1]
    
    # 'join_order;times...'
    df = pd.read_csv(f"results/time_mem/{query}.csv", sep=';')
    df = df[df['join_order'].str.startswith("//") == False]
    
    
    
    plt.title(f'Execution Time vs Peak Memory Use\nper Random Join Orders of {query}')
    plt.xlabel('time [s]')
    plt.ylabel('memory [B]')
    
    if '-e' in sys.argv:
        plt.errorbar(x=times_mean, y=mem_mean, xerr=times_err, yerr=mem_err, fmt='o')
    else:
        plt.scatter(x=times_mean, y=mem_mean)
    
    plt.show()