from benchmark.operations.get_query_instructions import get_execution_tree_instructions


def main(db_path:str, db_set:str, query:str, manual_parse=False):
    print(f'Parsing {db_set}/{query} ...')
    
    instructions = get_execution_tree_instructions(db_path, db_set, query, manual_parse)
    
    print('Parsing finished!')
    print('Compiling the execution tree...')

    data = instructions.s1_init()
    
    for filter in instructions.s2_filters:
        filter(data)

    for join in instructions.s3_joins:
        join(data)

    trees = list(set(data.cluster_names.values()))
    if len(trees) == 1:
        print('Execution tree: ')
        print(trees[0])
    else:
        print('Execution trees: ')
        for tree in trees:
            print(tree)
