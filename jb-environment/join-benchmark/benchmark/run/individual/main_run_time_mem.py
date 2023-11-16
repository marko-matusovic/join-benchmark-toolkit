import time
import tracemalloc
from benchmark.operations.get_query_instructions import get_real_instructions


def main(db_path:str, db_set:str, query:str, perm:list[int], skip_joins=False, manual_parse=False, log_file='', log_head=''):
    print(f'Running {db_set}/{query} with perm {perm}')
    
    if log_file == '':
        print("ERROR: missing the log file parameter!")
        exit(1)

    tracemalloc.start()
    start_time = time.time()
    
    instructions = get_real_instructions(db_path, db_set, query)

    dfs = instructions.s1_init()
    
    mem_load = tracemalloc.get_traced_memory()[1]
    tracemalloc.reset_peak()
    time_load = time.time() - start_time

    for filter in instructions.s2_filters:
        filter(dfs)
        
    mem_filters = tracemalloc.get_traced_memory()[1]
    time_filters = time.time() - start_time
    
    if skip_joins:
        print('Done loading and filtering, joins skipped.')
        time_total = time.time() - start_time
        with open(log_file, 'a') as file_out:
            file_out.write(f'{log_head};{time_total};{mem_filters};{time_load};{mem_load};{time_filters};{mem_filters};;\n')
        exit(0)
    
    time_joins:list[float] = []
    mem_joins:list[float] = []
    
    for p in perm:
        tracemalloc.reset_peak()
        instructions.s3_joins[p](dfs)
        time_joins.append(time.time() - start_time)
        mem_joins.append(tracemalloc.get_traced_memory()[1])

    time_total = time.time() - start_time
    mem_peak = max(mem_joins)

    # # print the results into csv file
    # dfs[list(dfs.keys())[0]].to_csv('output-job-20a.csv', header=True, index=True)
    
    # # log file header
    # print('join_order;execution_tree;time_total;mem_peak;time_load;mem_load;time_filters;mem_filters;time_joins;mem_joins')
    
    with open(log_file, 'a') as file_out:
        file_out.write(f'{log_head};{time_total};{mem_peak};{time_load};{mem_load};{time_filters};{mem_filters};{time_joins};{mem_joins}\n')
    