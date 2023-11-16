from benchmark.engine.engine import DataFrame
from benchmark.operations.operations_real import Operations_Real
from benchmark.operations.query_instructions_service import get_instruction_set

def main(db_path:str, db_set:str, query:str, perm:list[int]):
# Parse the schema and the query into a set of instructions
    instructions = get_instruction_set(db_path, db_set, query, Operations_Real())

    # Verify required tables for the query exist
    dfs: dict[str, DataFrame] = instructions.s1_init()

    # Execute the statements in WHERE which only filter
    for instruction in instructions.s2_filters:
        instruction(dfs)

    # Execute the statements in WHERE which join tables
    for join in instructions.s3_joins:
        join(dfs)
