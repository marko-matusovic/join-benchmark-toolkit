from typing import Any, Callable, NamedTuple

from benchmark.operations.operations import Operations, TVal
from benchmark.tools.schema_parser import TSchema, get_schema, rename_schema
from benchmark.tools.stats import (
    ColumnStats,
    TStats,
    TableStats,
    get_row_size,
    load_stats,
)
from benchmark.tools.tools import bound, cover, overlap_right
import numpy as np


# LINEAR SCALING
TIME_MULTIPLIER = 1.0 / 1e8
MEMORY_MULTIPLIER = 1.0 / 1e2


# CACHE FRESHNESS
CACHE_HIT_GUARANTEE = 1e6  # basically approx cache size TODO: should be set automatically based on the actual system
CACHE_HIT_MULTIPLIER = 1
CACHE_MISS_MULTIPLIER = 5


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


class HistoryTuple(NamedTuple):
    table: str
    length: float = 0  # number of rows in table
    row_size: float = 0  # size of one row

    # Overriding default behavior to be able to use operations on list (.index(), in) to search with just string (table) value
    def __eq__(self, other) -> bool:
        if type(other) == HistoryTuple:
            return self.table == other.table
        elif type(other) == str:
            return self.table == other
        return False


class Data(NamedTuple):
    schema: TSchema
    stats: TStats
    # selectivity multipliers applied per table
    selects: dict[str, list[float]]
    clusters: dict[
        str, set[str]
    ]  # to keep track of what is merged together (like union-find, but with lists)
    cluster_names: dict[str, str]  # to keep track of cluster names
    times: dict[str, float] = {}  # approx times per table
    memory: dict[str, float] = {}  # approx memory per table
    history: list[HistoryTuple] = []

    def copy(self):
        return Data(
            schema=self.schema.copy(),
            stats=self.stats.copy(),
            selects=self.selects.copy(),
            clusters=self.clusters.copy(),
            cluster_names=self.cluster_names.copy(),
            times=self.times.copy(),
            memory=self.memory.copy(),
            history=self.history.copy(),
        )


Res = tuple[float, float]


def find_table(schema: TSchema, field_name: str) -> str:
    for table_name in schema:
        full_field_name = f"{table_name}.{field_name}"
        if field_name in schema[table_name] or full_field_name in schema[table_name]:
            return table_name
    print(f"ERROR: No table with field ({field_name}) found!")
    exit(1)


def calc_age_mem(data: Data, table_name: str) -> float:
    if table_name not in data.history:
        return CACHE_MISS_MULTIPLIER

    idx = data.history.index(table_name)
    mem = 0.0
    for i in range(0, idx + 1):
        mem += data.history[i].length * data.history[i].row_size

    return mem


def calc_age_mult(data: Data, table_name: str) -> float:
    mem = calc_age_mem(data, table_name)

    if mem < CACHE_HIT_GUARANTEE:
        return CACHE_HIT_MULTIPLIER
    return CACHE_MISS_MULTIPLIER

    # Before we used the linear transition from hit mult to miss mult
    # return CACHE_HIT_MULTIPLIER + (bound(CACHE_HIT_GUARANTEE, age, CACHE_MISS_GUARANTEE) - CACHE_HIT_GUARANTEE) * (CACHE_MISS_MULTIPLIER - CACHE_HIT_MULTIPLIER) / (CACHE_MISS_GUARANTEE - CACHE_HIT_GUARANTEE)


def total_length_of_cluster(data: Data, cluster: set[str]) -> float:
    return float(
        np.prod(
            [np.prod([data.stats[tbl].length] + data.selects[tbl]) for tbl in cluster]
        )
    )


def sum_hist_overlap(
    section_1: tuple[tuple[np.ndarray, np.ndarray], int],
    section_2: tuple[tuple[np.ndarray, np.ndarray], int],
) -> float:
    ((counts_1, bins_1), i_1) = section_1
    ((counts_2, bins_2), i_2) = section_2

    assert overlap_right(bins_1[i_1], bins_1[i_1 + 1], bins_2[i_2], bins_2[i_2 + 1])

    overlap = bins_1[i_1 + 1] - bins_2[i_2]
    width_1 = bins_1[i_1 + 1] - bins_1[i_1]
    width_2 = bins_2[i_2 + 1] - bins_2[i_2]
    density_1 = counts_1[i_1] / np.sum(counts_1)
    density_2 = counts_2[i_2] / np.sum(counts_2)
    return (density_1 * overlap / width_1) * (density_2 * overlap / width_2)


