import pickle
from os.path import exists
from os import makedirs
from typing import NamedTuple, TypeVar

import numpy as np

from benchmark.engine.engine import DataFrame, get_engine_name
from benchmark.tools.load import load_table
from benchmark.tools.tools import bound

# Constants
HIST_MIN_ITEMS_COVERAGE = 0.75
HIST_MIN_NUM_BINS = 10
HIST_MAX_NUM_BINS = 5_000
HIST_MEAN_ITEMS_PER_BIN = 100


# Stats for one column
class ColumnStats(NamedTuple):
    dtype: float
    unique: float
    bounds: None | tuple[float, float] = None  # min and max values per column
    hist: None | tuple[np.ndarray, np.ndarray] = None  # [counts] and [bin_ranges]
    heat_map: None | dict[str, int] = None  # for str values, make a value:count hashmap


# Stats for one table
class TableStats(NamedTuple):
    length: float
    column: dict[str, ColumnStats]


# All stats
TStats = dict[str, TableStats]


def calc_simple_stats(df: DataFrame):
    return {"length": len(df.index), "unique": dict(df.nunique())}


def load_stats(
    db_path: str, db_name: str, tables: list[str], aliases: list[str]
) -> TStats:
    stats: TStats = {}

    stats_path = f"{db_path}/stats"

    if not exists(stats_path):
        makedirs(stats_path)

    for table in tables:
        file_path = f"{stats_path}/{table}.pickle"

        # try to load stats from cache
        if exists(file_path):
            table_stats: TableStats = pickle.load(open(file_path, "rb"))

        # If there is no cache, calculate new stats and create cache file
        else:
            df = load_table(db_path, db_name, table)
            table_stats = TableStats(
                length=len(df.index),
                column={
                    column: ColumnStats(
                        dtype=get_size_of_type(
                            df[column].dtypes.__str__()
                            if get_engine_name() == "cpu" else 
                            df[column]._dtypes.__str__()
                            ),
                        unique=df[column].nunique(),
                    )
                    for column in df
                },
            )

            # Bounds and Hist are conditional on number type
            for column in df:
                try:
                    low = df[column].min()
                    high = df[column].max()
                    table_stats.column[column] = table_stats.column[column]._replace(
                        bounds=(low, high),
                    )
                    # Select ints and floats for histogram
                    values = [
                        v for v in df[column] if type(v) == int or type(v) == float
                    ]
                    num_bins = bound(
                        HIST_MIN_NUM_BINS,  # min val
                        int(table_stats.length / HIST_MEAN_ITEMS_PER_BIN),  # calc val
                        min(1 + int(high - low), HIST_MAX_NUM_BINS),  # max val
                    )
                    # TODO: update histogram to be equi-deep
                    # If at least some % of values pass, make the histogram
                    # Otherwise, ignore it, as it wouldn't be appropriate representation
                    if HIST_MIN_ITEMS_COVERAGE * table_stats.length < len(values):
                        table_stats.column[column] = table_stats.column[
                            column
                        ]._replace(
                            hist=np.histogram(
                                values,
                                bins=num_bins,
                                range=(low - 1, high + 1),
                            )
                        )
                except:
                    pass
                if table_stats.column[column].hist == None:
                    try:
                        table_stats.column[column] = table_stats.column[
                            column
                        ]._replace(heat_map=dict(df.groupby(by=column).count().T.max()))
                    except:
                        pass

                pickle.dump(table_stats, open(file_path, "wb"))

        stats[table] = table_stats

    # rename stats to use aliases
    return {alias: stats[table] for (table, alias) in zip(tables, aliases)}


T = TypeVar("T")


def add_prefix(dict_orig: dict[str, T], alias: str) -> dict[str, T]:
    return {f"{alias}.{k}": v for (k, v) in dict_orig.items()}


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
    }[f"{type}"]


def get_row_size(stats: TableStats) -> float:
    return sum([stats.column[col].dtype for col in stats.column])
