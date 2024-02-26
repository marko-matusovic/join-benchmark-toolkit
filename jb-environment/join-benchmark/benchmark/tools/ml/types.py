from typing import NamedTuple, TypeAlias


class TableFeatures(NamedTuple):
    length: float
    unique: float
    id_size: float
    row_size: float
    cache_age: float
    cluster_size: float
    bounds_low: float
    bounds_high: float
    bounds_range: float


class CrossFeatures(NamedTuple):
    len_res: float
    len_possible_max: float
    len_unique_max: float
    selectivity: float
    cluster_size: float
    cluster_overlap: float
    tbl_ratio_length: float
    tbl_ratio_unique: float
    tbl_ratio_row_size: float
    tbl_ratio_cache_age: float
    tbl_ratio_bounds_range: float
    tbl_min_length: float
    tbl_min_unique: float
    tbl_min_row_size: float
    tbl_min_cache_age: float
    tbl_min_bounds_range: float
    tbl_max_length: float
    tbl_max_unique: float
    tbl_max_row_size: float
    tbl_max_cache_age: float
    tbl_max_bounds_range: float


feature_names = [
    "t_length",
    "t_unique",
    "t_id_size",
    "t_row_size",
    "t_cache_age",
    "t_cluster_size",
    "t_bounds_low",
    "t_bounds_high",
    "t_bounds_range",
    "c_len_res",
    "c_len_possible_max",
    "c_len_unique_max",
    "c_selectivity",
    "c_cluster_size",
    "c_cluster_overlap",
    "c_tbl_ratio_length",
    "c_tbl_ratio_unique",
    "c_tbl_ratio_row_size",
    "c_tbl_ratio_cache_age",
    "c_tbl_ratio_bounds_range",
    "c_tbl_min_length",
    "c_tbl_min_unique",
    "c_tbl_min_row_size",
    "c_tbl_min_cache_age",
    "c_tbl_min_bounds_range",
    "c_tbl_max_length",
    "c_tbl_max_unique",
    "c_tbl_max_row_size",
    "c_tbl_max_cache_age",
    "c_tbl_max_bounds_range",
]


def get_feature_names():
    return feature_names.copy()


def extract_t(tableFeatures: TableFeatures, featureName: str):
    if featureName == "t_length":
        return tableFeatures.length
    elif featureName == "t_unique":
        return tableFeatures.unique
    elif featureName == "t_id_size":
        return tableFeatures.id_size
    elif featureName == "t_row_size":
        return tableFeatures.row_size
    elif featureName == "t_cache_age":
        return tableFeatures.cache_age
    elif featureName == "t_cluster_size":
        return tableFeatures.cluster_size
    elif featureName == "t_bounds_low":
        return tableFeatures.bounds_low
    elif featureName == "t_bounds_high":
        return tableFeatures.bounds_high
    elif featureName == "t_bounds_range":
        return tableFeatures.bounds_range
    else:
        print(f"Error: unexpected feature name {featureName}")
        exit(1)


def extract_c(crossFeatures: CrossFeatures, featureName: str):
    if featureName == "c_len_res":
        return crossFeatures.len_res
    elif featureName == "c_len_possible_max":
        return crossFeatures.len_possible_max
    elif featureName == "c_len_unique_max":
        return crossFeatures.len_unique_max
    elif featureName == "c_selectivity":
        return crossFeatures.selectivity
    elif featureName == "c_cluster_size":
        return crossFeatures.cluster_size
    elif featureName == "c_cluster_overlap":
        return crossFeatures.cluster_overlap
    elif featureName == "c_tbl_ratio_length":
        return crossFeatures.tbl_ratio_length
    elif featureName == "c_tbl_ratio_unique":
        return crossFeatures.tbl_ratio_unique
    elif featureName == "c_tbl_ratio_row_size":
        return crossFeatures.tbl_ratio_row_size
    elif featureName == "c_tbl_ratio_cache_age":
        return crossFeatures.tbl_ratio_cache_age
    elif featureName == "c_tbl_ratio_bounds_range":
        return crossFeatures.tbl_ratio_bounds_range
    elif featureName == "c_tbl_min_length":
        return crossFeatures.tbl_min_length
    elif featureName == "c_tbl_min_unique":
        return crossFeatures.tbl_min_unique
    elif featureName == "c_tbl_min_row_size":
        return crossFeatures.tbl_min_row_size
    elif featureName == "c_tbl_min_cache_age":
        return crossFeatures.tbl_min_cache_age
    elif featureName == "c_tbl_min_bounds_range":
        return crossFeatures.tbl_min_bounds_range
    elif featureName == "c_tbl_max_length":
        return crossFeatures.tbl_max_length
    elif featureName == "c_tbl_max_unique":
        return crossFeatures.tbl_max_unique
    elif featureName == "c_tbl_max_row_size":
        return crossFeatures.tbl_max_row_size
    elif featureName == "c_tbl_max_cache_age":
        return crossFeatures.tbl_max_cache_age
    elif featureName == "c_tbl_max_bounds_range":
        return crossFeatures.tbl_max_bounds_range
    else:
        print(f"Error: unexpected feature name {featureName}")
        exit(1)


class DataFeatures(NamedTuple):
    table_1: TableFeatures
    table_2: TableFeatures
    cross: CrossFeatures


# The features dictionary has 3 levels:
#   1. by query name
#   2. by join order
#   3. by join id
AllDataFeatures: TypeAlias = dict[str, dict[str, dict[str, DataFeatures]]]


class Measurements(NamedTuple):
    parsing: float
    overhead: float
    filters: list[float]
    joins: list[float]


# The measurements dictionary has 2 levels:
#   1. by query name
#   2. by join order
AllMeasurements: TypeAlias = dict[str, dict[str, Measurements]]
