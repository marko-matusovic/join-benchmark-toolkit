from typing import Callable, NamedTuple
from benchmark.operations.operations import Operations, TVal
from benchmark.tools.schema_parser import TSchema, get_schema, rename_schema
import numpy as np


class Data(NamedTuple):
    schema: TSchema
    clusters: dict[str, set[str]]
    cluster_names: dict[str, str]

    def copy(self):
        return Data(
            schema=self.schema.copy(),
            clusters=self.clusters.copy(),
            cluster_names=self.cluster_names.copy(),
        )


def find_table(schema: TSchema, field_name: str) -> str:
    for table_name in schema:
        full_field_name = f"{table_name}.{field_name}"
        if field_name in schema[table_name] or full_field_name in schema[table_name]:
            return table_name
    print(f"ERROR: No table with field ({field_name}) found!")
    exit(1)


# =============== CLASS =================================================================


class Operations_ExecutionTree(Operations[Data, None]):
    def from_tables(
        self, db_path: str, db_name: str, tables: list[str], aliases: list[str] = []
    ):
        if len(aliases) != len(tables):
            aliases = tables

        def load() -> Data:
            data = Data(
                schema=rename_schema(get_schema(db_path, db_name), tables, aliases),
                clusters={ali: {ali} for ali in aliases},
                cluster_names={
                    ali: f"({ali})" for ali in aliases
                },  # Each cluster starts named as one table
            )
            return data

        return load

    # section :: FILTERS =================================

    def filter_field_eq(self, field_name: str, values: TVal | list[TVal]):
        if not isinstance(values, list):
            values = [values]

        def filter(data: Data):
            table_name = find_table(data.schema, field_name)

            cluster_name = f"({data.cluster_names[table_name]}S({field_name})={values})"
            for tbl in data.clusters[table_name]:
                data.cluster_names[tbl] = cluster_name

            return cluster_name

        return filter

    def filter_field_ne(self, field_name: str, value: TVal):
        def filter(data: Data):
            table_name = find_table(data.schema, field_name)

            cluster_name = f"({data.cluster_names[table_name]}S({field_name})!={value})"
            for tbl in data.clusters[table_name]:
                data.cluster_names[tbl] = cluster_name

            return cluster_name

        return filter

    def filter_ineq(
        self,
        field_name: str,
        value: TVal,
        comp: Callable[[TVal, TVal], bool],
    ):
        def filter(data: Data):
            table_name = find_table(data.schema, field_name)

            if comp == np.greater_equal:
                cluster_name = (
                    f"({data.cluster_names[table_name]}S({field_name})>={value})"
                )
            elif comp == np.greater:
                cluster_name = (
                    f"({data.cluster_names[table_name]}S({field_name})>{value})"
                )
            elif comp == np.less_equal:
                cluster_name = (
                    f"({data.cluster_names[table_name]}S({field_name})<={value})"
                )
            elif comp == np.less:
                cluster_name = (
                    f"({data.cluster_names[table_name]}S({field_name})<{value})"
                )
            else:
                print("ERROR: Unsupported comp operation")
                exit(1)

            for tbl in data.clusters[table_name]:
                data.cluster_names[tbl] = cluster_name

            return cluster_name

        return filter

    def filter_field_ge(self, field_name: str, value: TVal):
        return self.filter_ineq(field_name, value, np.greater_equal)

    def filter_field_gt(self, field_name: str, value: TVal):
        return self.filter_ineq(field_name, value, np.greater)

    def filter_field_le(self, field_name: str, value: TVal):
        return self.filter_ineq(field_name, value, np.less_equal)

    def filter_field_lt(self, field_name: str, value: TVal):
        return self.filter_ineq(field_name, value, np.less)

    def filter_field_like(self, field_name: str, values: list[str]):
        def filter(data: Data):
            table_name = find_table(data.schema, field_name)
            cluster_name = (
                f"({data.cluster_names[table_name]}S({field_name})LIKE{values})"
            )
            for tbl in data.clusters[table_name]:
                data.cluster_names[tbl] = cluster_name
            return cluster_name

        return filter

    def filter_field_not_like(self, field_name: str, value: str):
        def filter(data: Data):
            table_name = find_table(data.schema, field_name)
            cluster_name = (
                f"({data.cluster_names[table_name]}S({field_name})NOT-LIKE['{value}'])"
            )
            for tbl in data.clusters[table_name]:
                data.cluster_names[tbl] = cluster_name
            return cluster_name

        return filter

    # section :: JOIN =================================

    def join_fields(self, field_name_1: str, field_name_2: str):
        def join(data: Data):
            # ========== Logical Merging ==========
            table_name_1 = find_table(data.schema, field_name_1)
            table_name_2 = find_table(data.schema, field_name_2)

            cluster_name_1 = data.cluster_names[table_name_1]
            cluster_name_2 = data.cluster_names[table_name_2]
            cluster_1 = data.clusters[table_name_1]
            cluster_2 = data.clusters[table_name_2]

            # Figure out the new cluster name
            if cluster_name_1 != cluster_name_2:
                cluster_name = f"({data.cluster_names[table_name_1]}X{data.cluster_names[table_name_2]}ON({field_name_1})=({field_name_2}))"
                cluster = cluster_1.union(cluster_2)
            else:
                cluster_name = f"({cluster_name_1}XS({field_name_1})=({field_name_2}))"
                cluster = cluster_1

            # Update all tables in the cluster
            for tbl in cluster:
                data.clusters[tbl] = cluster
                data.cluster_names[tbl] = cluster_name

            return cluster_name

        return join
