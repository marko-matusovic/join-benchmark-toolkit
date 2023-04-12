import time
import tracemalloc
from benchmark.operations.get import get_instructions


def main(db_set, query, perm):
    tracemalloc.start()
    start_time = time.time()
    
    instructions = get_instructions(db_set, query)

    dfs = instructions[0][0]()

    for instruction in instructions[1]:
        instruction(dfs)

    for p in perm:
        instructions[2][p](dfs)

    actual_time = time.time() - start_time
    mem_peak = tracemalloc.get_traced_memory()[1]

    print(f'{perm};{list(dfs.keys())[0]};{actual_time};{mem_peak}')
    with open(f'results/time_mem_fresh/{query}.csv', 'a') as file:
        file.write(f'{perm};{list(dfs.keys())[0]};{actual_time};{mem_peak}\n')
    