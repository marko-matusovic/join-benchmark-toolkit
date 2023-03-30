def get_schema():
    return {
        "lineorder": ["lo_orderkey","lo_linenumber","lo_custkey","lo_partkey","lo_suppkey","lo_orderdate","lo_orderpriority","lo_shippriority","lo_quantity","lo_extendedprice","lo_ordtotalprice","lo_discount","lo_revenue","lo_supplycost","lo_tax","lo_commitdate","lo_shopmode"],
        "part": ["p_partkey","p_name","p_mfgr","p_category","p_brand1","p_color","p_type","p_size","p_container"],
        "supplier": ["s_suppkey","s_name","s_address","s_city","s_nation","s_region","s_phone"],
        "customer": ["c_custkey","c_name","c_address","c_city","c_nation","c_region","c_phone","c_mktsegment"],
        "date": ["d_datekey","d_date","d_dayofweek","d_month","d_year","d_yearmonthnum","d_yearmonth","d_daynuminweek","d_daynuminmonth","d_daynuminyear","d_monthnuminyear","d_weeknuminyear","d_sellingseasin","d_lastdayinweekfl","d_lastdayinmonthfl","d_holidayfl","d_weekdayfl"],
    }