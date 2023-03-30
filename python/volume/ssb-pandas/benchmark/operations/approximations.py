from copy import deepcopy
from benchmark.schema import get_schema

TIME_CONSTANT = 1/1_000_000_000 * 42
TIME_JOIN = TIME_CONSTANT * 1.5
TIME_COMP = TIME_CONSTANT * 0.9

class Approx_Instructions:
    
    
    def from_tables(self, tables):
        def from_tbls():
            return {key: get_schema()[key] for key in get_schema() if key in tables}
        return from_tbls

    def join_fields(self, field_1, field_2):
        def join(data):
            name_1 = self.find_table(data, field_1)
            name_2 = self.find_table(data, field_2)

            res = f'({name_1}X{name_2})'

            if res not in data["times"]:
                data["times"][res] = TIME_JOIN * (data["stats"][name_1]["length"] + data["stats"][name_2]["length"])
                
                joined_unique = data["stats"][name_1]["unique"] | data["stats"][name_2]["unique"]
                mult = max(data["stats"][name_1]["length"], data["stats"][name_2]["length"]) / min(data["stats"][name_1]["length"], data["stats"][name_2]["length"])
                data["stats"][res] = {
                    "length": min(data["stats"][name_1]["length"], data["stats"][name_2]["length"]),
                    "unique":  {col: joined_unique[col] * mult for col in joined_unique}
                }

            return data["times"][res]
        return join
    
    def filter_eq(self, data, field, values):
        name = self.find_table(data, field)
        res = f'({name}𝜎{field}={values})'
        
        if res not in data["times"]:
            reduction = 1.0 * data["stats"][name]["length"] / data["stats"][name]["unique"][field] * len(values)
            data["times"][res] = TIME_COMP * reduction * data["stats"][name]["length"]
            data["stats"][res] = {
                "length": data["stats"][name]["length"] * reduction,
                "unique": data["stats"][name]["unique"].copy()
            }
            data["stats"][res]["unique"][field] = len(values)
            
        return data["times"][res]
                
    def filter_comp(self, data, field, value):
        name = self.find_table(data, field)
        res = f'({name}𝜎{field}<>)'
        
        if res not in data["times"]:
            reduction = 0.5
            data["times"][res] = TIME_COMP * reduction * data["stats"][name]["length"]
            unique = data["stats"][name]["unique"].copy()
            data["stats"][res] = {
                "length": data["stats"][name]["length"] * reduction,
                "unique": {col: unique[col] * reduction for col in unique}
            }
            
        return data["times"][res]

    def filter_field_eq(self, field, values):
        def filter(data):
            return self.filter_eq(data, field, values)
        return filter

    def filter_field_ge(self, field, value):
        def filter(data):
            return self.filter_comp(data, field, value)
        return filter

    def filter_field_gt(self, field, value):
        def filter(data):
            return self.filter_comp(data, field, value)
        return filter

    def filter_field_le(self, field, value):
        def filter(data):
            return self.filter_comp(data, field, value)
        return filter

    def filter_field_lt(self, field, value):
        def filter(data):
            return self.filter_comp(data, field, value)
        return filter
    
    def find_table(self, data, field):
        for name in data["schema"]:
            if field in data["schema"][name]:
                return name
        return None
