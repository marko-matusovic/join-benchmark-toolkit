import numpy as np
from benchmark.tools.ml.encode import encode_all_reg, encode_all_cls
from benchmark.tools.ml.load_all import load_all
from benchmark.tools.ml.load_features import load_hw_features
from sklearn.ensemble import GradientBoostingClassifier
import pickle as pkl


def main(
    db_sets: list[str],
    training_set: int,
    hw_name: str,
    num_joins: int,
    res_path: str | None = None,
):
    if res_path == None:
        res_path = "./results"

    # create a gradient boosting regressor
    model = GradientBoostingClassifier(
        n_estimators=100, learning_rate=0.1, max_depth=20, random_state=None
    )

    X = []
    y = []
    ws = []

    hw_features = load_hw_features(hw_name, res_path)

    for db_set in db_sets:
        print("Loading features and measurements")
        (features, measurements) = load_all(db_set, training_set, res_path)
        print("Encoding features and measurements")
        (Xi, yi) = encode_all_cls(features, hw_features, measurements, num_joins)
        print(
            f"{db_set} has {len(Xi)} join-order combinations of join-length {num_joins}"
        )
        if len(Xi) == 0:
            continue
        X += Xi
        y += yi
        ws += [1.0 / len(yi)] * len(yi)

    # train the model
    print("Training")
    model.fit(X, y)

    file = f"{res_path}/models/gbdt_cls/set_{training_set}_NJO{num_joins}_{'_'.join(db_sets)}.pickle"
    print(f"Saving the model to {file}")
    with open(file, "wb") as file_out:
        pkl.dump(model, file_out)

    # print(model.feature_importances_)