def sum_hist_cover(
    section_1: tuple[tuple[np.ndarray, np.ndarray], int],
    section_2: tuple[tuple[np.ndarray, np.ndarray], int],
) -> float:
    ((counts_1, bins_1), i_1) = section_1
    ((counts_2, bins_2), i_2) = section_2

    assert cover(bins_1[i_1], bins_1[i_1 + 1], bins_2[i_2], bins_2[i_2 + 1])

    width_1 = bins_1[i_1 + 1] - bins_1[i_1]
    width_2 = bins_2[i_2 + 1] - bins_2[i_2]
    density_1 = counts_1[i_1] / np.sum(counts_1)
    density_2 = counts_2[i_2] / np.sum(counts_2)
    return (density_1 * width_2 / width_1) * (density_2)


def sel_join_hist(hist_1, hist_2):
    (counts_1, bins_1) = hist_1
    (counts_2, bins_2) = hist_2

    i_1 = 0
    i_2 = 0

    # Find the overlap
    selectivity = 0
    while i_1 + 1 < len(bins_1) and i_2 + 1 < len(bins_2):
        section_1 = (hist_1, i_1)
        section_2 = (hist_2, i_2)

        if overlap_right(bins_1[i_1], bins_1[i_1 + 1], bins_2[i_2], bins_2[i_2 + 1]):
            selectivity += sum_hist_overlap(section_1, section_2)
            i_1 += 1
        elif overlap_right(bins_2[i_2], bins_2[i_2 + 1], bins_1[i_1], bins_1[i_1 + 1]):
            selectivity += sum_hist_overlap(section_2, section_1)
            i_2 += 1
        elif cover(bins_1[i_1], bins_1[i_1 + 1], bins_2[i_2], bins_2[i_2 + 1]):
            selectivity += sum_hist_cover(section_1, section_2)
            i_2 += 1
        elif cover(bins_2[i_2], bins_2[i_2 + 1], bins_1[i_1], bins_1[i_1 + 1]):
            selectivity += sum_hist_cover(section_2, section_1)
            i_1 += 1
        else:
            if bins_1[i_1] < bins_2[i_2]:
                i_1 += 1
            else:
                i_2 += 1

    assert 0 <= selectivity <= 1
    return selectivity


def new_history_tuple(data: Data, cluster_name: str):
    tbl_in_cluster = list(data.cluster_names.keys())[
        list(data.cluster_names.values()).index(cluster_name)
    ]
    cluster = data.clusters[tbl_in_cluster]
    return HistoryTuple(
        table=cluster_name,
        length=total_length_of_cluster(data, cluster),
        row_size=sum([get_row_size(data.stats[tbl]) for tbl in cluster]),
    )


# =============== CLASS =================================================================


