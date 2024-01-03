from typing import TypeVar
from benchmark.operations.query_instructions import QueryInstructions
from benchmark.operations.operations import Operations

"""
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
"""
I = TypeVar("I")
O = TypeVar("O")


def instruction_set(
    db_path: str, operation_set: Operations[I, O]
) -> QueryInstructions[I, O]:
    return QueryInstructions(
        s1_init=operation_set.from_tables(
            db_path,
            "ssb",
            ["lineorder", "date", "part", "supplier"],
            ["lo", "d", "p", "s"],
        ),
        s2_filters=[
            operation_set.filter_field_eq("p.category", ["MFGR#12"]),
            operation_set.filter_field_eq("s.region", ["AMERICA"]),
        ],
        s3_joins=[
            operation_set.join_fields("lo.orderdate", "d.datekey"),
            operation_set.join_fields("lo.partkey", "p.partkey"),
            operation_set.join_fields("lo.suppkey", "s.suppkey"),
        ],
        s4_aggregation=[
            # group by
            # order by
            # select
        ],
    )
