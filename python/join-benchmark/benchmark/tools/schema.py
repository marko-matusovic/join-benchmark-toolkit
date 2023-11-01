import json
from os.path import exists
import re

TSchema = dict[str, list[str]]

def get_schema(db_name:str) -> TSchema:
    # schemas = {
        # OUTDATED SCHEMA, I ADJUSTED IT WHEN I DID MANUAL PARSING
        # "ssb": {
        #     "lineorder": ["orderkey", "linenumber", "custkey", "partkey", "suppkey", "orderdate", "orderpriority", "shippriority", "quantity", "extendedprice", "ordtotalprice", "discount", "revenue", "supplycost", "tax", "commitdate", "shopmode"],
        #     "part": ["partkey", "name", "mfgr", "category", "brand1", "color", "type", "size", "container"],
        #     "supplier": ["suppkey", "name", "address", "city", "nation", "region", "phone"],
        #     "customer": ["custkey", "name", "address", "city", "nation", "region", "phone", "mktsegment"],
        #     "date": ["datekey", "date", "dayofweek", "month", "year", "yearmonthnum", "yearmonth", "daynuminweek", "daynuminmonth", "daynuminyear", "monthnuminyear", "weeknuminyear", "sellingseasin", "lastdayinweekfl", "lastdayinmonthfl", "holidayfl", "weekdayfl"],
        # },
        # "ssb": {
        #     "lineorder": ["lo_orderkey", "lo_linenumber", "lo_custkey", "lo_partkey", "lo_suppkey", "lo_orderdate", "lo_orderpriority", "lo_shippriority", "lo_quantity", "lo_extendedprice", "lo_ordtotalprice", "lo_discount", "lo_revenue", "lo_supplycost", "lo_tax", "lo_commitdate", "lo_shopmode"],
        #     "part": [ "p_partkey", "p_name", "p_mfgr", "p_category", "p_brand1", "p_color", "p_type", "p_size", "p_container"],
        #     "supplier": ["s_suppkey", "s_name", "s_address", "s_city", "s_nation", "s_region", "s_phone"],
        #     "customer": ["c_custkey", "c_name", "c_address", "c_city", "c_nation", "c_region", "c_phone", "c_mktsegment"],
        #     "ddate": ["d_datekey", "d_date", "d_dayofweek", "d_month", "d_year", "d_yearmonthnum", "d_yearmonth", "d_daynuminweek", "d_daynuminmonth", "d_daynuminyear", "d_monthnuminyear", "d_weeknuminyear", "d_sellingseasin", "d_lastdayinweekfl", "d_lastdayinmonthfl", "d_holidayfl", "d_weekdayfl"]
        # },
        # "job": {
        #     "aka_name": ["id", "person_id", "name", "imdb_index", "name_pcode_cf", "name_pcode_nf", "surname_pcode", "md5sum",],
        #     "aka_title": ["id", "movie_id", "title", "imdb_index", "kind_id", "production_year", "phonetic_code", "episode_of_id", "season_nr", "episode_nr", "note", "md5sum",],
        #     "cast_info": ["id", "person_id", "movie_id", "person_role_id", "note", "nr_order", "role_id",],
        #     "char_name": ["id", "name", "imdb_index", "imdb_id", "name_pcode_nf", "surname_pcode", "md5sum",],
        #     "comp_cast_type": ["id", "kind",],
        #     "company_name": ["id", "name", "country_code", "imdb_id", "name_pcode_nf", "name_pcode_sf", "md5sum",],
        #     "company_type": ["id", "kind",],
        #     "complete_cast": ["id", "movie_id", "subject_id", "status_id"],
        #     "info_type": ["id", "info",],
        #     "keyword": ["id", "keyword", "phonetic_code",],
        #     "kind_type": ["id", "kind",],
        #     "link_type": ["id", "link",],
        #     "movie_companies": ["id", "movie_id", "company_id", "company_type_id", "note",],
        #     "movie_info": ["id", "movie_id", "info_type_id", "info", "note",],
        #     "movie_info_idx": ["id", "movie_id", "info_type_id", "info", "note",],
        #     "movie_keyword": ["id", "movie_id", "keyword_id",],
        #     "movie_link": ["id", "movie_id", "linked_movie_id", "link_type_id",],
        #     "name": ["id", "name", "imdb_index", "imdb_id", "gender", "name_pcode_cf", "name_pcode_nf", "surname_pcode", "md5sum",],
        #     "person_info": ["id", "person_id", "info_type_id", "info", "note",],
        #     "role_type": ["id", "role",],
        #     "title": ["id", "title", "imdb_index", "kind_id", "production_year", "imdb_id", "phonetic_code", "episode_of_id", "season_nr", "episode_nr", "series_years", "md5sum",],
        # }
    # }
    # if db_name in schemas:
    #     return schemas[db_name]
    
    # if exists(f'./data/{db_name}/schema_cached.json'):
    #     return load_from_cache(db_name)
    if exists(f'./data/{db_name}/schema.sql'):
        schema = load_from_file(db_name)
        save_to_cache(db_name, schema)
        return schema
    print(f"No schema found for db {db_name}")
    exit(1)

def rename_schema(schema: TSchema, tables: list[str], labels: list[str]) -> TSchema:
    return {
        label: [ f'{label}.{col}' for col in schema[table] ]
        for (table, label) in zip(tables, labels)
    }

def load_from_file(db_name:str) -> TSchema:
    schema = {}
    fin = open(f'./data/{db_name}/schema.sql', 'r')
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
                i = columns.find(",", next_bre) + 1
                j = columns.find(" ", i)
            else:
                i = next_col + 1
                j = columns.find(" ", i)
    
    return schema

def load_from_cache(db_name:str) -> TSchema:
    with open(f"./data/{db_name}/schema_cached.json", "r") as fin:
        return json.load(fin)

def save_to_cache(db_name:str, schema:TSchema) -> None:
    with open(f"./data/{db_name}/schema_cached.json", "w") as fout:
        fout.write(json.dumps(schema))
