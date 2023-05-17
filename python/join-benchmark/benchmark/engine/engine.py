import pandas
import cudf

def set_engine(name):
    global engine
    if name == "pandas":
        engine = pandas
    elif name == "cudf":
        engine = cudf

def get_engine():
    global engine
    return engine
