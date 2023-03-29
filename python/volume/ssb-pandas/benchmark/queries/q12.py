from typing import Callable
from pandas import DataFrame

from benchmark.instructions import filter_field_eq, filter_field_ge, filter_field_le, filter_field_lt, from_tables, join_fields
'''
# QUERY
| select sum(lo_extendedprice*lo_discount) as revenue
| from lineorder, ddate
| where lo_orderdate = d_datekey
| and d_yearmonthnum = 199401
| and lo_discount between 4 and 6
| and lo_quantity between 26 and 35
'''
def instruction_set() -> list[list[Callable[[dict[str, DataFrame]], None]]]:
    return [
        [
            from_tables(["lineorder", "date"])
        ],
        [
            join_fields("lo_orderdate", "d_datekey"),
            filter_field_eq("d_yearmonthnum", [199401]),
            filter_field_ge("lo_discount", 4),
            filter_field_le("lo_discount", 6),
            filter_field_ge("lo_quantity", 26),
            filter_field_le("lo_quantity", 35),
        ],
        [
            # select
        ]
    ]
