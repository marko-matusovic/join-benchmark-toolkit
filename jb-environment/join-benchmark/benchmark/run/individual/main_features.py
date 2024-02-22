import json
from math import nan
import math
from benchmark.tools.query_parser import load_query, get_joins
from benchmark.tools.ml.types import TableFeatures, CrossFeatures, DataFeatures
from benchmark.operations.operations_costmodel import (
    Data,
    Operations_CostModel,
    calc_age_mem,
    find_table,
    total_length_of_cluster,
)
from benchmark.operations.query_instructions_service import get_instruction_set


def main(
    db_path: str,
    db_set: str,
    query: str,
    perm: list[int] | None = None,
    log_file: str | None = None,
    log_head="",
    manual_parse=False,
):
    if log_file == None:
        log_file = f"results/training_data/{db_set}/{query}/features.log"

    instructions = get_instruction_set(
        db_path, db_set, query, Operations_CostModel(), manual_parse
    )
    joins = get_joins(load_query(db_path, query))

    data: Data = instructions.s1_init()

    for instruction in instructions.s2_filters:
        instruction(data)

    if perm == None:
        perm = list(range(len(instructions.s3_joins)))
    for p in perm:
        # Get data for the join
        [field_1, field_2] = joins[p]
        features_1 = collect_features(data, field_1)
        features_2 = collect_features(data, field_2)

        # Execute the join
        instructions.s3_joins[p](data)

        # Collect mix features
        features_mix = collect_mix_features(
            data, field_1, field_2, features_1, features_2
        )

        features_all = json.dumps(DataFeatures(features_1, features_2, features_mix))

        with open(log_file, "a") as fout:
            fout.write(f"{log_head};{p};{features_all}\n")


def collect_features(data: Data, field_name: str) -> TableFeatures:
    (table_name, full_field_name) = find_table(data.schema, field_name)
    short_field_name = full_field_name.split(".")[-1]

    cluster = data.clusters[table_name]
    bounds = data.stats[table_name].column[short_field_name].bounds
    if bounds != None:
        bounds_low = float(bounds[0])
        bounds_high = float(bounds[1])
        bounds_range = float(abs(bounds[1] - bounds[0]))
    else:
        bounds_low = math.nan
        bounds_high = math.nan
        bounds_range = math.nan
    return TableFeatures(
        length=total_length_of_cluster(data, cluster),
        unique=data.stats[table_name].column[short_field_name].unique,
        id_size=data.stats[table_name].column[short_field_name].dtype,
        row_size=float(
            sum([v.dtype for tbl in cluster for v in data.stats[tbl].column.values()])
        ),
        cache_age=calc_age_mem(data, table_name),
        cluster_size=float(len(cluster)),
        bounds_low=bounds_low,
        bounds_high=bounds_high,
        bounds_range=bounds_range,
    )


def collect_mix_features(
    data: Data,
    field_1: str,
    field_2: str,
    features_1: TableFeatures,
    features_2: TableFeatures,
) -> CrossFeatures:
    (table_name_1, full_field_name_1) = find_table(data.schema, field_1)
    (table_name_2, full_field_name_2) = find_table(data.schema, field_2)
    # short_field_1 = full_field_name_1.split(".")[-1]
    # short_field_2 = full_field_name_2.split(".")[-1]

    cluster = data.clusters[table_name_1]
    assert cluster == data.clusters[table_name_2]

    len_pos_max = float(features_1.length) * float(features_2.length)
    len_unq_max = float(features_1.unique) * float(features_2.unique)
    len_res = total_length_of_cluster(data, cluster)

    return CrossFeatures(
        len_res=len_res,
        len_possible_max=len_pos_max,
        len_unique_max=len_unq_max,
        selectivity=len_res / len_pos_max,
        cluster_size=float(len(cluster)),
        # overlap == 0 if res cluster size = cluster_size of left + cluster_size of right
        # overlap == 1 if res cluster size = max(cluster_size of left, cluster_size of right)
        cluster_overlap=1.0
        * (features_1.cluster_size + features_2.cluster_size - len(cluster))
        / min(float(features_1.cluster_size), float(features_2.cluster_size)),
    )


# # Cluster Overlap:
# defines how much the left and right clusters overlap
# Szymkiewicz–Simpson coefficient -> https://en.wikipedia.org/wiki/Overlap_coefficient
# but calculated from union and not intersection
