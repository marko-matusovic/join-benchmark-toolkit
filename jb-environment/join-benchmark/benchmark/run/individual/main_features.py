import json
from benchmark.tools.query_parser import load_query, get_joins
from benchmark.operations.operations_costmodel import Data, Operations_CostModel, calc_age_mult, find_table, total_length_of_cluster
from benchmark.operations.query_instructions_service import get_instruction_set

def main(db_path:str, db_set:str, query:str, perm:list[int]|None=None, log_file:str|None=None, log_head='', manual_parse=False):
    if log_file == None:
        log_file = f'results/training_data/{db_set}/{query}/features.log'
    
    instructions = get_instruction_set(db_path, db_set, query, Operations_CostModel(), manual_parse)
    joins = get_joins(load_query(db_path, query))
    
    data: Data = instructions.s1_init()
    
    for instruction in instructions.s2_filters:
        instruction(data)

    if perm == None:
        perm = list(range(len(instructions.s3_joins)))
    for p in perm:
        # Get data for the join
        [field_1, field_2] = joins[p]
        features_1 = collect_features(data, field_1)
        features_2 = collect_features(data, field_2)
        # Execute the join
        instructions.s3_joins[p](data)
        
        table_1 = find_table(data.schema, field_1)
        table_2 = find_table(data.schema, field_2)
        
        features_mix = json.dumps({
            'selectivity': data.selects[table_1][-1] * data.selects[table_2][-1]
        })
        
        with open(log_file, 'a') as fout:
            fout.write(f'{log_head};{p};{features_1};{features_2};{features_mix}\n')
        
def collect_features(data:Data, field_name:str) -> str:
    table = find_table(data.schema, field_name)
    short_field_name = field_name.split('.')[-1]
    
    cluster = data.clusters[table]
    
    return json.dumps({
        'length': total_length_of_cluster(data, cluster),
        'unique': data.stats[table].column[short_field_name].unique,
        'row_size': sum([v.dtype for tbl in cluster for v in data.stats[tbl].column.values()]),
        'cache_age': calc_age_mult(data, table)
    })
