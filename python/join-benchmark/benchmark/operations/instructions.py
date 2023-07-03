from typing import Any
from benchmark.engine.engine import DataFrame, get_engine_name
from benchmark.operations.operations import Operations, TVal
from benchmark.tools.load import load_named_tables

TDFs = dict[str, DataFrame]


class Real_Instructions(Operations[TDFs, None]):
    def from_tables(self, db_name: str, tables: list[str], aliases: list[str] = []):
        def load() -> dict[str, DataFrame]:
            dfs = load_named_tables(db_name, tables, aliases)
            return {f"({tbl})": dfs[tbl] for tbl in dfs}

        return load

    def join_fields(self, field_name_1: str, field_name_2: str):
        def join(dfs: TDFs) -> None:
            table_name_1 = self.find_names(dfs, field_name_1)
            table_name_2 = self.find_names(dfs, field_name_2)
            if table_name_1 == table_name_2:
                self.join_filter_eq(dfs, table_name_1, field_name_1, field_name_2)
                return
            table_1 = dfs[table_name_1]
            table_2 = dfs[table_name_2]
            del dfs[table_name_1]
            del dfs[table_name_2]
            dfs[f"({table_name_1}X{table_name_2})"] = table_1.merge(
                table_2, how="inner", left_on=field_name_1, right_on=field_name_2
            )

        return join

    # PRIVATE
    def join_filter_eq(
        self, dfs: TDFs, table_name: str, field_name_1: str, field_name_2: str
    ):
        table = dfs[table_name]
        del dfs[table_name]
        dfs[f"({table_name}XS({field_name_1})=({field_name_2}))"] = table.loc[
            table[field_name_1] == table[field_name_2]
        ]

    def filter_field_eq(self, field_name: str, values: list[TVal]):
        def filter(dfs: TDFs) -> None:
            table_name = self.find_names(dfs, field_name)
            table = dfs[table_name]
            del dfs[table_name]
            dfs[f"({table_name}S({field_name})={values})"] = table.loc[
                table[field_name].isin(values)
            ]

        return filter

    def filter_field_ne(self, field_name: str, value: TVal):
        def filter(dfs: TDFs) -> None:
            table_name = self.find_names(dfs, field_name)
            table = dfs[table_name]
            del dfs[table_name]
            dfs[f"({table_name}S({field_name})!={value})"] = table.loc[
                table[field_name] != value
            ]

        return filter

    def filter_field_ge(self, field_name: str, value: TVal):
        def filter(dfs: TDFs) -> None:
            table_name = self.find_names(dfs, field_name)
            table = dfs[table_name]
            del dfs[table_name]
            dfs[f"({table_name}S({field_name})>={value})"] = table.loc[
                table[field_name] >= value
            ]

        return filter

    def filter_field_gt(self, field_name: str, value: TVal):
        def filter(dfs: TDFs) -> None:
            table_name = self.find_names(dfs, field_name)
            table = dfs[table_name]
            del dfs[table_name]
            dfs[f"({table_name}S({field_name})>{value})"] = table.loc[
                table[field_name] > value
            ]

        return filter

    def filter_field_le(self, field_name: str, value: TVal):
        def filter(dfs: TDFs) -> None:
            table_name = self.find_names(dfs, field_name)
            table = dfs[table_name]
            del dfs[table_name]
            dfs[f"({table_name}S({field_name})<={value})"] = table.loc[
                table[field_name] <= value
            ]

        return filter

    def filter_field_lt(self, field_name: str, value: TVal):
        def filter(dfs: TDFs) -> None:
            table_name = self.find_names(dfs, field_name)
            table = dfs[table_name]
            del dfs[table_name]
            dfs[f"({table_name}S({field_name})<{value})"] = table.loc[
                table[field_name] < value
            ]

        return filter

    def filter_field_like(self, field_name: str, values: list[str]):
        def filter(dfs: TDFs) -> None:
            table_name = self.find_names(dfs, field_name)
            table = dfs[table_name]
            del dfs[table_name]
            index = self.like_index(table[field_name], values[0])
            for value in values[1:]:
                index = index | self.like_index(table[field_name], value)
            dfs[f"({table_name}S({field_name})LIKE{values})"] = table.loc[index]

        return filter

    def filter_field_not_like(self, field_name: str, value: str):
        def filter(dfs: TDFs) -> None:
            table_name = self.find_names(dfs, field_name)
            table = dfs[table_name]
            del dfs[table_name]
            index = self.like_index(table[field_name], value) != True
            dfs[f"({table_name}S({field_name})NOT-LIKE['{value}'])"] = table.loc[index]

        return filter

    # PRIVATE
    def like_index(self, col: Any, value: str) -> Any:
        # disallow regex expresions
        value = value.replace("\\", "\\\\")
        value = value.replace(".", "\\.")
        value = value.replace("(", "\\(")
        value = value.replace(")", "\\)")
        value = value.replace("[", "\\[")
        value = value.replace("]", "\\]")
        value = value.replace("|", "\\|")
        value = value.replace("{", "\\{")
        value = value.replace("}", "\\}")
        value = value.replace("*", "\\*")
        value = value.replace("+", "\\+")
        value = value.replace("?", "\\?")
        value = value.replace("^", "\\^")
        value = value.replace("$", "\\$")
        value = value.replace("/", "\\/")
        value = value.replace("-", "\\-")
        # allow wildcards
        value = value.replace("%", ".*")
        if get_engine_name() == "cpu":
            return col.str.contains(f"^{value}$", na=True)
        elif get_engine_name() == "gpu":
            return col.str.contains(f"^{value}$")
        else:
            print("ERROR: Unsupported engine name found!")
            exit(1)

    # PRIVATE
    def find_names(self, dfs: TDFs, field_name: str) -> str:
        for table_name in dfs:
            if field_name in dfs[table_name]:
                return table_name
        print("ERROR: No table found for field '{}'".format(field_name))
        exit(1)
