from math import factorial
from benchmark.load import load_files
from benchmark.queries import q11, q21, q31, q41
from pandas import DataFrame
import itertools
import numpy as np
import time

def get_instruction_set(query):
    if query == 'q11':
        return q11.instruction_set()
    elif query == 'q21':
        return q21.instruction_set()
    elif query == 'q31':
        return q31.instruction_set()
    elif query == 'q41':
        return q41.instruction_set()
    else:
        return None

def main(query):
    print(f'Started running benchmark for query {query}')
    
    dfs = load_files()
    instructions = get_instruction_set(query)

    jobs = np.array([j for j in itertools.permutations(range(len(instructions[1])))])
    np.random.shuffle(jobs)
    print(f'Generated {factorial(len(instructions[1]))} permutations.')
    
    permutations = calc_permutations(dfs, jobs, instructions)
    
    print(f'With {len(permutations)} unique execution paths.')
    
    out_file = open(f"results(MBP)/{query}.txt", "a")
    
    for job in jobs:
        copy = clone(dfs)
        start_time = time.time()
        instructions[0][0](copy)
        for ins in job:
            instructions[1][ins](copy)
            pass
        stop_time = time.time()
        msg = f'Permutation {job} produces {list(copy.keys())[0]} takes {stop_time - start_time} seconds.'
        print(msg)
        out_file.write(f'{msg}\n')
        out_file.flush()
    
    print("done")
    
def clone(dfs: dict[str, DataFrame]) -> dict[str, DataFrame]:
    return {key: dfs[key].copy() for key in dfs}

def calc_permutations(dfs, jobs, instructions):
    empty = clone(dfs)
    for key in empty:
        empty[key].drop(empty[key].index, inplace=True)
    
    permutations = {}
    for job in jobs:
        empty_copy = clone(empty)
        instructions[0][0](empty_copy)
        for ins in job:
            instructions[1][ins](empty_copy)
        
        end_tbl = list(empty_copy.keys())[0]
        if end_tbl not in permutations:
            permutations[end_tbl] = []
        permutations[end_tbl].append(job)
    
    return permutations