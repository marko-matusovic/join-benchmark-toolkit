from typing import TypeVar
from benchmark.operations.get import QueryInstructions
from benchmark.operations.operations import Operations
'''
# QUERY
| select sum(lo_revenue), d_year, p_brand1
| from lineorder, ddate, part, supplier
| where lo_orderdate = d_datekey
| and lo_partkey = p_partkey
| and lo_suppkey = s_suppkey
| and p_category = 'MFGR#12'
| and s_region = 'AMERICA'
| group by d_year, p_brand1
| order by d_year, p_brand1
'''
I = TypeVar('I')
O = TypeVar('O')

def instruction_set(operation_set: Operations[I,O]) -> QueryInstructions[I, O]:
    return QueryInstructions(
        s1_init = operation_set.from_tables('ssb', ["lineorder", "date", "part", "supplier"], []),
        s2_filters = [
            operation_set.filter_field_eq("p_category", ["MFGR#12"]),
            operation_set.filter_field_eq("s_region", ["AMERICA"]),
        ],
        s3_joins = [
            operation_set.join_fields("lo_orderdate", "d_datekey"),
            operation_set.join_fields("lo_partkey", "p_partkey"),
            operation_set.join_fields("lo_suppkey", "s_suppkey"),
        ],
        s4_aggregation = [
            # group by
            # order by
            # select
        ]
    )
