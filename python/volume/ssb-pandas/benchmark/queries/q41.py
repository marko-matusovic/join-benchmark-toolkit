from typing import Callable
from pandas import DataFrame

from benchmark.instructions import filter_field_eq, join_fields

'''
# QUERY
| select d_year, c_nation, sum(lo_revenue - lo_supplycost) as profit
| from ddate, customer, supplier, part, lineorder
| where lo_custkey = c_custkey
| and lo_suppkey = s_suppkey
| and lo_partkey = p_partkey
| and lo_orderdate = d_datekey
| and c_region = 'AMERICA'
| and s_region = 'AMERICA'
| and (p_mfgr = 'MFGR#1' or p_mfgr = 'MFGR#2')
| group by d_year, c_nation
| order by d_year, c_nation
'''
def instruction_set() -> list[list[Callable[[dict[str, DataFrame]], None]]]:
    return [
        [
            join_fields("lo_custkey", "c_custkey"),
            join_fields("lo_suppkey", "s_suppkey"),
            join_fields("lo_partkey", "p_partkey"),
            join_fields("lo_orderdate", "d_datekey"),
            filter_field_eq("c_region", ["AMERICA"]),
            filter_field_eq("s_region", ["AMERICA"]),
            filter_field_eq("p_mfgr", ['MFGR#1', 'MFGR#2'])
        ],
        [
            # group by
            # order by
        ],
        [
            # select
        ]
    ]
