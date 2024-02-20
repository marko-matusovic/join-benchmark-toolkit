from benchmark.operations.query_instructions_service import get_instruction_set
from benchmark.operations.operations_executiontree import Operations_ExecutionTree
from benchmark.tools.query_parser import (
    get_joins,
    load_query,
    parse_from_clause,
    parse_where_clause,
    split_parsing_groups,
)


def main(db_path: str, db_set: str, query: str, manual_parse=False):
    print(f"Parsing {db_set}/{query} ...")

    (_select_clause, from_clause, where_clause) = split_parsing_groups(
        load_query(db_path, query)
    )
    (tables, aliases) = parse_from_clause(from_clause)
    (filters, joins) = parse_where_clause(where_clause)

    print("From tables (aliases):")
    for t, a in zip(tables, aliases):
        print(f"\t{t} AS {a}")

    print(f"Filters: #{len(filters)}")
    for f1, f2, f3 in filters:
        print(f"\t{f1} {f2} {f3}")

    print(f"Joins: #{len(joins)}")
    for j1, j2 in joins:
        print(f"\t{j1} = {j2}")

    instructions = get_instruction_set(
        db_path, db_set, query, Operations_ExecutionTree(), manual_parse
    )
    print("Parsing finished!")

    print("Compiling the execution tree...")

    data = instructions.s1_init()

    for filter in instructions.s2_filters:
        filter(data)

    for join in instructions.s3_joins:
        join(data)

    trees = list(set(data.cluster_names.values()))
    if len(trees) == 1:
        print("Execution tree: ")
        print(trees[0])
    else:
        print("Execution trees: ")
        for tree in trees:
            print(tree)
