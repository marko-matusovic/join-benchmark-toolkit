from typing import Callable
from pandas import DataFrame

from benchmark.instructions import filter_field_eq, join_fields
'''
# QUERY
| select sum(lo_extendedprice*lo_discount) as revenue
| from lineorder, ddate
| where lo_orderdate = d_datekey
| and d_year = 1993
| and lo_discount between 1 and 3
| and lo_quantity < 25
'''
def instruction_set() -> list[list[Callable[[dict[str, DataFrame]], None]]]:
    return [
        [
            join_fields("lo_orderdate", "d_datekey"),
            filter_field_eq("d_year", [1993]),
            filter_field_ge("lo_discount", 1),
            filter_field_le("lo_discount", 3),
            filter_field_lt("lo_quantity", 25),
        ],
        [
            # select
        ]
    ]
