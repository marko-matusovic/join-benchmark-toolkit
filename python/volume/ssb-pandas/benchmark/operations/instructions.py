from typing import Callable
from pandas import DataFrame

from benchmark.tools.load import load_tables
from benchmark.tools.tools import clone

class Instructions:
    def from_tables(self, tables):
        dfs = load_tables(tables)

        def load():
            return clone(dfs)
        return load

    def join_fields(self, field_1, field_2):
        def join(dfs):
            name_1 = self.find_table(dfs, field_1)
            name_2 = self.find_table(dfs, field_2)
            table_1 = dfs[name_1]
            table_2 = dfs[name_2]
            del dfs[name_1]
            del dfs[name_2]
            dfs[f'({name_1}X{name_2})'] = table_1.merge(
                table_2, how='inner', left_on=field_1, right_on=field_2)
        return join

    def filter_field_eq(self, field, values):
        def filter(dfs):
            name = self.find_table(dfs, field)
            table = dfs[name]
            del dfs[name]
            dfs[f'({name}𝜎{field}∊{values})'] = table.loc[table[field].isin(values)]
        return filter

    def filter_field_ge(self, field, value):
        def filter(dfs):
            name = self.find_table(dfs, field)
            table = dfs[name]
            del dfs[name]
            dfs[f'({name}𝜎{field}≥{value})'] = table.loc[table[field] >= value]
        return filter

    def filter_field_gt(self, field, value):
        def filter(dfs):
            name = self.find_table(dfs, field)
            table = dfs[name]
            del dfs[name]
            dfs[f'({name}𝜎{field}>{value})'] = table.loc[table[field] > value]
        return filter

    def filter_field_le(self, field, value):
        def filter(dfs):
            name = self.find_table(dfs, field)
            table = dfs[name]
            del dfs[name]
            dfs[f'({name}𝜎{field}≤{value})'] = table.loc[table[field] <= value]
        return filter

    def filter_field_lt(self, field, value):
        def filter(dfs):
            name = self.find_table(dfs, field)
            table = dfs[name]
            del dfs[name]
            dfs[f'({name}𝜎{field}<{value})'] = table.loc[table[field] < value]
        return filter

    def find_table(self, dfs, field):
        for name in dfs:
            if field in dfs[name]:
                return name
        return None
