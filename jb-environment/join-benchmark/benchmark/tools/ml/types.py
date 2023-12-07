from typing import NamedTuple, TypeAlias


class TableFeatures(NamedTuple):
    length: float
    unique: float
    row_size: float
    cache_age: float


class CrossFeatures(NamedTuple):
    selectivity: float


class Features(NamedTuple):
    table_1: TableFeatures
    table_2: TableFeatures
    cross: CrossFeatures


# The features dictionary has 3 levels:
#   1. by query name
#   2. by join order
#   3. by join id
AllFeatures: TypeAlias = dict[str, dict[str, dict[str, Features]]]


class Measurements(NamedTuple):
    parsing: float
    overhead: float
    filters: list[float]
    joins: list[float]


# The measurements dictionary has 2 levels:
#   1. by query name
#   2. by join order
AllMeasurements: TypeAlias = dict[str, dict[str, Measurements]]
