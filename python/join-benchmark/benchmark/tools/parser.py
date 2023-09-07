from typing import TypeVar
import re
from re import RegexFlag
from benchmark.operations.operations import Operations
from benchmark.operations.query_instructions import QueryInstructions
from benchmark.tools.factor_join_parser import parse_query_simple

I = TypeVar("I")
O = TypeVar("O")

keywords = [
    "SELECT",
    "FROM",
    "AS",
    "WHERE",
    "NOT",
    "IN",
    "LIKE",
    "AND",
    "OR",
    "LIMIT",
    "GROUP BY",
    "ORDER BY",
]


# SELECT column+ FROM (table [AS alias])+ [WHERE clause+]
def parse(
    db_set: str, query_str: str, operation_set: Operations[I, O]
) -> QueryInstructions[I, O]:
    query_str = query_str.strip(" ;")
    query_str = f" {query_str} "
    for kw in keywords:
        query_str = re.sub(
            f"\\s+{kw}\\s+",
            f" {kw} ",
            query_str,
            flags=RegexFlag.IGNORECASE,
        )
    query_str = query_str.strip()
    query_str = re.sub(r"\\s\\s+", " ", query_str)

    (start, select_keyword, rest) = query_str.partition("SELECT")
    if select_keyword is None:
        rest = start

    (select_clause, from_keyword, rest) = rest.partition("FROM")
    if from_keyword is None:
        print("Error: The Query is missing a FROM clause.")
        exit(1)

    (from_clause, where_keyword, where_clause) = rest.partition("WHERE")
    if where_keyword is None:
        where_clause = ""

    # get rid of "LIMIT", "GROUP BY", "ORDER BY"
    end = min(
        [
            x
            for x in [
                len(where_clause),
                where_clause.find("LIMIT"),
                where_clause.find("GROUP BY"),
                where_clause.find("ORDER BY"),
            ]
            if x != -1
        ]
    )
    where_clause = where_clause[:end]

    select_clause = select_clause.strip()
    from_clause = from_clause.strip()
    where_clause = where_clause.strip()

    tables = []
    aliases = []
    for table in from_clause.split(","):
        (name, key, alias) = table.strip().partition("AS")
        tables.append(name.strip())
        if key is None:
            alias = name
        aliases.append(alias.strip())

    filters = []
    joins = []
    for clause in where_clause.split("AND"):
        clause = clause.strip()
        if clause.find("OR") != -1:
            print(
                f'ERROR: The parser does not support complex WHERE clauses: "{clause}"'
            )
            exit(1)
        (tbl, _space, op_and_val) = clause.partition(" ")
        (op, _space, val) = op_and_val.partition(" ")
        if op == "NOT":
            (op2, _space, val) = val.partition(" ")
            op = f"{op} {op2}"

        if (
            op == "="
            and re.match(f"^([a-z_]+\\.)[a-z_]+$", val, flags=RegexFlag.IGNORECASE)
            != None
        ):
            # op is a join
            joins.append(operation_set.join_fields(tbl, val))
            continue

        # op is a filter
        op_method = operation_set.get_filter(op)

        # parse the val
        if re.match(r"^\d+$", val) != None:
            val = int(val)
        # Shouldn't parse floats
        # elif re.match(r'^\'?\d+.\d+\'?$', val) != None:
        #     val = float(val.strip('\''))
        elif re.match(r"^\(.+\)?$", val) != None:
            val = [v.strip(" '") for v in val.strip(" ()").split(",")]
        else:
            val = val.strip(" '")

        filters.append(op_method(tbl, val))

    return QueryInstructions(
        s1_init=operation_set.from_tables(db_set, tables, aliases),
        s2_filters=filters,
        s3_joins=joins,
        s4_aggregation=[
            # NOT SUPPORTED RIGHT NOW
            # group by
            # order by
            # select
            # IGNORING SELECT CLAUSE
        ],
    )
