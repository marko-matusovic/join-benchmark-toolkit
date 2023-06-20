from typing import TypeVar
from benchmark.operations.get import QueryInstructions
from benchmark.operations.operations import Operations
'''
# QUERY
| select sum(lo_extendedprice*lo_discount) as revenue
| from lineorder, ddate
| where lo_orderdate = d_datekey
| and d_yearmonthnum = 199401
| and lo_discount between 4 and 6
| and lo_quantity between 26 and 35
'''

I = TypeVar('I')
O = TypeVar('O')

def instruction_set(operation_set: Operations[I,O]) -> QueryInstructions[I, O]:
    return QueryInstructions(
        s1_init = operation_set.from_tables('ssb', ["lineorder", "date"], []),
        s2_filters = [
            operation_set.filter_field_eq("d_yearmonthnum", [199401]),
            operation_set.filter_field_ge("lo_discount", 4),
            operation_set.filter_field_le("lo_discount", 6),
            operation_set.filter_field_ge("lo_quantity", 26),
            operation_set.filter_field_le("lo_quantity", 35),
        ],
        s3_joins = [
            operation_set.join_fields("lo_orderdate", "d_datekey"),
        ],
        s4_aggregation = [
            # select
        ]
    )
