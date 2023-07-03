from io import TextIOWrapper
from typing import TypeAlias

import numpy as np
from benchmark.operations.get_query_instructions import get_real_instructions, get_time_mem_approx_instructions
from benchmark.operations.instructions import TDFs
from benchmark.operations.time_mem_approximations import Data


def main(db_set:str, query:str, perm:list[int]):
    file = open(f'results/comp_card_est/{db_set}/{query}.csv', 'a')
    
    real_instructions = get_real_instructions(db_set, query)
    approx_instructions = get_time_mem_approx_instructions(db_set, query)

    dfs = real_instructions.s1_init()
    data = approx_instructions.s1_init()
    
    for tbl in dfs:
        measure_len(file, dfs, data, tbl)
    
    for f in range(len(real_instructions.s2_filters)):
        snapshot = take_tbl_snapshot(dfs)
        real_instructions.s2_filters[f](dfs)
        approx_instructions.s2_filters[f](data)
        evaluate_len(file, dfs, data, snapshot)
        
    for p in perm:
        snapshot = take_tbl_snapshot(dfs)
        real_instructions.s3_joins[p](dfs)
        approx_instructions.s3_joins[p](data)
        evaluate_len(file, dfs, data, snapshot)

    if len(dfs) != 1:
        print('ERROR: More than one cluster after all joins')
        exit(1)
        
    file.close()
    
    print('Completed successfully')

TSnapshot: TypeAlias = set[str]

def take_tbl_snapshot(dfs: TDFs) -> TSnapshot:
    return set(dfs.keys())

def evaluate_len(file: TextIOWrapper, dfs: TDFs, data: Data, snapshot: TSnapshot) -> None:
    tbls = set(dfs.keys()) - snapshot
    if len(tbls) != 1:
        print('ERROR: More than 1 new table appeared after 1 operation')
        exit(1)
    measure_len(file, dfs, data, tbls.pop())

def measure_len(file: TextIOWrapper, dfs: TDFs, data: Data, tbl: str) -> None:
    # Real length
    real_len = len(dfs[tbl].index)
    # Approximate length
    tbl_in_cluster = list(data.cluster_names.keys())[list(data.cluster_names.values()).index(tbl)]
    cluster = data.clusters[tbl_in_cluster]
    assert tbl == data.cluster_names[tbl_in_cluster]
    approx_len = float(
        np.product(
            [
                np.product(data.selects[tbl_orig] + [data.stats[tbl_orig].length])
                for tbl_orig in cluster
            ]
        )
    )
    # print
    file.write(f'"{tbl}";{real_len};{approx_len}\n')