from typing import TypeVar

from benchmark.operations.operations import Operations
from benchmark.operations.instructions import Real_Instructions
from benchmark.operations.time_mem_approximations import Time_Mem_Approx_Instructions
from benchmark.operations.execution_tree import Execution_Tree_Instructions
from benchmark.queries.ssb import q11, q12, q13, q21, q31, q41
from benchmark.queries.job import q1b, q20a, q22a, q28a, q2a, q30a
from benchmark.tools.parser import parse
from benchmark.operations.query_instructions import QueryInstructions


def get_real_instructions(db_path:str, db_set:str, query: str, manual_parse=False):
    return get_set(db_path, db_set, query, Real_Instructions(), manual_parse)

def get_time_mem_approx_instructions(db_path:str, db_set:str, query: str, manual_parse=False):
    return get_set(db_path, db_set, query, Time_Mem_Approx_Instructions(), manual_parse)

def get_execution_tree_instructions(db_path:str, db_set:str, query: str, manual_parse=False):
    return get_set(db_path, db_set, query, Execution_Tree_Instructions(), manual_parse)


I = TypeVar("I")
O = TypeVar("O")


def get_set(
    db_path:str, db_set:str, query: str, operation_class: Operations[I, O], manual_parse=False
) -> QueryInstructions[I, O]:
    if manual_parse:
        if db_set == "ssb":
            if query == "q11":
                return q11.instruction_set(db_path, operation_class)
            if query == "q12":
                return q12.instruction_set(db_path, operation_class)
            if query == "q13":
                return q13.instruction_set(db_path, operation_class)
            elif query == "q21":
                return q21.instruction_set(db_path, operation_class)
            elif query == "q31":
                return q31.instruction_set(db_path, operation_class)
            elif query == "q41":
                return q41.instruction_set(db_path, operation_class)
            pass
        elif db_set == "job":
            if query == "1b":
                return q1b.instruction_set(db_path, operation_class)
            if query == "2a":
                return q2a.instruction_set(db_path, operation_class)
            if query == "20a":
                return q20a.instruction_set(db_path, operation_class)
            if query == "22a":
                return q22a.instruction_set(db_path, operation_class)
            if query == "28a":
                return q28a.instruction_set(db_path, operation_class)
            if query == "30a":
                return q30a.instruction_set(db_path, operation_class)

    # No manual parsing found, attempting automatic parsing

    with open(f"{db_path}/queries/{query}.sql") as file:
        query = " ".join([line.strip() for line in file.readlines()])
        return parse(db_path, db_set, query, operation_class)
