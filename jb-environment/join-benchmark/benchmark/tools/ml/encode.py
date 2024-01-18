from itertools import combinations
from benchmark.tools.ml.types import AllDataFeatures, AllMeasurements, DataFeatures
import math

# ======== METHODS ===============================================


def encode_all_reg(
    data_features: AllDataFeatures,
    hw_features: list[float],
    measurements: AllMeasurements,
    joins_in_block: int,
) -> tuple[list[list[float]], list[float]]:
    X: list[list[float]] = []
    Y: list[float] = []
    for query in set(data_features.keys()) & set(measurements.keys()):
        (xs, ys) = encode_query_reg(
            data_features, hw_features, measurements, query, joins_in_block
        )
        X += xs
        Y += ys

    return (X, Y)


# Encodes a query into a list of Xs and Ys.
#
# If no "jo" is given, it iterates through all possible join orders
# and encodes blocks of JOINS_IN_BLOCK into each X and Y.
# If some "jo" is passed, it only encodes that join order.
def encode_query_reg(
    data_features: AllDataFeatures,
    hw_features: list[float],
    measurements: AllMeasurements,
    query: str,
    joins_in_block: int,
    jo=None,
) -> tuple[list[list[float]], list[float]]:
    xs: list[list[float]] = []
    ys: list[float] = []

    jos = set(data_features[query].keys()) & set(measurements[query].keys())
    if type(jo) == str:
        jos = set([jo])
    elif type(jo) == list or type(jo) == set:
        jos = jos.intersection(set(jo))

    for jo in jos:
        fs = data_features[query][jo]
        ms = measurements[query][jo]
        encoded_fs = [encode_feature(fs[j]) for j in jo.split(",")]
        encoded_hw = [sane_x(x) for x in hw_features]
        encoded_ms = ms.joins

        assert len(encoded_fs) == len(encoded_ms)

        # Fold encoded fs and ms to blocks of N and fill the end with 0s
        # Each block starts with one repetition of hw features, then all the data_features follow folded
        for j in range(0, len(encoded_fs), joins_in_block):
            x: list[float] = encoded_hw.copy()
            y = 0.0
            for i in range(j, j + joins_in_block):
                if i < len(encoded_fs):
                    x += encoded_fs[i]
                    y += encoded_ms[i]
                else:
                    x += encode_feature()
                    y += 0.0

            xs.append(x)
            ys.append(y)

    return (xs, ys)


def encode_feature(features: DataFeatures | None = None) -> list[float]:
    if features == None:
        return [0.0] * 24
    else:
        return [
            sane_x(x)
            for x in [
                features.table_1.length,
                features.table_1.unique,
                features.table_1.id_size,
                features.table_1.row_size,
                features.table_1.cache_age,
                features.table_1.cluster_size,
                features.table_1.bounds_low,
                features.table_1.bounds_high,
                features.table_1.bounds_range,
                features.table_2.length,
                features.table_2.unique,
                features.table_2.id_size,
                features.table_2.row_size,
                features.table_2.cache_age,
                features.table_2.cluster_size,
                features.table_2.bounds_low,
                features.table_2.bounds_high,
                features.table_2.bounds_range,
                features.cross.len_res,
                features.cross.len_possible_max,
                features.cross.len_unique_max,
                features.cross.selectivity,
                features.cross.cluster_size,
                features.cross.cluster_overlap,
            ]
        ]


def sane_x(x: float) -> float:
    if math.isnan(x):
        return 0
    if x > 1e25:
        return 1e25
    if x < -1e25:
        return -1e25
    return x

def encode_all_cls(
    data_features: AllDataFeatures,
    hw_features: list[float],
    measurements: AllMeasurements,
    num_joins: int,
) -> tuple[list[list[float]], list[float]]:
    X: list[list[float]] = []
    Y: list[float] = []
    queries = sorted(list(set(data_features.keys()) & set(measurements.keys())))
    for query in queries:
        if num_joins != list(data_features[query].keys())[0].count(',') + 1:
            continue
        (xs, ys) = encode_query_cls(
            data_features, hw_features, measurements, query
        )
        X += xs
        Y += ys

    return (X, Y)


# Encodes a query into a list of Xs and Ys.
#
# If no "jo" is given, it iterates through all possible join orders
# and encodes blocks of JOINS_IN_BLOCK into each X and Y.
# If some "jo" is passed, it only encodes that join order.
def encode_query_cls(
    data_features: AllDataFeatures,
    hw_features: list[float],
    measurements: AllMeasurements,
    query: str,
    jos: list[tuple[str,str]] | None = None
) -> tuple[list[list[float]], list[float]]:
    xs: list[list[float]] = []
    ys: list[float] = []
    
    if jos == None:
        all_joins = sorted(list(set(data_features[query].keys()) & set(measurements[query].keys())))
        jos = list(combinations(all_joins, 2))
    
    encoded_hw = [sane_x(x) for x in hw_features]
    encoded_fs = {}
    encoded_ms = {}
    for jo in set([jo for pair in jos for jo in pair]):
        encoded_fs[jo] = [encode_feature(data_features[query][jo][j]) for j in jo.split(",")]
        encoded_ms[jo] = sum(measurements[query][jo].joins)

    for (jo1,jo2) in jos:
        x: list[float] = []
        # x += encoded_hw.copy()
        for join_features in encoded_fs[jo1]:
            x += join_features
        # x += encoded_hw.copy()
        for join_features in encoded_fs[jo2]:
            x += join_features
        
        if encoded_ms[jo1] < encoded_ms[jo2]:
            y = 0
        elif encoded_ms[jo1] > encoded_ms[jo2]:
            y = 1
        else: # encoded_ms[jo1] = encoded_ms[jo2]:
            y = 0

        xs.append(x)
        ys.append(y)

    return (xs, ys)
