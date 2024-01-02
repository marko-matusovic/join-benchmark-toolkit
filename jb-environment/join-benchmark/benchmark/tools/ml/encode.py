from benchmark.tools.ml.types import AllFeatures, AllMeasurements, Features

# ======== TYPES =================================================

JOINS_IN_BLOCK = 4

# ======== METHODS ===============================================


def encode_all(
    features: AllFeatures, measurements: AllMeasurements
) -> tuple[list[list[float]], list[float]]:
    X: list[list[float]] = []
    Y: list[float] = []
    for query in set(features.keys()) & set(measurements.keys()):
        (xs, ys) = encode_query(features, measurements, query)
        X += xs
        Y += ys

    return (X, Y)

# Encodes a query into a list of Xs and Ys. 
# 
# If no "jo" is given, it iterates through all possible join orders 
# and encodes blocks of JOINS_IN_BLOCK into each X and Y.
# If some "jo" is passed, it only encodes that join order.
def encode_query(
    features: AllFeatures, measurements: AllMeasurements, query: str, jo=None
) -> tuple[list[list[float]], list[float]]:
    xs = []
    ys = []

    jos = set(features[query].keys()) & set(measurements[query].keys())
    if type(jo) == str:
        jos = set([jo])
    elif type(jo) == list or type(jo) == set:
        jos = jos.intersection(set(jo))

    for jo in jos:
        fs = features[query][jo]
        ms = measurements[query][jo]
        encoded_fs = [encode_feature(fs[j]) for j in jo.split(",")]
        encoded_ms = ms.joins

        assert len(encoded_fs) == len(encoded_ms)

        # Fold encoded fs and ms to blocks of N and fill the end with 0s
        for j in range(0, len(encoded_fs), JOINS_IN_BLOCK):
            x: list[float] = []
            y = 0.0
            for i in range(j, j + JOINS_IN_BLOCK):
                if i < len(encoded_fs):
                    x += encoded_fs[i]
                    y += encoded_ms[i]
                else:
                    x += encode_feature()
                    y += 0.0

            xs.append(x)
            ys.append(y)
    return (xs, ys)


def encode_feature(features: Features | None = None) -> list[float]:
    if features == None:
        return [0.0] * 9
    else:
        return [
            features.table_1.length,
            features.table_1.unique,
            features.table_1.row_size,
            features.table_1.cache_age,
            features.table_2.length,
            features.table_2.unique,
            features.table_2.row_size,
            features.table_2.cache_age,
            features.cross.selectivity,
        ]
