import json
import os
from typing import NamedTuple, TypeAlias
from benchmark.engine.engine import DataFrame, get_engine, get_engine_name
from benchmark.tools.schema_parser import get_schema

DB_NAME: TypeAlias = str


class DB_CONFIG(NamedTuple):
    file_suffix: str
    column_sep: str


def load_db_config() -> dict[DB_NAME, DB_CONFIG]:
    file_path = (
        os.path.abspath(__file__).removesuffix("/benchmark/tools/load.py")
        + "/db_config.json"
    )
    with open(file_path, "r") as config_file:
        lines = [
            line.strip()
            for line in config_file.readlines()
            if not line.strip().startswith("//")
        ]
        config_dict = json.loads(" ".join(lines))
        return {db_name: DB_CONFIG(**config) for db_name, config in config_dict.items()}


def load_named_tables(
    db_path: str, db_name: str, table_names: list[str], table_aliases: list[str] = []
) -> dict[str, DataFrame]:
    db_config = load_db_config()
    dfs = {}

    if len(table_aliases) < len(table_names):
        table_aliases = table_names

    schema = get_schema(db_path, db_name)
    for t_name, t_alias in zip(table_names, table_aliases):
        
        if get_engine_name() == "cpu":
            args = {
                'low_memory': False
            }
        else:
            args = {}
            
        try:
            dfs[t_alias] = get_engine().read_csv(
                f"{db_path}/tables/{t_name}.{db_config[db_name].file_suffix}",
                sep=db_config[db_name].column_sep,
                header=None,
                names=[f"{t_alias}.{col}" for col in schema[t_name]],
                index_col=False,
                **args
            )
        except Exception as e:
            print(f"Error! The table {t_name} as {t_alias} cannot be loaded.")
            print(e)

    return dfs


def load_table(db_path: str, db_name: str, table_name: str) -> DataFrame:
    db_config = load_db_config()
    schema = get_schema(db_path, db_name)
    return get_engine().read_csv(
        f"{db_path}/tables/{table_name}.{db_config[db_name].file_suffix}",
        sep=db_config[db_name].column_sep,
        header=None,
        names=schema[table_name],
        index_col=False,
    )
