from benchmark.operations.get_query_instructions import get_real_instructions


def main(db_set:str, query:str, perm:list[int], skip_joins=False, manual_parse=False):
    print(f'Running {db_set}/{query} with perm {perm}')

    print("Parsing the query...")
    instructions = get_real_instructions(db_set, query, manual_parse)

    print("Loading the tables...")
    dfs = instructions.s1_init()
    
    print("Running filters...")
    for instruction in instructions.s2_filters:
        instruction(dfs)

    if skip_joins:
        print('Done loading and filtering, joins skipped.')
        exit(0)
        
    print("Running joins...")
    for p in perm:
        instructions.s3_joins[p](dfs)

    if len(dfs) == 1:
        print('Completed successfully')
        tree = list(dfs.keys())[0]
        print(f'Tree: {tree}')
        print(f'# of rows: {len(dfs[tree])}')
        # dfs[tree].to_csv('result.csv')
    else:
        print('Failed execution')
        exit(1)
