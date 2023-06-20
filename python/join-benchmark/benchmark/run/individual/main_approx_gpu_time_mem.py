from benchmark.operations.get import get_approx_time_instructions
from benchmark.util import get_stats, print_write
import time

def main(db_set, query, perm):
    print(f'Running {db_set}/{query} with perm {perm}')
    
    instructions = get_approx_time_instructions(db_set, query)

    dfs = instructions[0][0]()
    
    for instruction in instructions[1]:
        instruction(dfs)

    for p in perm:
        instructions[2][p](dfs)

    if len(dfs) == 1:
        print('Completed succesfully')
        tree = list(dfs.keys())[0]
        print(f'Tree: {tree}')
        print(f'# of rows: {len(dfs[tree])}')
        dfs[tree].to_csv('result.csv')
    else:
        print('Failed execution')
        exit(1)
