def get_schema(db_name):
    return {
        "ssb": {
            "lineorder": ["lo_orderkey", "lo_linenumber", "lo_custkey", "lo_partkey", "lo_suppkey", "lo_orderdate", "lo_orderpriority", "lo_shippriority", "lo_quantity", "lo_extendedprice", "lo_ordtotalprice", "lo_discount", "lo_revenue", "lo_supplycost", "lo_tax", "lo_commitdate", "lo_shopmode"],
            "part": ["p_partkey", "p_name", "p_mfgr", "p_category", "p_brand1", "p_color", "p_type", "p_size", "p_container"],
            "supplier": ["s_suppkey", "s_name", "s_address", "s_city", "s_nation", "s_region", "s_phone"],
            "customer": ["c_custkey", "c_name", "c_address", "c_city", "c_nation", "c_region", "c_phone", "c_mktsegment"],
            "date": ["d_datekey", "d_date", "d_dayofweek", "d_month", "d_year", "d_yearmonthnum", "d_yearmonth", "d_daynuminweek", "d_daynuminmonth", "d_daynuminyear", "d_monthnuminyear", "d_weeknuminyear", "d_sellingseasin", "d_lastdayinweekfl", "d_lastdayinmonthfl", "d_holidayfl", "d_weekdayfl"],
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
