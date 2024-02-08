from benchmark.tools.ml.load_measurements import load_measurements
from benchmark.tools.ml.load_features import load_data_features
from benchmark.tools.ml.types import AllDataFeatures, AllMeasurements


def load_all(
    db_set: str, training_set: int, res_path: str, normalize=False
) -> tuple[AllDataFeatures, AllMeasurements]:
    features = load_data_features(db_set, training_set, res_path, normalize)
    measurements = load_measurements(db_set, training_set, res_path)

    # Find the intersection
    # Assuming features and measurements are your dictionaries
    common_keys = set(features.keys()) & set(measurements.keys())

    filtered_features = {k: features[k] for k in common_keys}
    filtered_measurements = {k: measurements[k] for k in common_keys}

    for key in common_keys:
        sub_common_keys = set(features[key].keys()) & set(measurements[key].keys())
        filtered_features[key] = {k: features[key][k] for k in sub_common_keys}
        filtered_measurements[key] = {k: measurements[key][k] for k in sub_common_keys}

    return (filtered_features, filtered_measurements)
