from typing import TypeVar
from benchmark.operations.query_instructions import QueryInstructions
from benchmark.operations.operations import Operations
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
I = TypeVar('I')
O = TypeVar('O')

def instruction_set(db_path:str, operation_set: Operations[I,O]) -> QueryInstructions[I, O]:
    return QueryInstructions(
        s1_init = operation_set.from_tables("ssb", ["lineorder", "date", "part", "supplier", "customer"],  ["lo", "d", "p", "s", "c"]),
        s2_filters = [
            operation_set.filter_field_eq("c.region", ["AMERICA"]),
            operation_set.filter_field_eq("s.region", ["AMERICA"]),
            operation_set.filter_field_eq("p.mfgr", ['MFGR#1', 'MFGR#2'])
        ],
        s3_joins = [
            operation_set.join_fields("lo.custkey", "c.custkey"),           # 0
            operation_set.join_fields("lo.suppkey", "s.suppkey"),           # 1
            operation_set.join_fields("lo.partkey", "p.partkey"),           # 2
            operation_set.join_fields("lo.orderdate", "d.datekey"),         # 3
        ],
        s4_aggregation = [
            # group by
            # order by
            # select
        ]
    )
