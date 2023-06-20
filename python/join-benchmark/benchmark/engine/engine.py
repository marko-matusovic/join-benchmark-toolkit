from typing import Any

DataFrame = Any

def set_engine(name:str):
    global engine
    if name == "pandas":
        import pandas
        engine = pandas
    elif name == "cudf":
        import cudf
        engine = cudf

def get_engine() -> Any:
    global engine
    return engine
