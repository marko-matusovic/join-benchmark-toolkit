from typing import Callable
from pandas import DataFrame

def from_tables(tables):
    def from_tbls(dfs: dict[str, DataFrame]) -> None:
        names = list(dfs.keys())
        for name in names:
            if name not in tables:
                del dfs[name]
    return from_tbls

def join_fields(field_1, field_2) -> Callable[[dict[str, DataFrame]], None]:
    def join(dfs: dict[str, DataFrame]) -> None:
        name_1 = find_table(dfs, field_1)
        name_2 = find_table(dfs, field_2)
        table_1 = dfs[name_1]
        table_2 = dfs[name_2]
        del dfs[name_1]
        del dfs[name_2]
        dfs[f'({name_1}X{name_2})'] = table_1.merge(table_2, how='inner', left_on=field_1, right_on=field_2)
    return join

def filter_field_eq(field:str, values:list[str]) -> Callable[[dict[str, DataFrame]], None]:
    def filter(dfs: dict[str, DataFrame]) -> None:
        name = find_table(dfs, field)
        table = dfs[name]
        del dfs[name]
        dfs[f'({name}𝜎{field}∊{values})'] = table.loc[table[field].isin(values)]
    return filter

def filter_field_ge(field:str, value) -> Callable[[dict[str, DataFrame]], None]:
    def filter(dfs: dict[str, DataFrame]) -> None:
        name = find_table(dfs, field)
        table = dfs[name]
        del dfs[name]
        dfs[f'({name}𝜎{field}≥{value})'] = table.loc[table[field] >= value]
    return filter

def filter_field_gt(field:str, value) -> Callable[[dict[str, DataFrame]], None]:
    def filter(dfs: dict[str, DataFrame]) -> None:
        name = find_table(dfs, field)
        table = dfs[name]
        del dfs[name]
        dfs[f'({name}𝜎{field}>{value})'] = table.loc[table[field] > value]
    return filter

def filter_field_le(field:str, value) -> Callable[[dict[str, DataFrame]], None]:
    def filter(dfs: dict[str, DataFrame]) -> None:
        name = find_table(dfs, field)
        table = dfs[name]
        del dfs[name]
        dfs[f'({name}𝜎{field}≤{value})'] = table.loc[table[field] <= value]
    return filter

def filter_field_lt(field:str, value) -> Callable[[dict[str, DataFrame]], None]:
    def filter(dfs: dict[str, DataFrame]) -> None:
        name = find_table(dfs, field)
        table = dfs[name]
        del dfs[name]
        dfs[f'({name}𝜎{field}<{value})'] = table.loc[table[field] < value]
    return filter

def find_table(dfs: dict[str, DataFrame], field: str) -> str | None:
    for name in dfs:
        if field in dfs[name]:
            return name
    return None
