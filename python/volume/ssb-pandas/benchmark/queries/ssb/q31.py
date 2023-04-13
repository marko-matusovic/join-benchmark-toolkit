from typing import Callable
from pandas import DataFrame
from benchmark.operations.approximations import Approx_Instructions
from benchmark.operations.instructions import Instructions

'''
# QUERY
select c_nation, s_nation, d_year, sum(lo_revenue)
as revenue from customer, lineorder, supplier, ddate
where lo_custkey = c_custkey
and lo_suppkey = s_suppkey
and lo_orderdate = d_datekey
and c_region = 'ASIA' and s_region = 'ASIA'
and d_year >= 1992 and d_year <= 1997
group by c_nation, s_nation, d_year
order by d_year asc, revenue desc
'''
def instruction_set(operation_set):
    return [
        [
            operation_set.from_tables('ssb', ["lineorder", "date", "supplier", "customer"], [])
        ],
        [
            operation_set.filter_field_eq("c_region", ["ASIA"]),
            operation_set.filter_field_eq("s_region", ["ASIA"]),
            operation_set.filter_field_ge("d_year", 1992),
            operation_set.filter_field_le("d_year", 1997),
        ],
        [
            operation_set.join_fields("lo_custkey", "c_custkey"),
            operation_set.join_fields("lo_suppkey", "s_suppkey"),
            operation_set.join_fields("lo_orderdate", "d_datekey"),
        ],
        [
            # group by
            # order by
        ],
        [
            # select
        ]
    ]