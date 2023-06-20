from io import TextIOWrapper
from typing import NamedTuple
from benchmark.engine.engine import DataFrame
from benchmark.operations.instructions import TDFs
from benchmark.tools.load import load_table
from os.path import exists
import pickle

def clone(dfs:TDFs) -> TDFs:
    return {key: dfs[key].copy() for key in dfs}


def print_write(msg:str, out_file:TextIOWrapper):
    print(msg)
    out_file.write(f'{msg}\n')
    out_file.flush()



# Stats for one table
class TableStats(NamedTuple):
    length: float
    unique: dict[str, float]
    dtype: dict[str, float]

# All stats 
TStats = dict[str, TableStats]

def calc_stats(df:DataFrame):
    return {
        "length": len(df.index),
        "unique": dict(df.nunique())
    }


def load_stats(db_name: str, tables: list[str], aliases: list[str]) -> TStats:

    stats: TStats = {}

    for table in tables:
        file_name = f'data/{db_name}/stats/{table}.pickle'

        # try to load stats from cache
        if exists(file_name):
            table_stats: TableStats = pickle.load(open(file_name, 'rb'))

        # If there is no cache, calculate new stats and create cache file
        else:
            df = load_table(db_name, table)
            table_stats = TableStats(
                length = len(df.index),
                unique = dict(df.nunique()),
                dtype = {k: get_size_of_type(f'{v}') for (k, v) in dict(df.dtypes).items()},
            )
            pickle.dump(table_stats, open(file_name, 'wb'))

        stats[table] = table_stats

    # rename stats to use aliases
    return {
        alias: TableStats(
            length = stats[table].length,
            unique = {f'{alias}.{k}': v for (k, v) in stats[table].unique.items()}, # here we have to rename columns
            dtype = {f'{alias}.{k}': v for (k, v) in stats[table].dtype.items()}, # here we have to rename columns
        )
        for (table, alias) in zip(tables, aliases)
    }


def get_size_of_type(type: str) -> int:
    return {
        "bool": 8,
        "int8": 8,
        "uint8": 8,
        "int32": 32,
        "uint32": 32,
        "float32": 32,
        "int64": 64,
        "uint64": 64,
        "float64": 64,
        "datetime64[ns]": 64,
        "datetime64[ns, tz]": 64,
        "object": 2056,
    }[f'{type}']


def bound(low:float, value:float, high:float) -> float:
    return min(max(low, value), high)
