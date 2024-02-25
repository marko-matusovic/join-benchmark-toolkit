import numpy as np
from benchmark.tools.ml.encode_cls import encode_all_cls
from benchmark.tools.ml.load_all import load_all
from benchmark.tools.ml.load_features import load_hw_features
from sklearn.ensemble import (
    GradientBoostingClassifier,
    RandomForestClassifier,
    ExtraTreesClassifier,
    BaggingClassifier,
    AdaBoostClassifier,
    HistGradientBoostingClassifier,
)
import pickle as pkl

from benchmark.tools.tools import ensure_dir


def main(
    db_sets: list[str],
    training_set: int,
    # hw_name: str,
    num_joins: int,
    ml_model: str | None = None,
    res_path: str | None = None,
    normalize: bool = False,
):
    if ml_model == None:
        ml_model = "gbdt"
    if res_path == None:
        res_path = "./results"

    if ml_model == "gbdt":  # 56.9  52.9  54.9  # normalized 68.3  62.7  65.0
        model = GradientBoostingClassifier(max_depth=15, learning_rate=0.1)
    elif ml_model == "rf":  # 55.6  64.7  66.0  # normalized 45.1  42.2  37.3
        model = RandomForestClassifier()
    elif ml_model == "et":  # 70.0  73.9  68.3  # normalized 69.3  69.3  69.0
        model = ExtraTreesClassifier()
    elif ml_model == "bg":  # 50.0  43.5  42.8  # normalized 52.3  45.4  71.2
        model = BaggingClassifier()
    elif ml_model == "ab":  # 49.0  46.7  53.6  # normalized 67.0  69.6  65.0
        model = AdaBoostClassifier()
    elif ml_model == "hgb":  # 54.6  54.6  54.6  # normalized 52.0  52.0  52.0
        model = HistGradientBoostingClassifier()
    else:
        print("Error: Unknown ml_model!")
        exit(1)

    X = []
    y = []
    # ws = []

    # hw_features = load_hw_features(hw_name, res_path)

    for db_set in db_sets:
        print("Loading features and measurements")
        (features, measurements) = load_all(db_set, training_set, res_path, normalize)
        print("Encoding features and measurements")
        (Xi, yi) = encode_all_cls(features, measurements, num_joins)
        print(
            f"{db_set} has {len(Xi)} join-order combinations of join-length {num_joins}"
        )
        if len(Xi) == 0:
            continue
        X += Xi
        y += yi
        # ws += [1.0 / len(yi)] * len(yi)

    # train the model
    print("Training")
    model.fit(X, y)  # type: ignore

    file = f"{res_path}/models/cls/{ml_model}/set_{training_set}_NJO{num_joins}_{'_'.join(db_sets)}.pickle"
    ensure_dir(file)
    print(f"Saving the model to {file}")
    with open(file, "wb") as file_out:
        pkl.dump(model, file_out)

    # print(model.feature_importances_)
