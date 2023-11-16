from copy import deepcopy
from io import TextIOWrapper
from os.path import exists
from typing import TypeAlias

import numpy as np

from benchmark.operations.operations_real import Operations_Real, TDFs
from benchmark.operations.operations_costmodel import Data, Operations_CostModel
from benchmark.operations.query_instructions import get_instruction_set


def main(db_path:str, db_set: str, query: str, perm: list[int]):
    path = f"results/comp_card_est/{db_set}/{query}.csv"
    if not exists(path):
        file = open(path, "a")
        file.write('operation name;T1_name;T2_name;T1_real_len;T1_approx_len;T2_real_len;T2_approx_len;R_real_len;R_approx_len;real_selectivity;approx_selectivity\n')
    else:
        file = open(path, "a")

    real_instructions = get_instruction_set(db_path, db_set, query, Operations_Real())
    approx_instructions = get_instruction_set(db_path, db_set, query, Operations_CostModel())

    dfs = real_instructions.s1_init()
    data = approx_instructions.s1_init()

    for f in range(len(real_instructions.s2_filters)):
        [dfs_s, data_s] = deepcopy([dfs, data])
        real_instructions.s2_filters[f](dfs)
        approx_instructions.s2_filters[f](data)
        measure(file, dfs_s, data_s, dfs, data)

    for p in perm:
        [dfs_s, data_s] = deepcopy([dfs, data])
        real_instructions.s3_joins[p](dfs)
        approx_instructions.s3_joins[p](data)
        measure(file, dfs_s, data_s, dfs, data)

    if len(dfs) != 1:
        print("ERROR: More than one cluster after all joins")
        exit(1)

    file.close()

    print("Completed successfully")


# TODO: replace deepcopy(dfs) with just table name and length
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
    tbls_in_cluster = [
        list(data_1.cluster_names.keys())[
            list(data_1.cluster_names.values()).index(name)
        ]
        for name in name_1
    ]
    clusters = [data_1.clusters[tbl_in_cluster] for tbl_in_cluster in tbls_in_cluster]
    approx_len_1 = [
        float(
            np.product(
                [
                    np.product(
                        data_1.selects[tbl_orig] + [data_1.stats[tbl_orig].length]
                    )
                    for tbl_orig in cluster
                ]
            )
        )
        for cluster in clusters
    ]

    tbl_in_cluster = list(data_2.cluster_names.keys())[
        list(data_2.cluster_names.values()).index(name_2)
    ]
    cluster = data_2.clusters[tbl_in_cluster]
    approx_len_2 = float(
        np.product(
            [
                np.product(data_2.selects[tbl_orig] + [data_2.stats[tbl_orig].length])
                for tbl_orig in cluster
            ]
        )
    )
    approx_selectivity = 1.0 * approx_len_2 / np.product(approx_len_1)
    approx_len_1.append(0)  # for printing in case len() == 1
    # print
    # keys: operation name;T1_real_len;T1_approx_len;T2_real_len;T2_approx_len;R_real_len;R_approx_len;real_selectivity;approx_selectivity
    file.write(
        ";".join(
            [
                str(i)
                for i in [
                    name_operation,
                    name_1[0],
                    name_1[1] if len(name_1)>1 else '',
                    real_len_1[0],
                    approx_len_1[0],
                    real_len_1[1],
                    approx_len_1[1],
                    real_len_2,
                    approx_len_2,
                    real_selectivity,
                    approx_selectivity,
                ]
            ]
        )
        + "\n"
    )
    file.flush()
