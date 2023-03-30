from benchmark.operations.approximations import Approx_Instructions
from benchmark.operations.instructions import Instructions
from benchmark.queries import q11, q12, q13, q21, q31, q41


def get_instructions(query):
    return get_set(query, Instructions())

def get_approx_instructs(query):    
    return get_set(query, Approx_Instructions())
    
def get_set(query, operation_class):
    if query == 'q11':
        return q11.instruction_set(operation_class)
    if query == 'q12':
        return q12.instruction_set(operation_class)
    if query == 'q13':
        return q13.instruction_set(operation_class)
    elif query == 'q21':
        return q21.instruction_set(operation_class)
    elif query == 'q31':
        return q31.instruction_set(operation_class)
    elif query == 'q41':
        return q41.instruction_set(operation_class)
    else:
        return None