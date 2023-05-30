
from benchmark.tools.schema import get_schema, rename_schema
from benchmark.tools.tools import bound, get_size_of_type, load_stats

GENERAL_REDUCTION_FACTOR = 0.9
CACHE_HIT_GUARANTEE = 3 # if result is THIS OR LESS entries in history, then it IS in cache
CACHE_MISS_GUARANTEE = 8 # if result is THIS OR MORE entries in history, then it IS NOT in cache
CACHE_HIT_MULTIPLIER = 0.8
CACHE_MISS_MULTIPLIER = 10.0
TIME_MULTIPLIER = 1.0 / 1E8
MEMORY_MULTIPLIER = 1.0

class Time_Mem_Approx_Instructions:
    def from_tables(self, db_name, tables, aliases=[]):
        if len(aliases) != len(tables):
            aliases = tables

        def load():
            schema = rename_schema(get_schema(db_name), tables, aliases)
            stats = load_stats(db_name, tables, aliases)
            data = {
                "schema": schema,
                "stats": stats,
                "times": {},
                "memory": {},
                "history": [],
            }
            return data

        return load

    def join_fields(self, field_name_1, field_name_2):
        def join(data):
            table_name_1 = self.find_table(data["schema"], field_name_1)
            table_name_2 = self.find_table(data["schema"], field_name_2)
            if table_name_1 == table_name_2:
                return (0, 0)

            res = f'({table_name_1}X{table_name_2})'
            data['history'].insert(0, res)
            data["schema"][res] = data["schema"][table_name_1] + data["schema"][table_name_2]
            del data["schema"][table_name_1]
            del data["schema"][table_name_2]

            stats_1 = data["stats"][table_name_1]
            stats_2 = data["stats"][table_name_2]
            
            if res not in data["stats"]:
                min_unique = min(stats_1['unique'][field_name_1],stats_2['unique'][field_name_2])
                rows_per_unique_1 = 1.0 * stats_1['length'] / stats_1['unique'][field_name_1]
                rows_per_unique_2 = 1.0 * stats_2['length'] / stats_2['unique'][field_name_2]

                multiplication_factor_1 = 1.0 * min_unique / stats_1['unique'][field_name_1]
                multiplication_factor_2 = 1.0 * min_unique / stats_2['unique'][field_name_2]

                data["stats"][res] = {
                    "length": min_unique * rows_per_unique_1 * rows_per_unique_2,
                    "unique": {k: v * multiplication_factor_1 for (k, v) in stats_1["unique"].items()}
                            | {k: v * multiplication_factor_2 for (k, v) in stats_2["unique"].items()},
                    "dtype": stats_1["dtype"] | stats_2["dtype"]
                }

                # General reduction factor
                self.scale_stats(data["stats"][res], GENERAL_REDUCTION_FACTOR)

            # Time Cost
            # Skipping the step to see how large were the tables merged after them, instead using general cache timeout
            age_1 = data['history'].index(table_name_1) if table_name_1 in data['history'] else CACHE_MISS_GUARANTEE
            age_2 = data['history'].index(table_name_2) if table_name_2 in data['history'] else CACHE_MISS_GUARANTEE
            age_multiplier = self.calc_history_multiplier(age_1) * self.calc_history_multiplier(age_2)
            length = stats_1['length'] + stats_2['length']
            data["times"][res] = length * age_multiplier * TIME_MULTIPLIER

            # Memory Cost
            size_1 = stats_1['length'] * sum(stats_1['dtype'].values())
            size_2 = stats_2['length'] * sum(stats_2['dtype'].values())
            data["memory"][res] = (size_1 + size_2) * MEMORY_MULTIPLIER

            return (data["times"][res], data["memory"][res])
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
    def calc_history_multiplier(self, age):
        return CACHE_HIT_MULTIPLIER + (bound(CACHE_HIT_GUARANTEE, age, CACHE_MISS_GUARANTEE) - CACHE_HIT_GUARANTEE) * (CACHE_MISS_MULTIPLIER - CACHE_HIT_MULTIPLIER) / (CACHE_MISS_GUARANTEE - CACHE_HIT_GUARANTEE)

    # PRIVATE
    def scale_stats(self, stats, mult_factor):
        stats['length'] *= mult_factor
        stats['unique'] = {col: stats['unique'][col]
                           * mult_factor for col in stats['unique']}

    def filter_field_eq(self, field_name, values):
        def filter(data):
            table_name = self.find_table(data['schema'], field_name)
            stats = data['stats'][table_name]
            mult_factor = 1.0 * len(values) / stats['unique'][field_name]
            self.scale_stats(stats, mult_factor)
            return (0, 0)  # does not return cost
        return filter

    def filter_field_ne(self, field_name, value):
        def filter(data):
            table_name = self.find_table(data['schema'], field_name)
            stats = data['stats'][table_name]
            mult_factor = 1 - (1.0 / stats['unique'][field_name])
            self.scale_stats(stats, mult_factor)
            return (0, 0)  # does not return cost
        return filter

    def filter_field_ge(self, field_name, value):
        def filter(data):
            table_name = self.find_table(data['schema'], field_name)
            self.scale_stats(data['stats'][table_name], 0.5)
            return (0, 0)  # does not return cost
        return filter

    def filter_field_gt(self, field_name, value):
        def filter(data):
            table_name = self.find_table(data['schema'], field_name)
            self.scale_stats(data['stats'][table_name], 0.5)
            return (0, 0)  # does not return cost
        return filter

    def filter_field_le(self, field_name, value):
        def filter(data):
            table_name = self.find_table(data['schema'], field_name)
            self.scale_stats(data['stats'][table_name], 0.5)
            return (0, 0)  # does not return cost
        return filter

    def filter_field_lt(self, field_name, value):
        def filter(data):
            table_name = self.find_table(data['schema'], field_name)
            self.scale_stats(data['stats'][table_name], 0.5)
            return (0, 0)  # does not return cost
        return filter

    def filter_field_like(self, field_name, values):
        def filter(data):
            table_name = self.find_table(data['schema'], field_name)
            stats = data['stats'][table_name]
            n_matches = sum([1.0 + 4 * value.count('%') for value in values])
            mult_factor = bound(
                0.0, n_matches / stats['unique'][field_name], 1.0)
            self.scale_stats(stats, mult_factor)
            return (0, 0)  # does not return cost
        return filter

    def filter_field_not_like(self, field_name, value):
        def filter(data):
            table_name = self.find_table(data['schema'], field_name)
            stats = data['stats'][table_name]
            n_matches = 1.0 + 4 * value.count('%')
            mult_factor = 1.0 - \
                bound(0.0, n_matches / stats['unique'][field_name], 1.0)
            self.scale_stats(stats, mult_factor)
            return (0, 0)  # does not return cost
        return filter

    # PRIVATE
    def find_table(self, schema, field_name):
        for table_name in schema:
            if field_name in schema[table_name]:
                return table_name
