from io import TextIOWrapper
from typing import TypeAlias

import numpy as np
from benchmark.operations.get_query_instructions import (
    get_real_instructions,
    get_time_mem_approx_instructions,
)
from benchmark.operations.instructions import TDFs
from benchmark.operations.time_mem_approximations import Data


def main(db_set: str, query: str, perm: list[int]):
    file = open(f"results/comp_card_est/{db_set}/{query}.csv", "a")

    real_instructions = get_real_instructions(db_set, query)
    approx_instructions = get_time_mem_approx_instructions(db_set, query)

    dfs = real_instructions.s1_init()
    data = approx_instructions.s1_init()

    for f in range(len(real_instructions.s2_filters)):
        [dfs_s, data_s] = [dfs, data].copy()
        real_instructions.s2_filters[f](dfs)
        approx_instructions.s2_filters[f](data)
        measure(file, dfs_s, data_s, dfs, data)

    for p in perm:
        [dfs_s, data_s] = [dfs, data].copy()
        real_instructions.s3_joins[p](dfs)
        approx_instructions.s3_joins[p](data)
        measure(file, dfs_s, data_s, dfs, data)

    if len(dfs) != 1:
        print("ERROR: More than one cluster after all joins")
        exit(1)

    file.close()

    print("Completed successfully")


def measure(
    file: TextIOWrapper, dfs_1: TDFs, data_1: Data, dfs_2: TDFs, data_2: Data
) -> None:
    # Find table_1 and table_2
    tables_1 = set(data_1.cluster_names.values())
    tables_2 = set(data_2.cluster_names.values())
    name_1 = list(tables_1 - tables_2)
    name_2 = list(tables_2 - tables_1)

    if not (0 < len(name_1) <= 2 and len(name_2) == 1):
        print("ERROR: Operation modified unexpected number of tables!")
        exit(1)
    name_2 = name_2.pop()

    # Get the operation name
    name_operation = name_2
    for i, n in enumerate(name_1):
        name_operation = name_operation.replace(n, f"(T{i})")

    # Real length
    real_len_1 = [len(dfs_1[name].index) for name in name_1]
    real_len_2 = len(dfs_2[name_2].index)
    real_selectivity = 1.0 * real_len_2 / np.product(real_len_1)
    real_len_1.append(0)  # for printing in case len() == 1

    # Approximate length
    approx_len_1 = [
        float(
            np.product(
                [
                    np.product(data_1.selects[tbl] + [data_1.stats[tbl].length])
                    for tbl in data_1.clusters[name]
                ]
            )
        )
        for name in name_1
    ]
    approx_len_2 = float(
        np.product(
            [
                np.product(data_2.selects[tbl] + [data_2.stats[tbl].length])
                for tbl in data_2.clusters[name_2]
            ]
        )
    )
    approx_selectivity = 1.0 * approx_len_2 / np.product(approx_len_1)
    approx_len_1.append(0)  # for printing in case len() == 1
    # print
    # keys: operation name; T1 real len, T1 approx len, T2 real len, T2 approx len, R real len, R approx len; real selectivity, approx selectivity
    file.write(f"{';'.join([str(i) for i in [
            real_len_1[0],
            approx_len_1[0],
            real_len_1[0],
            approx_len_1[0],
            real_len_2,
            approx_len_2,
            real_selectivity,
            approx_selectivity,
        ]])}\n")
