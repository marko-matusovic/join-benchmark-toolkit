from benchmark.operations.get import get_real_instructions


def main(db_set, query, perm):
    print(f'Running {db_set}/{query} with perm {perm}')
    
    instructions = get_real_instructions(db_set, query)

    dfs = instructions[0][0]()
    
    for instruction in instructions[1]:
        instruction(dfs)

    for p in perm:
        instructions[2][p](dfs)

    print(f'Completed succesfully')
