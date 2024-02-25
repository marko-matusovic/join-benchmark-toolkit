from benchmark.tools.ml.encode_reg import encode_all_reg
from benchmark.tools.ml.load_all import load_all
from benchmark.tools.ml.load_features import load_hw_features
from sklearn.ensemble import (
    GradientBoostingRegressor,
    RandomForestRegressor,
    ExtraTreesRegressor,
    RandomForestRegressor,
    BaggingRegressor,
    AdaBoostRegressor,
    HistGradientBoostingRegressor,
)
import pickle as pkl

from benchmark.tools.tools import ensure_dir


def main(
    db_sets: list[str],
    training_set: int,
    # hw_name: str,
    joins_in_block: int = 4,
    ml_model: str | None = None,
    res_path: str | None = None,
    normalize: bool = False,
):
    if ml_model == None:
        ml_model = "gbdt"
    if res_path == None:
        res_path = "./results"

    if ml_model == "gbdt":  # -0.13  -0.10  -0.14 ## norm:  0.27   0.26   0.33
        model = GradientBoostingRegressor()
    elif ml_model == "rf":  #  0.07   0.06   0.04 ## norm:  0.35   0.38   0.32
        model = RandomForestRegressor()
    elif ml_model == "et":  #  0.56   0.43   0.47 ## norm:  0.34   0.48   0.36
        model = ExtraTreesRegressor()
    elif ml_model == "bg":  #  0.16   0.18   0.14 ## norm:  0.31   0.16   0.02
        model = BaggingRegressor()
    elif ml_model == "ab":  #  0.15   0.08   0.09 ## norm:  0.34  -0.07   0.17
        model = AdaBoostRegressor()
    elif ml_model == "hgb":  #  0.08   0.08   0.07 ## norm: -0.09  -0.09  -0.09
        model = HistGradientBoostingRegressor()
    else:
        print("Error: Unknown ml_model!")
        exit(1)

    X = []
    y = []
    # ws = []

    # hw_features = load_hw_features(hw_name, res_path)

    for db_set in db_sets:
        (features, measurements) = load_all(db_set, training_set, res_path, normalize)
        (Xi, yi) = encode_all_reg(features, measurements, joins_in_block)
        # (Xi, yi) = encode_all_reg(features, hw_features, measurements, joins_in_block)
        X += Xi
        y += yi
        # ws += [1.0 / len(yi)] * len(yi)

    # train the model
    model.fit(X, y)  # type: ignore
    # model.fit(X, y, ws)

    file = f"{res_path}/models/reg/{ml_model}/set_{training_set}_BS{joins_in_block}_{'_'.join(db_sets)}.pickle"
    ensure_dir(file)
    with open(file, "wb") as file_out:
        pkl.dump(model, file_out)

    print("Feature importances:")
    print(model.feature_importances_)  # type: ignore
