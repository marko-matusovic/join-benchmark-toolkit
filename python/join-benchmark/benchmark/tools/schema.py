TSchema = dict[str, list[str]]

def get_schema(db_name:str) -> TSchema:
    return {
        # OUTDATED SCHEMA, I ADJUSTED IT WHEN I DID MANUAL PARSING
        # "ssb": {
        #     "lineorder": ["orderkey", "linenumber", "custkey", "partkey", "suppkey", "orderdate", "orderpriority", "shippriority", "quantity", "extendedprice", "ordtotalprice", "discount", "revenue", "supplycost", "tax", "commitdate", "shopmode"],
        #     "part": ["partkey", "name", "mfgr", "category", "brand1", "color", "type", "size", "container"],
        #     "supplier": ["suppkey", "name", "address", "city", "nation", "region", "phone"],
        #     "customer": ["custkey", "name", "address", "city", "nation", "region", "phone", "mktsegment"],
        #     "date": ["datekey", "date", "dayofweek", "month", "year", "yearmonthnum", "yearmonth", "daynuminweek", "daynuminmonth", "daynuminyear", "monthnuminyear", "weeknuminyear", "sellingseasin", "lastdayinweekfl", "lastdayinmonthfl", "holidayfl", "weekdayfl"],
        # },
        "ssb": {
            "lineorder": ["lo_orderkey", "lo_linenumber", "lo_custkey", "lo_partkey", "lo_suppkey", "lo_orderdate", "lo_orderpriority", "lo_shippriority", "lo_quantity", "lo_extendedprice", "lo_ordtotalprice", "lo_discount", "lo_revenue", "lo_supplycost", "lo_tax", "lo_commitdate", "lo_shopmode"],
            "part": [ "p_partkey", "p_name", "p_mfgr", "p_category", "p_brand1", "p_color", "p_type", "p_size", "p_container"],
            "supplier": ["s_suppkey", "s_name", "s_address", "s_city", "s_nation", "s_region", "s_phone"],
            "customer": ["c_custkey", "c_name", "c_address", "c_city", "c_nation", "c_region", "c_phone", "c_mktsegment"],
            "ddate": ["d_datekey", "d_date", "d_dayofweek", "d_month", "d_year", "d_yearmonthnum", "d_yearmonth", "d_daynuminweek", "d_daynuminmonth", "d_daynuminyear", "d_monthnuminyear", "d_weeknuminyear", "d_sellingseasin", "d_lastdayinweekfl", "d_lastdayinmonthfl", "d_holidayfl", "d_weekdayfl"]
        },
        "job": {
            "aka_name": ["id", "person_id", "name", "imdb_index", "name_pcode_cf", "name_pcode_nf", "surname_pcode", "md5sum",],
            "aka_title": ["id", "movie_id", "title", "imdb_index", "kind_id", "production_year", "phonetic_code", "episode_of_id", "season_nr", "episode_nr", "note", "md5sum",],
            "cast_info": ["id", "person_id", "movie_id", "person_role_id", "note", "nr_order", "role_id",],
            "char_name": ["id", "name", "imdb_index", "imdb_id", "name_pcode_nf", "surname_pcode", "md5sum",],
            "comp_cast_type": ["id", "kind",],
            "company_name": ["id", "name", "country_code", "imdb_id", "name_pcode_nf", "name_pcode_sf", "md5sum",],
            "company_type": ["id", "kind",],
            "complete_cast": ["id", "movie_id", "subject_id", "status_id"],
            "info_type": ["id", "info",],
            "keyword": ["id", "keyword", "phonetic_code",],
            "kind_type": ["id", "kind",],
            "link_type": ["id", "link",],
            "movie_companies": ["id", "movie_id", "company_id", "company_type_id", "note",],
            "movie_info": ["id", "movie_id", "info_type_id", "info", "note",],
            "movie_info_idx": ["id", "movie_id", "info_type_id", "info", "note",],
            "movie_keyword": ["id", "movie_id", "keyword_id",],
            "movie_link": ["id", "movie_id", "linked_movie_id", "link_type_id",],
            "name": ["id", "name", "imdb_index", "imdb_id", "gender", "name_pcode_cf", "name_pcode_nf", "surname_pcode", "md5sum",],
            "person_info": ["id", "person_id", "info_type_id", "info", "note",],
            "role_type": ["id", "role",],
            "title": ["id", "title", "imdb_index", "kind_id", "production_year", "imdb_id", "phonetic_code", "episode_of_id", "season_nr", "episode_nr", "series_years", "md5sum",],
        }
    }[db_name]

def rename_schema(schema: TSchema, tables: list[str], labels: list[str]) -> TSchema:
    return {
        label: [ f'{label}.{col}' for col in schema[table] ]
        for (table, label) in zip(tables, labels)
    }
