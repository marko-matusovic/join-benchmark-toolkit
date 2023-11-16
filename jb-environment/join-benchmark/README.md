# Join Benchmark

This folder is host to the join benchmark, implemented in python with the use of pandas and cudf.

This benchmark works with SSB and JOB.

## Running

Running configurations as well as required positional and optional named parameters are explained in the [main.py file](./main.py).

Example running configurations can be found in the [launch file](.vscode/launch.json). 

## Adding new DB Sets
To add a new dataset, you need to set-up a directory with 3 components.
1. The schema file.
2. A directory with queries.
3. A directory with table files.

The file structure should look like this:
```
new_db_set
├── schema.sql
├── queries
│   ├── query_1.sql
│   ├── query_2.sql
│   ┊
│   └── query_n.sql
└── tables
    ├── table_1.csv
    ├── table_2.csv
    ┊
    └── table_n.csv
```

> The default location for this directory is in the [data](./data) directory, alongside other data sets, however you can specify a custom `db_path` when running with `--db_path path/to/db_set`.



### How to use this framework?

The join benchmark framework in its simplest parses the query into instructions, and then exposes them. To immediately execute them in an arbitrary order, follow the code below:

```python
# Parse the schema and the query into a set of instructions
instructions = get_instruction_set(db_path, db_set, query, Operations_Real())

# Verify required tables for the query exist
dfs: dict[str, DataFrame] = instructions.s1_init()

# Execute the statements in WHERE which only filter
for instruction in instructions.s2_filters:
    instruction(dfs)

# Execute the statements in WHERE which join tables
for join in instructions.s3_joins:
    join(dfs)
```
source: [benchmark/run/individual/main_run_simple.py](benchmark/run/individual/main_run_simple.py)
