from benchmark.tools.ml.encode import encode_query
from benchmark.tools.ml.load_all import load_all
from sklearn.ensemble import GradientBoostingRegressor
import pickle as pkl


def main(db_set: str, training_set: int, model_name: str, res_path: str | None = None):
    if res_path == None:
        res_path = "./results"

    # load the model
    model: GradientBoostingRegressor = pkl.load(
        open(f"{res_path}/models/{model_name}.pickle", "rb")
    )

    # load the evaluation set
    (features, measurements) = load_all(db_set, training_set, res_path)

    print(f"Model:", model_name)
    print("Feature importances:")
    print(model.feature_importances_)

    for query in features:
        for jo in set(features[query].keys()) & set(measurements[query].keys()):
            (X, y_real) = encode_query(features, measurements, query, jo)

            y_predict = model.predict(X)  # type: ignore

            print(f"Query: {query}")
            print(f"Join Order: {jo}")
            print(f"Real Y: {y_real}")
            print(f"Pred Y: {y_predict}")
