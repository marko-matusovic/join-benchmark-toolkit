import pandas
from pandas import DataFrame

from benchmark.tools.schema import get_schema

def load_tables(db_name, table_names, table_aliases=[]) -> dict[str, DataFrame]:
	dfs = {}

	if len(table_aliases) < len(table_names):
		table_aliases = table_names

	schema = get_schema(db_name)
	for (t_name, t_alias) in zip(table_names, table_aliases):
		dfs[t_alias] =pandas.read_table( \
			f'data/{db_name}/tables/{t_name}.{get_extension(db_name)}',  \
			sep=get_separator(db_name),  \
			header=None,  \
			names=schema[t_name],  \
			index_col=False, \
			low_memory=False)
	
	return dfs

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