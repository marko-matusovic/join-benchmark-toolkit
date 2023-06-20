from math import factorial
import itertools
import numpy as np
import time
from benchmark.operations.get import get_approx_time_instructions, get_real_instructions

from benchmark.util import clone, get_stats, print_write

def main(query):
    out_file = open(f"results/{query}.csv", "a")
    # print_write(f'Started running benchmark for query {query}.', out_file)
    print(f'Started running benchmark for query {query}.')
    
    instructions = get_real_instructions(query)
    approx_ins = get_approx_time_instructions(query)

    jobs = np.array([j for j in itertools.permutations(range(len(instructions[1])))])
    np.random.shuffle(jobs)
    # print_write(f'Generated {factorial(len(instructions[1]))} permutations.', out_file)
    print(f'Generated {factorial(len(instructions[1]))} permutations.')
    
    permutations = calc_permutations(instructions, jobs)
    
    print(f'With {len(permutations)} unique execution paths.')
    
    unique_jobs = [p[0] for p in permutations.values()]
    
    run_all_jobs(instructions, approx_ins, unique_jobs, out_file)
    
    print(f'Done')
    
def calc_permutations(instructions, jobs):
    dfs = instructions[0][0]()
    for key in dfs:
        dfs[key].drop(dfs[key].index, inplace=True)
    
    permutations = {}
    for job in jobs:
        copy = clone(dfs)
        for ins in job:
            instructions[1][ins](copy)
        
        end_tbl = list(copy.keys())[0]
        if end_tbl not in permutations:
            permutations[end_tbl] = []
        permutations[end_tbl].append(job)
    
    return permutations

def run_all_jobs(instructions, approx_ins, jobs, out_file):
    
    dfs = instructions[0][0]()
    approx_data = {
        "stats": {key: get_stats(dfs[key]) for key in dfs},
        "times": {}
    }
    
    # print_write(f'permutation;execution_tree;approx_time;actual_time', out_file)
    print(f'permutation;execution_tree;approx_time;actual_time')
    for job in jobs:
        
        dfs = instructions[0][0]()
        approx_data["schema"] = approx_ins[0][0]()
        
        print("approx: ", end="")
        approx_time = 0
        for ins in job:
            t = approx_ins[1][ins](approx_data)
            print(f'I[{ins}]={t:5f}', end=", ")
            approx_time += t
        print()
        
        start_time = time.time()
        print("actual: ", end="")
        for ins in job:
            part_time = time.time()
            instructions[1][ins](dfs)
            t = time.time() - part_time
            print(f'I[{ins}]={t:5f}', end=", ")
        print()
        actual_time = time.time() - start_time
        
        print(f'{job};{list(dfs.keys())[0]};{approx_time};{actual_time}')
        # print_write(f'{job};{list(dfs.keys())[0]};{approx_time};{actual_time}', out_file)
