from typing import Callable
from pandas import DataFrame
from benchmark.operations.approximations import Approx_Instructions
from benchmark.operations.instructions import Instructions

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
def instruction_set(operation_set):
    return [
        [
            operation_set.from_tables(["lineorder", "date", "part", "supplier"])
        ],
        [
            operation_set.filter_field_eq("p_category", ["MFGR#12"]),
            operation_set.filter_field_eq("s_region", ["AMERICA"]),
        ],
        [
            operation_set.join_fields("lo_orderdate", "d_datekey"),
            operation_set.join_fields("lo_partkey", "p_partkey"),
            operation_set.join_fields("lo_suppkey", "s_suppkey"),
        ],
        [
            # group by
            # order by
        ],
        [
            # select
        ]
    ]
