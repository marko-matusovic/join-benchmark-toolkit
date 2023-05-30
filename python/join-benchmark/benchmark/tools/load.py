from benchmark.engine.engine import get_engine
from benchmark.tools.schema import get_schema

def load_named_tables(db_name, table_names, table_aliases=[]):
	dfs = {}

	if len(table_aliases) < len(table_names):
		table_aliases = table_names

	schema = get_schema(db_name)
	for (t_name, t_alias) in zip(table_names, table_aliases):
		dfs[t_alias] = get_engine().read_csv( \
			f'data/{db_name}/tables/{t_name}.{get_extension(db_name)}',  \
			sep=get_separator(db_name),  \
			header=None,  \
			names=[f'{t_alias}.{col}' for col in schema[t_name]],  \
			index_col=False)
	
	return dfs

def load_table(db_name, table_name):
	schema = get_schema(db_name)
	return get_engine().read_csv( \
		f'data/{db_name}/tables/{table_name}.{get_extension(db_name)}',  \
		sep=get_separator(db_name),  \
		header=None,  \
		names=schema[table_name],  \
		index_col=False)

def get_extension(db_name:str):
    return {
		"ssb": 'tbl',
		"job": "csv"
	}[db_name]

def get_separator(db_name: str):
    return {
		"ssb": '|',
		"job": ","
	}[db_name]
