from benchmark.tools.ml.encode import JOINS_IN_BLOCK, encode_all
from benchmark.tools.ml.load_all import load_all
from benchmark.tools.ml.load_features import load_hw_features
from sklearn.ensemble import GradientBoostingRegressor
import pickle as pkl


def main(
    db_sets: list[str], training_set: int, hw_name: str, res_path: str | None = None
):
    if res_path == None:
        res_path = "./results"

    # create a gradient boosting regressor
    model = GradientBoostingRegressor(
        n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0
    )

    X = []
    y = []
    ws = []

    hw_features = load_hw_features(hw_name, res_path)
    
    for db_set in db_sets:
        (features, measurements) = load_all(db_set, training_set, res_path)
        (Xi, yi) = encode_all(features, hw_features, measurements)
        X += Xi
        y += yi
        ws += [1.0 / len(yi)] * len(yi)

    # train the model
    model.fit(X, y, ws)

    file = f"{res_path}/models/gbdt/set_{training_set}_BS{JOINS_IN_BLOCK}_{'_'.join(db_sets)}.pickle"
    with open(file, "wb") as file_out:
        pkl.dump(model, file_out)

    print(model.feature_importances_)
