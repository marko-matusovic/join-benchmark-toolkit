import json
from os.path import exists
import re

TSchema = dict[str, list[str]]

def get_schema(db_path:str, db_name:str) -> TSchema:
    # if exists(f'{db_path}/schema_cached.json'):
    #     return load_from_cache(db_path, db_name)
    if exists(f'{db_path}/schema.sql'):
        schema = load_from_file(db_path)
        # save_to_cache(db_path, db_name, schema)
        return schema
    print(f"No schema found for db {db_name}")
    exit(1)

def rename_schema(schema: TSchema, tables: list[str], labels: list[str]) -> TSchema:
    return {
        label: [ f'{label}.{col}' for col in schema[table] ]
        for (table, label) in zip(tables, labels)
    }

def load_from_file(db_path:str) -> TSchema:
    schema = {}
    fin = open(f'{db_path}/schema.sql', 'r')
    lines = fin.readlines()
    lines = [line.strip() for line in lines if not line.strip().startswith('--')]
    clause = re.sub('[\\n\\t\\ ]+', ' ', ''.join(lines))
    tables = clause.split(';')[:-1]
    # remove front and end, extract which table it is
    for table in tables:
        table = table.strip()
        if not table.lower().startswith("create table "):
            print(f"Error: unexpected clause in the schema {table}")
            exit(1)
        table = table[13:-1].strip()
        (table_name, _brk, columns) = table.partition("(")
        table_name = table_name.strip()
        schema[table_name] = []
        i = 0
        j = min(columns.find(" "), columns.find(","))
        while True:
            if j == "-1" :
                break
            
            token = columns[i:j].strip()
                
            if token.lower() != 'primary':
                schema[table_name].append(token.strip())
            
            next_brs = columns.find("(", j+1)
            next_bre = columns.find(")", j+1)
            next_col = columns.find(",", j+1)
            if next_col == -1:
                break
            if next_brs != -1 and next_brs < next_col:
                next_col = columns.find(",", next_bre)
                if next_col == -1:
                    break
                i = next_col + 1
                j = columns.find(" ", i)
            else:
                i = next_col + 1
                j = columns.find(" ", i)
    
    return schema

# # ===== CACHING MIGHT PRODUCE INCONSISTENT MEASUREMENTS ===== 
# def load_from_cache(db_path:str, db_name:str) -> TSchema:
#     with open(f"{db_path}/schema_cached.json", "r") as fin:
#         return json.load(fin)

# def save_to_cache(db_path:str, db_name:str, schema:TSchema) -> None:
#     with open(f"{db_path}/schema_cached.json", "w") as fout:
#         fout.write(json.dumps(schema))
