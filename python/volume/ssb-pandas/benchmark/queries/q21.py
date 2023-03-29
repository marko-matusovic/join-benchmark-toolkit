from typing import Callable
from pandas import DataFrame

from benchmark.instructions import filter_field_eq, filter_field_ge, filter_field_le, filter_field_lt, from_tables, join_fields
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
def instruction_set() -> list[list[Callable[[dict[str, DataFrame]], None]]]:
    return [
        [
            from_tables(["lineorder", "date", "part", "supplier"])
        ],
        [
            join_fields("lo_orderdate", "d_datekey"),
            join_fields("lo_partkey", "p_partkey"),
            join_fields("lo_suppkey", "s_suppkey"),
            filter_field_eq("p_category", ["MFGR#12"]),
            filter_field_eq("s_region", ["AMERICA"]),
        ],
        [
            # group by
            # order by
        ],
        [
            # select
        ]
    ]
