from typing import TypeVar
from benchmark.operations.query_instructions import QueryInstructions
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
        s1_init = operation_set.from_tables('ssb', ["lineorder", "date", "supplier", "customer"], ["lo", "d", "p", "c"]),
        s2_filters = [
            operation_set.filter_field_eq("c.region", ["ASIA"]),
            operation_set.filter_field_eq("s.region", ["ASIA"]),
            operation_set.filter_field_ge("d.year", 1992),
            operation_set.filter_field_le("d.year", 1997),
        ],
        s3_joins = [
            operation_set.join_fields("lo.custkey", "c.custkey"),
            operation_set.join_fields("lo.suppkey", "s.suppkey"),
            operation_set.join_fields("lo.orderdate", "d.datekey"),
        ],
        s4_aggregation = [
            # group by
            # order by
            # select
        ]
    )
