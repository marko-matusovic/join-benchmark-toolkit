from typing import Callable
from pandas import DataFrame

from benchmark.instructions import filter_field_eq, filter_field_ge, filter_field_le, filter_field_lt, join_fields
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
def instruction_set() -> list[list[Callable[[dict[str, DataFrame]], None]]]:
    return [
        [
            join_fields("lo_orderdate", "d_datekey"),
            filter_field_eq("d_weeknuminyear", [6]),
            filter_field_eq("d_year", [1994]),
            filter_field_ge("lo_discount", 5),
            filter_field_le("lo_discount", 7),
            filter_field_ge("lo_quantity", 26),
            filter_field_le("lo_quantity", 35),
        ],
        [
            # select
        ]
    ]
