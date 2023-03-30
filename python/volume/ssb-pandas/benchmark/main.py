from math import factorial
import itertools
import numpy as np
import time
from benchmark.operations.get import get_approx_instructs, get_instructions

from benchmark.tools import clone, get_stats, print_write

def main(query):
    out_file = open(f"results/{query}.txt", "a")
    # print_write(f'Started running benchmark for query {query}.', out_file)
    print(f'Started running benchmark for query {query}.')
    
    instructions = get_instructions(query)
    approx_ins = get_approx_instructs(query)

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
    
    print_write(f'permutation;execution_tree;approx_time;actual_time', out_file)
    for job in jobs:
        dfs = instructions[0][0]()
        approx_data["schema"] = approx_ins[0][0]()
        
        approx_time = 0
        for ins in job:
            approx_time += approx_ins[1][ins](approx_data)
        
        start_time = time.time()
        for ins in job:
            instructions[1][ins](dfs)
        actual_time = time.time() - start_time
        
        print_write(f'{job};{list(dfs.keys())[0]};{approx_time};{actual_time}', out_file)
