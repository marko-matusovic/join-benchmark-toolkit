from typing import Callable
from pandas import DataFrame
from benchmark.operations.approximations import Approx_Instructions
from benchmark.operations.instructions import Instructions

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
def instruction_set(operation_set):
    return [
        [
            operation_set.from_tables(["lineorder", "date"])
        ],
        [
            operation_set.join_fields("lo_orderdate", "d_datekey"),
            operation_set.filter_field_eq("d_weeknuminyear", [6]),
            operation_set.filter_field_eq("d_year", [1994]),
            operation_set.filter_field_ge("lo_discount", 5),
            operation_set.filter_field_le("lo_discount", 7),
            operation_set.filter_field_ge("lo_quantity", 26),
            operation_set.filter_field_le("lo_quantity", 35),
        ],
        [
            # select
        ]
    ]
