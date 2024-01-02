import json
from benchmark.tools.query_parser import load_query, get_joins
from benchmark.operations.operations_costmodel import (
    Data,
    Operations_CostModel,
    calc_age_mult,
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

        features_all = json.dumps(
            {"left": features_1, "right": features_2, "mix": features_mix}
        )

        with open(log_file, "a") as fout:
            fout.write(f"{log_head};{p};{features_all}\n")


def collect_features(data: Data, field_name: str):
    table = find_table(data.schema, field_name)
    short_field_name = field_name.split(".")[-1]

    cluster = data.clusters[table]

    features = {
        "length": total_length_of_cluster(data, cluster),
        "unique": data.stats[table].column[short_field_name].unique,
        "id_size": data.stats[table].column[short_field_name].dtype,
        "row_size": sum(
            [v.dtype for tbl in cluster for v in data.stats[tbl].column.values()]
        ),
        "cache_age": calc_age_mult(data, table),
        "cluster_size": len(cluster),
        "bounds_low": 0,
        "bounds_high": 0,
        "bounds_range": 0,
    }
    bounds = data.stats[table].column[short_field_name].bounds
    if bounds != None:
        features = {
            **features,
            "bounds_low": bounds[0],
            "bounds_high": bounds[1],
            "bounds_range": abs(bounds[1] - bounds[0]),
        }

    assert len(features) == 9

    return features


def collect_mix_features(
    data: Data, field_1: str, field_2: str, features_1, features_2
):
    table_1 = find_table(data.schema, field_1)
    table_2 = find_table(data.schema, field_2)
    # short_field_1 = field_1.split(".")[-1]
    # short_field_2 = field_2.split(".")[-1]

    cluster_1 = data.clusters[table_1]
    cluster_2 = data.clusters[table_2]

    assert cluster_1 == cluster_2

    len_pos_max = features_1["length"] * features_2["length"]
    len_unq_max = features_1["unique"] * features_2["unique"]
    len_res = total_length_of_cluster(data, cluster_1)

    return {
        "len_res": len_res,
        "len_possible_max": len_pos_max,
        "len_unique_max": len_unq_max,
        "selectivity": len_res / len_pos_max,
        "cluster_size": len(cluster_1),
        # overlap == 0 if res cluster size = cluster_size of left + cluster_size of right
        # overlap == 1 if res cluster size = max(cluster_size of left, cluster_size of right)
        "cluster_overlap": 1.0
        * len(cluster_1)
        / max(features_1["cluster_size"], features_2["cluster_size"]),
    }
