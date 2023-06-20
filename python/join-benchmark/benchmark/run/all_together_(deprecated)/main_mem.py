from math import factorial
import itertools
import numpy as np
import time
import tracemalloc
from benchmark.operations.get import get_approx_instructs, get_real_instructions
from benchmark.tools.tools import print_write

def main(query):
    out_file = open(f"results(mem)/{query}.csv", "a")
    # print_write(f'Started running benchmark for query {query}.', out_file)
    print(f'Started running benchmark for query {query}.')
    
    instructions = get_real_instructions('ssb', query)
    approx_ins = get_approx_instructs('ssb', query)

    jobs = np.array([j for j in itertools.permutations(range(len(instructions.s2_filters)))])
    np.random.shuffle(jobs)
    # print_write(f'Generated {factorial(len(instructions.s2_filters))} permutations.', out_file)
    print(f'Generated {factorial(len(instructions.s2_filters))} permutations.')
    
    run_all_jobs(instructions, jobs, out_file)
    
    print(f'Done')
    
def run_all_jobs(instructions, jobs, out_file):
    
    print_write(f'permutation;execution_tree;actual_time;actual_mem_peak', out_file)
    for job in jobs:
        
        tracemalloc.start()
        cur_mem = tracemalloc.get_traced_memory()[0]
        
        dfs = instructions.s1_init()
        
        start_time = time.time()
        
        for ins in job:
            instructions.s2_filters[ins](dfs)
        
        actual_time = time.time() - start_time
        actual_mem_pk = tracemalloc.get_traced_memory()[1] - cur_mem
        tracemalloc.stop()
        
        print_write(f'{job};{list(dfs.keys())[0]};{actual_time};{actual_mem_pk}', out_file)
