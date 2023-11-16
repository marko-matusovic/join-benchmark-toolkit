from benchmark.tools.query_parser import get_joins
from benchmark.operations.operations_costmodel import Data, Operations_CostModel, find_table
from benchmark.operations.query_instructions import get_instruction_set
from time import time;


def main(db_path:str, db_set:str, query:str, perm:list[int], log_file, log_head, manual_parse=False):
    instructions = get_instruction_set(db_path, db_set, query, Operations_CostModel(), manual_parse)
    joins = get_joins(db_path, db_set, query)
    
    data: Data = instructions.s1_init()
    
    for instruction in instructions.s2_filters:
        instruction(data)

    for p in perm:
        # Get data for the join
        [field_1, field_2] = joins[p]
        table_1 = find_table(data.schema, field_1)
        table_2 = find_table(data.schema, field_2)
        
        data.stats[table_1].length
        data.stats[table_1].column[field_1].unique
        data.stats[table_1].column[field_1].dtype
        [col.dtype for col in data.stats[table_1].column.values()]
        
        # Execute the join
        instructions.s3_joins[p](data)
