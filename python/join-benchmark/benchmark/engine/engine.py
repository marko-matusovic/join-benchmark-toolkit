from typing import Any

DataFrame = Any

def set_engine(name: str):
    global engine
    global engine_name
    engine_name = name.lower().strip()
    if engine_name == "cpu":
        import pandas
        engine = pandas
    elif engine_name == "gpu":
        import cudf
        engine = cudf

def get_engine() -> Any:
    global engine
    return engine

def get_engine_name() -> str:
    global engine_name
    return engine_name
