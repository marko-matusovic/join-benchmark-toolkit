from benchmark.tools.load import load_tables

class Instructions:
    def from_tables(self, db_name, tables, aliases=[]):
        def load():
            return load_tables(db_name, tables, aliases)
        return load

    def join_fields(self, field_name_1, field_name_2):
        def join(dfs):
            table_name_1 = self.find_names(dfs, field_name_1)
            table_name_2 = self.find_names(dfs, field_name_2)
            if table_name_1 == table_name_2:
                return
            table_1 = dfs[table_name_1]
            table_2 = dfs[table_name_2]
            del dfs[table_name_1]
            del dfs[table_name_2]
            dfs[f'({table_name_1}[X]{table_name_2})'] = table_1.merge(
                table_2, how='inner', left_on=field_name_1, right_on=field_name_2)
        return join

    def filter_field_eq(self, field_name, values):
        def filter(dfs):
            table_name = self.find_names(dfs, field_name)
            table = dfs[table_name]
            del dfs[table_name]
            dfs[f'({table_name}[s]{field_name}[in]{values})'] = table.loc[table[field_name].isin(values)]
        return filter

    def filter_field_ge(self, field_name, value):
        def filter(dfs):
            table_name = self.find_names(dfs, field_name)
            table = dfs[table_name]
            del dfs[table_name]
            dfs[f'({table_name}[s]{field_name}[>=]{value})'] = table.loc[table[field_name] >= value]
        return filter

    def filter_field_gt(self, field_name, value):
        def filter(dfs):
            table_name = self.find_names(dfs, field_name)
            table = dfs[table_name]
            del dfs[table_name]
            dfs[f'({table_name}[s]{field_name}[>]{value})'] = table.loc[table[field_name] > value]
        return filter

    def filter_field_le(self, field_name, value):
        def filter(dfs):
            table_name = self.find_names(dfs, field_name)
            table = dfs[table_name]
            del dfs[table_name]
            dfs[f'({table_name}[s]{field_name}[<=]{value})'] = table.loc[table[field_name] <= value]
        return filter

    def filter_field_lt(self, field_name, value):
        def filter(dfs):
            table_name = self.find_names(dfs, field_name)
            table = dfs[table_name]
            del dfs[table_name]
            dfs[f'({table_name}[s]{field_name}[<]{value})'] = table.loc[table[field_name] < value]
        return filter
    
    def filter_field_like(self, field_name, values):
        def filter(dfs):
            table_name = self.find_names(dfs, field_name)
            table = dfs[table_name]
            del dfs[table_name]
            index = self.like_index(table[field_name], values[0])
            for value in values[1:]:
                index = index | self.like_index(table[field_name], value)
            dfs[f'({table_name}[s]{field_name}[like]{values})'] = table.loc[index]
        return filter

    def filter_field_not_like(self, field_name, value):
        def filter(dfs):
            table_name = self.find_names(dfs, field_name)
            table = dfs[table_name]
            del dfs[table_name]
            index = self.like_index(table[field_name], value) == False
            dfs[f'({table_name}[s]{field_name}[not-like]{value})'] = table.loc[index]
        return filter

    def like_index(self, col, value):
        reg = f'^{value.replace("%", ".*")}$'
        return col.str.contains(reg)

    # Hurrah spaghetti code
    def find_names(self, dfs, field_name):
        for table_name in dfs:
            if field_name in dfs[table_name]:
                return table_name
