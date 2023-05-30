def set_engine(name):
    global engine
    if name == "pandas":
        import pandas
        engine = pandas
    elif name == "cudf":
        import cudf
        engine = cudf

def get_engine():
    global engine
    return engine
