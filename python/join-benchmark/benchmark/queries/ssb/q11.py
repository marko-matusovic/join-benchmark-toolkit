from typing import TypeVar
from benchmark.operations.operations import Operations
from benchmark.operations.query_instructions import QueryInstructions
'''
# QUERY
| select sum(lo_extendedprice*lo_discount) as revenue
| from lineorder, ddate
| where lo_orderdate = d_datekey
| and d_year = 1993
| and lo_discount between 1 and 3
| and lo_quantity < 25
'''

I = TypeVar('I')
O = TypeVar('O')

def instruction_set(operation_set: Operations[I,O]) -> QueryInstructions[I, O]:
    return QueryInstructions(
        s1_init = operation_set.from_tables('ssb', ["lineorder", "date"], ["lo", "d"]),
        s2_filters = [
            operation_set.filter_field_eq("d.year", [1993]),
            operation_set.filter_field_ge("lo.discount", 1),
            operation_set.filter_field_le("lo.discount", 3),
            operation_set.filter_field_lt("lo.quantity", 25),
        ],
        s3_joins = [
            operation_set.join_fields("lo.orderdate", "d.datekey"),
        ],
        s4_aggregation = [
            # select
        ]
    )
