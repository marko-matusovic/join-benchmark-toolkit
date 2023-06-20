from benchmark.operations.get import get_real_instructions


def main(db_set:str, query:str, perm:list[int]):
    print(f'Running {db_set}/{query} with perm {perm}')
    
    instructions = get_real_instructions(db_set, query)

    dfs = instructions.s1_init()
    
    for instruction in instructions.s2_filters:
        instruction(dfs)

    for p in perm:
        instructions.s3_joins[p](dfs)

    if len(dfs) == 1:
        print('Completed successfully')
        tree = list(dfs.keys())[0]
        print(f'Tree: {tree}')
        print(f'# of rows: {len(dfs[tree])}')
        dfs[tree].to_csv('result.csv')
    else:
        print('Failed execution')
        exit(1)
