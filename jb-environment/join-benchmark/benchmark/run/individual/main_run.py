from benchmark.operations.get_query_instructions import get_real_instructions
from time import time;


def main(db_path:str, db_set:str, query:str, perm:list[int], skip_joins=False, manual_parse=False, log_file='', log_head=''):
    print(f'Running {db_set}/{query} with perm {perm}')
    
    start = time()
    
    print("Parsing the query...")
    instructions = get_real_instructions(db_path, db_set, query, manual_parse)
    parse = time()
    
    print("Loading the tables...")
    dfs = instructions.s1_init()
    overhead = time()
    
    print("Running filters...")
    filters = []
    for instruction in instructions.s2_filters:
        instruction(dfs)
        filters.append(time())

    if skip_joins:
        print('Done loading and filtering, joins skipped.')
        if log_file != '':
            with open(log_file, 'a') as file_out:
                file_out.write(f'{log_head};201;{print_times(start, parse, overhead, filters, [])}\n')
        exit(0)
        
    print("Running joins...")
    joins = []
    for p in perm:
        instructions.s3_joins[p](dfs)
        joins.append(time())

    if len(dfs) == 1:
        print('Completed successfully')
        tree = list(dfs.keys())[0]
        print(f'Tree: {tree}')
        print(f'# of rows: {len(dfs[tree])}')
        if log_file != '':
            with open(log_file, 'a') as file_out:
                file_out.write(f'{log_head};200;{print_times(start, parse, overhead, filters, joins)}\n')
    else:
        print('Failed execution')
        if log_file != '':
            with open(log_file, 'a') as file_out:
                file_out.write(f'{log_head};500;{print_times(start, parse, overhead, filters, joins)}\n')
        exit(1)

def print_times(start:float, parse:float, overhead:float, filters:list[float], joins:list[float]):
    return f'{parse - start};{overhead - parse};{format_times(overhead, filters)};{format_times(filters[-1], joins)}'

def format_times(fst:float, arr:list[float]):
    # all = [fst] + arr
    # for i, t0 in enumerate(all[:-1]):
    #     t1 = all[i+1]
    #     dt = t1 - t0
    ### as list comprehension:
    return ','.join([str(t - (arr[i-1] if i>0 else fst)) for i,t in enumerate(arr)])
    
