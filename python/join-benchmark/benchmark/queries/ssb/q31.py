from typing import TypeVar
from benchmark.operations.get import QueryInstructions
from benchmark.operations.operations import Operations

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
I = TypeVar('I')
O = TypeVar('O')

def instruction_set(operation_set: Operations[I,O]) -> QueryInstructions[I, O]:
    return QueryInstructions(
        s1_init = operation_set.from_tables('ssb', ["lineorder", "date", "supplier", "customer"], []),
        s2_filters = [
            operation_set.filter_field_eq("c_region", ["ASIA"]),
            operation_set.filter_field_eq("s_region", ["ASIA"]),
            operation_set.filter_field_ge("d_year", 1992),
            operation_set.filter_field_le("d_year", 1997),
        ],
        s3_joins = [
            operation_set.join_fields("lo_custkey", "c_custkey"),
            operation_set.join_fields("lo_suppkey", "s_suppkey"),
            operation_set.join_fields("lo_orderdate", "d_datekey"),
        ],
        s4_aggregation = [
            # group by
            # order by
            # select
        ]
    )
