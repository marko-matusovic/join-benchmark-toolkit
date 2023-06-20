from benchmark.tools.schema import get_schema
from benchmark.tools.stats import get_stats
from benchmark.tools.rename import rename_schema, rename_stats
from benchmark.tools.tools import bound

# Thass holds a cost model approximation for time and memory use of joins on GPU, is .
# The main principles of the two cost models are explained here:
#
# Time
#   When executing a join on GPU, the limiting factor is not the total number of operations
#   executed, as these can be done in parallel, but the data transfer from CPU memory to GPU memory.
#   Therefore, this cost model takes temporality into mind, and reduces the cost for tables that are
#   joined consecutively, such that they do not have to be transferred multiple times.
#
# Memory
#   When executing a join, the memory in GPU used is proportional to the two tables joined.
#   Notable aspect that affect memory size are: number of rows in the each table, cell size,
#   data type of the joining property.
#

# The `data` used during the calculation has the following structure:
# data = {
#   "schema": {                                 # column names for each table
#       table_alias: [ table_cols ]
#   },
#   "stats": {                                  # statistics per table
#       table_alias: {
#           "length": 123                       # length of the table
#           "unique": { table_col: 123 }        # unique values per each column
#           "dsize": { table_col: 123 }         # data type size per each column
#       }
#   },
#   "history" : [table_alias],                  # history of joins from the beginning
#   "time": {
#       table_alias: 0.123                      # execution time of each join
#   },
#   "memory": {
#       table_alias: 123                        # memory use of each join
#   },
# }


class Approx_Time_Memory_Instructions:
    def from_tables(self, db_name, tables, aliases=[]):
        if len(aliases) == len(tables):
            aliases = tables

        def load():
            return {  # data = {
                "schema": rename_schema(get_schema(db_name), tables, aliases),
                "stats": rename_stats(get_stats(db_name), tables, aliases),
                "history": [],
                "times": {},
                "memory": {},
            }

        return load

    def join_fields(self, field_name_1, field_name_2):
        def join(data):
            # table_name_1 = self.find_table(data, field_name_1)
            # table_name_2 = self.find_table(data, field_name_2)
            # if table_name_1 == table_name_2:
            #     self.join_filter_eq(
            #         data, table_name_1, field_name_1, field_name_2)
            #     return
            # table_1 = data[table_name_1]
            # table_2 = data[table_name_2]
            # del data[table_name_1]
            # del data[table_name_2]
            # data[f'({table_name_1}[X]{table_name_2})'] = table_1.merge(
            #     table_2, how='inner', left_on=field_name_1, right_on=field_name_2)
            pass

        return join

    # # PRIVATE
    # def join_filter_eq(self, data, table_name, field_name_1, field_name_2):
    #     table = data[table_name]
    #     del data[table_name]
    #     data[f'({table_name}[XS]{field_name_1}={field_name_2}'] = \
    #         table.loc[table[field_name_1] == table[field_name_2]]

    def filter_field_eq(self, field_name, values):
        def filter(data):
            stats = data["stats"][self.find_table(field_name)]
            reduction_factor = bound(0.0, 1.0 * len(values) / stats["unique"][field_name], 1.0)
            stats["length"] *= reduction_factor
            stats["unique"] = {
                col: stats["unique"][col] * reduction_factor for col in stats["unique"]
            }
        return filter

    def filter_field_ne(self, field_name, value):
        def filter(data):
            stats = data["stats"][self.find_table(field_name)]
            reduction_factor = bound(0.0, 1 - (1.0 / stats["unique"][field_name]), 1.0)
            stats["length"] *= reduction_factor
            stats["unique"] = {
                col: stats["unique"][col] * reduction_factor for col in stats["unique"]
            }
        return filter

    # PRIVATE
    def filter_any(self, field_name, reduction_factor=0.5):
        def filter(data):
            stats = data["stats"][self.find_table(field_name)]
            stats["length"] *= reduction_factor
            stats["unique"] = {
                col: stats["unique"][col] * reduction_factor for col in stats["unique"]
            }
        return filter

    def filter_field_ge(self, field_name, value):
        return self.filter_any(field_name, 0.5)

    def filter_field_gt(self, field_name, value):
        return self.filter_any(field_name, 0.5)

    def filter_field_le(self, field_name, value):
        return self.filter_any(field_name, 0.5)

    def filter_field_lt(self, field_name, value):
        return self.filter_any(field_name, 0.5)

    def filter_field_like(self, field_name, values):
        def filter(data):
            stats = data["stats"][self.find_table(field_name)]
            
            sum([1 + 5 * val.count("%") for val in values])
            reduction_factor = bound(0.0, 1.0 * len(values) / stats["unique"][field_name], 1.0)
            stats["length"] *= reduction_factor
            stats["unique"] = {
                col: stats["unique"][col] * reduction_factor for col in stats["unique"]
            }
        return filter

        return filter

    def filter_field_not_like(self, field_name, value):
        def filter(data):
            # table_name = self.find_table(data, field_name)
            # table = data[table_name]
            # del data[table_name]
            # index = self.like_index(table[field_name], value) != True
            # data[f'({table_name}[s]{field_name}[not-like]{value})'] = table.loc[index]
            pass

        return filter

    # PRIVATE
    def find_table(self, data, field_name):
        for table_name in data["schema"]:
            if field_name in data["schema"][table_name]:
                return table_name
