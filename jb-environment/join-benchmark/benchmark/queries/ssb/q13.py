from typing import TypeVar
from benchmark.operations.query_instructions import QueryInstructions
from benchmark.operations.operations import Operations
'''
# QUERY
| select sum(lo_extendedprice*lo_discount) as revenue
| from lineorder, ddate
| where lo_orderdate = d_datekey
| and d_weeknuminyear = 6
| and d_year = 1994
| and lo_discount between 5 and 7
| and lo_quantity between 26 and 35
'''
I = TypeVar('I')
O = TypeVar('O')

def instruction_set(db_path:str, operation_set: Operations[I,O]) -> QueryInstructions[I, O]:
    return QueryInstructions(
        s1_init = operation_set.from_tables(db_path, 'ssb', ["lineorder", "date"], ["lo", "d"]),
        s2_filters = [  
            operation_set.filter_field_eq("d.weeknuminyear", [6]),
            operation_set.filter_field_eq("d.year", [1994]),
            operation_set.filter_field_ge("lo.discount", 5),
            operation_set.filter_field_le("lo.discount", 7),
            operation_set.filter_field_ge("lo.quantity", 26),
            operation_set.filter_field_le("lo.quantity", 35),
        ],
        s3_joins = [
            operation_set.join_fields("lo.orderdate", "d.datekey"),
        ],
        s4_aggregation = [
            # select
        ]
    )
