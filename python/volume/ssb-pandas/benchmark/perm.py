from math import factorial
from benchmark.load import load_files
from benchmark.queries.q41 import *
import itertools
import numpy as np
import threading

def main():
    dfs = load_files()
    instructions = instruction_set()

    jobs = np.array([j for j in itertools.permutations(range(len(instructions[0])))])
    np.random.shuffle(jobs)
    print(f'Generated {factorial(len(instructions[0]))} permutations.')
    
    thread_count = 1
    for key in dfs:
        dfs[key].drop(dfs[key].index, inplace=True)
    
    jobs_chunks = np.array_split(jobs, thread_count)
    set_perm = {}
    
    threads = {}
    for i in range(thread_count):
        threads[i] = threading.Thread(target=execute_job_pool, args=(dfs, instructions, jobs_chunks[i], set_perm))
        threads[i].start()
    
    for i in range(thread_count):
        threads[i].join()
        
    print(f"detected {len(set_perm)} unique permutations")
    
    fout = open("perms.txt", "w")
    for tree in set_perm:
        fout.write(f'{set_perm[tree]} -> {tree}')
    fout.close()
    
    print("done")
    
def execute_job_pool(dfs, instructions, jobs, set_perm):
    for job in jobs:    
        copy = clone(dfs)
        
        for ins in job:
            instructions[0][ins](copy)
            pass
        
        end_tbl = list(copy.keys())[0]
        if end_tbl not in set_perm:
            set_perm[end_tbl] = job

def clone(dfs: dict[str, DataFrame]) -> dict[str, DataFrame]:
    return {key: dfs[key].copy() for key in dfs}