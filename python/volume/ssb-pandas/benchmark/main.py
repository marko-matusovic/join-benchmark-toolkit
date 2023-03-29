from io import TextIOWrapper
from math import factorial
from benchmark.load import load_files
from benchmark.queries.q31 import *
import itertools
import numpy as np
import time
import threading

def main():
    dfs = load_files()
    instructions = instruction_set()

    jobs = np.array([j for j in itertools.permutations(range(len(instructions[0])))])
    np.random.shuffle(jobs)
    print(f'Generated {factorial(len(instructions[0]))} permutations.')
    
    thread_count = 1
    
    out_file = open("results(MBP)/q31.txt", "a")
    write_lock = threading.Lock()
    jobs_chunks = np.array_split(jobs, thread_count)
    
    threads = {}
    for i in range(thread_count):
        threads[i] = threading.Thread(target=execute_job_pool, args=(dfs, instructions, jobs_chunks[i], out_file, write_lock))
        threads[i].start()
    
    for i in range(thread_count):
        threads[i].join()
    
    print("done")
    
def execute_job_pool(dfs, instructions, jobs, out_file: TextIOWrapper, write_lock):
    for job in jobs:    
        copy = clone(dfs)
        start_time = time.time()
        for ins in job:
            instructions[0][ins](copy)
            pass
        stop_time = time.time()
        msg = f'Permutation {job} produces {list(copy.keys())[0]} takes {stop_time - start_time} seconds.'
        with write_lock:
            print(msg)
            out_file.write(f'{msg}\n')
            out_file.flush()

def clone(dfs: dict[str, DataFrame]) -> dict[str, DataFrame]:
    return {key: dfs[key].copy() for key in dfs}