from typing import Callable
from pandas import DataFrame
from benchmark.operations.approximations import Approx_Instructions
from benchmark.operations.instructions import Instructions
'''
# QUERY
| select sum(lo_extendedprice*lo_discount) as revenue
| from lineorder, ddate
| where lo_orderdate = d_datekey
| and d_year = 1993
| and lo_discount between 1 and 3
| and lo_quantity < 25
'''
def instruction_set(operation_set):
    return [
        [
            operation_set.from_tables(["lineorder", "date"])
        ],
        [
            operation_set.join_fields("lo_orderdate", "d_datekey"),
            operation_set.filter_field_eq("d_year", [1993]),
            operation_set.filter_field_ge("lo_discount", 1),
            operation_set.filter_field_le("lo_discount", 3),
            operation_set.filter_field_lt("lo_quantity", 25),
        ],
        [
            # select
        ]
    ]
