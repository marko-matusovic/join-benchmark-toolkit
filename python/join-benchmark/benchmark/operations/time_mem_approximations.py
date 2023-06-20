
from typing import NamedTuple
from benchmark.operations.operations import Operations, TVal
from benchmark.tools.schema import TSchema, get_schema, rename_schema
from benchmark.tools.tools import TStats, TableStats, bound, load_stats

# ADDITIONAL REDUCTION FOR JOINS
GENERAL_REDUCTION_FACTOR = 0.9


# CACHE FRESHNESS
# if result is THIS OR LESS entries in history, then it IS in cache
CACHE_HIT_GUARANTEE = 3
# if result is THIS OR MORE entries in history, then it IS NOT in cache
CACHE_MISS_GUARANTEE = 8
CACHE_HIT_MULTIPLIER = 0.8
CACHE_MISS_MULTIPLIER = 10.0


# LINEAR SCALING
TIME_MULTIPLIER = 1.0 / 1E8
MEMORY_MULTIPLIER = 1.0


# DEFAULT SELECTIVITY VALUES
# A = B
DEFAULT_SEL_EQ = 0.005
# A < B
DEFAULT_SEL_INEQ = 0.33
# A < B AND A > C
DEFAULT_SEL_RANGE_INEQ = 0.005
# A LIKE "apple"
DEFAULT_SEL_MATCH = 0.005
# Default for anything unknown
DEFAULT_SEL_UNKNOWN = 0.005
#  Default for anything unknown with NOT modifier
DEFAULT_SEL_NOT_UNKNOWN = 1 - DEFAULT_SEL_UNKNOWN


class Data(NamedTuple):
    schema: TSchema
    stats: TStats
    times: dict[str, float]
    memory: dict[str, float]
    history: list[str]


TRes = tuple[float, float]


