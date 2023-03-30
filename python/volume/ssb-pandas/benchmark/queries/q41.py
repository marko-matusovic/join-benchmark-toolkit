from typing import Callable
from pandas import DataFrame
from benchmark.operations.approximations import Approx_Instructions
from benchmark.operations.instructions import Instructions


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
def instruction_set(operation_set):
    return [
        [
            operation_set.from_tables(["lineorder", "date", "part", "supplier", "customer"])
        ],
        [
            operation_set.join_fields("lo_custkey", "c_custkey"),
            operation_set.join_fields("lo_suppkey", "s_suppkey"),
            operation_set.join_fields("lo_partkey", "p_partkey"),
            operation_set.join_fields("lo_orderdate", "d_datekey"),
            operation_set.filter_field_eq("c_region", ["AMERICA"]),
            operation_set.filter_field_eq("s_region", ["AMERICA"]),
            operation_set.filter_field_eq("p_mfgr", ['MFGR#1', 'MFGR#2'])
        ],
        [
            # group by
            # order by
        ],
        [
            # select
        ]
    ]
