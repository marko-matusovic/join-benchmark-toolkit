import json
from benchmark.tools.load import load_tables
from benchmark.tools.schema import get_schema


def get_stats(db_name):
    try:
        stats = json.load(open(f"data/{db_name}/stats.json", "r"))
    except:
        stats = calc_stats(db_name)
        json.dump(stats, open(f"data/{db_name}/stats.json", "w"))

    return stats


def calc_stats(db_name):
    schema = get_schema(db_name)
    dfs = load_tables(db_name, schema.keys())
    return {
        name: {
            "length": len(dfs[name].index),
            "unique": dict(dfs[name].nunique()),
            "dsize": {col: get_dtype_size(dfs.dtypes[col]) for col in dfs[name]},
        }
        for name in schema.keys()
    }


def get_dtype_size(dtype):
    return {
        "bool": 8,
        "int8": 8,
        "int32": 32,
        "float32": 32,
        "int64": 64,
        "float64": 64,
        "datetime64": 64,
        "object": 256,
    }[f"{dtype}"]