class Operations_CostModel(Operations[Data, Res]):
    def from_tables(
        self, db_path: str, db_name: str, tables: list[str], aliases: list[str] = []
    ):
        if len(aliases) != len(tables):
            aliases = tables

        def load() -> Data:
            data = Data(
                schema=rename_schema(get_schema(db_path, db_name), tables, aliases),
                stats=load_stats(db_path, db_name, tables, aliases),
                selects={ali: [] for ali in aliases},
                clusters={ali: {ali} for ali in aliases},
                cluster_names={
                    ali: f"({ali})" for ali in aliases
                },  # Each cluster starts named as one table
            )
            data = data._replace(
                history=[
                    HistoryTuple(
                        table=data.cluster_names[ali],
                        length=data.stats[ali].length,
                        row_size=get_row_size(data.stats[ali]),
                    )
                    for ali in aliases[::-1]
                ],
            )
            return data

        return load

    # section :: FILTERS =================================

    def filter_field_eq(self, field_name: str, values: TVal | list[TVal]):
        if not isinstance(values, list):
            values = [values]

        def filter(data: Data):
            table_name = find_table(data.schema, field_name)
            short_field_name = field_name.split(".")[-1]
            stats = data.stats[table_name]

            # histogram
            # if stats.column[short_field_name].hist is not None :
            # (counts, bounds) = stats.column[short_field_name].hist
            # TODO: figure out if this is possible
            # heat map
            heat_map = stats.column[short_field_name].heat_map
            if heat_map != None:
                selectivity = (
                    np.sum(
                        [
                            (heat_map[str(value)] if str(value) in heat_map else 0)
                            for value in values  # type: ignore
                        ]
                    )
                    / stats.length
                )
            # unique
            else:
                selectivity = 1.0 * len(values) / stats.column[short_field_name].unique

            data.selects[table_name].append(selectivity)

            cluster_name = f"({data.cluster_names[table_name]}S({field_name})={values})"
            for tbl in data.clusters[table_name]:
                data.cluster_names[tbl] = cluster_name

            return (0, 0)  # does not return cost

        return filter

    def filter_field_ne(self, field_name: str, value: TVal):
        def filter(data: Data):
            table_name = find_table(data.schema, field_name)
            short_field_name = field_name.split(".")[-1]
            stats = data.stats[table_name]

            # histogram
            # if stats.column[short_field_name].hist is not None :
            # (counts, bounds) = stats.column[short_field_name].hist
            # TODO: figure out if this is possible
            # heat map
            heat_map = stats.column[short_field_name].heat_map
            if heat_map != None:
                selectivity = 1 - (1.0 * heat_map[str(value)] / stats.length)
            # unique
            else:
                selectivity = 1 - (1.0 / stats.column[short_field_name].unique)

            data.selects[table_name].append(selectivity)
            cluster_name = f"({data.cluster_names[table_name]}S({field_name})!={value})"
            for tbl in data.clusters[table_name]:
                data.cluster_names[tbl] = cluster_name

            return (0, 0)  # does not return cost

        return filter

    def filter_ineq(
        self,
        field_name: str,
        value: TVal,
        comp: Callable[[TVal, TVal], bool],
    ):
        def filter(data: Data):
            table_name = find_table(data.schema, field_name)
            short_field_name = field_name.split(".")[-1]
            table_stats = data.stats[table_name]
            column_stats = table_stats.column[short_field_name]

            # if there are no bounds, there is definitely no histogram, fall back to default selectivity
            if column_stats.bounds == None:
                selectivity = DEFAULT_SEL_INEQ

            # check if value is out of bounds
            elif comp(
                value,
                (
                    column_stats.bounds[1]
                    if comp(column_stats.bounds[1], column_stats.bounds[0])
                    else column_stats.bounds[0]
                ),
            ):
                selectivity = 0

            # check if there is a histogram
            elif column_stats.hist != None:
                (counts, bins) = column_stats.hist

                start_bin = 0 if comp(1, 0) else -1
                direction = 1 if comp(1, 0) else -1
                end_bin = start_bin + direction * len(bins)

                # while
                #   * haven't reached the end bin yet
                #   * value still satisfies the bin boundary
                while start_bin != end_bin and comp(value, bins[start_bin]):
                    start_bin += direction

                # sum the counts of bins
                total_count = sum(
                    counts[start_bin:end_bin]
                    if start_bin < end_bin
                    else counts[end_bin:start_bin]
                )

                # assume uniformity, add linear part of the previous bin to total_count
                # case filter greater
                if 0 < start_bin:
                    total_count += (
                        counts[start_bin - 1]
                        * (bins[start_bin] - value)
                        / (bins[start_bin] - bins[start_bin - 1])
                    )
                # case filter less
                elif start_bin < -1:
                    total_count += (
                        counts[start_bin + 1]
                        * (value - bins[start_bin])
                        / (bins[start_bin] - bins[start_bin + 1])
                    )
                selectivity = total_count / table_stats.length

            # if histogram failed, assume uniformity and approximate with bounds
            elif type(value) == int or type(value) == float:
                (low, high) = column_stats.bounds
                if comp(1, 0):  # filter greater than value
                    selectivity = (high - value) / (high - low)
                elif comp(0, 1):  # filter less than value
                    selectivity = (value - low) / (high - low)
                else:
                    print("ERROR: Unknown comparison function!")
                    exit(1)

            # using default selectivity
            else:
                selectivity = DEFAULT_SEL_INEQ

            data.selects[table_name].append(selectivity)

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

            return (0, 0)  # does not return cost

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
            stats = data.stats[table_name]
            n_matches = sum([1 + value.count("%") for value in values])
            selectivity = bound(0.0, DEFAULT_SEL_MATCH * n_matches, 1.0)
            data.selects[table_name].append(selectivity)
            cluster_name = (
                f"({data.cluster_names[table_name]}S({field_name})LIKE{values})"
            )
            for tbl in data.clusters[table_name]:
                data.cluster_names[tbl] = cluster_name
            return (0, 0)  # does not return cost

        return filter

    def filter_field_not_like(self, field_name: str, value: str):
        def filter(data: Data):
            table_name = find_table(data.schema, field_name)
            stats = data.stats[table_name]
            n_matches = 1 + value.count("%")
            selectivity = bound(0.0, 1.0 - n_matches * DEFAULT_SEL_MATCH, 1.0)
            data.selects[table_name].append(selectivity)
            cluster_name = (
                f"({data.cluster_names[table_name]}S({field_name})NOT-LIKE['{value}'])"
            )
            for tbl in data.clusters[table_name]:
                data.cluster_names[tbl] = cluster_name
            return (0, 0)  # does not return cost

        return filter

    # section :: JOIN =================================

    def join_fields(
        self, field_name_1: str, field_name_2: str
    ) -> Callable[[Data], Res]:
        def join(data: Data) -> Res:
            # ========== Logical Merging ==========
            table_name_1 = find_table(data.schema, field_name_1)
            table_name_2 = find_table(data.schema, field_name_2)
            short_field_name_1 = field_name_1.split(".")[-1]
            short_field_name_2 = field_name_2.split(".")[-1]

            cluster_name_1 = data.cluster_names[table_name_1]
            cluster_name_2 = data.cluster_names[table_name_2]
            cluster_1 = data.clusters[table_name_1]
            cluster_2 = data.clusters[table_name_2]

            # Figure out the new cluster name
            if cluster_name_1 != cluster_name_2:
                cluster_name = f"({data.cluster_names[table_name_1]}X{data.cluster_names[table_name_2]}ON({field_name_1})=({field_name_2}))"
                cluster = cluster_1.union(cluster_2)
                already_joined = False
            else:
                cluster_name = f"({cluster_name_1}XS({field_name_1})=({field_name_2}))"
                cluster = cluster_1
                already_joined = True

            # Update all tables in the cluster
            for tbl in cluster:
                data.clusters[tbl] = cluster
                data.cluster_names[tbl] = cluster_name

            if already_joined:
                return (0, 0)

            # ========== Cardinality Estimate ==========

            stats_1 = data.stats[table_name_1]
            stats_2 = data.stats[table_name_2]
            col_stats_1 = stats_1.column[short_field_name_1]
            col_stats_2 = stats_2.column[short_field_name_2]
            hist_1 = col_stats_1.hist
            hist_2 = col_stats_2.hist

            if hist_1 != None and hist_2 != None:
                selectivity = sel_join_hist(hist_1, hist_2)
            else:
                # Cannot use histograms, calculating selectivity naively with # unique values
                next_cardinality = max(stats_1.length, stats_2.length) * min(
                    col_stats_1.unique, col_stats_2.unique
                )
                selectivity = 1.0 * next_cardinality / next_cardinality

            # ========== Cost Model ==========

            total_length_1 = total_length_of_cluster(data, cluster_1)
            total_length_2 = total_length_of_cluster(data, cluster_2)
            total_length = total_length_of_cluster(data, cluster)

            # Time Cost Model
            age_1 = calc_age_mult(data, table_name_1)
            age_2 = calc_age_mult(data, table_name_2)

            data.times[cluster_name] = (
                total_length_1 * age_1 + total_length_2 * age_2
            ) * TIME_MULTIPLIER

            # Memory Cost Model
            row_size = sum(
                [v.dtype for tbl in cluster for v in data.stats[tbl].column.values()]
            )
            data.memory[cluster_name] = (
                float(total_length * row_size) * MEMORY_MULTIPLIER
            )

            # ========== Update Selectivity ==========

            if already_joined:
                data.selects[table_name_1].append(selectivity)
            else:
                # Store selectivity (sqrt, because it will be multiplied together when calculating)
                selectivity_sqrt = np.sqrt(selectivity)
                data.selects[table_name_1].append(selectivity_sqrt)
                data.selects[table_name_2].append(selectivity_sqrt)

            # ========== Update History ==========

            # new entry, at the front
            data.history.insert(
                0,
                HistoryTuple(
                    table=cluster_name,
                    length=total_length,  # should be resulting size (product of length scaled by selects from cluster)
                    row_size=row_size,  # should be size of all rows in cluster
                ),
            )

            return (data.times[cluster_name], data.memory[cluster_name])

        return join
