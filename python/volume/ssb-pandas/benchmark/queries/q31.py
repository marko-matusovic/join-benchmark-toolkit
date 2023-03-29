from typing import Callable
from pandas import DataFrame

from benchmark.instructions import filter_field_eq, filter_field_ge, filter_field_le, filter_field_lt, from_tables, join_fields
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
def instruction_set() -> list[list[Callable[[dict[str, DataFrame]], None]]]:
    return [
        [
            from_tables(["lineorder", "date", "supplier", "customer"])
        ],
        [
            join_fields("lo_custkey", "c_custkey"),
            join_fields("lo_suppkey", "s_suppkey"),
            join_fields("lo_orderdate", "d_datekey"),
            filter_field_eq("c_region", ["ASIA"]),
            filter_field_eq("s_region", ["ASIA"]),
            filter_field_ge("d_year", 1992),
            filter_field_le("d_year", 1997),
        ],
        [
            # group by
            # order by
        ],
        [
            # select
        ]
    ]
