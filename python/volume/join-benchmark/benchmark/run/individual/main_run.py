from benchmark.operations.get import get_real_instructions


def main(db_set, query, perm):
    instructions = get_real_instructions(db_set, query)

    dfs = instructions[0][0]()
    
    for instruction in instructions[1]:
        instruction(dfs)

    for p in perm:
        instructions[2][p](dfs)
