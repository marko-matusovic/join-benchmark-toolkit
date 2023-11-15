from benchmark.engine.engine import DataFrame, get_engine
from benchmark.tools.schema import get_schema


def load_named_tables(db_path:str, db_name: str, table_names: list[str], table_aliases: list[str] = []) -> dict[str, DataFrame]:
    dfs = {}

    if len(table_aliases) < len(table_names):
        table_aliases = table_names

    schema = get_schema(db_path, db_name)
    for (t_name, t_alias) in zip(table_names, table_aliases):
        dfs[t_alias] = get_engine().read_csv(
            f'{db_path}/tables/{t_name}.{get_extension(db_name)}',
            sep=get_separator(db_name),
            header=None,
            names=[f'{t_alias}.{col}' for col in schema[t_name]],
            index_col=False)

    return dfs # type: ignore


def load_table(db_path:str, db_name:str, table_name:str) -> DataFrame:
    schema = get_schema(db_path, db_name)
    return get_engine().read_csv(
        f'{db_path}/tables/{table_name}.{get_extension(db_name)}',
        sep=get_separator(db_name),
        header=None,
        names=schema[table_name],
        index_col=False)


def get_extension(db_name: str) -> str:
    return {
        "ssb": 'tbl',
        "job": "csv",
        "tpcds": "csv"
    }[db_name]


def get_separator(db_name: str) -> str:
    return {
        "ssb": '|',
        "job": ",",
        "tpcds": ","
    }[db_name]
