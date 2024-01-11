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
