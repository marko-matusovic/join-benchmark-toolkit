from typing import Any, TypeVar
import re
from re import RegexFlag
from benchmark.operations.operations import Operations, TVal
from benchmark.operations.query_instructions import QueryInstructions

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
    "BETWEEN",
]


# SELECT column+ FROM (table [AS alias])+ [WHERE clause+]
def parse(
    db_path:str, db_set: str, query_str: str, operation_set: Operations[I, O]
) -> QueryInstructions[I, O]:
    print("Parsing automatically.")
    (_select_clause, from_clause, where_clause) = split_parsing_groups(query_str)

    (tables, aliases) = parse_from_clause(from_clause)

    (filters, joins) = parse_where_clause(where_clause)

    return QueryInstructions(
        s1_init=operation_set.from_tables(db_path, db_set, tables, aliases),
        s2_filters=[operation_set.get_filter(op)(tbl, val) for tbl, op, val in filters],
        s3_joins=[operation_set.join_fields(f1, f2) for f1, f2 in joins],
        s4_aggregation=[
            # NOT SUPPORTED RIGHT NOW
            # group by
            # order by
            # select
        ],
    )

# This function only parses out the joins
def get_joins(db_set: str, query_str: str) -> list[tuple[str,str]] :
    (_select_clause, _from_clause, where_clause) = split_parsing_groups(query_str)

    (_filters, joins) = parse_where_clause(where_clause)
    
    return joins


def split_parsing_groups(query_str:str):
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
    if select_keyword == "":
        rest = start

    (select_clause, from_keyword, rest) = rest.partition("FROM")
    if from_keyword == "":
        print("Error: The Query is missing a FROM clause.")
        exit(1)

    (from_clause, where_keyword, where_clause) = rest.partition("WHERE")
    if where_keyword == "":
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

    return (select_clause.strip(), from_clause.strip(), where_clause.strip())


def parse_from_clause(from_clause:str) -> tuple[list[str],list[str]] :
    tables:list[str] = []
    aliases:list[str] = []

    for table in from_clause.split(","):
        (name, key, alias) = table.strip().partition("AS")
        tables.append(name.strip())
        if key == "":
            alias = name
        aliases.append(alias.strip())

    return (tables, aliases)


def parse_where_clause(
    where_clause: str,
) -> tuple[list[tuple[str, str, Any]], list[tuple[str, str]]]:
    filters: list[tuple[str, str, Any]] = []
    joins: list[tuple[str, str]] = []
    where_clause_parts = where_clause.split("AND")
    where_clause_i = 0
    while where_clause_i < len(where_clause_parts):
        clause = where_clause_parts[where_clause_i].strip()
        where_clause_i += 1

        if clause.find("OR") != -1:
            # Currently only (clause1 OR clause2 OR ... OR clauseX) is supported
            # if the field and operation is the same for all
            # and the operation is from the set ["=", "LIKE"]
            big_clause = clause
            try:
                multi_clause = clause.strip("() ").split("OR")
                field = ""
                op = ""
                values:list[TVal | list[TVal]] = []
                for clause in multi_clause:
                    (field_cur, _space, op_and_val) = clause.strip().partition(" ")
                    (op_cur, _space, val_cur) = op_and_val.partition(" ")
                    assert field == "" or field == field_cur.strip()
                    field = field_cur.strip()
                    assert op == "" or op == op_cur.strip()
                    op = op_cur.strip()
                    values.append(parse_value(val_cur))
                assert op in ["=", "LIKE"]
                filters.append((field, op, values))
                continue
            except AssertionError:
                print(f'ERROR: Unsupported WHERE clauses: "{big_clause}"')
                exit(1)

        (tbl, _space, op_and_val) = clause.partition(" ")
        (op, _space, val) = op_and_val.partition(" ")
        if op == "NOT":
            (op2, _space, val) = val.partition(" ")
            op = f"{op} {op2}"

        if op == "=" and re.match(f"^([a-zA-Z_]+\\.)?[a-zA-Z_]+$", val) != None:
            # op is a join
            joins.append((tbl, val))
            continue

        # op is a filter
        if op == "BETWEEN":
            val1 = parse_value(val)
            val2 = parse_value(where_clause_parts[where_clause_i].strip())
            where_clause_i += 1
            filters.append((tbl, ">=", val1))
            filters.append((tbl, "<=", val2))
            continue

        filters.append((tbl, op, parse_value(val)))

    return (filters, joins)


def parse_value(val:str) -> TVal | list[TVal]:
    # parse the val
    if re.match(r"^\d+$", val) != None:
        return int(val)
    # Shouldn't parse floats
    # elif re.match(r'^\'?\d+.\d+\'?$', val) != None:
    #     val = float(val.strip('\''))
    elif re.match(r"^\(.+\)?$", val) != None:
        return [v.strip(" '") for v in val.strip(" ()").split(",")]
    else:
        return val.strip(" '")
