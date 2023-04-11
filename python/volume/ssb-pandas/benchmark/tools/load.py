import pandas
from pandas import DataFrame

from benchmark.tools.schema import get_schema

def load_tables(names) -> dict[str, DataFrame]:
	dfs = {}
	root_path = "data/tables"

	schema = get_schema()
	for name in names:
		dfs[name] = pandas.read_table( \
			f'{root_path}/{name}.tbl',  \
			sep='|',  \
			header=None,  \
			names=schema[name],  \
			index_col=False)
	
	return dfs
