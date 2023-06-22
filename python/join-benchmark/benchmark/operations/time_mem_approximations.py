from typing import Any, Callable, NamedTuple
from benchmark.operations.operations import Operations, TVal
from benchmark.tools.schema import TSchema, get_schema, rename_schema
from benchmark.tools.stats import ColumnStats, TStats, TableStats, load_stats
from benchmark.tools.tools import bound
import numpy as np

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
TIME_MULTIPLIER = 1.0 / 1e8
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
        str, list[str]
    ]  # to keep track of what is merged together (like union-find, but with lists)
    cluster_names: dict[str, str] # to keep track of cluster names
    times: dict[str, float] = {}  # approx times per table
    memory: dict[str, float] = {}  # approx memory per table
    history: list[HistoryTuple] = []


TRes = tuple[float, float]


class Time_Mem_Approx_Instructions(Operations[Data, TRes]):
    def from_tables(self, db_name: str, tables: list[str], aliases: list[str] = []):
        if len(aliases) != len(tables):
            aliases = tables

        def load() -> Data:
            return Data(
                schema=rename_schema(get_schema(db_name), tables, aliases),
                stats=load_stats(db_name, tables, aliases),
                selects={ali: [] for ali in aliases},
                clusters={ali: [ali] for ali in aliases},
                cluster_names={ali: f'({ali})' for ali in aliases}, # Each cluster starts named as one table
            )

        return load

    # PRIVATE
    def find_table(self, schema: TSchema, field_name: str) -> str:
        for table_name in schema:
            if field_name in schema[table_name]:
                return table_name
        print(f"ERROR: No table with field {field_name} found!")
        exit(1)

    # PRIVATE
    def calc_history_multiplier(self, age: float) -> float:
        """
        The plot below shows the function calculated in this method.
        - X asis is the age of the result, it is the number of other joins performed since the join in question
        - Y axis is the multiplier used for time cost calculation
        ::

            >                             CACHE_MISS_GUARANTEE
            >                                    |
            >                                    v
            >                                     _________ CACHE_MISS_MULTIPLIER
            >                                   /
            >                                 /
            > CACHE_HIT_MULTIPLIER ________ /
            >                               ^
            >                               |
            >                       CACHE_HIT_GUARANTEE

        """
        return CACHE_HIT_MULTIPLIER + (
            bound(CACHE_HIT_GUARANTEE, age, CACHE_MISS_GUARANTEE) - CACHE_HIT_GUARANTEE
        ) * (CACHE_MISS_MULTIPLIER - CACHE_HIT_MULTIPLIER) / (
            CACHE_MISS_GUARANTEE - CACHE_HIT_GUARANTEE
        )

    # Old approach used to rescale the tables when applying filters, new approach collects the selectivities in list
    # # PRIVATE
    # def scale_stats(self, stats: TableStats, selectivity: float) -> TableStats:
    #     return TableStats(
    #         length=stats.length * selectivity,
    #         column={
    #             c: ColumnStats(
    #                 dtype=stats.column[c].dtype,
    #                 unique=stats.column[c].unique * selectivity,
    #                 bounds=stats.column[c].bounds,
    #                 hist=stats.column[c].hist,  # TODO: scale the histogram?
    #             )
    #             for c in stats.column
    #         },
    #     )

    # section :: FILTERS =================================

    def filter_field_eq(self, field_name: str, values: list[TVal]):
        def filter(data: Data):
            table_name = self.find_table(data.schema, field_name)
            stats = data.stats[table_name]
            selectivity = 1.0 * len(values) / stats.column[field_name].unique
            # stats = self.scale_stats(stats, selectivity)
            data.selects[table_name].append(selectivity)
            return (0, 0)  # does not return cost

        return filter

    def filter_field_ne(self, field_name: str, value: TVal):
        def filter(data: Data):
            table_name = self.find_table(data.schema, field_name)
            stats = data.stats[table_name]
            selectivity = 1 - (1.0 / stats.column[field_name].unique)
            # self.scale_stats(stats, selectivity)
            data.selects[table_name].append(selectivity)
            return (0, 0)  # does not return cost

        return filter

    def filter_ineq(
        self,
        field_name: str,
        value: TVal,
        comp: Callable[[TVal, TVal], bool],
    ):
        def filter(data: Data):
            table_name = self.find_table(data.schema, field_name)
            # data.stats[table_name] = self.scale_stats(data.stats[table_name], 0.5)
            table_stats = data.stats[table_name]
            column_stats = table_stats.column[field_name]

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
            table_name = self.find_table(data.schema, field_name)
            stats = data.stats[table_name]
            n_matches = sum([1 + value.count("%") for value in values])
            selectivity = bound(0.0, DEFAULT_SEL_MATCH * n_matches, 1.0)
            # stats = self.scale_stats(stats, selectivity)
            data.selects[table_name].append(selectivity)
            return (0, 0)  # does not return cost

        return filter

    def filter_field_not_like(self, field_name: str, value: str):
        def filter(data: Data):
            table_name = self.find_table(data.schema, field_name)
            stats = data.stats[table_name]
            n_matches = 1 + value.count("%")
            selectivity = bound(0.0, 1.0 - n_matches * DEFAULT_SEL_MATCH, 1.0)
            # stats = self.scale_stats(stats, selectivity)
            data.selects[table_name].append(selectivity)
            return (0, 0)  # does not return cost

        return filter

    # section :: JOIN =================================

    def sum_hist_overlap(
        self,
        hist_1: tuple[np.ndarray, np.ndarray],
        hist_2: tuple[np.ndarray, np.ndarray],
        i_1: int,
        i_2: int,
        total_1: float,
        total_2: float,
    ) -> float:
        """
        Assumes
            * bins_1[i_1] <= bins_2[i_2]
            * bins_1[i_1+1] <= bins_2[i_2+1]
            * bins_1[i_1+1] > bins_2[i_2]

        Illustrated overlap is calculated
        ::

                    i_1     i_1+1
            his_1 --|-------|--------
                    |    xxx|
                        |xxx    |
            his_2 ------|-------|----
                        i_2     i_2+1
        """
        (counts_1, bins_1) = hist_1
        (counts_2, bins_2) = hist_2

        assert bins_1[i_1] <= bins_2[i_2]
        assert bins_1[i_1 + 1] <= bins_2[i_2 + 1]
        assert bins_1[i_1 + 1] > bins_2[i_2]

        overlap = bins_1[i_1 + 1] - bins_2[i_2]
        width_1 = bins_1[i_1 + 1] - bins_1[i_1]
        width_2 = bins_2[i_2 + 1] - bins_2[i_2]
        density_1 = counts_1[i_1] / total_1
        density_2 = counts_2[i_2] / total_2
        return (density_1 * overlap / width_1) * (density_2 * overlap / width_2)

    def join_fields(
        self, field_name_1: str, field_name_2: str
    ) -> Callable[[Data], TRes]:
        def join(data: Data) -> TRes:
            # ========== Logical Merging ==========
            table_name_1 = self.find_table(data.schema, field_name_1)
            table_name_2 = self.find_table(data.schema, field_name_2)

            # If merged already, skip
            if (
                table_name_1 == table_name_2
                or data.clusters[table_name_1] == data.clusters[table_name_2]
            ):
                return (0, 0)

            # Merge tables
            data.clusters[table_name_1].extend(data.clusters[table_name_2])
            data.clusters[table_name_2] = data.clusters[table_name_1]
            
            # Figure out the new cluster name
            res = f'({data.cluster_names[table_name_1]}X{data.cluster_names[table_name_2]})'
            # Rename all tables to this cluster
            for t in data.clusters[table_name_1]:
                data.cluster_names[t] = res
                
            # ========== Cardinality Estimate ==========

            stats_1 = data.stats[table_name_1]
            stats_2 = data.stats[table_name_2]
            col_stats_1 = stats_1.column[field_name_1]
            col_stats_2 = stats_2.column[field_name_2]
            len_1 = stats_1.length
            len_2 = stats_2.length
            hist_1 = col_stats_1.hist
            hist_2 = col_stats_2.hist

            if hist_1 != None and hist_2 != None:
                (counts_1, bins_1) = hist_1
                (counts_2, bins_2) = hist_2

                i_1 = 0
                i_2 = 0

                # Find the overlap and then use @self.sum_hist_overlap to calculate it
                selectivity = 0
                while i_1 + 1 < len(bins_1) and i_2 + 1 < len(bins_2):
                    if bins_1[i_1] < bins_2[i_2]:
                        if bins_2[i_2] < bins_1[i_1 + 1]:
                            selectivity += self.sum_hist_overlap(
                                hist_1, hist_2, i_1, i_2, len_1, len_2
                            )
                        # when == or > then no overlap and move forward
                        i_1 += 1
                    elif bins_2[i_2] < bins_1[i_1]:
                        if bins_1[i_1] < bins_2[i_2 + 1]:
                            selectivity += self.sum_hist_overlap(
                                hist_2, hist_1, i_2, i_1, len_2, len_1
                            )
                        # when == or > then no overlap and move forward
                        i_2 += 1
                    else:
                        # equal, find lower next bound
                        if bins_1[i_1 + 1] < bins_2[i_2 + 1]:
                            selectivity += self.sum_hist_overlap(
                                hist_1, hist_2, i_1, i_2, len_1, len_2
                            )
                            i_1 += 1
                        elif bins_2[i_2 + 1] < bins_1[i_1 + 1]:
                            selectivity += self.sum_hist_overlap(
                                hist_2, hist_1, i_2, i_1, len_2, len_1
                            )
                            i_2 += 1
                        else:
                            # If they are perfectly equal, increment both
                            selectivity += self.sum_hist_overlap(
                                hist_1, hist_2, i_1, i_2, len_1, len_2
                            )
                            i_1 += 1
                            i_2 += 1

                assert 0 <= selectivity <= 1
            else:
                # Cannot use histograms, calculating selectivity naively with # unique values
                low = min(col_stats_1.unique, col_stats_2.unique)
                high = max(col_stats_1.unique, col_stats_2.unique)

                selectivity = low/high
            
            # Store selectivity (sqrt, because it will be squared when calculating)
            selectivity_sqrt = np.sqrt(selectivity)
            data.selects[table_name_1].append(selectivity_sqrt)
            data.selects[table_name_2].append(selectivity_sqrt)

            # ========== Cost Model ==========

            # TODO: update to use selectivities in cluster

            stats_1 = data.stats[table_name_1]
            stats_2 = data.stats[table_name_2]

            # Time Cost Model
            # Skipping the step to see how large were the tables merged after them, instead using general cache timeout
            age_1 = (
                data.history.index(HistoryTuple(table=table_name_1))
                if HistoryTuple(table=table_name_1) in data.history
                else CACHE_MISS_GUARANTEE
            )
            age_2 = (
                data.history.index(table_name_2)
                if table_name_2 in data.history
                else CACHE_MISS_GUARANTEE
            )
            age_multiplier = self.calc_history_multiplier(
                age_1
            ) * self.calc_history_multiplier(age_2)
            length = len_1 + len_2
            data.times[res] = length * age_multiplier * TIME_MULTIPLIER

            # Memory Cost Model
            size_1 = len_1 * sum([v.dtype for v in stats_1.column.values()])
            size_2 = len_2 * sum([v.dtype for v in stats_2.column.values()])
            data.memory[res] = (size_1 + size_2) * MEMORY_MULTIPLIER
            
            # ========== Update History ==========
            
            # new entry, at the front
            data.history.insert(0, HistoryTuple(
                table=res,
                length=0, # should be resulting size (product of length scaled by selects from cluster)
                row_size=0, # should be size of all rows in cluster
            ))

            return (data.times[res], data.memory[res])

        return join
