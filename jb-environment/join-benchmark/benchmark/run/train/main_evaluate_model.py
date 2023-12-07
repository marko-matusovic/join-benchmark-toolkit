from benchmark.tools.ml.types import AllMeasurements, AllFeatures
from benchmark.tools.ml.encode import encode_feature, encode_query
from benchmark.tools.ml.load_all import load_all
from sklearn.ensemble import GradientBoostingRegressor
import pickle as pkl


def main(db_set: str, training_set: int, model_name:str, res_path: str | None = None):
    if res_path == None:
        res_path = "./results"

    # load the model
    model:GradientBoostingRegressor = pkl.load(open(f'{res_path}/models/{model_name}.pickle', 'rb'))
    
    # load the evaluation set
    (features, measurements) = load_all(db_set, training_set, res_path)
    
    print(f'Model:', model_name)
    print('Feature importances:')
    print(model.feature_importances_)
    
    for query in features:
        (X, y_real) = encode_query(features, measurements, query)
        
        y_predict = model.predict(X)
        
        print(f'Query: {query}')
        print(f'Real Y: {y_real}')
        print(f'Predicted Y: {y_predict}')
        
    
    
    
