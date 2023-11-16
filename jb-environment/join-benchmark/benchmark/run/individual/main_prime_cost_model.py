from benchmark.operations.operations_costmodel import Data, Operations_CostModel
from benchmark.operations.query_instructions import get_instruction_set
from time import time;


def main(db_path:str, db_set:str, query:str, perm:list[int], log_file, log_head, manual_parse=False):
    instructions = get_instruction_set(db_path, db_set, query, Operations_CostModel(), manual_parse)
    
    data: Data = instructions.s1_init()
    
    for instruction in instructions.s2_filters:
        instruction(data)

    for p in perm:
        instructions.s3_joins[p](data)
