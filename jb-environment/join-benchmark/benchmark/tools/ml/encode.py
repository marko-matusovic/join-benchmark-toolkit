from math import isnan
from benchmark.tools.ml.types import DataFeatures


# select
#   None    -> include all features
#   []      -> only cardinality estimates
#   [f1...] -> include cardinality estimates, f1 and all the rest
#   - must be from the feature_names set
def encode_feature(
    features: DataFeatures | None = None, select: None | list[str] = None
) -> list[float]:
    if features == None:
        return [0.0] * feature_length(select)
    else:
        encoded = []
        if select == None or "t_length" in select:
            encoded.append(features.table_1.length)
        if select == None or "t_unique" in select:
            encoded.append(features.table_1.unique)
        if select == None or "t_id_size" in select:
            encoded.append(features.table_1.id_size)
        if select == None or "t_row_size" in select:
            encoded.append(features.table_1.row_size)
        if select == None or "t_cache_age" in select:
            encoded.append(features.table_1.cache_age)
        if select == None or "t_cluster_size" in select:
            encoded.append(features.table_1.cluster_size)
        if select == None or "t_bounds_low" in select:
            encoded.append(features.table_1.bounds_low)
        if select == None or "t_bounds_high" in select:
            encoded.append(features.table_1.bounds_high)
        if select == None or "t_bounds_range" in select:
            encoded.append(features.table_1.bounds_range)

        if select == None or "t_length" in select:
            encoded.append(features.table_2.length)
        if select == None or "t_unique" in select:
            encoded.append(features.table_2.unique)
        if select == None or "t_id_size" in select:
            encoded.append(features.table_2.id_size)
        if select == None or "t_row_size" in select:
            encoded.append(features.table_2.row_size)
        if select == None or "t_cache_age" in select:
            encoded.append(features.table_2.cache_age)
        if select == None or "t_cluster_size" in select:
            encoded.append(features.table_2.cluster_size)
        if select == None or "t_bounds_low" in select:
            encoded.append(features.table_2.bounds_low)
        if select == None or "t_bounds_high" in select:
            encoded.append(features.table_2.bounds_high)
        if select == None or "t_bounds_range" in select:
            encoded.append(features.table_2.bounds_range)

        if select == None or "c_len_res" in select:
            encoded.append(features.cross.len_res)
        if select == None or "c_len_possible_max" in select:
            encoded.append(features.cross.len_possible_max)
        if select == None or "c_len_unique_max" in select:
            encoded.append(features.cross.len_unique_max)
        if select == None or "c_selectivity" in select:
            encoded.append(features.cross.selectivity)
        if select == None or "c_cluster_size" in select:
            encoded.append(features.cross.cluster_size)
        if select == None or "c_cluster_overlap" in select:
            encoded.append(features.cross.cluster_overlap)

    if feature_length(select) != len(encoded):
        print("Error: unexpected feature length!")
        exit(1)
    return [sane_x(x) for x in encoded]


def sane_x(x: float) -> float:
    if isnan(x):
        return 0
    if x > 1e25:
        return 1e25
    if x < -1e25:
        return -1e25
    return x


# Closely coupled with encode_feature
def feature_length(select: None | list[str] = None) -> int:
    if select is None:
        return 24
    num_features = 0
    for f in select:
        if f.startswith("t_"):
            num_features += 2
        if f.startswith("c_"):
            num_features += 1
    return num_features
