from benchmark.tools.load import load_named_tables, load_table
from os.path import exists
import pickle


def clone(dfs):
    return {key: dfs[key].copy() for key in dfs}


def print_write(msg, out_file):
    print(msg)
    out_file.write(f'{msg}\n')
    out_file.flush()


def get_stats(df):
    return {
        "length": len(df.index),
        "unique": dict(df.nunique())
    }


def load_stats(db_name, tables, aliases):

    stats = {}

    for table in tables:
        file_name = f'data/{db_name}/stats/{table}.pickle'

        # try to load stats from cache
        if exists(file_name):
            table_stats = pickle.load(open(file_name, 'rb'))

        # If there is no cache, calculate new stats and create cache file
        else:
            df = load_table(db_name, table)
            table_stats = {
                'length': len(df.index),
                'unique': dict(df.nunique()),
                'dtype': {k: get_size_of_type(f'{v}') for (k, v) in dict(df.dtypes).items()},
            }
            pickle.dump(table_stats, open(file_name, 'wb'))

        stats[table] = table_stats

    # rename stats to use aliases
    return {
        alias: {
            'length': stats[table]['length'],
            'unique': {f'{alias}.{k}': v for (k, v) in stats[table]['unique'].items()}, # here we have to rename columns
            'dtype': {f'{alias}.{k}': v for (k, v) in stats[table]['dtype'].items()}, # here we have to rename columns
        }
        for (table, alias) in zip(tables, aliases)
    }


def get_size_of_type(type):
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


def bound(low, value, high):
    return min(max(low, value), high)
