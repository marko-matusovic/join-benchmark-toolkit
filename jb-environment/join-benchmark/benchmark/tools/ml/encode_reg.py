from benchmark.tools.ml.encode import encode_feature
from benchmark.tools.ml.types import AllDataFeatures, AllMeasurements


def encode_all_reg(
    data_features: AllDataFeatures,
    # hw_features: list[float],
    measurements: AllMeasurements,
    joins_in_block: int,
    select: None | list[str] = None,
) -> tuple[list[list[float]], list[float]]:
    X: list[list[float]] = []
    Y: list[float] = []
    queries = set(data_features.keys()) & set(measurements.keys())
    # queries = sorted(list(queries))
    for query in queries:
        (xs, ys) = encode_query_reg(
            data_features, measurements, query, joins_in_block, select=select
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
    # hw_features: list[float],
    measurements: AllMeasurements,
    query: str,
    joins_in_block: int,
    jo=None,
    select: None | list[str] = None,
) -> tuple[list[list[float]], list[float]]:
    xs: list[list[float]] = []
    ys: list[float] = []

    jos = set(data_features[query].keys()) & set(measurements[query].keys())
    if type(jo) == str:
        jos = set([jo])
    elif type(jo) == list or type(jo) == set:
        jos = jos.intersection(set(jo))

    jos = sorted(list(jos))

    for jo in jos:
        fs = data_features[query][jo]
        ms = measurements[query][jo]
        encoded_fs = [encode_feature(fs[j], select=select) for j in jo.split(",")]
        # encoded_hw = [sane_x(x) for x in hw_features]
        encoded_ms = ms.joins

        assert len(encoded_fs) == len(encoded_ms)

        # Fold encoded fs and ms to blocks of N and fill the end with 0s
        # Each block starts with one repetition of hw features, then all the data_features follow folded
        for j in range(0, len(encoded_fs), joins_in_block):
            x: list[float] = []
            # x: list[float] = encoded_hw.copy()
            y = 0.0
            for i in range(j, j + joins_in_block):
                if i < len(encoded_fs):
                    x += encoded_fs[i]
                    y += encoded_ms[i]
                else:
                    x += encode_feature(select=select)
                    y += 0.0

            xs.append(x)
            ys.append(y)

    return (xs, ys)
