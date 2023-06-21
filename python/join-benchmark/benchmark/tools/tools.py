from io import TextIOWrapper

from benchmark.operations.instructions import TDFs


def clone(dfs: TDFs) -> TDFs:
    return {key: dfs[key].copy() for key in dfs}


def print_write(msg: str, out_file: TextIOWrapper):
    print(msg)
    out_file.write(f"{msg}\n")
    out_file.flush()


def bound(low: float, value: float, high: float) -> float:
    return min(max(low, value), high)
