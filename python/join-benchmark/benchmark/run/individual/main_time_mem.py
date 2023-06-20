import time
import tracemalloc
from benchmark.operations.get import get_real_instructions


def main(db_set:str, query:str, perm:list[int]):
    tracemalloc.start()
    start_time = time.time()
    
    instructions = get_real_instructions(db_set, query)

    dfs = instructions[0][0]()
    
    mem_load = tracemalloc.get_traced_memory()[1]
    tracemalloc.reset_peak()
    time_load = time.time() - start_time

    for instruction in instructions[1]:
        instruction(dfs)

    mem_filters = tracemalloc.get_traced_memory()[1]
    time_filters = time.time() - start_time
    
    time_joins = []
    mem_joins = []
    
    for p in perm:
        tracemalloc.reset_peak()
        instructions[2][p](dfs)
        time_joins.append(time.time() - start_time)
        mem_joins.append(tracemalloc.get_traced_memory()[1])

    time_total = time.time() - start_time
    mem_peak = max(mem_joins)

    # dfs[list(dfs.keys())[0]].to_csv('output-job-20a.csv', header=True, index=True)
    
    print('join_order;execution_tree;time_total;mem_peak;time_load;mem_load;time_filters;mem_filters;time_joins;mem_joins')
    print(f'{perm};{list(dfs.keys())[0]};{time_total};{mem_peak};{time_load};{mem_load};{time_filters};{mem_filters};{time_joins};{mem_joins}')
    with open(f'results/time_mem/{db_set}/{query}.csv', 'a') as file:
        file.write(f'{perm};{list(dfs.keys())[0]};{time_total};{mem_peak};{time_load};{mem_load};{time_filters};{mem_filters};{time_joins};{mem_joins}\n')
    