from io import TextIOWrapper
import os
from typing import TypeVar

from benchmark.operations.operations_real import TDFs


def clone(dfs: TDFs) -> TDFs:
    return {key: dfs[key].copy() for key in dfs}


def print_write(msg: str, out_file: TextIOWrapper):
    print(msg)
    out_file.write(f"{msg}\n")
    out_file.flush()


def bound(low: float, value: float, high: float) -> float:
    return min(max(low, value), high)


def overlap_right(x_1: int, x_2: int, y_1: int, y_2: int) -> bool:
    """
    Illustrated overlap is verified.
    ::

        |     x_1     x_2+1
        | ----|-------|--------
        |     |    xxx|
        |         |xxx    |
        | --------|-------|----
        |         y_1     y_2+1
    """
    assert x_1 <= x_2
    assert y_1 <= y_2
    return x_1 <= y_1 and x_2 <= y_2 and y_1 < x_2


def cover(x_1: int, x_2: int, y_1: int, y_2: int) -> bool:
    """
    Illustrated overlap is verified.
    ::

        |    x_1          x_2+1
        | ---|------------|----
        |    |    xxxxx   |
        |        |xxxxx|
        | -------|-----|-------
        |        y_1   y_2+1
    """
    assert x_1 <= x_2
    assert y_1 <= y_2
    return x_1 <= y_1 and y_2 <= x_2


T = TypeVar("T")


def flatten(arr: list[list[T]]) -> list[T]:
    return [b for a in arr for b in a]

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)