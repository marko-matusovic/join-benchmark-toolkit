def rename_schema(orig_schema, tables, aliases):
    new_schema = {}
    for name in orig_schema:
        alias = aliases[tables.index(name)]
        new_schema[alias] = [f'{alias}.{col}' for col in orig_schema]
    return new_schema

def rename_stats(stats, tables, aliases):
    return {
        alias: {
            "length": stats[table]["length"],
            "unique": dict_prepend(stats[table]["unique"], f"{alias}."),
            "dsize": dict_prepend(stats[table]["dsize"], f"{alias}."),
        }
        for (table, alias) in zip(tables, aliases)
    }

def dict_prepend(data, prefix):
    return {f"{prefix}{col}": data[col] for col in data}