class Time_Mem_Approx_Instructions(Operations[Data, TRes]):

    def from_tables(self, db_name: str, tables: list[str], aliases: list[str] = []):
        if len(aliases) != len(tables):
            aliases = tables

        def load() -> Data:
            schema = rename_schema(get_schema(db_name), tables, aliases)
            stats = load_stats(db_name, tables, aliases)
            return Data(
                schema=schema,
                stats=stats,
                times={},
                memory={},
                history=[],
            )

        return load

    def join_fields(self, field_name_1: str, field_name_2: str):
        def join(data: Data):
            table_name_1 = self.find_table(data.schema, field_name_1)
            table_name_2 = self.find_table(data.schema, field_name_2)
            if table_name_1 == table_name_2:
                return (0, 0)

            res = f'({table_name_1}X{table_name_2})'
            data.history.insert(0, res)
            data.schema[res] = data.schema[table_name_1] + \
                data.schema[table_name_2]
            del data.schema[table_name_1]
            del data.schema[table_name_2]

            stats_1 = data.stats[table_name_1]
            stats_2 = data.stats[table_name_2]

            if res not in data.stats:
                min_unique = min(
                    stats_1.unique[field_name_1], stats_2.unique[field_name_2])
                rows_per_unique_1 = 1.0 * stats_1.length / \
                    stats_1.unique[field_name_1]
                rows_per_unique_2 = 1.0 * stats_2.length / \
                    stats_2.unique[field_name_2]

                multiplication_factor_1 = 1.0 * \
                    min_unique / stats_1.unique[field_name_1]
                multiplication_factor_2 = 1.0 * \
                    min_unique / stats_2.unique[field_name_2]

                data.stats[res] = TableStats(
                    length=min_unique * rows_per_unique_1 * rows_per_unique_2,
                    unique={
                        k: v * multiplication_factor_1 for (k, v) in stats_1.unique.items()}
                    | {k: v * multiplication_factor_2 for (k, v) in stats_2.unique.items()},
                    dtype=stats_1.dtype | stats_2.dtype
                )

                # General reduction factor
                data.stats[res] = self.scale_stats(
                    data.stats[res], GENERAL_REDUCTION_FACTOR)

            # Time Cost
            # Skipping the step to see how large were the tables merged after them, instead using general cache timeout
            age_1 = data.history.index(
                table_name_1) if table_name_1 in data.history else CACHE_MISS_GUARANTEE
            age_2 = data.history.index(
                table_name_2) if table_name_2 in data.history else CACHE_MISS_GUARANTEE
            age_multiplier = self.calc_history_multiplier(
                age_1) * self.calc_history_multiplier(age_2)
            length = stats_1.length + stats_2.length
            data.times[res] = length * age_multiplier * TIME_MULTIPLIER

            # Memory Cost
            size_1 = stats_1.length * sum(stats_1.dtype.values())
            size_2 = stats_2.length * sum(stats_2.dtype.values())
            data.memory[res] = (size_1 + size_2) * MEMORY_MULTIPLIER

            return (data.times[res], data.memory[res])
        return join

    # The plot below shows the function calculated in this method.
    # X asis is the age of the result, it is the number of other joins performed since the join in question
    # Y axis is the multiplier used for time cost calculation
    #
    #                             CACHE_MISS_GUARANTEE
    #                                    |
    #                                    v
    #                                     _________ CACHE_MISS_MULTIPLIER
    #                                   /
    #                                 /
    # CACHE_HIT_MULTIPLIER ________ /
    #                               ^
    #                               |
    #                       CACHE_HIT_GUARANTEE
    # PRIVATE
    def calc_history_multiplier(self, age: float) -> float:
        return CACHE_HIT_MULTIPLIER + (bound(CACHE_HIT_GUARANTEE, age, CACHE_MISS_GUARANTEE) - CACHE_HIT_GUARANTEE) * (CACHE_MISS_MULTIPLIER - CACHE_HIT_MULTIPLIER) / (CACHE_MISS_GUARANTEE - CACHE_HIT_GUARANTEE)

    # PRIVATE
    def scale_stats(self, stats: TableStats, mult_factor: float) -> TableStats:
        return TableStats(
            length=stats.length * mult_factor,
            unique={col: stats.unique[col] *
                    mult_factor for col in stats.unique},
            dtype=stats.dtype
        )

    def filter_field_eq(self, field_name: str, values: list[TVal]):
        def filter(data: Data):
            table_name = self.find_table(data.schema, field_name)
            stats = data.stats[table_name]
            mult_factor = 1.0 * len(values) / stats.unique[field_name]
            stats = self.scale_stats(stats, mult_factor)
            return (0, 0)  # does not return cost
        return filter

    def filter_field_ne(self, field_name: str, value: TVal):
        def filter(data: Data):
            table_name = self.find_table(data.schema, field_name)
            stats = data.stats[table_name]
            mult_factor = 1 - (1.0 / stats.unique[field_name])
            self.scale_stats(stats, mult_factor)
            return (0, 0)  # does not return cost
        return filter

    def filter_field_ge(self, field_name: str, value: TVal):
        def filter(data: Data):
            table_name = self.find_table(data.schema, field_name)
            data.stats[table_name] = self.scale_stats(
                data.stats[table_name], 0.5)
            return (0, 0)  # does not return cost
        return filter

    def filter_field_gt(self, field_name: str, value: TVal):
        def filter(data: Data):
            table_name = self.find_table(data.schema, field_name)
            data.stats[table_name] = self.scale_stats(
                data.stats[table_name], 0.5)
            return (0, 0)  # does not return cost
        return filter

    def filter_field_le(self, field_name: str, value: TVal):
        def filter(data: Data):
            table_name = self.find_table(data.schema, field_name)
            data.stats[table_name] = self.scale_stats(
                data.stats[table_name], 0.5)
            return (0, 0)  # does not return cost
        return filter

    def filter_field_lt(self, field_name: str, value: TVal):
        def filter(data: Data):
            table_name = self.find_table(data.schema, field_name)
            data.stats[table_name] = self.scale_stats(
                data.stats[table_name], 0.5)
            return (0, 0)  # does not return cost
        return filter

    def filter_field_like(self, field_name: str, values: list[str]):
        def filter(data: Data):
            table_name = self.find_table(data.schema, field_name)
            stats = data.stats[table_name]
            n_matches = sum([1.0 + 4 * value.count('%') for value in values])
            mult_factor = bound(
                0.0, n_matches / stats.unique[field_name], 1.0)
            stats = self.scale_stats(stats, mult_factor)
            return (0, 0)  # does not return cost
        return filter

    def filter_field_not_like(self, field_name: str, value: str):
        def filter(data: Data):
            table_name = self.find_table(data.schema, field_name)
            stats = data.stats[table_name]
            n_matches = 1.0 + 4 * value.count('%')
            mult_factor = 1.0 - \
                bound(0.0, n_matches / stats.unique[field_name], 1.0)
            stats = self.scale_stats(stats, mult_factor)
            return (0, 0)  # does not return cost
        return filter

    # PRIVATE
    def find_table(self, schema: TSchema, field_name: str) -> str:
        for table_name in schema:
            if field_name in schema[table_name]:
                return table_name
        print(f"ERROR: No table with field {field_name} found!")
        exit(1)
