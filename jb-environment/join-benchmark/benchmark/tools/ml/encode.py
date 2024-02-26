from math import isnan
from benchmark.tools.ml.types import (
    DataFeatures,
    extract_c,
    extract_t,
    get_feature_names,
)


# select
#   None    -> include all features
#   []      -> only cardinality estimates
#   [f1...] -> include cardinality estimates, f1 and all the rest
#   - must be from the feature_names set
def encode_feature(
    features: DataFeatures | None = None,
    select: None | list[str] = None,
    t_unify: bool = False,
) -> list[float]:
    if select is None:
        select = get_feature_names()

    if features == None:
        return [0.0] * feature_length(select, t_unify)
    else:
        encoded = []

        for s in select:
            if s.startswith("t_"):
                if not t_unify:
                    encoded.append(extract_t(features.table_1, s))
                    encoded.append(extract_t(features.table_2, s))
                else:
                    encoded.append(
                        extract_t(features.table_1, s) + extract_t(features.table_2, s)
                    )
            elif s.startswith("c_"):
                encoded.append(extract_c(features.cross, s))

    if feature_length(select, t_unify) != len(encoded):
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
def feature_length(select: None | list[str] = None, t_unify=False) -> int:
    if select is None:
        return 24

    if t_unify is True:
        return len(select)

    num_features = 0
    for f in select:
        if f.startswith("t_"):
            num_features += 2
        if f.startswith("c_"):
            num_features += 1
    return num_features
