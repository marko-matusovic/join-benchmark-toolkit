from benchmark.tools.ml.encode import encode_feature
from benchmark.tools.ml.types import AllDataFeatures, AllMeasurements
from benchmark.tools.tools import flatten


def encode_all_cls(
    data_features: AllDataFeatures,
    # hw_features: list[float],
    measurements: AllMeasurements,
    num_joins: int | None,  # When None use the FLEX cls model
    flex: bool = False,
    flex_all: bool = False,
) -> tuple[list[list[float]], list[float]]:
    assert (num_joins == None) == flex
    X: list[list[float]] = []
    Y: list[float] = []
    queries = set(data_features.keys()) & set(measurements.keys())
    # queries = sorted(list(queries))
    for query in queries:
        if (
            num_joins != None
            and num_joins != list(data_features[query].keys())[0].count(",") + 1
        ):
            continue
        (xs, ys) = encode_query_cls(data_features, measurements, query, flex, flex_all)
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
    # hw_features: list[float],
    measurements: AllMeasurements,
    query: str,
    flex: bool = False,
    flex_all: bool = False,
    jo_pairs: list[tuple[str, str]] | None = None,
) -> tuple[list[list[float]], list[float]]:
    xs: list[list[float]] = []
    ys: list[float] = []

    if jo_pairs == None:
        jos = set(data_features[query].keys()) & set(measurements[query].keys())
        jos = sorted(list(jos))
        jo_pairs = [(jo1, jo2) for jo1 in jos for jo2 in jos if jo1 != jo2]
    else:
        jos = set([jo for pair in jo_pairs for jo in pair])
        jos = sorted(list(jos))

    for pair in jo_pairs:
        if not flex:
            (x, y) = encode_cls_jo_pair(data_features, measurements, query, pair)
            xs.append(x)
            ys.append(y)
        else:  # flex
            (x, y) = encode_cls_jo_pair_flex(
                data_features, measurements, query, pair, flex_all
            )
            xs += x
            ys += y

    return (xs, ys)


def encode_cls_jo_pair(
    data_features, measurements, query, jo_pair
) -> tuple[list[float], float]:
    (jo1, jo2) = jo_pair
    x: list[float] = []
    # x += encoded_hw.copy()
    x.extend(
        flatten([encode_feature(data_features[query][jo1][j]) for j in jo1.split(",")])
    )
    # x += encoded_hw.copy()
    x.extend(
        flatten([encode_feature(data_features[query][jo2][j]) for j in jo2.split(",")])
    )

    if sum(measurements[query][jo1].joins) < sum(measurements[query][jo2].joins):
        y = 0
    else:  # if >=
        y = 1

    return (x, y)


def encode_cls_jo_pair_flex(
    data_features: AllDataFeatures,
    measurements: AllMeasurements,
    query: str,
    jo_pair: tuple[str, str],
    flex_all: bool,
) -> tuple[list[list[float]], list[float]]:
    (jo1, jo2) = jo_pair
    num_joins = len(data_features[query][jo1])

    assert num_joins == len(data_features[query][jo2])

    xs = []
    ys = []
    for i in range(0, 20 - num_joins + 1):
        x: list[float] = []
        for _ in range(i):
            x.extend(encode_feature(None))
            x.extend(encode_feature(None))
        for j1, j2 in zip(jo1.split(","), jo2.split(",")):
            x.extend(encode_feature(data_features[query][jo1][j1]))
            x.extend(encode_feature(data_features[query][jo2][j2]))
        for _ in range(20 - num_joins - i):
            x.extend(encode_feature(None))
            x.extend(encode_feature(None))
        if sum(measurements[query][jo1].joins) < sum(measurements[query][jo2].joins):
            y = 0
        else:  # if >=
            y = 1

        xs.append(x)
        ys.append(y)

        if not flex_all:
            break

    return (xs, ys)
