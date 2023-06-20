
from typing import Any
from benchmark.operations.operations import Operations, TVal
from benchmark.tools.schema import get_schema


TIME_CONSTANT = 1.0 / 1_000_000_000

TIME_JOIN = TIME_CONSTANT * 300.0
TIME_JOIN_POW = 1.0

TIME_COMP = TIME_CONSTANT * 100.0
TIME_COMP_POW = 1.0

TData = dict[str, Any]

class Approx_Instructions(Operations[TData,float]):
    
    def from_tables(self, db_name:str, tables:list[str], aliases:list[str]=[]):
        if len(aliases) < len(tables):
            aliases = tables
        schema = get_schema(db_name)
        def from_tbls():
            return {aliases[tables.index(key)]: schema[key] for key in schema if key in tables}
        return from_tbls

    def join_fields(self, field_name_1:str, field_name_2:str):
        def join(data:TData) -> float:
            name_1 = self.find_table(data, field_name_1)
            name_2 = self.find_table(data, field_name_2)

            res = f'({name_1}X{name_2})'
            data["schema"][res] = data["schema"][name_1] + data["schema"][name_2]
            
            del data["schema"][name_1]
            del data["schema"][name_2]

            if res not in data["times"]:
                sm = min(data["stats"][name_1]["length"], data["stats"][name_2]["length"])
                bg = max(data["stats"][name_1]["length"], data["stats"][name_2]["length"])
                
                data["times"][res] =  ((sm + bg) ** TIME_JOIN_POW) * TIME_JOIN
        
                data["stats"][res] = {
                    "length": bg,
                    "unique": data["stats"][name_1]["unique"] | data["stats"][name_2]["unique"]
                }

            return data["times"][res]
        return join
    
    def filter_eq(self, data:TData, field:str, values:list[TVal]):
        name = self.find_table(data, field)
        res = f'({name}𝜎{field}={values})'
        data["schema"][res] = data["schema"][name]
        del data["schema"][name]
        
        if res not in data["times"]:
            reduction = 1.0 * len(values) / data["stats"][name]["unique"][field]
            data["times"][res] = (data["stats"][name]["length"] ** TIME_COMP_POW) * TIME_COMP
            data["stats"][res] = {
                "length": data["stats"][name]["length"] * reduction,
                "unique": data["stats"][name]["unique"].copy()
            }
            data["stats"][res]["unique"][field] = len(values)
            
        return data["times"][res]
    
    def filter_comp(self, data:TData, field:str, value:TVal):
        name = self.find_table(data, field)
        res = f'({name}𝜎{field}<>)'
        data["schema"][res] = data["schema"][name]
        del data["schema"][name]
        
        if res not in data["times"]:
            reduction = 0.5
            data["times"][res] = (data["stats"][name]["length"] ** TIME_COMP_POW) * TIME_COMP
            unique = data["stats"][name]["unique"].copy()
            data["stats"][res] = {
                "length": data["stats"][name]["length"] * reduction,
                "unique": {col: unique[col] * reduction for col in unique}
            }
            
        return data["times"][res]

    def filter_field_eq(self, field_name:str, values:list[TVal]):
        def filter(data:TData):
            return self.filter_eq(data, field_name, values)
        return filter
    
    def filter_field_ne(self, field_name:str, value:TVal):
        def filter(data:TData):
            return self.filter_eq(data, field_name, [value])
        return filter

    def filter_field_ge(self, field_name:str, value:TVal):
        def filter(data:TData):
            return self.filter_comp(data, field_name, value)
        return filter

    def filter_field_gt(self, field_name:str, value:TVal):
        def filter(data:TData):
            return self.filter_comp(data, field_name, value)
        return filter

    def filter_field_le(self, field_name:str, value:TVal):
        def filter(data:TData):
            return self.filter_comp(data, field_name, value)
        return filter

    def filter_field_lt(self, field_name:str, value:TVal):
        def filter(data:TData):
            return self.filter_comp(data, field_name, value)
        return filter
    
    def filter_field_like(self, field_name:str, values:list[TVal]):
        def filter(data:TData):
            print("Not implemented!")
            exit(1)
        return filter
    
    def filter_field_not_like(self, field_name:str, value:TVal):
        def filter(data:TData):
            print("Not implemented!")
            exit(1)
        return filter
    
    def find_table(self, data:TData, field_name:str) -> str:
        for name in data["schema"]:
            if field_name in data["schema"][name]:
                return name
        exit(1)
